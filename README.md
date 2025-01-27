# Deep PDF

A Python-based tool specifically designed to solve the challenge of extracting data from complex PDF tables, including nested tables and intricate layouts. While most PDF extraction tools struggle with complex table structures, this project uses advanced techniques to accurately parse and extract data from sophisticated table formats.

## Features

- Advanced table extraction handling:
  - Nested tables with multiple levels of hierarchy
  - Complex merged cells and spanning columns/rows
  - Tables with mixed formatting and styles
  - Multiple tables on the same page
  - Tables split across pages
- Intelligent structure recognition for nested data
- Web-based interface using Streamlit for easy interaction
- Modular architecture for different types of extractors
- OpenAI integration for enhanced parsing accuracy

## Key Differentiators

This tool specifically addresses common challenges in PDF table extraction:

- **Nested Structure Recognition**: Accurately identifies and preserves hierarchical relationships in nested tables
- **Complex Layout Handling**: Successfully processes tables with irregular layouts, merged cells, and varying formats
- **Structural Integrity**: Maintains the logical structure of complex tables in the extracted data
- **Format Preservation**: Retains the semantic meaning of nested data relationships

## Project Structure

```
pdf-extractor/
├── src/
│   └── pdf_extractor/
│       ├── config/          # Configuration and constants
│       ├── core/            # Core functionality and base classes
│       ├── extractors/      # Specialized table extractors
│       └── utils/           # Utility functions
├── streamlit_app/
│   └── app.py              # Streamlit web application
└── requirements.txt        # Project dependencies
```

## Requirements

- Python 3.9+
- Dependencies:
  - streamlit >= 1.24.0
  - openai >= 1.0.0
  - pdfplumber >= 0.9.0
  - Pillow >= 9.5.0
  - python-dotenv >= 1.0.0

## Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd pdf-extractor
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.streamlit/secrets.toml` file with necessary configurations (e.g., OpenAI API key)

## Usage

### Running the Web Interface

Start the Streamlit application:
```bash
cd streamlit_app
streamlit run app.py
```

The application will be available at `http://localhost:8501`

### Using as a Library

```python
from pdf_extractor.extractors.table_extractor import TableExtractor

# Initialize the extractor
extractor = TableExtractor()

# Extract complex tables from a PDF
tables = extractor.extract("path/to/your.pdf")

# The extracted data maintains nested structure
# Example output format for nested tables:
# {
#     'main_table': {
#         'header': ['Col1', 'Col2'],
#         'nested_tables': {
#             'position': [1, 1],  # Location in main table
#             'data': {...}        # Nested table content
#         }
#     }
# }
```

## Architecture

The project follows a modular architecture optimized for complex table extraction:

- `core/base_extractor.py`: Defines the base extractor class with common functionality
- `extractors/table_extractor.py`: Implements advanced table extraction logic
  - Handles nested structure detection
  - Manages complex cell relationships
  - Processes multi-level hierarchies
- `config/constants.py`: Contains configuration constants
- `utils/`: Helper functions and utilities for table processing

## Development

The project uses a modular structure that allows for easy extension:

1. Base classes in `core/` define common interfaces
2. Specialized extractors in `extractors/` implement complex table parsing
3. Configuration is centralized in `config/`
4. Web interface provides visual feedback and extraction results

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Here's how you can help improve this project:

1. **Fork the Repository**
   - Fork the project to your GitHub account
   - Clone your fork locally

2. **Create a Branch**
   - Create a new branch for your feature or bug fix
   - Use clear, descriptive branch names (e.g., `feature/nested-table-detection` or `fix/merged-cell-handling`)

3. **Make Changes**
   - Follow the existing code style and conventions
   - Add or update tests as needed
   - Add or update documentation as needed

4. **Test Your Changes**
   - Ensure all tests pass
   - Add new test cases for new features
   - Test with various PDF formats and table structures

5. **Submit a Pull Request**
   - Push your changes to your fork
   - Submit a pull request to the main repository
   - Provide a clear description of the changes
   - Link any relevant issues

6. **Code Review**
   - Address any code review feedback
   - Keep your PR up to date with the main branch

### Development Guidelines

- Follow PEP 8 style guidelines for Python code
- Write descriptive commit messages
- Document new features and changes
- Add type hints to Python functions
- Keep functions focused and modular

### Reporting Issues

When reporting issues, please include:

- A clear description of the problem
- Steps to reproduce the issue
- Expected vs actual behavior
- Sample PDF files (if possible)
- Your environment details (OS, Python version, etc.)

### Feature Requests

Feature requests are welcome! Please provide:

- A clear description of the feature
- Use cases and benefits
- Any potential implementation ideas

Thank you for contributing to PDF Extractor!
