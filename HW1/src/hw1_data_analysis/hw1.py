"""Analyze Fremont Bridge bicycle counts for the CSE 583 HW1 assignment."""

from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


DATA_FILE = Path(__file__).with_name("bicycle_data.csv")
PLOT_FILE = Path(__file__).with_name("counts_by_hour.png")


def decode_date(value):
    """Decode the assignment's yyyy-mm-ddThh date or the CSV's date format."""
    date_text = str(value)
    if "T" in date_text:
        return datetime.strptime(date_text, "%Y-%m-%dT%H")
    if "\t" in date_text:
        return datetime.strptime(date_text, "%Y-%m-%d\t%H")
    return datetime.strptime(date_text, "%m/%d/%Y %I:%M:%S %p")


def main():
    # The CSV columns are Date (timestamp; should be datetime64[ns]), the
    # reported total count, west sidewalk count, and east sidewalk count
    # (all counts; should be integer values, with missing values allowed).
    # Parse Date as datetime and store counts as nullable integers so missing
    # observations remain NA without representing cyclist counts as floats.
    df = pd.read_csv(DATA_FILE)
    df["Date"] = pd.to_datetime(df["Date"].map(decode_date))
    west_column = "Fremont Bridge Sidewalks, south of N 34th St Cyclist West Sidewalk"
    east_column = "Fremont Bridge Sidewalks, south of N 34th St Cyclist East Sidewalk"

    # Keep counts numeric, representing missing observations as NaN.
    count_columns = [
        "Fremont Bridge Sidewalks, south of N 34th St Total",
        west_column,
        east_column,
    ]
    df[count_columns] = df[count_columns].apply(
        lambda column: pd.to_numeric(column, errors="coerce").astype("Int64")
    )

    # Add the east + west count, hour of day, and calendar year.
    # min_count=2 prevents one-sided or fully missing observations from looking complete.
    df["Total Count"] = df[[east_column, west_column]].sum(axis=1, min_count=2)
    df["Hour"] = df["Date"].dt.hour
    df["Year"] = df["Date"].dt.year

    # Restrict the analysis to observations from 2016.
    data_2016 = df.loc[df["Year"] == 2016].copy()

    missing_points = int(data_2016["Total Count"].isna().sum())
    # There is 1 time point with missing East/West count data in 2016; drop it
    # so it cannot affect the plot or busiest-hour calculation.
    data_2016 = data_2016.dropna(subset=["Total Count"])

    # Plot each 2016 hourly observation: clock hour on x, total East + West
    # bicycle count for that observation on y.
    plt.figure(figsize=(10, 6))
    plt.scatter(data_2016["Hour"], data_2016["Total Count"], alpha=0.25, s=10)
    plt.title("Fremont Bridge Bicycle Counts by Hour (2016)")
    plt.xlabel("Hour of Day")
    plt.ylabel("Total Bicycle Count")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(PLOT_FILE)
    plt.close()

    average_counts_by_hour = data_2016.groupby("Hour")["Total Count"].mean()
    busiest_hour = int(average_counts_by_hour.idxmax())
    # The busiest hour on average is 17:00 (5 PM).
    print(f"Missing 2016 time points: {missing_points}")
    print(f"Busiest hour on average: {busiest_hour}:00")


if __name__ == "__main__":
    main()
