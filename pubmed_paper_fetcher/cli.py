"""Command-line interface for PubMed paper fetcher."""

import sys
from typing import Optional
import click

from .fetcher import PubMedFetcher
from .exporter import CSVExporter


@click.command()
@click.argument('query', required=True)
@click.option('-f', '--file', 'output_file', help='Output file path for CSV results')
@click.option('-d', '--debug', is_flag=True, help='Enable debug mode')
@click.option('-m', '--max-results', default=100, help='Maximum number of results to process')
def main(query: str, output_file: Optional[str], debug: bool, max_results: int) -> None:
    """
    Fetch research papers from PubMed with pharmaceutical/biotech company affiliations.
    
    QUERY: PubMed search query (e.g., "cancer immunotherapy")
    
    Examples:
        get-papers-list "cancer immunotherapy"
        get-papers-list "diabetes treatment" -f results.csv
        get-papers-list "vaccine development" -d -m 50
    """
    try:
        # Initialize fetcher
        fetcher = PubMedFetcher(debug=debug)
        
        if debug:
            click.echo(f"Searching for papers with query: {query}")
            click.echo(f"Max results: {max_results}")
            if output_file:
                click.echo(f"Output file: {output_file}")
        
        # Fetch papers with pharmaceutical/biotech authors
        papers = fetcher.fetch_papers_with_pharma_authors(query, max_results)
        
        if not papers:
            click.echo("No papers found with pharmaceutical/biotech affiliations.")
            sys.exit(0)
        
        # Initialize exporter
        exporter = CSVExporter()
        
        if output_file:
            # Export to CSV file
            exporter.export_to_csv(papers, output_file)
            click.echo(f"Results exported to {output_file}")
        else:
            # Export to console
            exporter.export_to_console(papers)
            
            if debug:
                click.echo(f"\nCSV content:")
                click.echo(exporter.get_csv_string(papers))
        
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        if debug:
            import traceback
            click.echo(traceback.format_exc(), err=True)
        sys.exit(1)


if __name__ == '__main__':
    main() 