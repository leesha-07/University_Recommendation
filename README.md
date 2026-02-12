# University Recommendation System

A comprehensive backend system that recommends universities to students based on their academic profile, budget, and preferences. The system uses intelligent filtering and ranking algorithms to match students with the most suitable universities worldwide.

## Features

- **Smart Recommendations**: Matches students with universities based on GPA, test scores, budget, and preferences
- **Global Dataset**: 100+ universities from top institutions worldwide including US, UK, Canada, Europe, Asia, and Australia
- **RESTful API**: Clean and well-documented Flask REST API
- **Advanced Filtering**: Multi-criteria filtering by country, budget, test scores, and academic sectors
- **Match Scoring**: Intelligent scoring algorithm that considers multiple factors:
  - GPA compatibility
  - Budget affordability
  - Test score proximity
  - World ranking
- **Comprehensive Statistics**: Dataset analytics and insights

## Technology Stack

- **Backend Framework**: Flask 3.0.0
- **CORS Support**: Flask-CORS 4.0.0
- **Language**: Python 3.x
- **Data Format**: JSON

## Project Structure

```
University_Recommendation/
├── data/
│   └── universities.json          # Dataset with 100 universities
├── src/
│   ├── __init__.py               # Package initialization
│   ├── app.py                    # Flask REST API
│   └── recommendation_engine.py  # Recommendation logic
├── requirements.txt              # Python dependencies
├── .gitignore                   # Git ignore rules
└── README.md                    # This file
```

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/leesha-07/University_Recommendation.git
   cd University_Recommendation
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Running the API

Start the Flask development server:

```bash
python src/app.py
```

The API will be available at `http://localhost:5000`

You should see output like:
```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

## API Documentation

### Base URL
```
http://localhost:5000
```

### Endpoints

#### 1. Get API Information
```http
GET /
```

Returns information about the API and available endpoints.

**Response:**
```json
{
  "message": "University Recommendation API",
  "version": "1.0.0",
  "endpoints": {
    "/": "API information",
    "/api/universities": "Get all universities (supports filtering)",
    "/api/recommend": "Get personalized recommendations (POST)",
    "/api/countries": "Get list of all countries",
    "/api/stats": "Get dataset statistics"
  }
}
```

#### 2. Get All Universities
```http
GET /api/universities
```

Returns all universities with optional filtering.

**Query Parameters:**
- `country` (string, optional): Filter by country name
- `max_tuition` (float, optional): Maximum tuition in USD
- `min_rank` (integer, optional): Minimum world rank
- `max_rank` (integer, optional): Maximum world rank

**Example Request:**
```bash
curl "http://localhost:5000/api/universities?country=United%20States&max_tuition=50000"
```

**Response:**
```json
{
  "success": true,
  "count": 15,
  "universities": [
    {
      "name": "Massachusetts Institute of Technology",
      "country": "United States",
      "world_rank": 1,
      "tuition_usd": 57986,
      "gpa_min": 3.6,
      "gpa_competitive": 3.92,
      "test_benchmark": 1535,
      "ielts_min": 7.5,
      "scholarship_links": "https://mitfinancialaid.com",
      "app_deadline": "2026-01-01",
      "top_sectors": "Engineering, Computer Science, Physics"
    }
  ]
}
```

#### 3. Get Personalized Recommendations
```http
POST /api/recommend
```

Get personalized university recommendations based on user profile.

**Request Body:**
```json
{
  "gpa": 3.5,
  "budget": 40000,
  "test_score": 1400,
  "ielts_score": 7.0,
  "preferred_countries": ["United States", "United Kingdom"],
  "preferred_sectors": ["Engineering", "Computer Science"]
}
```

**Required Fields:**
- `gpa` (float): Student's GPA (0.0 - 4.0)
- `budget` (float): Maximum tuition budget in USD
- `test_score` (integer): SAT score (400 - 1600)
- `ielts_score` (float): IELTS score (0.0 - 9.0)

**Optional Fields:**
- `preferred_countries` (array): List of preferred country names
- `preferred_sectors` (array): List of academic sectors/fields of interest

**Example Request:**
```bash
curl -X POST http://localhost:5000/api/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "gpa": 3.5,
    "budget": 40000,
    "test_score": 1400,
    "ielts_score": 7.0,
    "preferred_countries": ["United States", "Canada"],
    "preferred_sectors": ["Engineering"]
  }'
