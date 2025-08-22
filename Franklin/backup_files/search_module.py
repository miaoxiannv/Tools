import requests
import re
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
@dataclass
class AnalysisResult:
    contribution: str
    novelty: int
    biological_impact: int
    technical_innovation: int
@dataclass
class Paper:
    doi: str
    title: str
    authors: List[str] = field(default_factory=list)
    publication_year: Optional[int] = None
    abstract: Optional[str] = None
    url: Optional[str] = None
    status: str = 'NEW'
    analysis_result: Optional[AnalysisResult] = None
    translated_abstract: Optional[str] = None
    error_message: Optional[str] = None
def _clean_html(raw_html: Optional[str]) -> Optional[str]:
    if not raw_html:
        return None
    cleantext = re.sub('<.*?>', '', raw_html, flags=re.DOTALL)
    return cleantext.strip()

def _parse_crossref_item(item: Dict[str, Any]) -> Paper:
    """
    Parses a raw item from the Crossref API into our clean, internal Paper object.
    """
    doi = item.get('DOI', 'N/A')
    title = item.get('title', ['No Title'])[0]
    
    authors = []
    for author_data in item.get('author', []):
        given = author_data.get('given', '')
        family = author_data.get('family', '')
        authors.append(f"{given} {family}".strip())

    year = None
    if 'issued' in item and 'date-parts' in item['issued']:
        try:
            year = item['issued']['date-parts'][0][0]
        except (IndexError, TypeError):
            pass

    abstract = _clean_html(item.get('abstract'))
    url = item.get('URL')

    return Paper(
        doi=doi,
        title=title,
        authors=authors,
        publication_year=year,
        abstract=abstract,
        url=url
    )
class SearchError(Exception):
    """Custom exception for search-related errors."""
    pass

def search_papers(query: str, limit: int = 5, filters: Optional[Dict[str, Any]] = None) -> List[Paper]:
    """
    Searches Crossref for papers and returns a list of Paper objects.
    
    Args:
        query: The search term.
        limit: Max number of results to return.
        filters: A dictionary of additional filters, e.g., {'type': 'journal-article'}.

    Returns:
        A list of Paper objects. Returns an empty list if no results are found.
        
    Raises:
        SearchError: If the API request fails.
    """
    BASE_URL = "https://api.crossref.org/works"
    
    params = {
        'query': query,
        'rows': limit,
    }

    filter_parts = ['has-abstract:true'] # Always require an abstract
    if filters:
        for key, value in filters.items():
            filter_parts.append(f"{key}:{str(value).lower()}")
    params['filter'] = ",".join(filter_parts)

    # A polite User-Agent is good practice.
    headers = {
        'User-Agent': 'ProjectPauling/1.0 (mailto:your-email@example.com)'
    }

    try:
        response = requests.get(BASE_URL, params=params, headers=headers, timeout=20)
        response.raise_for_status()  # This will raise an HTTPError for bad responses (4xx or 5xx)

        data = response.json()
        items = data.get('message', {}).get('items', [])
        
        # This is the key part: convert raw items to our clean Paper objects
        paper_list = [_parse_crossref_item(item) for item in items]
        return paper_list

    except requests.exceptions.RequestException as e:
        # For network errors, wrap it in our custom exception
        raise SearchError(f"Network error during search: {e}") from e
if __name__ == "__main__":
    print("--- [Test Case 1] Successful search ---")
    try:
        papers = search_papers(
            query="computational biology deep learning", 
            limit=2, 
            filters={'from-pub-date': '2023'}
        )
        if papers:
            print(f"Found {len(papers)} papers.")
            for paper in papers:
                print(f"  - DOI: {paper.doi}, Title: {paper.title}")
                print(f"    Abstract available: {bool(paper.abstract)}")
        else:
            print("No papers found.")
    except SearchError as e:
        print(f"Error: {e}")

    print("\n--- [Test Case 2] Search with no results ---")
    try:
        papers = search_papers(query="asdfqwerzxcv", limit=2)
        if not papers:
            print("Correctly returned an empty list for a query with no results.")
    except SearchError as e:
        print(f"Error: {e}")