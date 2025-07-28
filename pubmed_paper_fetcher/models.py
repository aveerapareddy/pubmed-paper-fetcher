"""Data models for PubMed paper fetcher."""

from dataclasses import dataclass
from datetime import date
from typing import List, Optional


@dataclass
class Affiliation:
    """Represents an author's affiliation."""
    
    name: str
    is_academic: bool
    company_name: Optional[str] = None


@dataclass
class Author:
    """Represents a paper author."""
    
    name: str
    email: Optional[str] = None
    affiliations: List[Affiliation] = None
    
    def __post_init__(self) -> None:
        """Initialize default values."""
        if self.affiliations is None:
            self.affiliations = []
    
    @property
    def has_pharma_affiliation(self) -> bool:
        """Check if author has pharmaceutical/biotech affiliation."""
        return any(not aff.is_academic for aff in self.affiliations)
    
    @property
    def pharma_companies(self) -> List[str]:
        """Get list of pharmaceutical/biotech companies."""
        return [aff.company_name for aff in self.affiliations 
                if not aff.is_academic and aff.company_name]


@dataclass
class Paper:
    """Represents a research paper."""
    
    pubmed_id: str
    title: str
    publication_date: date
    authors: List[Author] = None
    corresponding_author_email: Optional[str] = None
    
    def __post_init__(self) -> None:
        """Initialize default values."""
        if self.authors is None:
            self.authors = []
    
    @property
    def has_pharma_authors(self) -> bool:
        """Check if paper has authors with pharmaceutical/biotech affiliations."""
        return any(author.has_pharma_affiliation for author in self.authors)
    
    @property
    def non_academic_authors(self) -> List[str]:
        """Get names of authors with non-academic affiliations."""
        return [author.name for author in self.authors 
                if author.has_pharma_affiliation]
    
    @property
    def company_affiliations(self) -> List[str]:
        """Get all pharmaceutical/biotech company names."""
        companies = []
        for author in self.authors:
            companies.extend(author.pharma_companies)
        return list(set(companies))  # Remove duplicates 