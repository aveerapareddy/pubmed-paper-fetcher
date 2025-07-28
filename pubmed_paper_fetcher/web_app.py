"""Flask web application for PubMed Paper Fetcher."""

import os
import tempfile
from datetime import datetime
from typing import List, Optional
from flask import Flask, render_template, request, jsonify, send_file, flash
from werkzeug.utils import secure_filename

from .fetcher import PubMedFetcher
from .exporter import CSVExporter


app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key')


@app.route('/')
def index():
    """Main page with search form."""
    return render_template('index.html')


@app.route('/search', methods=['POST'])
def search():
    """Handle search requests."""
    try:
        query = request.form.get('query', '').strip()
        max_results = int(request.form.get('max_results', 50))
        debug_mode = request.form.get('debug_mode') == 'on'
        
        if not query:
            flash('Please enter a search query.', 'error')
            return jsonify({'error': 'Query is required'}), 400
        
        # Initialize fetcher
        fetcher = PubMedFetcher(debug=debug_mode)
        
        # Fetch papers
        papers = fetcher.fetch_papers_with_pharma_authors(query, max_results)
        
        # Prepare results for display
        results = []
        for paper in papers:
            result = {
                'pubmed_id': paper.pubmed_id,
                'title': paper.title,
                'publication_date': paper.publication_date.strftime('%Y-%m-%d'),
                'non_academic_authors': ', '.join(paper.non_academic_authors),
                'company_affiliations': ', '.join(paper.company_affiliations),
                'corresponding_author_email': paper.corresponding_author_email or 'N/A',
                'total_authors': len(paper.authors),
                'has_pharma_authors': paper.has_pharma_authors
            }
            results.append(result)
        
        return jsonify({
            'success': True,
            'query': query,
            'total_found': len(results),
            'max_searched': max_results,
            'results': results,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/download', methods=['POST'])
def download_csv():
    """Download results as CSV file."""
    try:
        query = request.form.get('query', '').strip()
        max_results = int(request.form.get('max_results', 50))
        
        if not query:
            flash('Please enter a search query.', 'error')
            return jsonify({'error': 'Query is required'}), 400
        
        # Initialize fetcher and exporter
        fetcher = PubMedFetcher(debug=False)
        exporter = CSVExporter()
        
        # Fetch papers
        papers = fetcher.fetch_papers_with_pharma_authors(query, max_results)
        
        if not papers:
            flash('No papers found with pharmaceutical/biotech affiliations.', 'warning')
            return jsonify({'error': 'No papers found'}), 404
        
        # Create temporary CSV file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as tmp_file:
            exporter.export_to_csv(papers, tmp_file.name)
            tmp_file_path = tmp_file.name
        
        # Generate filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        safe_query = secure_filename(query.replace(' ', '_')[:50])
        filename = f"pubmed_papers_{safe_query}_{timestamp}.csv"
        
        return send_file(
            tmp_file_path,
            as_attachment=True,
            download_name=filename,
            mimetype='text/csv'
        )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/status')
def api_status():
    """API status endpoint."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })


@app.route('/test-data')
def test_data():
    """Test endpoint with sample data for demonstration."""
    sample_results = [
        {
            'pubmed_id': '12345678',
            'title': 'Novel Cancer Immunotherapy Treatment by Pfizer',
            'publication_date': '2023-06-15',
            'non_academic_authors': 'Dr. John Smith, Dr. Sarah Johnson',
            'company_affiliations': 'Pfizer Inc., Pfizer Research',
            'corresponding_author_email': 'john.smith@pfizer.com',
            'total_authors': 5,
            'has_pharma_authors': True
        },
        {
            'pubmed_id': '87654321',
            'title': 'Diabetes Treatment Clinical Trial Results',
            'publication_date': '2023-05-20',
            'non_academic_authors': 'Dr. Michael Brown',
            'company_affiliations': 'Novartis Pharmaceuticals',
            'corresponding_author_email': 'michael.brown@novartis.com',
            'total_authors': 3,
            'has_pharma_authors': True
        },
        {
            'pubmed_id': '11223344',
            'title': 'Vaccine Development Study',
            'publication_date': '2023-04-10',
            'non_academic_authors': 'Dr. Emily Davis, Dr. Robert Wilson',
            'company_affiliations': 'Johnson & Johnson, Janssen Research',
            'corresponding_author_email': 'emily.davis@jnj.com',
            'total_authors': 7,
            'has_pharma_authors': True
        }
    ]
    
    return jsonify({
        'success': True,
        'query': 'test data',
        'total_found': len(sample_results),
        'max_searched': 10,
        'results': sample_results,
        'timestamp': datetime.now().isoformat()
    })


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 