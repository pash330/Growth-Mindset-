from io import BytesIO
import streamlit as st
import pandas as pd
import os

# Set Streamlit page configuration
st.set_page_config(page_title="Smart Data Cleaner & Converter", layout="wide")

# Custom CSS for styling
st.markdown(
    """
    <style>
    .stApp {
        background-color: #F1E8B8;
        color: black;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# Title and description
st.title("📀 Smart Data Cleaner & Converter by Pashmina Zehra!")
st.write("Convert files between CSV and Excel formats with advanced data cleaning and visualization features.!")

# File uploader
uploaded_files = st.file_uploader(
    "Upload your file (accepts CSV or Excel ):",
    type=["csv", "xlsx"],
    accept_multiple_files=True
)

# Process uploaded files
if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df =  pd.read_excel(file, engine="openpyxl")

        else:
            st.error(f"Unsupported file type: {file_ext}")
            continue

        # Display the first few rows of the uploaded file
        st.write("Preview the head of the DataFrame")
        st.dataframe(df.head())

        # Data Cleaning Options
        st.subheader("Data Cleaning Options")
        if st.checkbox(f"Clean data for {file.name}"):
            col1, col2 = st.columns(2)

            # Column 1: Remove Duplicates
            with col1:
                if st.button(f"Remove duplicates from {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("✅ Duplicates removed!")

            # Column 2: Fill Missing Values
            with col2:
                if st.button(f"Fill missing values for {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("✅ Missing values filled!")

            # Select Columns to Keep
            st.subheader("Select Columns to Keep")
            columns = st.multiselect(f"Choose columns for {file.name}", df.columns, default=df.columns)
            df = df[columns]

        # Data Visualization Section
        st.subheader("Data Visualization")
        if st.checkbox(f"Show visualization for {file.name}"):
            st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])

        # Conversion Option
        st.subheader("Conversion Options")
        conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)

        if st.button(f"Convert {file.name}"):
            buffer = BytesIO()

            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"
            
            elif conversion_type == "Excel":
                df.to_excel(buffer, index=False)
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

            buffer.seek(0)  # Reset buffer position

            # Download button
            st.download_button(
                label=f"Download {file.name} as {conversion_type}",
                data=buffer,
                file_name=file_name,
                mime=mime_type
            )

st.success("All files processed successfully!")