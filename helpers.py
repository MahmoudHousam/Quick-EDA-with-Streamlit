import pandas as pd
import numpy as np
import datetime as dt
import plotly.graph_objects as go
import streamlit as st

rename_cols = {
    "phone number": "phone_number",
    "next of kin": "next_of_kin",
    "phone number.1": "kin_phone_number",
    "med.ins": "medical_insurance",
}


def replace_values(row):
    if row == "TOH":
        return "No"
    elif row == "TIH":
        return "Yes"
    elif row == "Out":
        return "No"
    elif row == "IN":
        return "Yes"
    elif row == "FALSE":
        return "No"
    elif row == "TRUE":
        return "Yes"
    elif row == False:
        return "No"
    elif row == True:
        return "Yes"
    elif row == "M":
        return "Male"
    elif row == "F":
        return "Female"
    elif row == "m":
        return "Yes"
    elif row == "A":
        return "Yes"
    elif row == "n":
        return "No"
    else:
        np.nan


def to_datetime(df):
    try:
        df = pd.to_datetime(df, errors="coerce")
    except:
        np.nan
    return df


def subtract_from_current_date(col):
    new_col = round((pd.Timestamp.now().normalize() - col) / np.timedelta64(1, "Y"), 2)
    return new_col


def intervals(row):
    if row < 1:
        return "Beginner Experience"
    elif 1 <= row <= 3:
        return "Junior Experience"
    elif 3 < row <= 5:
        return "Senior Experience"
    elif 5 < row <= 7:
        return "Supervisor Experience"
    elif row > 7:
        return "Head Experience"
    else:
        return np.nan


def years_of_experience(row):
    if (row["year"] == 2016) and (row["turnover"] == "Yes"):
        return (row["ended_at_ahc"] - row["started_at_ahc"]) / np.timedelta64(1, "Y")
    elif (row["year"] == 2016) and (row["turnover"] == "No"):
        return (pd.to_datetime("2016-12-31") - row["started_at_ahc"]) / np.timedelta64(
            1, "Y"
        )
    elif (row["year"] == 2017) and (row["turnover"] == "Yes"):
        return (row["ended_at_ahc"] - row["started_at_ahc"]) / np.timedelta64(1, "Y")
    elif (row["year"] == 2017) and (row["turnover"] == "No"):
        return (pd.to_datetime("2017-12-31") - row["started_at_ahc"]) / np.timedelta64(
            1, "Y"
        )
    elif (row["year"] == 2018) and (row["turnover"] == "Yes"):
        return (row["ended_at_ahc"] - row["started_at_ahc"]) / np.timedelta64(1, "Y")
    elif (row["year"] == 2018) and (row["turnover"] == "No"):
        return (pd.to_datetime("2018-12-31") - row["started_at_ahc"]) / np.timedelta64(
            1, "Y"
        )
    elif (row["year"] == 2019) and (row["turnover"] == "Yes"):
        return (row["ended_at_ahc"] - row["started_at_ahc"]) / np.timedelta64(1, "Y")
    elif (row["year"] == 2019) and (row["turnover"] == "No"):
        return (pd.to_datetime("2019-12-31") - row["started_at_ahc"]) / np.timedelta64(
            1, "Y"
        )
    elif (row["year"] == 2020) and (row["turnover"] == "Yes"):
        return (row["ended_at_ahc"] - row["started_at_ahc"]) / np.timedelta64(1, "Y")
    elif (row["year"] == 2020) and (row["turnover"] == "No"):
        return (
            pd.Timestamp.now().normalize() - row["started_at_ahc"]
        ) / np.timedelta64(1, "Y")


def explore_nans(df, title):
    """a function that takes a dataframe and inspect the Null vs
    Not-null values to visualize a groupped bar chart that will help take
    decisions to deal with missing data.

    Args:
        df: pandas dataframe
        title: (string): x label title

    Returns:
        bar chart: Null vs Not-null values
    """
    df_null = df.isnull().sum()
    df_not_null = df.notnull().sum()
    labels = df.columns.tolist()
    null_values = df_null.values.tolist()
    not_null_values = df_not_null.values.tolist()
    data = [
        go.Bar(
            name="Not Null",
            x=not_null_values,
            y=labels,
            orientation="h",
            marker=dict(
                color="rgb(128,128,128)",
            ),
        ),
        go.Bar(
            name="Null",
            x=null_values,
            y=labels,
            orientation="h",
            marker=dict(
                color="rgb(192,192,192)",
            ),
        ),
    ]
    layout = go.Layout(title=title, barmode="stack", yaxis={"dtick": 1})
    fig = go.Figure(data, layout)
    return st.plotly_chart(fig, use_container_width=False)


def tables(df):
    table = go.Figure(
        go.Table(
            header=dict(values=df.reset_index().columns.tolist(), align="left"),
            cells=dict(
                values=df.reset_index().transpose().values.tolist(), align="left"
            ),
        )
    )
    return st.plotly_chart(table, use_container_width=False)