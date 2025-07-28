"""Utility functions for PubMed paper fetcher."""

import re
from typing import List, Optional
from datetime import datetime


def is_academic_affiliation(affiliation: str) -> bool:
    """
    Determine if an affiliation is academic based on keywords.
    
    Args:
        affiliation: The affiliation string to analyze
        
    Returns:
        True if the affiliation appears to be academic, False otherwise
    """
    if not affiliation:
        return False
    
    affiliation_lower = affiliation.lower()
    
    # Academic keywords
    academic_keywords = [
        'university', 'college', 'institute', 'school', 'academy',
        'medical center', 'hospital', 'clinic', 'research center',
        'laboratory', 'lab', 'department', 'faculty', 'professor',
        'associate professor', 'assistant professor', 'lecturer',
        'researcher', 'scientist', 'phd', 'postdoc', 'postdoctoral'
    ]
    
    # Check for academic keywords
    for keyword in academic_keywords:
        if keyword in affiliation_lower:
            return True
    
    # Check for email patterns (academic emails often contain .edu)
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(email_pattern, affiliation)
    for email in emails:
        if '.edu' in email.lower():
            return True
    
    return False


def extract_company_name(affiliation: str) -> Optional[str]:
    """
    Extract company name from affiliation string.
    
    Args:
        affiliation: The affiliation string to analyze
        
    Returns:
        Extracted company name or None if not found
    """
    if not affiliation or is_academic_affiliation(affiliation):
        return None
    
    # Remove common non-company words
    affiliation_clean = affiliation.strip()
    
    # Remove email addresses
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    affiliation_clean = re.sub(email_pattern, '', affiliation_clean)
    
    # Remove common prefixes/suffixes
    prefixes = ['Dr.', 'Prof.', 'Professor', 'Associate Professor', 'Assistant Professor']
    for prefix in prefixes:
        if affiliation_clean.startswith(prefix):
            affiliation_clean = affiliation_clean[len(prefix):].strip()
    
    # Clean up extra whitespace and punctuation
    affiliation_clean = re.sub(r'\s+', ' ', affiliation_clean).strip()
    affiliation_clean = re.sub(r'^[,\s]+|[,\s]+$', '', affiliation_clean)
    
    return affiliation_clean if affiliation_clean else None


def parse_date(date_str: str) -> Optional[datetime]:
    """
    Parse date string into datetime object.
    
    Args:
        date_str: Date string in various formats
        
    Returns:
        Parsed datetime object or None if parsing fails
    """
    if not date_str:
        return None
    
    # Common date formats
    date_formats = [
        '%Y-%m-%d',
        '%Y %m %d',
        '%Y/%m/%d',
        '%Y-%m',
        '%Y %m',
        '%Y/%m',
        '%Y'
    ]
    
    for fmt in date_formats:
        try:
            return datetime.strptime(date_str.strip(), fmt)
        except ValueError:
            continue
    
    return None


def clean_text(text: str) -> str:
    """
    Clean and normalize text.
    
    Args:
        text: Text to clean
        
    Returns:
        Cleaned text
    """
    if not text:
        return ""
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text.strip())
    
    # Remove HTML tags if present
    text = re.sub(r'<[^>]+>', '', text)
    
    return text


def extract_emails(text: str) -> List[str]:
    """
    Extract email addresses from text.
    
    Args:
        text: Text to search for emails
        
    Returns:
        List of found email addresses
    """
    if not text:
        return []
    
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.findall(email_pattern, text) 