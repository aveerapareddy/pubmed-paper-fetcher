"""Tests for data models."""

import pytest
from datetime import date

from pubmed_paper_fetcher.models import Paper, Author, Affiliation


class TestAffiliation:
    """Test Affiliation model."""
    
    def test_affiliation_creation(self):
        """Test creating an affiliation."""
        affiliation = Affiliation(
            name="Pfizer Inc.",
            is_academic=False,
            company_name="Pfizer Inc."
        )
        
        assert affiliation.name == "Pfizer Inc."
        assert not affiliation.is_academic
        assert affiliation.company_name == "Pfizer Inc."
    
    def test_academic_affiliation(self):
        """Test academic affiliation."""
        affiliation = Affiliation(
            name="Harvard University",
            is_academic=True,
            company_name=None
        )
        
        assert affiliation.name == "Harvard University"
        assert affiliation.is_academic
        assert affiliation.company_name is None


class TestAuthor:
    """Test Author model."""
    
    def test_author_creation(self):
        """Test creating an author."""
        author = Author(
            name="John Smith",
            email="john.smith@example.com",
            affiliations=[]
        )
        
        assert author.name == "John Smith"
        assert author.email == "john.smith@example.com"
        assert author.affiliations == []
    
    def test_author_with_affiliations(self):
        """Test author with affiliations."""
        affiliations = [
            Affiliation("Pfizer Inc.", False, "Pfizer Inc."),
            Affiliation("Harvard University", True, None)
        ]
        
        author = Author(
            name="Jane Doe",
            email="jane.doe@example.com",
            affiliations=affiliations
        )
        
        assert len(author.affiliations) == 2
        assert author.has_pharma_affiliation
        assert "Pfizer Inc." in author.pharma_companies
    
    def test_author_pharma_detection(self):
        """Test pharmaceutical affiliation detection."""
        # Author with pharma affiliation
        pharma_author = Author(
            name="Pharma Author",
            affiliations=[Affiliation("Pfizer Inc.", False, "Pfizer Inc.")]
        )
        assert pharma_author.has_pharma_affiliation
        assert pharma_author.pharma_companies == ["Pfizer Inc."]
        
        # Author with only academic affiliation
        academic_author = Author(
            name="Academic Author",
            affiliations=[Affiliation("Harvard University", True, None)]
        )
        assert not academic_author.has_pharma_affiliation
        assert academic_author.pharma_companies == []
    
    def test_author_default_affiliations(self):
        """Test author with default affiliations."""
        author = Author(name="Test Author")
        assert author.affiliations == []


class TestPaper:
    """Test Paper model."""
    
    def test_paper_creation(self):
        """Test creating a paper."""
        authors = [
            Author("John Smith", affiliations=[Affiliation("Pfizer Inc.", False, "Pfizer Inc.")]),
            Author("Jane Doe", affiliations=[Affiliation("Harvard University", True, None)])
        ]
        
        paper = Paper(
            pubmed_id="12345",
            title="Test Paper",
            publication_date=date(2023, 1, 15),
            authors=authors,
            corresponding_author_email="corresponding@example.com"
        )
        
        assert paper.pubmed_id == "12345"
        assert paper.title == "Test Paper"
        assert paper.publication_date == date(2023, 1, 15)
        assert len(paper.authors) == 2
        assert paper.corresponding_author_email == "corresponding@example.com"
    
    def test_paper_pharma_detection(self):
        """Test pharmaceutical author detection in papers."""
        # Paper with pharma authors
        pharma_authors = [
            Author("Pharma Author", affiliations=[Affiliation("Pfizer Inc.", False, "Pfizer Inc.")])
        ]
        
        pharma_paper = Paper(
            pubmed_id="12345",
            title="Pharma Paper",
            publication_date=date(2023, 1, 15),
            authors=pharma_authors
        )
        
        assert pharma_paper.has_pharma_authors
        assert "Pharma Author" in pharma_paper.non_academic_authors
        assert "Pfizer Inc." in pharma_paper.company_affiliations
        
        # Paper with only academic authors
        academic_authors = [
            Author("Academic Author", affiliations=[Affiliation("Harvard University", True, None)])
        ]
        
        academic_paper = Paper(
            pubmed_id="67890",
            title="Academic Paper",
            publication_date=date(2023, 1, 15),
            authors=academic_authors
        )
        
        assert not academic_paper.has_pharma_authors
        assert academic_paper.non_academic_authors == []
        assert academic_paper.company_affiliations == []
    
    def test_paper_default_authors(self):
        """Test paper with default authors."""
        paper = Paper(
            pubmed_id="12345",
            title="Test Paper",
            publication_date=date(2023, 1, 15)
        )
        
        assert paper.authors == []
        assert not paper.has_pharma_authors
        assert paper.non_academic_authors == []
        assert paper.company_affiliations == []
    
    def test_paper_duplicate_companies(self):
        """Test handling of duplicate company affiliations."""
        authors = [
            Author("Author 1", affiliations=[Affiliation("Pfizer Inc.", False, "Pfizer Inc.")]),
            Author("Author 2", affiliations=[Affiliation("Pfizer Inc.", False, "Pfizer Inc.")]),
            Author("Author 3", affiliations=[Affiliation("Johnson & Johnson", False, "Johnson & Johnson")])
        ]
        
        paper = Paper(
            pubmed_id="12345",
            title="Test Paper",
            publication_date=date(2023, 1, 15),
            authors=authors
        )
        
        # Should have unique companies
        companies = paper.company_affiliations
        assert len(companies) == 2
        assert "Pfizer Inc." in companies
        assert "Johnson & Johnson" in companies 