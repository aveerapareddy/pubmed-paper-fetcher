"""CSV exporter for PubMed papers."""

import csv
from typing import List, TextIO
import pandas as pd

from .models import Paper


class CSVExporter:
    """Exports papers to CSV format."""
    
    def __init__(self) -> None:
        """Initialize the CSV exporter."""
        pass
    
    def export_to_csv(self, papers: List[Paper], output_file: str) -> None:
        """
        Export papers to CSV file.
        
        Args:
            papers: List of papers to export
            output_file: Path to output CSV file
        """
        data = []
        
        for paper in papers:
            row = {
                'PubmedID': paper.pubmed_id,
                'Title': paper.title,
                'Publication Date': paper.publication_date.strftime('%Y-%m-%d'),
                'Non-academic Author(s)': '; '.join(paper.non_academic_authors),
                'Company Affiliation(s)': '; '.join(paper.company_affiliations),
                'Corresponding Author Email': paper.corresponding_author_email or ''
            }
            data.append(row)
        
        # Use pandas for better CSV handling
        df = pd.DataFrame(data)
        df.to_csv(output_file, index=False, quoting=csv.QUOTE_ALL)
    
    def export_to_console(self, papers: List[Paper]) -> None:
        """
        Export papers to console output.
        
        Args:
            papers: List of papers to export
        """
        if not papers:
            print("No papers found with pharmaceutical/biotech affiliations.")
            return
        
        print(f"Found {len(papers)} papers with pharmaceutical/biotech affiliations:\n")
        
        for i, paper in enumerate(papers, 1):
            print(f"Paper {i}:")
            print(f"  PubmedID: {paper.pubmed_id}")
            print(f"  Title: {paper.title}")
            print(f"  Publication Date: {paper.publication_date.strftime('%Y-%m-%d')}")
            print(f"  Non-academic Author(s): {', '.join(paper.non_academic_authors)}")
            print(f"  Company Affiliation(s): {', '.join(paper.company_affiliations)}")
            print(f"  Corresponding Author Email: {paper.corresponding_author_email or 'N/A'}")
            print()
    
    def get_csv_string(self, papers: List[Paper]) -> str:
        """
        Get CSV content as string.
        
        Args:
            papers: List of papers to export
            
        Returns:
            CSV content as string
        """
        import io
        
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write header
        writer.writerow([
            'PubmedID',
            'Title', 
            'Publication Date',
            'Non-academic Author(s)',
            'Company Affiliation(s)',
            'Corresponding Author Email'
        ])
        
        # Write data
        for paper in papers:
            writer.writerow([
                paper.pubmed_id,
                paper.title,
                paper.publication_date.strftime('%Y-%m-%d'),
                '; '.join(paper.non_academic_authors),
                '; '.join(paper.company_affiliations),
                paper.corresponding_author_email or ''
            ])
        
        return output.getvalue() 