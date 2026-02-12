// ===================================
// University Recommendation System - Frontend JS
// ===================================

// Global state
let countriesData = [];

// ===================================
// Initialize App on Page Load
// ===================================

document.addEventListener('DOMContentLoaded', async () => {
    // Fetch and populate countries
    await fetchCountries();
    
    // Set up event listeners
    setupEventListeners();
    
    // Set up "Select All" functionality
    setupSelectAll();
    
    // Set up form validation enhancement
    setupFormValidation();
});

// ===================================
// Fetch Countries from API
// ===================================

async function fetchCountries() {
    try {
        const response = await fetch('/api/countries');
        const data = await response.json();
        
        if (data.success && data.countries) {
            countriesData = data.countries;
            populateCountries(data.countries);
        } else {
            console.error('Failed to fetch countries:', data.error);
            showError('Failed to load countries. Please refresh the page.');
        }
    } catch (error) {
        console.error('Error fetching countries:', error);
        showError('Failed to load countries. Please check your connection.');
    }
}

// ===================================
// Populate Countries Checkboxes
// ===================================

function populateCountries(countries) {
    const container = document.getElementById('countries-container');
    
    // Keep the "Select All" checkbox
    const selectAllCheckbox = container.querySelector('#select-all-countries').parentElement;
    
    // Clear existing country checkboxes (keep Select All)
    container.innerHTML = '';
    container.appendChild(selectAllCheckbox);
    
    // Add country checkboxes
    countries.forEach(country => {
        const label = document.createElement('label');
        label.className = 'checkbox-label';
        
        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.name = 'country';
        checkbox.value = country;
        checkbox.className = 'checkbox-input';
        
        const span = document.createElement('span');
        span.className = 'checkbox-text';
        span.textContent = country;
        
        label.appendChild(checkbox);
        label.appendChild(span);
        container.appendChild(label);
    });
}

// ===================================
// Setup Event Listeners
// ===================================

function setupEventListeners() {
    // Form submission
    const form = document.getElementById('recommendation-form');
    form.addEventListener('submit', getRecommendations);
    
    // Clear button
    const clearBtn = document.getElementById('clear-btn');
    clearBtn.addEventListener('click', clearForm);
    
    // Search again button
    const searchAgainBtn = document.getElementById('search-again-btn');
    searchAgainBtn.addEventListener('click', searchAgain);
}

// ===================================
// Setup "Select All" Functionality
// ===================================

function setupSelectAll() {
    // Select All Countries
    const selectAllCountries = document.getElementById('select-all-countries');
    selectAllCountries.addEventListener('change', function() {
        const countryCheckboxes = document.querySelectorAll('input[name="country"]');
        countryCheckboxes.forEach(checkbox => {
            checkbox.checked = this.checked;
        });
    });
    
    // Select All Sectors
    const selectAllSectors = document.getElementById('select-all-sectors');
    selectAllSectors.addEventListener('change', function() {
        const sectorCheckboxes = document.querySelectorAll('input[name="sector"]');
        sectorCheckboxes.forEach(checkbox => {
            checkbox.checked = this.checked;
        });
    });
}

// ===================================
// Get Recommendations (Form Submit)
// ===================================

async function getRecommendations(event) {
    event.preventDefault();
    
    // Validate form
    const form = event.target;
    if (!form.checkValidity()) {
        form.reportValidity();
        return;
    }
    
    // Get selected countries
    const selectedCountries = getSelectedCountries();
    if (selectedCountries.length === 0) {
        showError('Please select at least one country.');
        return;
    }
    
    // Show loading state
    showLoading();
    hideError();
    
    // Collect form data
    const userProfile = {
        gpa: parseFloat(document.getElementById('gpa').value),
        budget: parseFloat(document.getElementById('budget').value),
        test_score: parseInt(document.getElementById('test_score').value),
        ielts_score: parseFloat(document.getElementById('ielts_score').value),
        preferred_countries: selectedCountries,
        preferred_sectors: getSelectedSectors()
    };
    
    try {
        // Make POST request to /api/recommend
        const response = await fetch('/api/recommend', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(userProfile)
        });
        
        const data = await response.json();
        
        if (data.success) {
            // Display results
            displayResults(data.recommendations, userProfile, data.count);
        } else {
            // Show error message
            showError(data.error || 'Failed to get recommendations. Please try again.');
            hideLoading();
        }
    } catch (error) {
        console.error('Error getting recommendations:', error);
        showError('Network error. Please check your connection and try again.');
        hideLoading();
    }
}

// ===================================
// Display Results
// ===================================

