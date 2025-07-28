# PubMed Paper Fetcher

A Python program to fetch research papers from PubMed that have authors affiliated with pharmaceutical or biotech companies. The program filters papers based on author affiliations and exports the results in CSV format.

## 🚀 Quick Start

> **💡 For the fastest setup, see [QUICKSTART.md](QUICKSTART.md)**

### Prerequisites

- **Python 3.10+** (required for dependencies)
- **Poetry** (for dependency management)
- **Git** (for version control)

### Installation

#### Option 1: Automated Setup (Recommended)

1. **Clone the repository:**

   ```bash
   git clone <repository-url>
   cd likitha
   ```

2. **Run the setup script:**
   ```bash
   ./setup.sh
   ```

#### Option 2: Manual Setup

1. **Clone the repository:**

   ```bash
   git clone <repository-url>
   cd likitha
   ```

2. **Install Poetry (if not installed):**

   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

3. **Install dependencies:**

   ```bash
   poetry install
   ```

4. **Verify installation:**
   ```bash
   poetry run get-papers-list --help
   ```

### Running the Application

#### Option 1: Web Interface (Recommended)

1. **Start the web server:**

   ```bash
   poetry run python run_web_server.py
   ```

2. **Open your browser:**
   Navigate to http://localhost:3000

3. **Search for papers:**
   - Enter search terms (e.g., "clinical trial", "cancer immunotherapy")
   - Select number of results to search
   - Click "Search Papers"
   - Download results as CSV

#### Option 2: Command Line Interface

1. **Basic search:**

   ```bash
   poetry run get-papers-list "clinical trial"
   ```

2. **With options:**

   ```bash
   poetry run get-papers-list "cancer immunotherapy" -m 25 -f results.csv
   ```

3. **Debug mode:**
   ```bash
   poetry run get-papers-list "vaccine development" -d -m 10
   ```

### Troubleshooting

#### Port Already in Use

If you see "Address already in use" error:

1. **Find the process using the port:**

   ```bash
   lsof -i :3000
   ```

2. **Kill the process:**

   ```bash
   kill -9 <PID>
   ```

3. **Or use a different port:**
   ```bash
   poetry run python run_web_server.py --port 3001
   ```

#### Python Version Issues

If you encounter Python version errors:

1. **Check your Python version:**

   ```bash
   python --version
   ```

2. **Install Python 3.10+ if needed:**

   ```bash
   # On macOS with Homebrew
   brew install python@3.10

   # On Ubuntu/Debian
   sudo apt update
   sudo apt install python3.10
   ```

#### Poetry Issues

If Poetry is not found:

1. **Install Poetry:**

   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

2. **Add to PATH (if needed):**
   ```bash
   export PATH="$HOME/.local/bin:$PATH"
   ```

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
likitha/
├── pubmed_paper_fetcher/          # Main package
│   ├── __init__.py               # Package initialization
│   ├── models.py                 # Data models (Paper, Author, Affiliation)
│   ├── utils.py                  # Utility functions for text processing
│   ├── fetcher.py                # Main PubMed API fetcher
│   ├── exporter.py               # CSV export functionality
│   ├── cli.py                   # Command-line interface
│   ├── web_app.py               # Flask web application
│   ├── templates/               # HTML templates
│   │   └── index.html          # Main web interface
│   └── static/                  # Static assets
│       ├── css/
│       │   └── style.css       # Modern CSS styles
│       └── js/
│           └── app.js          # Frontend JavaScript
├── tests/                       # Test suite
│   ├── __init__.py
│   ├── test_models.py          # Model tests
│   └── test_utils.py           # Utility function tests
├── pyproject.toml              # Poetry configuration
├── README.md                   # This file
├── run_web_server.py          # Web server launcher
└── .gitignore                 # Git ignore rules
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

### Web Interface (Recommended)

Start the web server:

```bash
poetry run python run_web_server.py
```

Then open your browser and go to: http://localhost:3000

The modern web interface provides:

- **Sleek, professional design** with smooth animations
- **Intuitive search form** with large input fields and clear labels
- **Beautiful paper cards** displaying results with hover effects
- **Real-time search** with loading indicators
- **Interactive elements** with clickable PubMed links
- **One-click CSV download** for data export
- **Responsive design** optimized for all devices
- **Search tips and suggestions** to help users find relevant papers
- **Modern typography** using Inter font family
- **Smooth transitions** and micro-interactions

