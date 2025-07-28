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
        'researcher', 'scientist', 'phd', 'postdoc', 'postdoctoral',
        'school of', 'department of', 'center for', 'centre for'
    ]
    
    # Company/industry keywords that indicate non-academic
    company_keywords = [
        'consultants', 'consulting', 'corporation', 'corp', 'inc',
        'ltd', 'limited', 'company', 'co', 'pharmaceuticals',
        'pharma', 'biotech', 'biotechnology', 'therapeutics',
        'vaccines', 'drugs', 'medicines', 'products'
    ]
    
    # Check for company keywords first (these override academic keywords)
    for keyword in company_keywords:
        if keyword in affiliation_lower:
            return False  # This is a company, not academic
    
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
    
    # Remove author names (common pattern: "Name, Company")
    if ',' in affiliation_clean:
        parts = affiliation_clean.split(',')
        # If we have multiple parts, take the first one as it's likely the company
        if len(parts) > 1:
            affiliation_clean = parts[0].strip()
    
    # Look for specific company patterns
    company_patterns = [
        r'([A-Z][a-z]+ Consultants?)',
        r'([A-Z][a-z]+ Pharmaceuticals?)',
        r'([A-Z][a-z]+ Inc\.?)',
        r'([A-Z][a-z]+ Corp\.?)',
        r'([A-Z][a-z]+ Limited?)',
        r'([A-Z][a-z]+ Company)',
        r'([A-Z][a-z]+ Therapeutics?)',
        r'([A-Z][a-z]+ Biotech)',
        r'([A-Z][a-z]+ Vaccines?)'
    ]
    
    for pattern in company_patterns:
        match = re.search(pattern, affiliation_clean)
        if match:
            return match.group(1)
    
    # If no specific pattern found, try to extract the first part before a comma
    if ',' in affiliation_clean:
        first_part = affiliation_clean.split(',')[0].strip()
        # Check if it looks like a company name (not just a location)
        if len(first_part) > 3 and not first_part.lower() in ['usa', 'australia', 'uk', 'canada']:
            return first_part
    
    # If we still have a reasonable length affiliation, return it
    if len(affiliation_clean) > 3 and len(affiliation_clean) < 50:
        return affiliation_clean
    
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