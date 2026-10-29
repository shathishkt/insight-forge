import os

import streamlit as st
import pandas as pd

from core.data_loader import load_data

from core.data_analyzer import (
    get_basic_information,
    get_column_types,
    get_missing_values,
    get_numeric_statistics,
    find_business_columns,
    calculate_business_metrics
)

from core.llm_service import ask_llm
from core.query_processor import (
    detect_query_type,
    calculate_data_result
)

from visualization.charts import (
    create_histogram,
    create_bar_chart,
    create_sales_trend,
    create_profit_trend,
    create_region_sales_chart,
    create_region_profit_chart,
    create_product_sales_chart,
    create_product_profit_chart,
    create_quantity_product_chart
)

from core.document_loader import (
    load_document
)

from core.rag_service import (
    create_vectorstore,
    build_rag_context
)

from core.llm_service import (
    ask_rag_llm
)

# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="InsightForge",
    page_icon="📊",
    layout="wide"
)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
    

# ==========================================================
# CUSTOM CSS
# ==========================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 0px;
    }

    .subtitle {
        font-size: 18px;
        color: #666666;
        margin-bottom: 25px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ==========================================================
# HEADER
# ==========================================================

st.markdown(
    '<div class="main-title">📊 InsightForge</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'AI-Powered Business Intelligence Assistant'
    '</div>',
    unsafe_allow_html=True
)


# ==========================================================
# SIDEBAR
# ==========================================================

st.sidebar.title("⚙️ Controls")

uploaded_file = st.sidebar.file_uploader(
    "Upload Business Data",
    type=["csv", "xlsx", "xls"]
)

st.sidebar.divider()

st.sidebar.subheader(
    "📚 Knowledge Base"
)

uploaded_document = st.sidebar.file_uploader(
    "Upload Business Document",
    type=["pdf", "txt", "docx"]
)

if uploaded_document is not None:

    try:

        os.makedirs(
            "documents",
            exist_ok=True
        )

        document_path = os.path.join(
            "documents",
            uploaded_document.name
        )

        with open(
            document_path,
            "wb"
        ) as file:

            file.write(
                uploaded_document.getbuffer()
            )


        # ----------------------------------------------
        # Extract text
        # ----------------------------------------------

        document_text = load_document(
            document_path
        )


        # ----------------------------------------------
        # Create embeddings and vector store
        # ----------------------------------------------

        create_vectorstore(
            document_text,
            uploaded_document.name
        )


        st.sidebar.success(
            "Document indexed successfully."
        )


    except Exception as error:

        st.sidebar.error(
            f"Document processing failed: {error}"
        )
# ==========================================================
# INITIAL STATE
# ==========================================================

if uploaded_file is None:

    st.info(
        """
        👈 Upload a CSV or Excel business datasets
        from the sidebar to begin.
        """
    )

    st.markdown(
        """
        ### What InsightForge can do

        📈 Analyze sales and profit trends

        🌎 Compare regional performance

        📦 Analyze product performance

        📊 Generate business KPIs

        🔍 Identify data-quality issues

        🤖 Ask business questions using AI
        """
    )

    st.stop()


# ==========================================================
# LOAD DATA
# ==========================================================

try:

    df = load_data(uploaded_file)

except Exception as error:

    st.error(
        f"Unable to load the file: {error}"
    )

    st.stop()


st.success(
    f"Loaded successfully: {uploaded_file.name}"
)


# ==========================================================
# CONVERT DATE COLUMNS
# ==========================================================

date_columns = []

for column in df.columns:

    if (
        df[column].dtype == "object"
        and "date" in column.lower()
    ):

        try:

            df[column] = pd.to_datetime(
                df[column]
            )

            date_columns.append(column)

        except Exception:
            pass


# ==========================================================
# IDENTIFY COLUMNS
# ==========================================================

numerical_columns, categorical_columns = (
    get_column_types(df)
)

business_columns = find_business_columns(df)


# ==========================================================
# SIDEBAR FILTERS
# ==========================================================

st.sidebar.divider()

st.sidebar.subheader("🔎 Filters")


# Region filter

region_column = None

for column in categorical_columns:

    if "region" in column.lower():

        region_column = column
        break


if region_column:

    regions = sorted(
        df[region_column]
        .dropna()
        .unique()
        .tolist()
    )

    selected_regions = st.sidebar.multiselect(
        "Region",
        regions,
        default=regions
    )

else:

    selected_regions = None


# Product filter

product_column = None

for column in categorical_columns:

    if "product" in column.lower():

        product_column = column
        break


if product_column:

    products = sorted(
        df[product_column]
        .dropna()
        .unique()
        .tolist()
    )

    selected_products = st.sidebar.multiselect(
        "Product",
        products,
        default=products
    )

else:

    selected_products = None


# ==========================================================
# APPLY FILTERS
# ==========================================================

filtered_df = df.copy()


if (
    region_column
    and selected_regions is not None
):

    filtered_df = filtered_df[
        filtered_df[region_column].isin(
            selected_regions
        )
    ]


if (
    product_column
    and selected_products is not None
):

    filtered_df = filtered_df[
        filtered_df[product_column].isin(
            selected_products
        )
    ]


# ==========================================================
# DASHBOARD HEADER
# ==========================================================

st.header("📊 Business Dashboard")


# ==========================================================
# KPI SECTION
# ==========================================================

st.subheader("Key Performance Indicators")


metrics = calculate_business_metrics(
    filtered_df
)


# ----------------------------------------------------------
# KPI VALUES
# ----------------------------------------------------------

total_sales = metrics.get(
    "Total Sales",
    0
)

total_profit = metrics.get(
    "Total Profit",
    0
)

total_quantity = metrics.get(
    "Total Quantity",
    0
)

total_cost = metrics.get(
    "Total Cost",
    0
)


# ----------------------------------------------------------
# PROFIT MARGIN
# ----------------------------------------------------------

if total_sales != 0:

    profit_margin = (
        total_profit / total_sales
    ) * 100

else:

    profit_margin = 0


# ==========================================================
# KPI CARDS
# ==========================================================

col1, col2, col3, col4, col5 = st.columns(5)


with col1:

    st.metric(
        "💰 Total Sales",
        f"{total_sales:,.0f}"
    )


with col2:

    st.metric(
        "📈 Total Profit",
        f"{total_profit:,.0f}"
    )


with col3:

    st.metric(
        "📦 Quantity Sold",
        f"{total_quantity:,.0f}"
    )


with col4:

    st.metric(
        "💸 Total Cost",
        f"{total_cost:,.0f}"
    )


with col5:

    st.metric(
        "📊 Profit Margin",
        f"{profit_margin:.2f}%"
    )


# ==========================================================
# DASHBOARD TABS
# ==========================================================

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "📈 Trends",
        "🌎 Regions",
        "📦 Products",
        "🔍 Data Analysis"
    ]
)


