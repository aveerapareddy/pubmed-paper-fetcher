"""Tests for utility functions."""

import pytest
from datetime import datetime

from pubmed_paper_fetcher.utils import (
    is_academic_affiliation,
    extract_company_name,
    parse_date,
    clean_text,
    extract_emails
)


class TestAffiliationDetection:
    """Test affiliation detection functions."""
    
    def test_academic_affiliations(self):
        """Test detection of academic affiliations."""
        academic_affiliations = [
            "Harvard University",
            "Department of Medicine, Stanford University",
            "John Smith, PhD, University of California",
            "Research Laboratory, MIT",
            "john.doe@harvard.edu",
            "Medical Center, Johns Hopkins University"
        ]
        
        for affiliation in academic_affiliations:
            assert is_academic_affiliation(affiliation), f"Should be academic: {affiliation}"
    
    def test_non_academic_affiliations(self):
        """Test detection of non-academic affiliations."""
        non_academic_affiliations = [
            "Pfizer Inc.",
            "Johnson & Johnson",
            "Novartis Pharmaceuticals",
            "Biotech Company Ltd.",
            "john.doe@company.com"
        ]
        
        for affiliation in non_academic_affiliations:
            assert not is_academic_affiliation(affiliation), f"Should not be academic: {affiliation}"
    
    def test_company_name_extraction(self):
        """Test company name extraction."""
        test_cases = [
            ("Pfizer Inc.", "Pfizer Inc."),
            ("Dr. John Smith, Pfizer Inc.", "Pfizer Inc."),
            ("Johnson & Johnson, New Jersey", "New Jersey"),
            ("", None),
            ("Harvard University", None),  # Academic
        ]
        
        for affiliation, expected in test_cases:
            result = extract_company_name(affiliation)
            assert result == expected, f"Expected {expected}, got {result} for '{affiliation}'"


class TestDateParsing:
    """Test date parsing functions."""
    
    def test_valid_dates(self):
        """Test parsing of valid date formats."""
        test_cases = [
            ("2023-01-15", datetime(2023, 1, 15)),
            ("2023 01 15", datetime(2023, 1, 15)),
            ("2023/01/15", datetime(2023, 1, 15)),
            ("2023-01", datetime(2023, 1, 1)),
            ("2023", datetime(2023, 1, 1)),
        ]
        
        for date_str, expected in test_cases:
            result = parse_date(date_str)
            assert result == expected, f"Expected {expected}, got {result} for '{date_str}'"
    
    def test_invalid_dates(self):
        """Test parsing of invalid date formats."""
        invalid_dates = [
            "",
            "invalid-date",
            "2023-13-45",  # Invalid month/day
        ]
        
        for date_str in invalid_dates:
            result = parse_date(date_str)
            assert result is None, f"Expected None, got {result} for '{date_str}'"


class TestTextProcessing:
    """Test text processing functions."""
    
    def test_clean_text(self):
        """Test text cleaning function."""
        test_cases = [
            ("  Hello   World  ", "Hello World"),
            ("<p>Hello World</p>", "Hello World"),
            ("", ""),
            ("\n\nHello\n\nWorld\n\n", "Hello World"),
        ]
        
        for input_text, expected in test_cases:
            result = clean_text(input_text)
            assert result == expected, f"Expected '{expected}', got '{result}' for '{input_text}'"
    
    def test_extract_emails(self):
        """Test email extraction function."""
        test_cases = [
            ("Contact: john.doe@example.com", ["john.doe@example.com"]),
            ("Email: jane@company.com and bob@university.edu", ["jane@company.com", "bob@university.edu"]),
            ("No email here", []),
            ("", []),
        ]
        
        for input_text, expected in test_cases:
            result = extract_emails(input_text)
            assert result == expected, f"Expected {expected}, got {result} for '{input_text}'" 