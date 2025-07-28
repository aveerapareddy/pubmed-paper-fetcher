// Modern PubMed Paper Fetcher JavaScript

document.addEventListener('DOMContentLoaded', function () {
  const searchForm = document.getElementById('searchForm')
  const loadingSpinner = document.getElementById('loadingSpinner')
  const resultsSection = document.getElementById('resultsSection')
  const resultsContainer = document.getElementById('resultsContainer')
  const errorAlert = document.getElementById('errorAlert')
  const errorMessage = document.getElementById('errorMessage')
  const downloadBtn = document.getElementById('downloadBtn')
  const resultCount = document.getElementById('resultCount')

  // Search form submission
  searchForm.addEventListener('submit', function (e) {
    e.preventDefault()
    performSearch()
  })

  // Download button click
  downloadBtn.addEventListener('click', function () {
    downloadCSV()
  })

  // Perform search
  async function performSearch() {
    const formData = new FormData(searchForm)
    const query = formData.get('query').trim()
    const maxResults = formData.get('max_results')

    if (!query) {
      showError('Please enter a search query.')
      return
    }

    // Show loading state
    showLoading()
    hideResults()
    hideError()

    try {
      const response = await fetch('/search', {
        method: 'POST',
        body: formData,
      })

      const data = await response.json()

      if (response.ok && data.success) {
        displayResults(data)
      } else {
        showError(data.error || 'An error occurred while searching.')
      }
    } catch (error) {
      console.error('Search error:', error)
      showError('Network error. Please try again.')
    } finally {
      hideLoading()
    }
  }

  // Display results
  function displayResults(data) {
    if (!data.results || data.results.length === 0) {
      showError(
        'No papers found with pharmaceutical/biotech affiliations. Try different search terms.'
      )
      return
    }

    // Update result count
    resultCount.textContent = `${data.total_found} papers found`

    // Create results HTML
    const resultsHTML = data.results
      .map((paper, index) => createPaperCard(paper, index))
      .join('')

    resultsContainer.innerHTML = resultsHTML

    // Show results with animation
    resultsSection.style.display = 'block'
    resultsSection.classList.add('fade-in')

    // Show download button
    downloadBtn.style.display = 'inline-block'
    downloadBtn.classList.add('slide-up')
  }

  // Create paper card
  function createPaperCard(paper, index) {
    const pubmedUrl = `https://pubmed.ncbi.nlm.nih.gov/${paper.pubmed_id}/`
    const hasPharma = paper.has_pharma_authors ? 'text-success' : 'text-muted'
    const pharmaIcon = paper.has_pharma_authors
      ? 'fas fa-check-circle'
      : 'fas fa-times-circle'

    return `
            <div class="paper-card slide-up" style="animation-delay: ${
              index * 0.1
            }s;">
                <div class="paper-header">
                    <div class="d-flex justify-content-between align-items-start">
                        <div class="flex-grow-1">
                            <h5 class="paper-title">
                                <a href="${pubmedUrl}" target="_blank" class="text-decoration-none">
                                    ${paper.title}
                                    <i class="fas fa-external-link-alt ms-2 text-muted" style="font-size: 0.8rem;"></i>
                                </a>
                            </h5>
                            <div class="paper-meta">
                                <span class="paper-id">PMID: ${
                                  paper.pubmed_id
                                }</span>
                                <span class="paper-date">
                                    <i class="fas fa-calendar-alt me-1"></i>
                                    ${paper.publication_date}
                                </span>
                                <span class="paper-authors">
                                    <i class="fas fa-users me-1"></i>
                                    ${paper.total_authors} authors
                                </span>
                                <span class="badge ${hasPharma}">
                                    <i class="${pharmaIcon} me-1"></i>
                                    ${
                                      paper.has_pharma_authors
                                        ? 'Pharma Affiliations'
                                        : 'No Pharma Affiliations'
                                    }
                                </span>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="paper-body">
                    <div class="paper-details">
                        <div class="detail-item">
                            <div class="detail-icon">
                                <i class="fas fa-user-tie"></i>
                            </div>
                            <div class="detail-content">
                                <div class="detail-label">Non-academic Authors</div>
                                <div class="detail-value">${
                                  paper.non_academic_authors || 'None found'
                                }</div>
                            </div>
                        </div>
                        <div class="detail-item">
                            <div class="detail-icon">
                                <i class="fas fa-building"></i>
                            </div>
                            <div class="detail-content">
                                <div class="detail-label">Company Affiliations</div>
                                <div class="detail-value">${
                                  paper.company_affiliations || 'None found'
                                }</div>
                            </div>
                        </div>
                        <div class="detail-item">
                            <div class="detail-icon">
                                <i class="fas fa-envelope"></i>
                            </div>
                            <div class="detail-content">
                                <div class="detail-label">Corresponding Author Email</div>
                                <div class="detail-value">
                                    ${
                                      paper.corresponding_author_email !== 'N/A'
                                        ? `<a href="mailto:${paper.corresponding_author_email}" class="text-decoration-none">${paper.corresponding_author_email}</a>`
                                        : 'Not available'
                                    }
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="d-flex justify-content-between align-items-center">
                        <small class="text-muted">
                            <i class="fas fa-clock me-1"></i>
                            Found in search results
                        </small>
                        <a href="${pubmedUrl}" target="_blank" class="btn btn-outline-primary btn-sm">
                            <i class="fas fa-external-link-alt me-1"></i>
                            View on PubMed
                        </a>
                    </div>
                </div>
            </div>
        `
  }

  // Download CSV
  function downloadCSV() {
    const formData = new FormData(searchForm)

    // Create a temporary form for download
    const downloadForm = document.createElement('form')
    downloadForm.method = 'POST'
    downloadForm.action = '/download'
    downloadForm.target = '_blank'

    // Add form data
    for (let [key, value] of formData.entries()) {
      const input = document.createElement('input')
      input.type = 'hidden'
      input.name = key
      input.value = value
      downloadForm.appendChild(input)
    }

    // Submit form
    document.body.appendChild(downloadForm)
    downloadForm.submit()
    document.body.removeChild(downloadForm)
  }

  // Show loading spinner
  function showLoading() {
    loadingSpinner.style.display = 'block'
    loadingSpinner.classList.add('fade-in')
  }

  // Hide loading spinner
  function hideLoading() {
    loadingSpinner.style.display = 'none'
    loadingSpinner.classList.remove('fade-in')
  }

  // Show results section
  function showResults() {
    resultsSection.style.display = 'block'
  }

  // Hide results section
  function hideResults() {
    resultsSection.style.display = 'none'
    downloadBtn.style.display = 'none'
  }

  // Show error message
  function showError(message) {
    errorMessage.textContent = message
    errorAlert.style.display = 'block'
    errorAlert.classList.add('show')

    // Auto-hide after 5 seconds
    setTimeout(() => {
      hideError()
    }, 5000)
  }

  // Hide error message
  function hideError() {
    errorAlert.style.display = 'none'
    errorAlert.classList.remove('show')
  }

  // Add smooth scrolling for anchor links
  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener('click', function (e) {
      e.preventDefault()
      const target = document.querySelector(this.getAttribute('href'))
      if (target) {
        target.scrollIntoView({
          behavior: 'smooth',
          block: 'start',
        })
      }
    })
  })

  // Add input focus effects
  const inputs = document.querySelectorAll('.form-control, .form-select')
  inputs.forEach((input) => {
    input.addEventListener('focus', function () {
      this.parentElement.classList.add('focused')
    })

    input.addEventListener('blur', function () {
      this.parentElement.classList.remove('focused')
    })
  })

  // Add button hover effects
  const buttons = document.querySelectorAll('.btn')
  buttons.forEach((button) => {
    button.addEventListener('mouseenter', function () {
      this.style.transform = 'translateY(-1px)'
    })

    button.addEventListener('mouseleave', function () {
      this.style.transform = 'translateY(0)'
    })
  })

  // Add card hover effects
  const cards = document.querySelectorAll('.card')
  cards.forEach((card) => {
    card.addEventListener('mouseenter', function () {
      this.style.transform = 'translateY(-2px)'
    })

    card.addEventListener('mouseleave', function () {
      this.style.transform = 'translateY(0)'
    })
  })

  // Initialize tooltips if Bootstrap is available
  if (typeof bootstrap !== 'undefined') {
    const tooltipTriggerList = [].slice.call(
      document.querySelectorAll('[data-bs-toggle="tooltip"]')
    )
    tooltipTriggerList.map(function (tooltipTriggerEl) {
      return new bootstrap.Tooltip(tooltipTriggerEl)
    })
  }

  // Add keyboard shortcuts
  document.addEventListener('keydown', function (e) {
    // Ctrl/Cmd + Enter to submit search
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
      e.preventDefault()
      searchForm.dispatchEvent(new Event('submit'))
    }

    // Escape to clear form
    if (e.key === 'Escape') {
      searchForm.reset()
      hideResults()
      hideError()
    }
  })

  // Add search suggestions
  const searchInput = document.getElementById('query')
  const suggestions = [
    'clinical trial',
    'cancer immunotherapy',
    'vaccine development',
    'drug discovery',
    'Pfizer vaccine',
    'Novartis cancer',
    'biotechnology research',
  ]

  searchInput.addEventListener('input', function () {
    const value = this.value.toLowerCase()
    if (value.length > 2) {
      const matchingSuggestions = suggestions.filter((s) =>
        s.toLowerCase().includes(value)
      )
      // You could implement a dropdown with suggestions here
    }
  })

  // Add form validation
  searchForm.addEventListener('input', function () {
    const query = document.getElementById('query').value.trim()
    const submitBtn = searchForm.querySelector('button[type="submit"]')

    if (query.length > 0) {
      submitBtn.disabled = false
      submitBtn.classList.remove('btn-secondary')
      submitBtn.classList.add('btn-primary')
    } else {
      submitBtn.disabled = true
      submitBtn.classList.remove('btn-primary')
      submitBtn.classList.add('btn-secondary')
    }
  })

  // Initialize form validation
  searchForm.dispatchEvent(new Event('input'))
})
