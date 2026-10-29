import pandas as pd


def load_data(uploaded_file):
    """
    Load CSV or Excel data into a Pandas DataFrame.

    Parameters:
        uploaded_file: Streamlit UploadedFile object

    Returns:
        pandas.DataFrame
    """

    file_name = uploaded_file.name.lower()

    if file_name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)

    elif file_name.endswith(".xlsx"):
        df = pd.read_excel(uploaded_file)

    elif file_name.endswith(".xls"):
        df = pd.read_excel(uploaded_file)

    else:
        raise ValueError(
            "Unsupported file format. Please upload CSV or Excel."
        )

    if df.empty:
        raise ValueError("The uploaded file contains no data.")

    return df