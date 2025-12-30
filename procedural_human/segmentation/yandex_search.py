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
        Search for images using the given query.
        
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
        
        logger.info(f"Searching for: '{query}' (orientation={orientation}, size={size})")
        
        # Track which source was used for notifications
        self._last_source_used = "Unsplash"
        self._fallback_messages = []
        
        # Try Unsplash first (most reliable, no captcha issues)
        results = self._search_unsplash(query, per_page)
        
        # If Unsplash failed, try DuckDuckGo as fallback
        if not results:
            logger.info("Unsplash returned no results, trying DuckDuckGo fallback...")
            self._fallback_messages.append("Unsplash failed, trying DuckDuckGo...")
            results = self._search_duckduckgo(query, per_page)
            self._last_source_used = "DuckDuckGo"
        
        # If still no results, try Yandex (likely to be blocked by captcha)
        if not results:
            logger.info("DuckDuckGo returned no results, trying Yandex fallback...")
            self._fallback_messages.append("DuckDuckGo failed, trying Yandex...")
            results = self._search_with_requests(query, orientation, size, page, per_page)
            self._last_source_used = "Yandex"
        
        return results
    
    def get_last_source(self) -> str:
        """Get the last search source used."""
        return getattr(self, '_last_source_used', 'Unknown')
    
    def get_fallback_messages(self) -> list:
        """Get any fallback messages from the last search."""
        return getattr(self, '_fallback_messages', [])
    
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
        
        Parses the HTML response to extract image URLs using multiple methods.
        """
        import re
        import json
        
        results = []
        
        # Build search URL - use the JSON API endpoint
        base_url = "https://yandex.com/images/search"
        params = {
            "text": query,
            "p": page - 1,  # Yandex uses 0-based pagination
            "format": "json",  # Request JSON format
            "request": '{"blocks":[{"block":"serp-controller"}]}',
        }
        
        # Add orientation filter
        if orientation != "any" and orientation in self.ORIENTATION_MAP:
            params["iorient"] = self.ORIENTATION_MAP[orientation]
        
        # Add size filter
        if size != "any" and size in self.SIZE_MAP:
            params["isize"] = self.SIZE_MAP[size]
        
        # More complete browser headers to avoid bot detection
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Cache-Control": "max-age=0",
        }
        
        try:
            # First try without format=json to get regular HTML
            params_html = {k: v for k, v in params.items() if k not in ["format", "request"]}
            response = requests.get(base_url, params=params_html, headers=headers, timeout=30)
            response.raise_for_status()
            
            logger.info(f"Yandex search returned status {response.status_code}")
            html_content = response.text
            
            # Debug: log a snippet of the response
            logger.info(f"Response length: {len(html_content)} chars")
            
            # Save response to file for debugging
            debug_file = os.path.join(self._cache_dir, "yandex_debug_response.html")
            try:
                with open(debug_file, "w", encoding="utf-8") as f:
                    f.write(f"<!-- Query: {query} -->\n")
                    f.write(f"<!-- URL: {response.url} -->\n")
                    f.write(f"<!-- Status: {response.status_code} -->\n")
                    f.write(html_content)
                logger.info(f"Saved Yandex response to: {debug_file}")
            except Exception as e:
                logger.warning(f"Could not save debug file: {e}")
            
            # Method 1: Look for serp-item data in data-bem attributes (escaped JSON)
            # Pattern matches both single and double quoted data-bem
            bem_pattern = r'data-bem=[\'"]({.*?serp-item.*?})[\'"]'
            bem_matches = re.findall(bem_pattern, html_content)
            
            logger.info(f"Found {len(bem_matches)} data-bem matches")
            
            for match in bem_matches:
                try:
                    # Unescape HTML entities
                    unescaped = match.replace('&quot;', '"').replace('&amp;', '&').replace('&#39;', "'")
                    data = json.loads(unescaped)
                    
                    if "serp-item" in data:
                        item = data["serp-item"]
                        img_url = item.get("img_href") or item.get("url") or ""
                        thumb = item.get("thumb", {})
                        thumb_url = thumb.get("url") if isinstance(thumb, dict) else (thumb or img_url)
                        
                        if img_url:
                            result = SearchResult(
                                url=img_url,
                                thumbnail_url=thumb_url or img_url,
                                title=item.get("alt", item.get("snippet", {}).get("title", "") if isinstance(item.get("snippet"), dict) else ""),
                            )
                            results.append(result)
                except (json.JSONDecodeError, KeyError, TypeError) as e:
                    continue
            
            # Method 2: Look for img_href pattern in the raw HTML
            if not results:
                # Pattern for Yandex's image URLs in various formats
                patterns = [
                    r'"img_href"\s*:\s*"([^"]+)"',
                    r'"origin"\s*:\s*{\s*"url"\s*:\s*"([^"]+)"',
                    r'"origUrl"\s*:\s*"([^"]+)"',
                    r'"fullUrl"\s*:\s*"([^"]+)"',
                ]
                
                seen_urls = set()
                for pattern in patterns:
                    matches = re.findall(pattern, html_content)
                    logger.info(f"Pattern {pattern[:30]}... found {len(matches)} matches")
                    
                    for url in matches:
                        # Unescape URL
                        url = url.replace("\\/", "/").replace("\\u002F", "/")
                        
                        if url in seen_urls:
                            continue
                        if not url.startswith("http"):
                            continue
                        if "yandex" in url.lower() or "yastatic" in url.lower():
                            continue
                            
                        seen_urls.add(url)
                        results.append(SearchResult(
                            url=url,
                            thumbnail_url=url,
                            title="",
                        ))
                        
                        if len(results) >= per_page:
                            break
                    
                    if len(results) >= per_page:
                        break
            
            # Method 3: Look for preview/thumbnail URLs (avatars.mds.yandex.net)
            if not results:
                # Yandex uses avatars.mds.yandex.net for thumbnails
                thumb_pattern = r'(https?://avatars\.mds\.yandex\.net/[^"\'>\s]+)'
                thumb_matches = re.findall(thumb_pattern, html_content)
                
                logger.info(f"Found {len(thumb_matches)} thumbnail URLs")
                
                seen_urls = set()
                for url in thumb_matches:
                    if url in seen_urls:
                        continue
                    # Skip very small sizes
                    if "/n=" in url or "orig" in url or any(s in url for s in ["/200x", "/300x", "/400x", "/500x"]):
                        seen_urls.add(url)
                        results.append(SearchResult(
                            url=url,
                            thumbnail_url=url,
                            title="",
                        ))
                        if len(results) >= per_page:
                            break
            
            logger.info(f"Found {len(results)} images from Yandex search")
            
        except requests.RequestException as e:
            logger.error(f"Yandex search request failed: {e}")
        
        return results
    
    def _search_duckduckgo(self, query: str, per_page: int = 30) -> List[SearchResult]:
        """
        Search using DuckDuckGo Images as a fallback.
        DuckDuckGo is more permissive with scraping.
        """
        import re
        import json
        
        results = []
        
        try:
            # DuckDuckGo uses a token-based API
            # First, get a token from the main search page
            token_url = "https://duckduckgo.com/"
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            }
            
            session = requests.Session()
            resp = session.get(token_url, headers=headers, timeout=10)
            
            # Extract vqd token
            vqd_match = re.search(r'vqd=([^&]+)', resp.text)
            if not vqd_match:
                vqd_match = re.search(r"vqd='([^']+)'", resp.text)
            if not vqd_match:
                vqd_match = re.search(r'vqd="([^"]+)"', resp.text)
            
            if not vqd_match:
                logger.warning("Could not extract DuckDuckGo token")
                return results
            
            vqd = vqd_match.group(1)
            
            # Now search images
            search_url = "https://duckduckgo.com/i.js"
            params = {
                "l": "us-en",
                "o": "json",
                "q": query,
                "vqd": vqd,
                "f": ",,,,,",
                "p": "1",
            }
            
            resp = session.get(search_url, params=params, headers=headers, timeout=30)
            data = resp.json()
            
            for item in data.get("results", [])[:per_page]:
                image_url = item.get("image", "")
                thumb_url = item.get("thumbnail", image_url)
                title = item.get("title", "")
                
                if image_url:
                    results.append(SearchResult(
                        url=image_url,
                        thumbnail_url=thumb_url,
                        title=title,
                        width=item.get("width", 0),
                        height=item.get("height", 0),
                    ))
            
            logger.info(f"Found {len(results)} images from DuckDuckGo")
            
        except Exception as e:
            logger.error(f"DuckDuckGo search failed: {e}")
        
        return results
    
    def _search_unsplash(self, query: str, per_page: int = 30) -> List[SearchResult]:
        """
        Search Unsplash for high-quality images.
        Uses the public API endpoint (no auth required for basic search).
        """
        results = []
        
        try:
            # Unsplash public search endpoint
            search_url = f"https://unsplash.com/napi/search/photos"
            params = {
                "query": query,
                "per_page": min(per_page, 30),
                "page": 1,
            }
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Accept": "application/json",
            }
            
            resp = requests.get(search_url, params=params, headers=headers, timeout=30)
            data = resp.json()
            
            for item in data.get("results", []):
                urls = item.get("urls", {})
                image_url = urls.get("regular") or urls.get("full") or urls.get("raw", "")
                thumb_url = urls.get("thumb") or urls.get("small", image_url)
                
                if image_url:
                    results.append(SearchResult(
                        url=image_url,
                        thumbnail_url=thumb_url,
                        title=item.get("alt_description", item.get("description", "")),
                        width=item.get("width", 0),
                        height=item.get("height", 0),
                    ))
            
            logger.info(f"Found {len(results)} images from Unsplash")
            
        except Exception as e:
            logger.error(f"Unsplash search failed: {e}")
        
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


