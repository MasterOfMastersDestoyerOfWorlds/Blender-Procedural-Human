"""
Yandex Image Search integration for Blender.

This module provides image search functionality using the Yandex Images service.
Search history is tracked for convenience.
"""

import os
import tempfile
from typing import List, Dict, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
import requests
from PIL import Image
from io import BytesIO

from procedural_human.logger import logger


@dataclass 
class SearchResult:
    """Represents a single image search result."""
    url: str
    thumbnail_url: str
    title: str = ""
    width: int = 0
    height: int = 0
    
    def download_full(self) -> Optional[Image.Image]:
        """Download the full resolution image."""
        try:
            response = requests.get(self.url, timeout=30)
            response.raise_for_status()
            return Image.open(BytesIO(response.content)).convert("RGB")
        except Exception as e:
            logger.error(f"Failed to download image: {e}")
            return None
    
    def download_thumbnail(self) -> Optional[Image.Image]:
        """Download the thumbnail image."""
        try:
            url = self.thumbnail_url or self.url
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return Image.open(BytesIO(response.content)).convert("RGB")
        except Exception as e:
            logger.error(f"Failed to download thumbnail: {e}")
            return None


@dataclass
class SearchQuery:
    """Represents a search query with filters."""
    query: str
    orientation: str = "any"  # "any", "horizontal", "vertical", "square"
    size: str = "large"  # "any", "small", "medium", "large", "wallpaper"
    timestamp: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "query": self.query,
            "orientation": self.orientation,
            "size": self.size,
            "timestamp": self.timestamp.isoformat(),
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SearchQuery":
        return cls(
            query=data["query"],
            orientation=data.get("orientation", "any"),
            size=data.get("size", "large"),
            timestamp=datetime.fromisoformat(data.get("timestamp", datetime.now().isoformat())),
        )


class YandexImageSearch:
    """
    Yandex Image Search client with history tracking.
    
    Uses web scraping to fetch image results from Yandex Images.
    Search history is maintained for quick access to previous searches.
    """
    
    # Orientation filter mapping
    ORIENTATION_MAP = {
        "any": "",
        "horizontal": "horizontal",
        "vertical": "vertical",
        "square": "square",
    }
    
    # Size filter mapping
    SIZE_MAP = {
        "any": "",
        "small": "small",
        "medium": "medium",
        "large": "large",
        "wallpaper": "wallpaper",
    }
    
    def __init__(self, max_history: int = 50):
        """
        Initialize the Yandex Image Search client.
        
        Args:
            max_history: Maximum number of search queries to keep in history
        """
        self.max_history = max_history
        self.search_history: List[SearchQuery] = []
        self._cache_dir = os.path.join(tempfile.gettempdir(), "yandex_search_cache")
        os.makedirs(self._cache_dir, exist_ok=True)
    
    def search(
        self, 
        query: str, 
        orientation: str = "any",
        size: str = "large",
        page: int = 1,
        per_page: int = 30,
    ) -> List[SearchResult]:
        """
        Search Yandex Images for the given query.
        
        Args:
            query: Search query string
            orientation: Image orientation filter
            size: Image size filter
            page: Page number for pagination
            per_page: Number of results per page
            
        Returns:
            List of SearchResult objects
        """
        # Add to history
        search_query = SearchQuery(query=query, orientation=orientation, size=size)
        self._add_to_history(search_query)
        
        logger.info(f"Searching Yandex for: '{query}' (orientation={orientation}, size={size})")
        
        try:
            # Try using yandex-image-scraper if available
            results = self._search_with_scraper(query, orientation, size, page, per_page)
            if results:
                return results
        except ImportError:
            logger.warning("yandex-image-scraper not installed. Using fallback method.")
        except Exception as e:
            logger.warning(f"Scraper failed: {e}. Using fallback method.")
        
        # Fallback to direct HTTP request
        return self._search_with_requests(query, orientation, size, page, per_page)
    
    def _search_with_scraper(
        self,
        query: str,
        orientation: str,
        size: str,
        page: int,
        per_page: int,
    ) -> List[SearchResult]:
        """
        Search using yandex-image-scraper library.
        """
        # Note: yandex-image-scraper is a command-line tool
        # We'll need to wrap it or use an alternative approach
        # For now, this is a placeholder that returns empty
        # The actual implementation would depend on the library's API
        
        # Attempt import
        try:
            # The yandex-image-scraper package might not have a Python API
            # In that case, we fall back to requests
            raise ImportError("Using fallback method")
        except ImportError:
            raise
    
    def _search_with_requests(
        self,
        query: str,
        orientation: str,
        size: str,
        page: int,
        per_page: int,
    ) -> List[SearchResult]:
        """
        Search using direct HTTP requests to Yandex Images.
        
        Note: This is a simplified implementation. Web scraping may
        be blocked by Yandex. For production use, consider using
        the official Yandex Search API.
        """
        results = []
        
        # Build search URL
        base_url = "https://yandex.com/images/search"
        params = {
            "text": query,
            "p": page - 1,  # Yandex uses 0-based pagination
        }
        
        # Add orientation filter
        if orientation != "any" and orientation in self.ORIENTATION_MAP:
            params["iorient"] = self.ORIENTATION_MAP[orientation]
        
        # Add size filter
        if size != "any" and size in self.SIZE_MAP:
            params["isize"] = self.SIZE_MAP[size]
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
        }
        
        try:
            response = requests.get(base_url, params=params, headers=headers, timeout=30)
            response.raise_for_status()
            
            # Parse the response
            # Note: This is a simplified parser. Real implementation would use
            # BeautifulSoup or similar to parse the HTML/JSON response
            # For now, return placeholder results
            
            logger.info(f"Yandex search returned status {response.status_code}")
            
            # The actual parsing would extract image URLs from the response
            # This is a placeholder that shows the structure
            
        except requests.RequestException as e:
            logger.error(f"Yandex search request failed: {e}")
        
        return results
    
    def _add_to_history(self, query: SearchQuery):
        """Add a query to search history, removing duplicates."""
        # Remove existing entries with same query text
        self.search_history = [
            q for q in self.search_history 
            if q.query.lower() != query.query.lower()
        ]
        
        # Add new query at the beginning
        self.search_history.insert(0, query)
        
        # Trim history if needed
        if len(self.search_history) > self.max_history:
            self.search_history = self.search_history[:self.max_history]
    
    def get_history(self) -> List[SearchQuery]:
        """Get the search history."""
        return self.search_history.copy()
    
    def clear_history(self):
        """Clear the search history."""
        self.search_history.clear()
    
    def download_image(self, url: str) -> Optional[Image.Image]:
        """
        Download an image from URL.
        
        Args:
            url: Image URL
            
        Returns:
            PIL Image or None if download failed
        """
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            return Image.open(BytesIO(response.content)).convert("RGB")
        except Exception as e:
            logger.error(f"Failed to download image from {url}: {e}")
            return None
    
    def save_history(self, filepath: str):
        """Save search history to a JSON file."""
        import json
        data = [q.to_dict() for q in self.search_history]
        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)
    
    def load_history(self, filepath: str):
        """Load search history from a JSON file."""
        import json
        if os.path.exists(filepath):
            try:
                with open(filepath, "r") as f:
                    data = json.load(f)
                self.search_history = [SearchQuery.from_dict(d) for d in data]
            except Exception as e:
                logger.error(f"Failed to load search history: {e}")


