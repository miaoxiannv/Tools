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
    pass

def search_papers(query: str, limit: int = 5, filters: Optional[Dict[str, Any]] = None) -> List[Paper]:
    BASE_URL = "https://api.crossref.org/works"
    
    params = {
        'query': query,
        'rows': limit,
    }

    filter_parts = ['has-abstract:true']
    if filters:
        for key, value in filters.items():
            filter_parts.append(f"{key}:{str(value).lower()}")
    params['filter'] = ",".join(filter_parts)

    headers = {
        'User-Agent': 'ProjectPauling/1.0 (mailto:your-email@example.com)'
    }

    try:
        response = requests.get(BASE_URL, params=params, headers=headers, timeout=20)
        response.raise_for_status()

        data = response.json()
        items = data.get('message', {}).get('items', [])
        
        paper_list = [_parse_crossref_item(item) for item in items]
        return paper_list

    except requests.exceptions.RequestException as e:
        raise SearchError(f"Network error during search: {e}") from e
