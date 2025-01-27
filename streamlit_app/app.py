import streamlit as st
from pathlib import Path
import tempfile
import json
import sys
import os
import time
import pdfplumber
from PIL import Image
import io

# Add the src directory to Python path
src_path = str(Path(__file__).parent.parent / 'src')
if src_path not in sys.path:
    sys.path.append(src_path)

from pdf_extractor.extractors.table_extractor import TableExtractor

def render_pdf_page(pdf_bytes: bytes, page_number: int) -> Image.Image:
    """Render a PDF page as an image using pdfplumber."""
    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        page = pdf.pages[page_number - 1]
        return page.to_image().original

def get_download_json(results):
    """Prepare the complete JSON data for download."""
    full_data = {
        "total_pages": len(results),
        "pages": results,
        "metadata": {
            "extraction_time": st.session_state.processing_time,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
    }
    return json.dumps(full_data, indent=2, ensure_ascii=False).encode('utf-8')

def main():
    st.set_page_config(
        page_title="Deep PDF",
        page_icon="📄",
        layout="wide"
    )

    # Custom CSS
    st.markdown("""
        <style>
        /* Hide Streamlit elements */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .uploadedFile {display: none;}
        
        /* Layout and spacing */
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
            max-width: 95%;
        }
        
        /* Title and text styles */
        h1 {
            font-size: 2rem !important;
            font-weight: 600 !important;
            margin-bottom: 2rem !important;
        }
        
        h3 {
            font-size: 1.2rem !important;
            font-weight: 500 !important;
            margin-bottom: 1rem !important;
        }
        
        /* JSON container */
        .stJson {
            height: calc(100vh - 300px) !important;
            min-height: 600px;
            overflow-y: auto !important;
            padding: 1rem !important;
            border-radius: 4px !important;
        }
        
        /* Ensure JSON content stays within bounds */
        .stJson > div {
            overflow: auto !important;
            max-width: 100% !important;
        }

        /* Navigation styling */
        .nav-group {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 1rem;
        }
        
        .page-nav {
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        
        .stSelectbox {
            min-width: 100px;
        }
        </style>
    """, unsafe_allow_html=True)

    st.title("Deep PDF")

    # File uploader with instructions
    uploaded_file = st.file_uploader("Upload PDF file", type=['pdf'])

    # Initialize session state
    if 'extracted_data' not in st.session_state:
        st.session_state.extracted_data = None
    if 'processing_time' not in st.session_state:
        st.session_state.processing_time = None
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 1
    if 'pdf_content' not in st.session_state:
        st.session_state.pdf_content = None

    if uploaded_file is not None:
        st.session_state.pdf_content = uploaded_file.getvalue()
        
        # Process button
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("Extract Tables"):
                with st.spinner("Processing..."):
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                        tmp_file.write(st.session_state.pdf_content)
                        temp_path = Path(tmp_file.name)

                    try:
                        extractor = TableExtractor(
                            api_key=st.secrets["OPENAI_API_KEY"]
                        )
                        start_time = time.time()
                        results = extractor.extract(temp_path)
                        processing_time = time.time() - start_time
                        
                        st.session_state.extracted_data = results
                        st.session_state.processing_time = processing_time
                        st.session_state.current_page = 1

                    finally:
                        temp_path.unlink()

    # Main content section
    if st.session_state.extracted_data is not None and st.session_state.pdf_content is not None:
        results = st.session_state.extracted_data
        total_pages = len(results)
        
        # Top controls row
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col1:
            st.info(f"⏱️ {st.session_state.processing_time:.1f}s")

        # Page navigation
        with col2:
            left_col, mid_col, right_col = st.columns([1, 3, 1])
            
            with left_col:
                if st.button("◀", disabled=st.session_state.current_page <= 1):
                    st.session_state.current_page -= 1
            
            with mid_col:
                # Use radio buttons styled as a dropdown
                page_options = [f"Page {i}/{total_pages}" for i in range(1, total_pages + 1)]
                selected = st.select_slider(
                    "Select page",
                    options=page_options,
                    value=f"Page {st.session_state.current_page}/{total_pages}",
                    label_visibility="collapsed"
                )
                st.session_state.current_page = page_options.index(selected) + 1
            
            with right_col:
                if st.button("▶", disabled=st.session_state.current_page >= total_pages):
                    st.session_state.current_page += 1

        with col3:
            st.download_button(
                "Download JSON",
                data=get_download_json(results),
                file_name="extracted_data.json",
                mime="application/json"
            )

        st.divider()

        # Main content columns
        json_col, page_col = st.columns(2)
        current_page_data = results[st.session_state.current_page - 1]

        with json_col:
            st.subheader(f"Extracted Data (Page {current_page_data['page_number']})")
            if current_page_data['extraction_type'] == 'table':
                st.json(current_page_data['content'])
            else:
                st.text(current_page_data['content'])

        with page_col:
            st.subheader(f"PDF Preview (Page {current_page_data['page_number']})")
            try:
                page_image = render_pdf_page(
                    st.session_state.pdf_content,
                    current_page_data['page_number']
                )
                st.image(page_image, use_container_width=True)
            except Exception as e:
                st.error(f"Error rendering page: {str(e)}")

if __name__ == "__main__":
    main()