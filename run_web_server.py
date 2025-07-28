#!/usr/bin/env python3
"""Run the PubMed Paper Fetcher web server."""

from pubmed_paper_fetcher.web_app import app

if __name__ == '__main__':
    print("Starting PubMed Paper Fetcher Web Server...")
    print("Open your browser and go to: http://localhost:3000")
    print("Press Ctrl+C to stop the server")
    app.run(debug=True, host='0.0.0.0', port=3000) 