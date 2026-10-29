import pandas as pd
import numpy as np


def get_basic_information(df):
    """
    Return basic information about the dataset.
    """

    return {
        "rows": df.shape[0],
        "columns": df.shape[1],
        "column_names": list(df.columns)
    }


def get_column_types(df):
    """
    Identify numerical and categorical columns.
    """

    numerical_columns = df.select_dtypes(
        include=np.number
    ).columns.tolist()

    categorical_columns = df.select_dtypes(
        exclude=np.number
    ).columns.tolist()

    return numerical_columns, categorical_columns


def get_missing_values(df):
    """
    Calculate missing values for every column.
    """

    missing = df.isnull().sum()

    missing = missing[missing > 0]

    return missing.sort_values(ascending=False)


def get_numeric_statistics(df):
    """
    Generate descriptive statistics for numerical columns.
    """

    numeric_df = df.select_dtypes(include=np.number)

    if numeric_df.empty:
        return pd.DataFrame()

    statistics = numeric_df.describe().T

    statistics["missing"] = numeric_df.isnull().sum()

    return statistics


def find_business_columns(df):
    """
    Try to identify common business-related columns.
    """

    business_columns = {}

    for column in df.columns:

        column_lower = str(column).lower()

        if any(
            keyword in column_lower
            for keyword in [
                "sales",
                "revenue",
                "turnover"
            ]
        ):
            business_columns["sales"] = column

        elif "profit" in column_lower:
            business_columns["profit"] = column

        elif any(
            keyword in column_lower
            for keyword in [
                "quantity",
                "qty",
                "units"
            ]
        ):
            business_columns["quantity"] = column

        elif any(
            keyword in column_lower
            for keyword in [
                "cost",
                "expense"
            ]
        ):
            business_columns["cost"] = column

    return business_columns


def calculate_business_metrics(df):
    """
    Calculate common business KPIs when suitable
    columns are available.
    """

    business_columns = find_business_columns(df)

    metrics = {}

    if "sales" in business_columns:

        column = business_columns["sales"]

        metrics["Total Sales"] = df[column].sum()
        metrics["Average Sales"] = df[column].mean()
        metrics["Maximum Sales"] = df[column].max()
        metrics["Minimum Sales"] = df[column].min()

    if "profit" in business_columns:

        column = business_columns["profit"]

        metrics["Total Profit"] = df[column].sum()
        metrics["Average Profit"] = df[column].mean()
        metrics["Maximum Profit"] = df[column].max()
        metrics["Minimum Profit"] = df[column].min()

    if "quantity" in business_columns:

        column = business_columns["quantity"]

        metrics["Total Quantity"] = df[column].sum()
        metrics["Average Quantity"] = df[column].mean()

    if "cost" in business_columns:

        column = business_columns["cost"]

        metrics["Total Cost"] = df[column].sum()
        metrics["Average Cost"] = df[column].mean()

    return metrics


def generate_summary(df):
    """
    Generate a human-readable summary of the dataset.
    """

    info = get_basic_information(df)

    numerical_columns, categorical_columns = get_column_types(df)

    business_columns = find_business_columns(df)

    summary = {
        "rows": info["rows"],
        "columns": info["columns"],
        "numerical_columns": numerical_columns,
        "categorical_columns": categorical_columns,
        "business_columns": business_columns
    }

    return summary