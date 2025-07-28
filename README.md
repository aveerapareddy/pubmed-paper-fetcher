# PubMed Paper Fetcher

A Python program to fetch research papers from PubMed that have authors affiliated with pharmaceutical or biotech companies. The program filters papers based on author affiliations and exports the results in CSV format.

## Features

- **PubMed API Integration**: Uses NCBI's E-utilities API to search and fetch paper details
- **Smart Affiliation Detection**: Identifies academic vs. non-academic affiliations using keyword analysis
- **CSV Export**: Exports results with required columns (PubmedID, Title, Publication Date, Non-academic Authors, Company Affiliations, Corresponding Author Email)
- **Command-line Interface**: Easy-to-use CLI with various options
- **Type Safety**: Fully typed Python code for better maintainability
- **Error Handling**: Robust error handling for API failures and invalid data

## Code Organization

The project is organized into modular components:

```
pubmed_paper_fetcher/
├── __init__.py          # Package initialization
├── models.py            # Data models (Paper, Author, Affiliation)
├── utils.py             # Utility functions for text processing
├── fetcher.py           # Main PubMed API fetcher
├── exporter.py          # CSV export functionality
└── cli.py              # Command-line interface
```

### Key Components

- **`models.py`**: Defines data structures for papers, authors, and affiliations
- **`utils.py`**: Contains utility functions for affiliation detection and text processing
- **`fetcher.py`**: Handles PubMed API interactions and data parsing
- **`exporter.py`**: Manages CSV export functionality
- **`cli.py`**: Command-line interface using Click

## Installation

### Prerequisites

- Python 3.8 or higher
- Poetry (for dependency management)

### Setup

1. **Clone the repository**:

   ```bash
   git clone <repository-url>
   cd pubmed-paper-fetcher
   ```

2. **Install dependencies**:

   ```bash
   poetry install
   ```

3. **Verify installation**:
   ```bash
   poetry run get-papers-list --help
   ```

## Usage

### Basic Usage

Search for papers with a simple query:

```bash
poetry run get-papers-list "cancer immunotherapy"
```

### Advanced Usage

Export results to a CSV file:

```bash
poetry run get-papers-list "diabetes treatment" -f results.csv
```

Enable debug mode for detailed logging:

```bash
poetry run get-papers-list "vaccine development" -d -m 50
```

### Command-line Options

- `QUERY`: PubMed search query (required)
- `-f, --file`: Specify output CSV file path
- `-d, --debug`: Enable debug mode for detailed logging
- `-m, --max-results`: Maximum number of results to process (default: 100)
- `-h, --help`: Show help message

### Examples

```bash
# Search for cancer immunotherapy papers
poetry run get-papers-list "cancer immunotherapy"

# Export diabetes treatment papers to CSV
poetry run get-papers-list "diabetes treatment" -f diabetes_papers.csv

# Debug mode with limited results
poetry run get-papers-list "vaccine development" -d -m 25

# Search for papers from specific years
poetry run get-papers-list "COVID-19 vaccine[dp:2020:2023]"
```

## Output Format

The program outputs a CSV file with the following columns:

| Column                     | Description                                               |
| -------------------------- | --------------------------------------------------------- |
| PubmedID                   | Unique PubMed identifier                                  |
| Title                      | Paper title                                               |
| Publication Date           | Date of publication (YYYY-MM-DD)                          |
| Non-academic Author(s)     | Names of authors with pharmaceutical/biotech affiliations |
| Company Affiliation(s)     | Names of pharmaceutical/biotech companies                 |
| Corresponding Author Email | Email address of the corresponding author                 |

## Affiliation Detection

The program uses heuristics to identify non-academic affiliations:

### Academic Keywords

- university, college, institute, school, academy
- medical center, hospital, clinic, research center
- laboratory, lab, department, faculty
- professor, researcher, scientist, phd, postdoc

### Email Analysis

- `.edu` email addresses are considered academic
- Other email patterns are analyzed for institutional domains

### Company Extraction

- Non-academic affiliations are processed to extract company names
- Common academic prefixes are removed
- Email addresses are filtered out

## Development

### Running Tests

```bash
poetry run pytest
```

### Code Formatting

```bash
poetry run black pubmed_paper_fetcher/
```

### Type Checking

```bash
poetry run mypy pubmed_paper_fetcher/
```

### Building the Package

```bash
poetry build
```

## Dependencies

### Core Dependencies

- **requests**: HTTP library for API calls
- **pandas**: Data manipulation and CSV export
- **click**: Command-line interface framework
- **python-dateutil**: Date parsing utilities
- **typing-extensions**: Enhanced type hints

### Development Dependencies

- **pytest**: Testing framework
- **black**: Code formatter
- **mypy**: Static type checker

## External Tools Used

This project was developed with assistance from:

- **Claude Sonnet 4**: AI coding assistant for initial development and code review
- **GitHub Copilot**: AI pair programming for code suggestions
- **Cursor IDE**: AI-powered code editor for development

## API Rate Limiting

The PubMed E-utilities API has rate limiting:

- 3 requests per second for registered users
- 10 requests per second for unregistered users

The program includes appropriate delays to respect these limits.

## Error Handling

The program handles various error scenarios:

- Network connectivity issues
- Invalid PubMed queries
- Missing or malformed data
- API rate limiting
- File I/O errors

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions:

1. Check the existing issues
2. Create a new issue with detailed information
3. Include debug output when reporting bugs

## Future Enhancements

- Support for additional output formats (JSON, XML)
- Enhanced affiliation detection with machine learning
- Caching for improved performance
- Support for other biomedical databases
- Web interface for easier interaction
