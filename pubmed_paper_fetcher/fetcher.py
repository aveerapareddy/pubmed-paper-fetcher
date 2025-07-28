"""PubMed API fetcher for research papers."""

import json
import logging
import time
from datetime import date
from typing import List, Optional, Dict, Any
import requests

from .models import Paper, Author, Affiliation
from .utils import is_academic_affiliation, extract_company_name, parse_date, clean_text, extract_emails


class PubMedFetcher:
    """Fetches research papers from PubMed API."""
    
    BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
    SEARCH_URL = f"{BASE_URL}/esearch.fcgi"
    FETCH_URL = f"{BASE_URL}/efetch.fcgi"
    SUMMARY_URL = f"{BASE_URL}/esummary.fcgi"
    
    def __init__(self, debug: bool = False) -> None:
        """
        Initialize the PubMed fetcher.
        
        Args:
            debug: Enable debug logging
        """
        self.debug = debug
        self.logger = logging.getLogger(__name__)
        
        if debug:
            logging.basicConfig(level=logging.DEBUG)
    
    def search_papers(self, query: str, max_results: int = 100) -> List[str]:
        """
        Search for papers using PubMed query.
        
        Args:
            query: PubMed search query
            max_results: Maximum number of results to return
            
        Returns:
            List of PubMed IDs
        """
        if self.debug:
            self.logger.debug(f"Searching for papers with query: {query}")
        
        params = {
            'db': 'pubmed',
            'term': query,
            'retmax': max_results,
            'retmode': 'json',
            'sort': 'relevance'
        }
        
        try:
            response = requests.get(self.SEARCH_URL, params=params, timeout=30)
            response.raise_for_status()
            
            # Rate limiting: wait between requests
            time.sleep(0.5)  # ~2 requests per second (more conservative)
            
            data = response.json()
            id_list = data.get('esearchresult', {}).get('idlist', [])
            
            if self.debug:
                self.logger.debug(f"Found {len(id_list)} papers")
            
            return id_list
            
        except requests.RequestException as e:
            self.logger.error(f"Error searching PubMed: {e}")
            raise RuntimeError(f"Failed to search PubMed: {e}")
        except json.JSONDecodeError as e:
            self.logger.error(f"Error parsing JSON response: {e}")
            raise RuntimeError(f"Failed to parse PubMed response: {e}")
    
    def fetch_paper_details(self, pubmed_id: str) -> Optional[Paper]:
        """
        Fetch detailed information for a single paper.
        
        Args:
            pubmed_id: PubMed ID of the paper
            
        Returns:
            Paper object or None if not found
        """
        if self.debug:
            self.logger.debug(f"Fetching details for PMID: {pubmed_id}")
        
        # Get summary information
        summary_params = {
            'db': 'pubmed',
            'id': pubmed_id,
            'retmode': 'json'
        }
        
        try:
            summary_response = requests.get(self.SUMMARY_URL, params=summary_params, timeout=30)
            summary_response.raise_for_status()
            
            # Rate limiting: wait between requests
            time.sleep(0.5)  # ~2 requests per second (more conservative)
            summary_data = summary_response.json()
            
            paper_data = summary_data.get('result', {}).get(pubmed_id, {})
            if not paper_data:
                return None
            
            # Extract basic information
            title = clean_text(paper_data.get('title', ''))
            pub_date = paper_data.get('pubdate', '')
            publication_date = self._parse_publication_date(pub_date)
            
            # Get detailed information including authors
            fetch_params = {
                'db': 'pubmed',
                'id': pubmed_id,
                'retmode': 'xml'
            }
            
            fetch_response = requests.get(self.FETCH_URL, params=fetch_params, timeout=30)
            fetch_response.raise_for_status()
            
            # Rate limiting: wait between requests
            time.sleep(0.5)  # ~2 requests per second (more conservative)
            
            # Parse XML to extract author information
            authors = self._parse_authors_from_xml(fetch_response.text)
            
            # Find corresponding author email
            corresponding_email = self._find_corresponding_author_email(fetch_response.text)
            
            paper = Paper(
                pubmed_id=pubmed_id,
                title=title,
                publication_date=publication_date,
                authors=authors,
                corresponding_author_email=corresponding_email
            )
            
            return paper
            
        except requests.RequestException as e:
            self.logger.error(f"Error fetching paper details for {pubmed_id}: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Unexpected error processing paper {pubmed_id}: {e}")
            return None
    
    def fetch_papers_with_pharma_authors(self, query: str, max_results: int = 100) -> List[Paper]:
        """
        Fetch papers that have authors with pharmaceutical/biotech affiliations.
        
        Args:
            query: PubMed search query
            max_results: Maximum number of results to process
            
        Returns:
            List of papers with pharmaceutical/biotech authors
        """
        if self.debug:
            self.logger.debug(f"Fetching papers with pharma authors for query: {query}")
        
        # Search for papers
        pubmed_ids = self.search_papers(query, max_results)
        
        papers_with_pharma = []
        
        for pubmed_id in pubmed_ids:
            paper = self.fetch_paper_details(pubmed_id)
            if paper and paper.has_pharma_authors:
                papers_with_pharma.append(paper)
                
                if self.debug:
                    self.logger.debug(f"Found paper with pharma authors: {paper.title}")
        
        if self.debug:
            self.logger.debug(f"Found {len(papers_with_pharma)} papers with pharma authors")
        
        return papers_with_pharma
    
    def _parse_publication_date(self, pub_date: str) -> date:
        """
        Parse publication date string.
        
        Args:
            pub_date: Publication date string from PubMed
            
        Returns:
            Parsed date object
        """
        if not pub_date:
            return date.today()
        
        # Try to parse the date
        parsed_date = parse_date(pub_date)
        if parsed_date:
            return parsed_date.date()
        
        # Fallback to today's date
        return date.today()
    
    def _parse_authors_from_xml(self, xml_content: str) -> List[Author]:
        """
        Parse author information from PubMed XML.
        
        Args:
            xml_content: XML content from PubMed
            
        Returns:
            List of Author objects
        """
        authors = []
        
        # Simple XML parsing for author information
        # This is a simplified approach - in production, you might want to use a proper XML parser
        
        # Extract author names and affiliations
        import re
        
        if self.debug:
            self.logger.debug(f"Parsing XML content length: {len(xml_content)}")
        
        # Try different author patterns
        author_patterns = [
            r'<Author>(.*?)</Author>',
            r'<AuthorList>(.*?)</AuthorList>',
            r'<Author ValidYN="Y">(.*?)</Author>'
        ]
        
        author_sections = []
        for pattern in author_patterns:
            author_sections = re.findall(pattern, xml_content, re.DOTALL)
            if author_sections:
                if self.debug:
                    self.logger.debug(f"Found {len(author_sections)} authors with pattern: {pattern}")
                break
        
        if not author_sections:
            # Try to find authors in a different format
            author_sections = re.findall(r'<Author ValidYN="Y">(.*?)</Author>', xml_content, re.DOTALL)
            if not author_sections:
                # Look for any author-like content
                author_sections = re.findall(r'<Author[^>]*>(.*?)</Author>', xml_content, re.DOTALL)
        
        if self.debug:
            self.logger.debug(f"Total author sections found: {len(author_sections)}")
        
        for section in author_sections:
            # Extract author name - try multiple patterns
            author_name = ""
            
            # Try LastName + ForeName pattern
            name_match = re.search(r'<LastName>(.*?)</LastName>', section)
            last_name = name_match.group(1) if name_match else ""
            
            forename_match = re.search(r'<ForeName>(.*?)</ForeName>', section)
            fore_name = forename_match.group(1) if forename_match else ""
            
            if last_name or fore_name:
                author_name = f"{fore_name} {last_name}".strip()
            
            # If no name found, try alternative patterns
            if not author_name:
                # Try CollectiveName
                collective_match = re.search(r'<CollectiveName>(.*?)</CollectiveName>', section)
                if collective_match:
                    author_name = collective_match.group(1).strip()
            
            if not author_name:
                # Try to extract any text that looks like a name
                name_text = re.sub(r'<[^>]+>', '', section).strip()
                if name_text and len(name_text) < 100:  # Reasonable name length
                    author_name = name_text
            
            # Extract affiliations - try multiple patterns
            affiliations = []
            affiliation_patterns = [
                r'<AffiliationInfo>(.*?)</AffiliationInfo>',
                r'<Affiliation>(.*?)</Affiliation>',
                r'<AffiliationInfo[^>]*>(.*?)</AffiliationInfo>'
            ]
            
            for aff_pattern in affiliation_patterns:
                affiliation_sections = re.findall(aff_pattern, section, re.DOTALL)
                for aff_section in affiliation_sections:
                    # Clean the affiliation text
                    affiliation_text = re.sub(r'<[^>]+>', '', aff_section).strip()
                    affiliation_text = clean_text(affiliation_text)
                    
                    if affiliation_text and len(affiliation_text) > 3:  # Reasonable length
                        is_academic = is_academic_affiliation(affiliation_text)
                        company_name = extract_company_name(affiliation_text) if not is_academic else None
                        
                        if self.debug:
                            self.logger.debug(f"Affiliation: '{affiliation_text}' -> Academic: {is_academic}, Company: {company_name}")
                        
                        affiliation = Affiliation(
                            name=affiliation_text,
                            is_academic=is_academic,
                            company_name=company_name
                        )
                        affiliations.append(affiliation)
            
            # Extract email if available
            email = None
            email_match = re.search(r'<Email>(.*?)</Email>', section)
            if email_match:
                email = email_match.group(1).strip()
            
            if author_name:
                author = Author(
                    name=author_name,
                    email=email,
                    affiliations=affiliations
                )
                authors.append(author)
                
                if self.debug:
                    self.logger.debug(f"Added author: {author_name} with {len(affiliations)} affiliations")
        
        return authors
    
    def _find_corresponding_author_email(self, xml_content: str) -> Optional[str]:
        """
        Find corresponding author email from XML content.
        
        Args:
            xml_content: XML content from PubMed
            
        Returns:
            Corresponding author email or None
        """
        # Look for corresponding author email in the XML
        import re
        
        # Check for explicit corresponding author email
        email_match = re.search(r'<CorrespondingAuthorEmail>(.*?)</CorrespondingAuthorEmail>', xml_content)
        if email_match:
            return email_match.group(1).strip()
        
        # Extract all emails and return the first one
        emails = extract_emails(xml_content)
        return emails[0] if emails else None 