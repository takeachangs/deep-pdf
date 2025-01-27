from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from pathlib import Path

class BaseExtractor(ABC):
    """Base class for all extractors."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the base extractor.
        
        Args:
            config: Optional configuration dictionary
        """
        self.config = config or {}
        
    @abstractmethod
    def extract(self, input_path: Path) -> Any:
        """Extract content from the input path.
        
        Args:
            input_path: Path to the input file
            
        Returns:
            Extracted content in the appropriate format
        """
        pass
    
    @abstractmethod
    def validate_input(self, input_path: Path) -> bool:
        """Validate the input file.
        
        Args:
            input_path: Path to validate
            
        Returns:
            True if valid, False otherwise
        """
        pass
    
    def cleanup(self) -> None:
        """Cleanup any resources."""
        pass
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cleanup()