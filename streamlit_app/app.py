import streamlit as st
from pathlib import Path
import tempfile
import json
import sys
import os

# Add the src directory to Python path
src_path = str(Path(__file__).parent.parent / 'src')
if src_path not in sys.path:
    sys.path.append(src_path)

from pdf_extractor.extractors.table_extractor import TableExtractor

def main():
    st.set_page_config(
        page_title="Deep PDF",
        page_icon="📄",
        layout="wide"
    )

    st.title("Deep PDF – Data Extractor for PDFs with complex tables ")
    st.write("Upload a PDF file to extract tables and convert them to structured data.")

    # Initialize session state
    if 'extracted_data' not in st.session_state:
        st.session_state.extracted_data = None

    # File uploader
    uploaded_file = st.file_uploader("Choose a PDF file", type=['pdf'])

    if uploaded_file is not None:
        # Show file details
        file_details = {
            "Filename": uploaded_file.name,
            "File size": f"{uploaded_file.size / 1024:.2f} KB"
        }
        st.write(file_details)

        # Process button
        if st.button("Extract Tables"):
            with st.spinner("Processing PDF..."):
                # Save uploaded file temporarily
                with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                    tmp_file.write(uploaded_file.getvalue())
                    temp_path = Path(tmp_file.name)

                try:
                    # Initialize extractor
                    extractor = TableExtractor(
                        api_key=st.secrets["OPENAI_API_KEY"]
                    )

                    # Extract tables
                    results = extractor.extract(temp_path)
                    st.session_state.extracted_data = results

                finally:
                    # Cleanup temporary file
                    temp_path.unlink()

    # Display results if they exist (only once)
    if st.session_state.extracted_data is not None:
        st.subheader("Extracted Data")
        results = st.session_state.extracted_data
        for page_data in results:
            with st.expander(f"Page {page_data['page_number']}"):
                if page_data['extraction_type'] == 'table':
                    st.json(page_data['content'])
                else:
                    st.text(page_data['content'])

if __name__ == "__main__":
    main()