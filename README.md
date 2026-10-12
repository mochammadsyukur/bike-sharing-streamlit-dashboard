# Bike Sharing — Data Analysis and Streamlit Dashboard

A data-analysis learning project exploring patterns in historical hourly and daily bicycle rentals (2011–2012). This repository contains the original Python analysis notebook and an interactive Streamlit / Plotly dashboard.

## Features
- Interactive filters for exploring rental activity.
- Rental trends and comparisons by time, weather and rider category.
- Exploratory analysis in `notebooks/bike_sharing_analysis.ipynb`.

## Tech stack
Python · pandas · Streamlit · Plotly · Matplotlib · seaborn · Jupyter Notebook.

## Run locally

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
streamlit run dashboard/dashboard.py
```

Run the command from the repository's root directory. The files `dashboard/day.csv` and `dashboard/hour.csv` are included as expected by the dashboard script. For notebook analysis, the files are also under `data/`.

## Dataset attribution
The datasets are the **Bike Sharing Dataset** by Hadi Fanaee-T, distributed by the UCI Machine Learning Repository under **CC BY 4.0**. Original source: https://archive.ics.uci.edu/dataset/275/bike+sharing+dataset . DOI: https://doi.org/10.24432/C5W894 . Data cover 2011–2012 and should not be mistaken for current ridership.

## Notes
The original notebook's student email/ID were omitted from this GitHub-ready copy; analysis code and visualizations are retained. This is a course learning project, not a production dashboard.

## Author
Mochammad Syukur Alhamdulillah.
