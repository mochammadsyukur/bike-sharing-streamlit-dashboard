import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Bike Sharing Dashboard",
    page_icon="🚲",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# LOAD & PREPARE DATA
# ─────────────────────────────────────────────
@st.cache_data
def load_data():
    day_df  = pd.read_csv("dashboard/day.csv")
    hour_df = pd.read_csv("dashboard/hour.csv")

    for df in [day_df, hour_df]:
        df["dteday"] = pd.to_datetime(df["dteday"])
        df["season_label"]     = df["season"].map({1:"Spring", 2:"Summer", 3:"Fall", 4:"Winter"})
        df["weather_label"]    = df["weathersit"].map({1:"Clear", 2:"Mist/Cloudy", 3:"Light Rain/Snow", 4:"Heavy Rain/Snow"})
        df["yr_label"]         = df["yr"].map({0:"2011", 1:"2012"})
        df["workingday_label"] = df["workingday"].map({0:"Holiday/Weekend", 1:"Working Day"})
        df["weekday_label"]    = df["weekday"].map({0:"Sun",1:"Mon",2:"Tue",3:"Wed",4:"Thu",5:"Fri",6:"Sat"})
        df["month_label"]      = df["mnth"].map({
            1:"Jan",2:"Feb",3:"Mar",4:"Apr",5:"May",6:"Jun",
            7:"Jul",8:"Aug",9:"Sep",10:"Oct",11:"Nov",12:"Dec"
        })

    return day_df, hour_df

day_df, hour_df = load_data()

# ─────────────────────────────────────────────
# SIDEBAR FILTERS
# ─────────────────────────────────────────────
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/bicycle.png", width=60)
    st.title("🚲 Bike Sharing")
    st.markdown("---")

    st.subheader("🔽 Filter Data")

    selected_year = st.multiselect(
        "Tahun",
        options=["2011", "2012"],
        default=["2011", "2012"],
    )

    selected_season = st.multiselect(
        "Musim",
        options=["Spring", "Summer", "Fall", "Winter"],
        default=["Spring", "Summer", "Fall", "Winter"],
    )

    selected_weather = st.multiselect(
        "Kondisi Cuaca",
        options=["Clear", "Mist/Cloudy", "Light Rain/Snow"],
        default=["Clear", "Mist/Cloudy", "Light Rain/Snow"],
    )

    selected_daytype = st.multiselect(
        "Jenis Hari",
        options=["Working Day", "Holiday/Weekend"],
        default=["Working Day", "Holiday/Weekend"],
    )

    st.markdown("---")
    st.caption("Data: Bike Sharing Dataset (2011–2012)")

# ─────────────────────────────────────────────
# APPLY FILTERS
# ─────────────────────────────────────────────
filtered_day = day_df[
    day_df["yr_label"].isin(selected_year) &
    day_df["season_label"].isin(selected_season) &
    day_df["weather_label"].isin(selected_weather) &
    day_df["workingday_label"].isin(selected_daytype)
]

filtered_hour = hour_df[
    hour_df["yr_label"].isin(selected_year) &
    hour_df["season_label"].isin(selected_season) &
    hour_df["weather_label"].isin(selected_weather) &
    hour_df["workingday_label"].isin(selected_daytype)
]

# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
st.title("🚲 Bike Sharing Dashboard")
st.markdown("Analisis pola penyewaan sepeda berdasarkan data harian dan per jam (2011–2012)")
st.markdown("---")

# ─────────────────────────────────────────────
# KPI METRICS
# ─────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)

total_rentals  = filtered_day["cnt"].sum()
avg_daily      = filtered_day["cnt"].mean()
total_casual   = filtered_day["casual"].sum()
total_register = filtered_day["registered"].sum()

col1.metric("🚴 Total Penyewaan",   f"{total_rentals:,.0f}")
col2.metric("📅 Rata-rata/Hari",    f"{avg_daily:,.0f}")
col3.metric("👤 Total Casual",      f"{total_casual:,.0f}")
col4.metric("🎫 Total Registered",  f"{total_register:,.0f}")

