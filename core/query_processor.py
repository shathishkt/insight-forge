import pandas as pd


def detect_query_type(question):
    """
    Determine whether the question is likely to require
    numerical/data analysis or general business reasoning.
    """

    question_lower = question.lower()

    numerical_keywords = [
        "total",
        "sum",
        "average",
        "mean",
        "maximum",
        "minimum",
        "highest",
        "lowest",
        "best",
        "worst",
        "sales",
        "profit",
        "revenue",
        "cost",
        "quantity",
        "margin",
        "percentage",
        "%",
        "compare",
        "trend",
        "growth"
    ]

    for keyword in numerical_keywords:

        if keyword in question_lower:
            return "data"

    return "general"


def calculate_data_result(df, question, business_columns):
    """
    Perform basic numerical analysis based on the user's
    question.

    Returns a text context that can be supplied to the LLM.
    """

    question_lower = question.lower()

    results = []

    # --------------------------------------------------
    # Sales
    # --------------------------------------------------

    if "sales" in business_columns:

        sales_column = business_columns["sales"]

        if "total" in question_lower:

            total_sales = df[sales_column].sum()

            results.append(
                f"Total sales: {total_sales:,.2f}"
            )

        elif (
            "average" in question_lower
            or "mean" in question_lower
        ):

            average_sales = df[
                sales_column
            ].mean()

            results.append(
                f"Average sales: {average_sales:,.2f}"
            )

        elif (
            "highest" in question_lower
            or "maximum" in question_lower
        ):

            maximum_sales = df[
                sales_column
            ].max()

            results.append(
                f"Maximum sales: {maximum_sales:,.2f}"
            )

        elif "lowest" in question_lower:

            minimum_sales = df[
                sales_column
            ].min()

            results.append(
                f"Minimum sales: {minimum_sales:,.2f}"
            )


    # --------------------------------------------------
    # Profit
    # --------------------------------------------------

    if "profit" in business_columns:

        profit_column = business_columns["profit"]

        if "total" in question_lower:

            total_profit = df[
                profit_column
            ].sum()

            results.append(
                f"Total profit: {total_profit:,.2f}"
            )

        elif (
            "average" in question_lower
            or "mean" in question_lower
        ):

            average_profit = df[
                profit_column
            ].mean()

            results.append(
                f"Average profit: {average_profit:,.2f}"
            )

        elif (
            "highest" in question_lower
            or "maximum" in question_lower
        ):

            maximum_profit = df[
                profit_column
            ].max()

            results.append(
                f"Maximum profit: {maximum_profit:,.2f}"
            )

        elif "lowest" in question_lower:

            minimum_profit = df[
                profit_column
            ].min()

            results.append(
                f"Minimum profit: {minimum_profit:,.2f}"
            )


    # --------------------------------------------------
    # Regional analysis
    # --------------------------------------------------

    region_column = None

    for column in df.columns:

        if "region" in str(column).lower():

            region_column = column
            break


    if region_column:

        if (
            "region" in question_lower
            and "profit" in question_lower
        ):

            profit_column = business_columns.get(
                "profit"
            )

            if profit_column:

                regional_profit = (
                    df.groupby(region_column)[
                        profit_column
                    ]
                    .sum()
                    .sort_values(
                        ascending=False
                    )
                )

                results.append(
                    "Profit by region:\n"
                    + regional_profit
                    .to_string()
                )


        elif (
            "region" in question_lower
            and "sales" in question_lower
        ):

            sales_column = business_columns.get(
                "sales"
            )

            if sales_column:

                regional_sales = (
                    df.groupby(region_column)[
                        sales_column
                    ]
                    .sum()
                    .sort_values(
                        ascending=False
                    )
                )

                results.append(
                    "Sales by region:\n"
                    + regional_sales
                    .to_string()
                )


    # --------------------------------------------------
    # Product analysis
    # --------------------------------------------------

    product_column = None

    for column in df.columns:

        if "product" in str(column).lower():

            product_column = column
            break


    if product_column:

        if (
            "product" in question_lower
            and "profit" in question_lower
        ):

            profit_column = business_columns.get(
                "profit"
            )

            if profit_column:

                product_profit = (
                    df.groupby(product_column)[
                        profit_column
                    ]
                    .sum()
                    .sort_values(
                        ascending=False
                    )
                )

                results.append(
                    "Profit by product:\n"
                    + product_profit
                    .to_string()
                )


        elif (
            "product" in question_lower
            and "sales" in question_lower
        ):

            sales_column = business_columns.get(
                "sales"
            )

            if sales_column:

                product_sales = (
                    df.groupby(product_column)[
                        sales_column
                    ]
                    .sum()
                    .sort_values(
                        ascending=False
                    )
                )

                results.append(
                    "Sales by product:\n"
                    + product_sales
                    .to_string()
                )


    # --------------------------------------------------
    # Return result
    # --------------------------------------------------

    if not results:

        return (
            "No specific numerical calculation "
            "was identified. Use the available "
            "dataset context to answer the question."
        )

    return "\n\n".join(results)