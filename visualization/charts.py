import pandas as pd
import plotly.express as px


def create_histogram(df, column):
    """
    Create a histogram for a numerical column.
    """

    fig = px.histogram(
        df,
        x=column,
        title=f"Distribution of {column}",
        marginal="box"
    )

    fig.update_layout(
        xaxis_title=column,
        yaxis_title="Count",
        template="plotly_white"
    )

    return fig


def create_bar_chart(df, column):
    """
    Create a bar chart for a categorical column.
    """

    counts = df[column].value_counts().reset_index()

    counts.columns = [column, "Count"]

    fig = px.bar(
        counts,
        x=column,
        y="Count",
        title=f"{column} Distribution",
        text_auto=True
    )

    fig.update_layout(
        template="plotly_white"
    )

    return fig


def create_sales_trend(df, date_column, sales_column):
    """
    Create a sales trend over time.
    """

    trend = (
        df.groupby(date_column)[sales_column]
        .sum()
        .reset_index()
        .sort_values(date_column)
    )

    fig = px.line(
        trend,
        x=date_column,
        y=sales_column,
        markers=True,
        title="Sales Trend"
    )

    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Sales",
        template="plotly_white"
    )

    return fig


def create_profit_trend(df, date_column, profit_column):
    """
    Create a profit trend over time.
    """

    trend = (
        df.groupby(date_column)[profit_column]
        .sum()
        .reset_index()
        .sort_values(date_column)
    )

    fig = px.line(
        trend,
        x=date_column,
        y=profit_column,
        markers=True,
        title="Profit Trend"
    )

    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Profit",
        template="plotly_white"
    )

    return fig


def create_region_sales_chart(
    df,
    region_column,
    sales_column
):
    """
    Create sales by region chart.
    """

    region_data = (
        df.groupby(region_column)[sales_column]
        .sum()
        .reset_index()
        .sort_values(
            sales_column,
            ascending=False
        )
    )

    fig = px.bar(
        region_data,
        x=region_column,
        y=sales_column,
        title="Sales by Region",
        text_auto=".2s"
    )

    fig.update_layout(
        xaxis_title="Region",
        yaxis_title="Sales",
        template="plotly_white"
    )

    return fig


def create_region_profit_chart(
    df,
    region_column,
    profit_column
):
    """
    Create profit by region chart.
    """

    region_data = (
        df.groupby(region_column)[profit_column]
        .sum()
        .reset_index()
        .sort_values(
            profit_column,
            ascending=False
        )
    )

    fig = px.bar(
        region_data,
        x=region_column,
        y=profit_column,
        title="Profit by Region",
        text_auto=".2s"
    )

    fig.update_layout(
        xaxis_title="Region",
        yaxis_title="Profit",
        template="plotly_white"
    )

    return fig


def create_product_sales_chart(
    df,
    product_column,
    sales_column
):
    """
    Create sales by product chart.
    """

    product_data = (
        df.groupby(product_column)[sales_column]
        .sum()
        .reset_index()
        .sort_values(
            sales_column,
            ascending=False
        )
    )

    fig = px.bar(
        product_data,
        x=product_column,
        y=sales_column,
        title="Sales by Product",
        text_auto=".2s"
    )

    fig.update_layout(
        xaxis_title="Product",
        yaxis_title="Sales",
        template="plotly_white"
    )

    return fig


def create_product_profit_chart(
    df,
    product_column,
    profit_column
):
    """
    Create profit by product chart.
    """

    product_data = (
        df.groupby(product_column)[profit_column]
        .sum()
        .reset_index()
        .sort_values(
            profit_column,
            ascending=False
        )
    )

    fig = px.bar(
        product_data,
        x=product_column,
        y=profit_column,
        title="Profit by Product",
        text_auto=".2s"
    )

    fig.update_layout(
        xaxis_title="Product",
        yaxis_title="Profit",
        template="plotly_white"
    )

    return fig


def create_quantity_product_chart(
    df,
    product_column,
    quantity_column
):
    """
    Create quantity sold by product chart.
    """

    product_data = (
        df.groupby(product_column)[quantity_column]
        .sum()
        .reset_index()
        .sort_values(
            quantity_column,
            ascending=False
        )
    )

    fig = px.bar(
        product_data,
        x=product_column,
        y=quantity_column,
        title="Quantity Sold by Product",
        text_auto=True
    )

    fig.update_layout(
        xaxis_title="Product",
        yaxis_title="Quantity",
        template="plotly_white"
    )

    return fig