st.markdown("---")

# ─────────────────────────────────────────────
# ROW 1: Tren Bulanan & Pie Proporsi
# ─────────────────────────────────────────────
st.subheader("📈 Pertanyaan 1: Pola Pengguna Casual vs Registered per Jenis Hari")

col_left, col_right = st.columns([2, 1])

with col_left:
    monthly = (
        filtered_day
        .groupby(["yr_label", "mnth", "month_label", "workingday_label"])[["casual", "registered"]]
        .mean()
        .round(1)
        .reset_index()
        .sort_values("mnth")
    )

    month_order = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    monthly["month_label"] = pd.Categorical(monthly["month_label"], categories=month_order, ordered=True)
    monthly = monthly.sort_values("month_label")

    tab1, tab2 = st.tabs(["Casual", "Registered"])

    for tab, user_col, color_map in [
        (tab1, "casual",     {"2011":"#FBBF24", "2012":"#F59E0B"}),
        (tab2, "registered", {"2011":"#34D399", "2012":"#059669"}),
    ]:
        with tab:
            fig = px.line(
                monthly,
                x="month_label", y=user_col,
                color="yr_label",
                line_dash="workingday_label",
                markers=True,
                color_discrete_map=color_map,
                labels={user_col: "Rata-rata Penyewaan/Hari", "month_label": "Bulan",
                        "yr_label": "Tahun", "workingday_label": "Jenis Hari"},
                title=f"Tren Bulanan — {user_col.capitalize()}",
                category_orders={"month_label": month_order},
            )
            fig.update_layout(height=350, legend=dict(orientation="h", yanchor="bottom", y=1.02))
            st.plotly_chart(fig, use_container_width=True)

with col_right:
    agg_type = (
        filtered_day
        .groupby("workingday_label")[["casual", "registered"]]
        .sum()
        .reset_index()
        .melt(id_vars="workingday_label", var_name="Tipe Pengguna", value_name="Total")
    )

    fig_pie = px.bar(
        agg_type,
        x="workingday_label", y="Total",
        color="Tipe Pengguna",
        barmode="stack",
        color_discrete_map={"casual": "#F4A261", "registered": "#2A9D8F"},
        labels={"workingday_label": "Jenis Hari", "Total": "Total Penyewaan"},
        title="Proporsi Casual vs Registered",
        text_auto=".2s",
    )
    fig_pie.update_layout(height=400, legend=dict(orientation="h", yanchor="bottom", y=1.02))
    st.plotly_chart(fig_pie, use_container_width=True)

# ─────────────────────────────────────────────
# ROW 2: Cuaca x Musim
# ─────────────────────────────────────────────
st.markdown("---")
st.subheader("🌤️ Pertanyaan 2: Pola Penyewaan Berdasarkan Cuaca & Musim")

col_left2, col_right2 = st.columns([1, 1])

with col_left2:
    season_order  = ["Spring", "Summer", "Fall", "Winter"]
    weather_order = ["Clear", "Mist/Cloudy", "Light Rain/Snow"]

    agg_q2 = (
        filtered_hour
        .groupby(["season_label", "weather_label"])["cnt"]
        .mean()
        .round(1)
        .reset_index()
    )
    pivot_q2 = (
        agg_q2
        .pivot(index="weather_label", columns="season_label", values="cnt")
        .reindex(index=weather_order, columns=season_order)
    )

    fig_heat = go.Figure(data=go.Heatmap(
        z=pivot_q2.values,
        x=pivot_q2.columns.tolist(),
        y=pivot_q2.index.tolist(),
        colorscale="YlOrRd",
        text=np.round(pivot_q2.values, 1),
        texttemplate="%{text}",
        textfont={"size": 13},
        hoverongaps=False,
        colorbar=dict(title="Avg/Jam"),
    ))
    fig_heat.update_layout(
        title="Heatmap: Rata-rata Penyewaan per Jam (Cuaca × Musim)",
        xaxis_title="Musim",
        yaxis_title="Kondisi Cuaca",
        height=350,
    )
    st.plotly_chart(fig_heat, use_container_width=True)