# ==========================================================
# TAB 1 — TRENDS
# ==========================================================

with tab1:

    st.subheader(
        "Sales and Profit Trends"
    )

    if date_columns:

        date_column = date_columns[0]

        # --------------------------------------------------
        # SALES TREND
        # --------------------------------------------------

        if "sales" in business_columns:

            sales_column = business_columns[
                "sales"
            ]

            sales_fig = create_sales_trend(
                filtered_df,
                date_column,
                sales_column
            )

            st.plotly_chart(
                sales_fig,
                use_container_width=True
            )

        # --------------------------------------------------
        # PROFIT TREND
        # --------------------------------------------------

        if "profit" in business_columns:

            profit_column = business_columns[
                "profit"
            ]

            profit_fig = create_profit_trend(
                filtered_df,
                date_column,
                profit_column
            )

            st.plotly_chart(
                profit_fig,
                use_container_width=True
            )

    else:

        st.warning(
            "No date column was detected."
        )


# ==========================================================
# TAB 2 — REGIONS
# ==========================================================

with tab2:

    st.subheader(
        "Regional Performance"
    )

    if region_column:

        col1, col2 = st.columns(2)

        with col1:

            if "sales" in business_columns:

                sales_column = business_columns[
                    "sales"
                ]

                fig = create_region_sales_chart(
                    filtered_df,
                    region_column,
                    sales_column
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

        with col2:

            if "profit" in business_columns:

                profit_column = business_columns[
                    "profit"
                ]

                fig = create_region_profit_chart(
                    filtered_df,
                    region_column,
                    profit_column
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

    else:

        st.info(
            "No Region column was detected."
        )


# ==========================================================
# TAB 3 — PRODUCTS
# ==========================================================

with tab3:

    st.subheader(
        "Product Performance"
    )

    if product_column:

        # --------------------------------------------------
        # SALES BY PRODUCT
        # --------------------------------------------------

        if "sales" in business_columns:

            sales_column = business_columns[
                "sales"
            ]

            fig = create_product_sales_chart(
                filtered_df,
                product_column,
                sales_column
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )


        # --------------------------------------------------
        # PROFIT BY PRODUCT
        # --------------------------------------------------

        if "profit" in business_columns:

            profit_column = business_columns[
                "profit"
            ]

            fig = create_product_profit_chart(
                filtered_df,
                product_column,
                profit_column
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )


        # --------------------------------------------------
        # QUANTITY BY PRODUCT
        # --------------------------------------------------

        if "quantity" in business_columns:

            quantity_column = business_columns[
                "quantity"
            ]

            fig = create_quantity_product_chart(
                filtered_df,
                product_column,
                quantity_column
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

    else:

        st.info(
            "No Product column was detected."
        )


# ==========================================================
# TAB 4 — DATA ANALYSIS
# ==========================================================

with tab4:

    st.subheader(
        "Dataset Analysis"
    )

    # ------------------------------------------------------
    # DATA PREVIEW
    # ------------------------------------------------------

    st.write("### Data Preview")

    st.dataframe(
        filtered_df.head(20),
        use_container_width=True
    )


    # ------------------------------------------------------
    # DATA QUALITY
    # ------------------------------------------------------

    st.write("### Data Quality")

    missing_values = get_missing_values(
        filtered_df
    )

    if not missing_values.empty:

        missing_df = (
            missing_values
            .reset_index()
        )

        missing_df.columns = [
            "Column",
            "Missing Values"
        ]

        st.dataframe(
            missing_df,
            use_container_width=True
        )

    else:

        st.success(
            "No missing values detected."
        )


    # ------------------------------------------------------
    # STATISTICS
    # ------------------------------------------------------

    st.write(
        "### Numerical Statistics"
    )

    statistics = get_numeric_statistics(
        filtered_df
    )

    if not statistics.empty:

        st.dataframe(
            statistics.round(2),
            use_container_width=True
        )

    else:

        st.info(
            "No numerical columns found."
        )


# ==========================================================
# DOWNLOAD FILTERED DATA
# ==========================================================

st.divider()

st.subheader(
    "⬇️ Export Data"
)


csv_data = filtered_df.to_csv(
    index=False
).encode("utf-8")


st.download_button(
    label="Download Filtered Data",
    data=csv_data,
    file_name="insightforge_filtered_data.csv",
    mime="text/csv"
)

# ==========================================================
# AI BUSINESS ASSISTANT
# ==========================================================

st.divider()

st.header("🤖 Ask InsightForge")

# ==========================================================
# DOCUMENT Q&A
# ==========================================================

st.divider()

st.header(
    "📚 Ask Your Business Documents"
)

st.write(
    """
    Ask questions about the documents that
    you have uploaded into the InsightForge
    knowledge base.
    """
)


document_question = st.text_input(
    "Ask a document question",
    placeholder=(
        "Example: What is the company's return policy?"
    ),
    key="document_question"
)


if st.button(
    "📚 Search Knowledge Base",
    type="secondary"
):

    if not document_question.strip():

        st.warning(
            "Please enter a question."
        )

    else:

        try:

            with st.spinner(
                "Searching business documents..."
            ):

                rag_context = (
                    build_rag_context(
                        document_question
                    )
                )


            with st.spinner(
                "Generating answer..."
            ):

                answer = ask_rag_llm(
                    document_question,
                    rag_context
                )


            st.subheader(
                "💡 Document-Based Answer"
            )

            st.write(
                answer
            )


            with st.expander(
                "View retrieved context"
            ):

                st.text(
                    rag_context
                )


        except Exception as error:

            st.error(
                f"RAG processing failed: {error}"
            )

st.write(
    """
    Ask questions about your business data using
    natural language.
    """
)


question = st.text_input(
    "Ask a business question",
    placeholder=(
        "Example: Which region generated the highest profit?"
    )
)


if st.button("🔍 Analyze", type="primary"):

    if not question.strip():

        st.warning(
            "Please enter a question."
        )

    else:

        try:

            # --------------------------------------------------
            # Determine question type
            # --------------------------------------------------

            query_type = detect_query_type(
                question
            )


            # --------------------------------------------------
            # Data question
            # --------------------------------------------------

            if query_type == "data":

                data_context = (
                    calculate_data_result(
                        filtered_df,
                        question,
                        business_columns
                    )
                )


            # --------------------------------------------------
            # General business question
            # --------------------------------------------------

            else:

                data_context = (
                    "Dataset summary:\n"
                    f"Rows: {len(filtered_df)}\n"
                    f"Columns: "
                    f"{list(filtered_df.columns)}\n\n"
                    f"Business columns: "
                    f"{business_columns}\n\n"
                    "Sample data:\n"
                    f"{filtered_df.head(10).to_string()}"
                )


            # --------------------------------------------------
            # Generate AI answer
            # --------------------------------------------------

            with st.spinner(
                "InsightForge is analyzing your question..."
            ):

                answer = ask_llm(
                    question,
                    data_context
                )   
                
                st.session_state.chat_history.append(
                {
                    "question": question,
                    "answer": answer
                }
)


            # --------------------------------------------------
            # Display answer
            # --------------------------------------------------

            st.subheader(
                "💡 InsightForge Analysis"
            )

            st.write(answer)


            # --------------------------------------------------
            # Show technical context
            # --------------------------------------------------

            with st.expander(
                "View analysis context"
            ):

                st.write(
                    f"Query type: `{query_type}`"
                )

                st.text(
                    data_context
                )


        except Exception as error:

            st.error(
                f"""
                Unable to process your question.

                Error: {error}
                """
            )
            
# ==========================================================
# CHAT HISTORY
# ==========================================================

if st.session_state.chat_history:

    st.divider()

    st.subheader(
        "💬 Previous Questions"
    )

    for item in reversed(
        st.session_state.chat_history
    ):

        with st.expander(
            item["question"]
        ):

            st.write(
                item["answer"]
            )
# ==========================================================
# FOOTER
# ==========================================================

st.divider()

st.caption(
    "InsightForge — AI-Powered Business Intelligence Assistant"
)