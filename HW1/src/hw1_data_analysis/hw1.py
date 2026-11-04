"""Analyze Fremont Bridge bicycle counts for the CSE 583 HW1 assignment."""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


DATA_FILE = Path(__file__).with_name("bicycle_data.csv")
PLOT_FILE = Path(__file__).with_name("counts_by_hour.png")


def main():
    # Date is a timestamp (datetime64); the existing total, west, and east
    # sidewalk count columns are numeric counts (float64 because the CSV has
    # missing observations). Parse the source Date text as datetime64.
    df = pd.read_csv(DATA_FILE)
    df["Date"] = pd.to_datetime(df["Date"], format="%m/%d/%Y %I:%M:%S %p")
    west_column = "Fremont Bridge Sidewalks, south of N 34th St Cyclist West Sidewalk"
    east_column = "Fremont Bridge Sidewalks, south of N 34th St Cyclist East Sidewalk"

    # Keep counts numeric, representing missing observations as NaN.
    count_columns = [
        "Fremont Bridge Sidewalks, south of N 34th St Total",
        west_column,
        east_column,
    ]
    df[count_columns] = df[count_columns].apply(pd.to_numeric, errors="coerce")

    # Add the east + west count, hour of day, and calendar year.
    # min_count=2 prevents one-sided or fully missing observations from looking complete.
    df["Total Count"] = df[[east_column, west_column]].sum(axis=1, min_count=2)
    df["Hour"] = df["Date"].dt.hour
    df["Year"] = df["Date"].dt.year

    # Restrict the analysis to observations from 2016.
    data_2016 = df.loc[df["Year"] == 2016].copy()

    missing_points = int(data_2016["Total Count"].isna().sum())
    # There is 1 time point with missing East/West count data in 2016; drop it
    # so it cannot affect the hourly averages or busiest-hour calculation.
    data_2016 = data_2016.dropna(subset=["Total Count"])

    # Average counts for each clock hour over the 2016 observations.
    average_counts_by_hour = data_2016.groupby("Hour")["Total Count"].mean()
    average_counts_by_hour.plot(kind="bar", figsize=(10, 6))
    plt.title("Average Fremont Bridge Bicycle Counts by Hour (2016)")
    plt.xlabel("Hour of Day")
    plt.ylabel("Average Bicycle Count")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(PLOT_FILE)
    plt.close()

    busiest_hour = int(average_counts_by_hour.idxmax())
    # The busiest hour on average is 17:00 (5 PM).
    print(f"Missing 2016 time points: {missing_points}")
    print(f"Busiest hour on average: {busiest_hour}:00")


if __name__ == "__main__":
    main()