with col_right2:
    agg_weather = (
        filtered_hour
        .groupby("weather_label")["cnt"]
        .mean()
        .round(1)
        .reindex(weather_order)
        .reset_index()
    )

    fig_bar_w = px.bar(
        agg_weather,
        x="weather_label", y="cnt",
        color="weather_label",
        color_discrete_sequence=["#2EC4B6", "#E9C46A", "#E76F51"],
        labels={"weather_label": "Kondisi Cuaca", "cnt": "Rata-rata Penyewaan/Jam"},
        title="Rata-rata Penyewaan per Jam per Kondisi Cuaca",
        text_auto=".1f",
    )
    fig_bar_w.update_layout(height=350, showlegend=False)
    st.plotly_chart(fig_bar_w, use_container_width=True)

# ─────────────────────────────────────────────
# ROW 3: Pola Per Jam & Per Hari dalam Seminggu
# ─────────────────────────────────────────────
st.markdown("---")
st.subheader("🕐 Pola Penyewaan per Jam & Hari dalam Seminggu")

col_l3, col_r3 = st.columns([1, 1])

with col_l3:
    hourly = (
        filtered_hour
        .groupby(["hr", "workingday_label"])["cnt"]
        .mean()
        .round(1)
        .reset_index()
    )
    fig_hourly = px.line(
        hourly,
        x="hr", y="cnt",
        color="workingday_label",
        markers=True,
        color_discrete_map={"Working Day": "#2A9D8F", "Holiday/Weekend": "#F4A261"},
        labels={"hr": "Jam", "cnt": "Rata-rata Penyewaan", "workingday_label": "Jenis Hari"},
        title="Pola Penyewaan per Jam (Hari Kerja vs Libur)",
    )
    fig_hourly.update_layout(height=350, legend=dict(orientation="h", yanchor="bottom", y=1.02))
    st.plotly_chart(fig_hourly, use_container_width=True)

with col_r3:
    weekday_order = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    weekly = (
        filtered_day
        .groupby("weekday_label")["cnt"]
        .mean()
        .round(1)
        .reindex(weekday_order)
        .reset_index()
    )
    fig_weekly = px.bar(
        weekly,
        x="weekday_label", y="cnt",
        color="cnt",
        color_continuous_scale="Teal",
        labels={"weekday_label": "Hari", "cnt": "Rata-rata Penyewaan/Hari"},
        title="Rata-rata Penyewaan per Hari dalam Seminggu",
        text_auto=".0f",
    )
    fig_weekly.update_layout(height=350, showlegend=False, coloraxis_showscale=False)
    st.plotly_chart(fig_weekly, use_container_width=True)

# ─────────────────────────────────────────────
# ROW 4: Raw Data Table (Collapsible)
# ─────────────────────────────────────────────
st.markdown("---")
with st.expander("🗂️ Lihat Data Mentah (day_df)"):
    display_cols = ["dteday", "yr_label", "season_label", "weather_label",
                    "workingday_label", "casual", "registered", "cnt", "temp", "hum", "windspeed"]
    st.dataframe(
        filtered_day[display_cols].rename(columns={
            "dteday": "Tanggal", "yr_label": "Tahun", "season_label": "Musim",
            "weather_label": "Cuaca", "workingday_label": "Jenis Hari",
            "temp": "Suhu", "hum": "Kelembapan", "windspeed": "Kecepatan Angin"
        }),
        use_container_width=True,
        height=300,
    )
    st.caption(f"Menampilkan {len(filtered_day):,} baris setelah filter diterapkan.")