function displayResults(universities, userProfile, count) {
    // Hide loading and form
    hideLoading();
    document.getElementById('form-section').classList.add('hidden');
    
    // Show results section
    const resultsSection = document.getElementById('results-section');
    resultsSection.classList.remove('hidden');
    
    // Update title
    const resultsTitle = document.getElementById('results-title');
    if (count === 0) {
        resultsTitle.textContent = 'No Universities Found';
        showError('No universities match your profile. Try adjusting your criteria.');
        return;
    }
    
    resultsTitle.textContent = `We found ${count} ${count === 1 ? 'university' : 'universities'} matching your profile`;
    
    // Clear previous results
    const container = document.getElementById('results-container');
    container.innerHTML = '';
    
    // Create university cards
    universities.forEach((university, index) => {
        const card = createUniversityCard(university, userProfile, index);
        container.appendChild(card);
    });
}

// ===================================
// Create University Card
// ===================================

function createUniversityCard(university, userProfile, index) {
    const card = document.createElement('div');
    card.className = 'university-card';
    card.style.animationDelay = `${index * 0.05}s`;
    
    // Card Header
    const header = document.createElement('div');
    header.className = 'card-header';
    
    // University Name
    const name = document.createElement('h3');
    name.className = 'university-name';
    name.textContent = university.name;
    header.appendChild(name);
    
    // Country
    const country = document.createElement('div');
    country.className = 'university-country';
    country.innerHTML = `<span>📍</span> ${university.country}`;
    header.appendChild(country);
    
    // Badges (Rank, Match Score)
    const badges = document.createElement('div');
    badges.className = 'card-badges';
    
    const rankBadge = document.createElement('span');
    rankBadge.className = 'badge badge-rank';
    rankBadge.textContent = `World Rank #${university.world_rank}`;
    badges.appendChild(rankBadge);
    
    const matchBadge = document.createElement('span');
    matchBadge.className = 'badge badge-match';
    matchBadge.textContent = `${university.match_score}% Match`;
    badges.appendChild(matchBadge);
    
    header.appendChild(badges);
    card.appendChild(header);
    
    // Card Content
    const content = document.createElement('div');
    content.className = 'card-content';
    
    // Tuition
    const tuition = createDetailItem('Annual Tuition', formatCurrency(university.tuition_usd), 'large');
    content.appendChild(tuition);
    
    // GPA Requirements
    const gpaSection = document.createElement('div');
    gpaSection.className = 'card-detail';
    
    const gpaLabel = document.createElement('div');
    gpaLabel.className = 'card-detail-label';
    gpaLabel.textContent = 'GPA Requirements';
    gpaSection.appendChild(gpaLabel);
    
    const gpaComparison = document.createElement('div');
    gpaComparison.className = 'score-comparison';
    gpaComparison.innerHTML = `
        <div class="score-item">
            <span class="score-label">Minimum: </span>
            <span class="score-value">${university.gpa_min.toFixed(2)}</span>
        </div>
        <div class="score-item">
            <span class="score-label">Competitive: </span>
            <span class="score-value">${university.gpa_competitive.toFixed(2)}</span>
        </div>
        <div class="score-item">
            <span class="score-label">Your GPA: </span>
            <span class="score-value">${userProfile.gpa.toFixed(2)}</span>
        </div>
    `;
    gpaSection.appendChild(gpaComparison);
    
    // GPA Status
    const gpaStatus = getGPAStatus(userProfile.gpa, university.gpa_min, university.gpa_competitive);
    const gpaStatusBadge = document.createElement('div');
    gpaStatusBadge.className = `gpa-status ${gpaStatus.class}`;
    gpaStatusBadge.textContent = `${gpaStatus.icon} ${gpaStatus.text}`;
    gpaSection.appendChild(gpaStatusBadge);
    
    content.appendChild(gpaSection);
    
    // Test Score
    const testScore = document.createElement('div');
    testScore.className = 'card-detail';
    testScore.innerHTML = `
        <div class="card-detail-label">Test Score Benchmark</div>
        <div class="score-comparison">
            <div class="score-item">
                <span class="score-label">Required: </span>
                <span class="score-value">${university.test_benchmark}</span>
            </div>
            <div class="score-item">
                <span class="score-label">Your Score: </span>
                <span class="score-value">${userProfile.test_score}</span>
            </div>
        </div>
    `;
    content.appendChild(testScore);
    
    // IELTS Score
    const ielts = document.createElement('div');
    ielts.className = 'card-detail';
    ielts.innerHTML = `
        <div class="card-detail-label">IELTS Requirement</div>
        <div class="score-comparison">
            <div class="score-item">
                <span class="score-label">Required: </span>
                <span class="score-value">${university.ielts_min.toFixed(1)}</span>
            </div>
            <div class="score-item">
                <span class="score-label">Your Score: </span>
                <span class="score-value">${userProfile.ielts_score.toFixed(1)}</span>
            </div>
        </div>
    `;
    content.appendChild(ielts);
    
    // Top Sectors
    const sectors = document.createElement('div');
    sectors.className = 'card-detail';
    sectors.innerHTML = `
        <div class="card-detail-label">Top Fields of Study</div>
        <div class="card-badges">
            ${university.top_sectors.split(',').map(sector => 
                `<span class="badge badge-sector">${sector.trim()}</span>`
            ).join('')}
        </div>
    `;
    content.appendChild(sectors);
    
    // Application Deadline
    const deadline = createDetailItem('Application Deadline', formatDate(university.app_deadline));
    content.appendChild(deadline);
    
    // Scholarships
    const scholarships = document.createElement('div');
    scholarships.className = 'card-detail';
    scholarships.innerHTML = `
        <div class="card-detail-label">Scholarships Available</div>
        <div class="card-detail-value">
            <a href="${university.scholarship_links}" target="_blank" rel="noopener noreferrer" 
               style="color: var(--primary-color); text-decoration: none;">
                View Scholarship Options →
            </a>
        </div>
    `;
    content.appendChild(scholarships);
    
    card.appendChild(content);
    
    // Card Actions
    const actions = document.createElement('div');
    actions.className = 'card-actions';
    actions.innerHTML = `
        <button class="card-btn card-btn-primary" onclick="window.open('${university.scholarship_links}', '_blank')">
            Learn More
        </button>
        <button class="card-btn" onclick="alert('Application feature coming soon!')">
            Apply Now
        </button>
    `;
    card.appendChild(actions);
    
    return card;
}