```

**Response:**
```json
{
  "success": true,
  "count": 10,
  "total_matches": 25,
  "user_profile": {
    "gpa": 3.5,
    "budget": 40000,
    "test_score": 1400,
    "ielts_score": 7.0,
    "preferred_countries": ["United States", "Canada"],
    "preferred_sectors": ["Engineering"]
  },
  "recommendations": [
    {
      "name": "University of Toronto",
      "country": "Canada",
      "world_rank": 17,
      "tuition_usd": 55000,
      "gpa_min": 3.4,
      "gpa_competitive": 3.8,
      "test_benchmark": 1430,
      "ielts_min": 6.5,
      "match_score": 87.5,
      "scholarship_links": "https://future.utoronto.ca/scholarships",
      "app_deadline": "2026-01-15",
      "top_sectors": "Medicine, Engineering, Computer Science"
    }
  ]
}
```

#### 4. Get Countries
```http
GET /api/countries
```

Returns a list of all unique countries in the dataset.

**Example Request:**
```bash
curl http://localhost:5000/api/countries
```

**Response:**
```json
{
  "success": true,
  "count": 20,
  "countries": [
    "Australia",
    "Belgium",
    "Canada",
    "China",
    "Denmark",
    "Finland",
    "Germany",
    "Hong Kong",
    "Japan",
    "Netherlands",
    "New Zealand",
    "Norway",
    "Singapore",
    "South Korea",
    "Sweden",
    "Switzerland",
    "United Kingdom",
    "United States"
  ]
}
```

#### 5. Get Dataset Statistics
```http
GET /api/stats
```

Returns comprehensive statistics about the university dataset.

**Example Request:**
```bash
curl http://localhost:5000/api/stats
```

**Response:**
```json
{
  "success": true,
  "total_universities": 100,
  "countries_count": 20,
  "tuition_range": {
    "min": 0,
    "max": 65524,
    "average": 28000.5
  },
  "gpa_min_range": {
    "min": 3.0,
    "max": 3.7,
    "average": 3.3
  },
  "gpa_competitive_range": {
    "min": 3.55,
    "max": 3.96,
    "average": 3.72
  },
  "test_score_range": {
    "min": 1280,
    "max": 1545,
    "average": 1395
  },
  "ielts_range": {
    "min": 6.0,
    "max": 7.5,
    "average": 6.7
  }
}
```

## Recommendation Algorithm

The recommendation engine uses a sophisticated multi-factor scoring system:

### Filtering Phase
1. **GPA Filter**: Removes universities where student doesn't meet minimum GPA
2. **Budget Filter**: Removes universities exceeding student's budget
3. **Test Score Filter**: Keeps universities within reasonable test score range
4. **IELTS Filter**: Removes universities where student doesn't meet minimum IELTS
5. **Country Filter**: Applies preferred country filter if specified
6. **Sector Filter**: Applies academic sector preference if specified

### Ranking Phase
Universities are scored 0-100 based on:

- **GPA Match (30 points)**: How close student's GPA is to competitive GPA
- **Budget Affordability (25 points)**: How affordable the tuition is relative to budget
- **Test Score Proximity (20 points)**: How close student's test score is to benchmark
- **World Rank (25 points)**: University's global ranking (lower rank = higher score)

Final recommendations are sorted by match score (highest first).

## Example Usage Scenarios

### Scenario 1: High-achieving student with moderate budget
```bash
curl -X POST http://localhost:5000/api/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "gpa": 3.8,
    "budget": 30000,
    "test_score": 1480,
    "ielts_score": 7.5,
    "preferred_countries": ["Germany", "Netherlands", "Switzerland"]
  }'
```

### Scenario 2: Engineering student targeting US universities
```bash
curl -X POST http://localhost:5000/api/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "gpa": 3.6,
    "budget": 60000,
    "test_score": 1520,
    "ielts_score": 7.0,
    "preferred_countries": ["United States"],
    "preferred_sectors": ["Engineering", "Computer Science"]
  }'
```

### Scenario 3: Budget-conscious student seeking affordable options
```bash
curl -X POST http://localhost:5000/api/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "gpa": 3.4,
    "budget": 15000,
    "test_score": 1380,
    "ielts_score": 6.5
  }'
```

## Error Handling

The API returns appropriate HTTP status codes and error messages:

- `200`: Success
- `400`: Bad request (missing/invalid parameters)
- `404`: Endpoint not found
- `500`: Internal server error

**Error Response Format:**
```json
{
  "success": false,
  "error": "Error message description"
}
```

## Development

### Code Style
The project follows Python PEP 8 style guidelines:
- Clear, descriptive variable names
- Comprehensive docstrings
- Proper error handling
- Type hints where appropriate

### Project Components

#### recommendation_engine.py
Contains the `UniversityRecommender` class with methods for:
- Loading university data
- Filtering universities by various criteria
- Calculating match scores
- Ranking recommendations

#### app.py
Flask application with:
- REST API endpoints
- Request validation
- Error handling
- CORS support

## Future Enhancements

Potential improvements for future versions:

1. **User Profiles**: Persistent user profiles with save/load functionality
2. **Machine Learning**: ML-based recommendations using historical data
3. **More Filters**: Additional filters (campus size, location, weather, etc.)
4. **Comparison Tool**: Side-by-side university comparison
5. **Application Tracking**: Track application status and deadlines
6. **Database**: Migration from JSON to PostgreSQL/MongoDB
7. **Authentication**: User authentication and authorization
8. **Email Notifications**: Alert users about approaching deadlines
9. **Frontend**: React/Vue.js web interface
10. **Mobile App**: iOS/Android applications
11. **Scholarship Database**: Expanded scholarship information
12. **Alumni Network**: Connect with university alumni
13. **Virtual Tours**: Integration with university virtual tours
14. **Cost Calculator**: Total cost of attendance calculator
15. **Visa Information**: Country-specific visa requirements

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available for educational purposes.

## Contact

For questions or suggestions, please open an issue on GitHub.

## Acknowledgments

- University data compiled from various public sources
- Built with Flask and Python
- Inspired by the need to help students make informed university choices
