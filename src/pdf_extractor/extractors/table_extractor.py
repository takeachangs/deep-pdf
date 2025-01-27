from pathlib import Path
from typing import Dict, List, Optional, Any
import pdfplumber
from openai import OpenAI
from ..config.constants import GPT4_MODEL, DEFAULT_RESOLUTION

from ..core.base_extractor import BaseExtractor

class TableExtractor(BaseExtractor):
    """Extractor for handling table content from PDFs."""
    
    def __init__(self, api_key: Optional[str] = None, config: Optional[Dict] = None):
        """Initialize the table extractor.
        
        Args:
            api_key: OpenAI API key
            config: Optional configuration dictionary
        """
        super().__init__(config)
        self.client = OpenAI(api_key=api_key)
    
    def validate_input(self, input_path: Path) -> bool:
        """Validate that the input file is a valid PDF."""
        return input_path.suffix.lower() == '.pdf'
    
    def extract_table_from_image(self, image: Any, model: str = GPT4_MODEL) -> Dict:
        """Extract table data from an image using OpenAI's vision model."""
        
        prompt = '''
            Your task is to analyze and extract data from this table with absolute precision. Follow these steps:

            1. First identify and analyze:
            - All header levels and their relationships
            - The type of data in each column (text, numbers, percentages, etc.)
            - Any special formatting or highlighted elements
            - Empty cell representations (-, N/A, blank, etc.)

            2. For data extraction:
            - Keep numbers exactly as they appear, including all formatting
            - Maintain the exact column-value relationships by tracing each value to its header
            - Preserve any cell's special formatting or emphasis
            - Report empty cells consistently
            - Maintain the original position of each value

            3. Before finalizing:
            - Verify each value is under its correct column by tracing back to headers
            - Check that the data types match their respective columns
            - Confirm no values have shifted between columns

            Return the data in a JSON structure that preserves the table's hierarchy and relationships.
        '''
        
        response = self.client.chat.completions.create(
            model=model,
            messages=[{
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {
                        "url": f"data:image/jpeg;base64,{self._image_to_base64(image)}"
                    }}
                ]
            }],
            response_format={"type": "json_object"},
            temperature=0
        )
        
        return response.choices[0].message.content
    
    def extract(self, input_path: Path) -> List[Dict]:
        """Extract tables from PDF file.
        
        Args:
            input_path: Path to PDF file
            
        Returns:
            List of dictionaries containing extracted content
        """
        if not self.validate_input(input_path):
            raise ValueError(f"Invalid PDF file: {input_path}")
        
        results = []
        
        with pdfplumber.open(input_path) as pdf:
            for i, page in enumerate(pdf.pages, start=1):
                tables = page.extract_tables()
                
                if tables:
                    img = page.to_image(resolution=self.config.get('resolution', DEFAULT_RESOLUTION)).original
                    content = self.extract_table_from_image(img)
                    content_type = "table"
                else:
                    content = (page.extract_text() or "").strip()
                    content_type = "text"
                
                results.append({
                    "page_number": i,
                    "extraction_type": content_type,
                    "content": content
                })
        
        return results
    
    def _image_to_base64(self, image: Any) -> str:
        """Convert PIL Image to base64 string."""
        import base64
        import io
        
        buffer = io.BytesIO()
        image.save(buffer, format="JPEG")
        return base64.b64encode(buffer.getvalue()).decode("utf-8")