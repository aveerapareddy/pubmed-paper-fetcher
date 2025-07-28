# Quick Start Guide

Get up and running with PubMed Paper Fetcher in 5 minutes!

## 🚀 Super Quick Start

1. **Clone and setup:**

   ```bash
   git clone <repository-url>
   cd likitha
   ./setup.sh
   ```

2. **Start the web server:**

   ```bash
   poetry run python run_web_server.py
   ```

3. **Open your browser:**
   Navigate to http://localhost:3000

4. **Search for papers:**
   - Enter: `clinical trial`
   - Click "Search Papers"
   - Download results as CSV

## 🎯 Test It Works

### Web Interface Test

```bash
# Start server
poetry run python run_web_server.py

# In another terminal, test the API
curl -X POST http://localhost:3000/search -F "query=clinical trial" -F "max_results=3"
```

### CLI Test

```bash
poetry run get-papers-list "clinical trial" -m 3
```

## 🔍 Effective Search Terms

These keywords consistently return pharmaceutical affiliations:

- **"clinical trial"** - ✅ Most reliable
- **"cancer immunotherapy"** - ✅ Good results
- **"vaccine development"** - ✅ Pharmaceutical focus
- **"drug discovery"** - ✅ Industry research

## 🛠️ Troubleshooting

### Port 3000 Busy?

```bash
# Find what's using the port
lsof -i :3000

# Kill the process
kill -9 <PID>

# Or use a different port
poetry run python run_web_server.py --port 3001
```

### Python Version Issues?

```bash
# Check version
python --version

# Install Python 3.10+ if needed
# macOS: brew install python@3.10
# Ubuntu: sudo apt install python3.10
```

## 📊 Expected Output

You should see papers with:

- **Berry Consultants** (consulting company)
- **Wesfarmers Centre of Vaccines** (vaccine research)
- **Center for Neuro-Oncology** (medical center)

## 🎉 Success!

If you see papers with pharmaceutical affiliations, you're all set!

For more details, see the full [README.md](README.md).