### Testing the Application

#### Test with Sample Data

1. **Test the web interface:**

   ```bash
   # Start the server
   poetry run python run_web_server.py

   # In another terminal, test the API
   curl -X POST http://localhost:3000/search -F "query=clinical trial" -F "max_results=3"
   ```

2. **Test the CLI:**
   ```bash
   poetry run get-papers-list "clinical trial" -m 3 -d
   ```

#### Effective Search Terms

These keywords consistently return papers with pharmaceutical affiliations:

- **"clinical trial"** - ✅ Most reliable
- **"cancer immunotherapy"** - ✅ Good results
- **"vaccine development"** - ✅ Pharmaceutical focus
- **"drug discovery"** - ✅ Industry research
- **"Pfizer vaccine"** - ✅ Company-specific
- **"Novartis cancer"** - ✅ Company-specific

### Command Line Interface

#### Basic Usage

Search for papers with a simple query:

```bash
poetry run get-papers-list "cancer immunotherapy"
```

#### Advanced Usage

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

### Example Output

#### CSV Format

```csv
PubmedID,Title,Publication Date,Non-academic Author(s),Company Affiliation(s),Corresponding Author Email
31427159,An introduction to clinical trial design.,2025-07-27,A Schultz; B R Saville; J A Marsh; T L Snelling,Berry Consultants; Wesfarmers Centre of Vaccines & Infectious Diseases; Faculty of Health and Medical Sciences,andre.schultz@health.wa.gov.au
34213625,Clinical Trial Considerations in Neuro-oncology.,2025-07-27,Eudocia Q Lee,Center for Neuro-Oncology,eqlee@partners.org
```

#### Web Interface Display

The web interface shows results in beautiful cards with:

- **Paper title** with clickable PubMed link
- **Publication metadata** (date, authors, PMID)
- **Pharmaceutical affiliation badges**
- **Detailed author and company information**
- **Email links** for corresponding authors

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

### Development Server

For development with auto-reload:

```bash
# Set Flask environment
export FLASK_ENV=development
export FLASK_DEBUG=1

# Run the server
poetry run python run_web_server.py
```

### Testing Different Ports

If port 3000 is busy, you can modify the port in `run_web_server.py`:

```python
app.run(debug=True, host='0.0.0.0', port=3001)  # Change port number
```

### API Testing

Test the API endpoints directly:

```bash
# Health check
curl http://localhost:3000/api/status

# Search papers
curl -X POST http://localhost:3000/search \
  -F "query=clinical trial" \
  -F "max_results=5"

# Download CSV
curl -X POST http://localhost:3000/download \
  -F "query=clinical trial" \
  -F "max_results=10" \
  -o results.csv
```

## Dependencies

### Core Dependencies

- **requests**: HTTP library for API calls
- **pandas**: Data manipulation and CSV export
- **click**: Command-line interface framework
- **flask**: Web framework for the web interface
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

## Project Status

### ✅ Completed Features

- **✅ Core Functionality**: PubMed API integration with affiliation detection
- **✅ CLI Interface**: Command-line tool with all required options
- **✅ Web Interface**: Modern, responsive web UI with real-time search
- **✅ CSV Export**: Complete data export with all required columns
- **✅ Error Handling**: Robust error handling and rate limiting
- **✅ Testing**: Unit tests for core functionality
- **✅ Documentation**: Comprehensive README and setup guides
- **✅ Modern UI**: Professional design with animations and interactions

### 🚀 Ready for Use

The application is **production-ready** and includes:

- **Automated setup script** (`setup.sh`)
- **Quick start guide** (`QUICKSTART.md`)
- **Comprehensive documentation** (`README.md`)
- **Modern web interface** with professional design
- **Robust CLI** with all required features
- **Real data testing** with pharmaceutical affiliations

### 🔮 Future Enhancements

- Support for additional output formats (JSON, XML)
- Enhanced affiliation detection with machine learning
- Caching for improved performance
- Support for other biomedical databases
- Advanced search filters and date ranges
- User authentication and saved searches
- API rate limit optimization
- Mobile app version