// ===================================
// Helper Functions
// ===================================

function createDetailItem(label, value, valueClass = '') {
    const detail = document.createElement('div');
    detail.className = 'card-detail';
    
    const labelDiv = document.createElement('div');
    labelDiv.className = 'card-detail-label';
    labelDiv.textContent = label;
    
    const valueDiv = document.createElement('div');
    valueDiv.className = `card-detail-value ${valueClass}`;
    valueDiv.textContent = value;
    
    detail.appendChild(labelDiv);
    detail.appendChild(valueDiv);
    
    return detail;
}

function getSelectedCountries() {
    const checkboxes = document.querySelectorAll('input[name="country"]:checked');
    return Array.from(checkboxes).map(cb => cb.value);
}

function getSelectedSectors() {
    const checkboxes = document.querySelectorAll('input[name="sector"]:checked');
    return Array.from(checkboxes).map(cb => cb.value);
}

function getGPAStatus(userGPA, minGPA, competitiveGPA) {
    if (userGPA >= competitiveGPA) {
        return {
            class: 'excellent',
            icon: '✓',
            text: 'Excellent Match'
        };
    } else if (userGPA >= minGPA) {
        return {
            class: 'good',
            icon: '○',
            text: 'Good Match'
        };
    } else {
        return {
            class: 'low',
            icon: '!',
            text: 'Below Minimum'
        };
    }
}

function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
    }).format(amount);
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

// ===================================
// UI State Functions
// ===================================

function showLoading() {
    document.getElementById('form-section').classList.add('hidden');
    document.getElementById('loading-section').classList.remove('hidden');
    document.getElementById('results-section').classList.add('hidden');
}

function hideLoading() {
    document.getElementById('loading-section').classList.add('hidden');
}

function showError(message) {
    const errorElement = document.getElementById('error-message');
    const errorText = document.getElementById('error-text');
    errorText.textContent = message;
    errorElement.classList.remove('hidden');
    
    // Auto-hide after 10 seconds
    setTimeout(() => {
        hideError();
    }, 10000);
}

function hideError() {
    document.getElementById('error-message').classList.add('hidden');
}

function clearForm() {
    document.getElementById('recommendation-form').reset();
    
    // Uncheck all checkboxes
    document.querySelectorAll('input[type="checkbox"]').forEach(cb => {
        cb.checked = false;
    });
    
    hideError();
}

function searchAgain() {
    // Hide results, show form
    document.getElementById('results-section').classList.add('hidden');
    document.getElementById('form-section').classList.remove('hidden');
    
    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// ===================================
// Form Validation Enhancement
// ===================================

function setupFormValidation() {
    const inputs = document.querySelectorAll('.form-input');
    
    inputs.forEach(input => {
        input.addEventListener('blur', function() {
            if (this.value && !this.checkValidity()) {
                this.classList.add('invalid');
            } else {
                this.classList.remove('invalid');
            }
        });
        
        input.addEventListener('input', function() {
            if (this.classList.contains('invalid') && this.checkValidity()) {
                this.classList.remove('invalid');
            }
        });
    });
}
