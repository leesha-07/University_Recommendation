"""
University Recommendation API
Flask REST API for university recommendations.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from recommendation_engine import UniversityRecommender
import os

app = Flask(__name__)
CORS(app)

# Initialize recommender
data_path = os.path.join(os.path.dirname(__file__), '../data/universities.json')
recommender = UniversityRecommender(data_path)


@app.route('/')
def home():
    """
    API home endpoint with information about available endpoints.
    """
    return jsonify({
        'message': 'University Recommendation API',
        'version': '1.0.0',
        'endpoints': {
            '/': 'API information',
            '/api/universities': 'Get all universities (supports filtering)',
            '/api/recommend': 'Get personalized recommendations (POST)',
            '/api/countries': 'Get list of all countries',
            '/api/stats': 'Get dataset statistics'
        }
    })


@app.route('/api/universities', methods=['GET'])
def get_universities():
    """
    Get all universities with optional filtering.
    
    Query parameters:
    - country: Filter by country name
    - max_tuition: Filter by maximum tuition
    - min_rank: Filter by minimum world rank
    - max_rank: Filter by maximum world rank
    """
    try:
        universities = recommender.get_all_universities()
        
        # Apply filters from query parameters
        country = request.args.get('country')
        if country:
            universities = [u for u in universities if u.get('country') == country]
        
        max_tuition = request.args.get('max_tuition', type=float)
        if max_tuition is not None:
            universities = [u for u in universities if u.get('tuition_usd', 0) <= max_tuition]
        
        min_rank = request.args.get('min_rank', type=int)
        if min_rank is not None:
            universities = [u for u in universities if u.get('world_rank', 999) >= min_rank]
        
        max_rank = request.args.get('max_rank', type=int)
        if max_rank is not None:
            universities = [u for u in universities if u.get('world_rank', 999) <= max_rank]
        
        return jsonify({
            'success': True,
            'count': len(universities),
            'universities': universities
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/recommend', methods=['POST'])
def recommend():
    """
    Get personalized university recommendations.
    
    Request body (JSON):
    {
        "gpa": 3.5,
        "budget": 40000,
        "test_score": 1400,
        "ielts_score": 7.0,
        "preferred_countries": ["United States", "United Kingdom"],
        "preferred_sectors": ["Engineering", "Computer Science"]
    }
    
    Required fields: gpa, budget, test_score, ielts_score
    Optional fields: preferred_countries, preferred_sectors
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'Request body must be JSON'
            }), 400
        
        # Validate required fields
        required_fields = ['gpa', 'budget', 'test_score', 'ielts_score']
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            return jsonify({
                'success': False,
                'error': f'Missing required fields: {", ".join(missing_fields)}'
            }), 400
        
        # Validate field types and ranges
        if not isinstance(data.get('gpa'), (int, float)) or data['gpa'] < 0 or data['gpa'] > 4.0:
            return jsonify({
                'success': False,
                'error': 'GPA must be a number between 0 and 4.0'
            }), 400
        
        if not isinstance(data.get('budget'), (int, float)) or data['budget'] < 0:
            return jsonify({
                'success': False,
                'error': 'Budget must be a positive number'
            }), 400
        
        if not isinstance(data.get('test_score'), int) or data['test_score'] < 400 or data['test_score'] > 1600:
            return jsonify({
                'success': False,
                'error': 'Test score must be an integer between 400 and 1600'
            }), 400
        
        if not isinstance(data.get('ielts_score'), (int, float)) or data['ielts_score'] < 0 or data['ielts_score'] > 9:
            return jsonify({
                'success': False,
                'error': 'IELTS score must be a number between 0 and 9'
            }), 400
        
        # Get recommendations
        recommendations = recommender.recommend(data)
        
        # Return top 20 recommendations
        top_recommendations = recommendations[:20]
        
        return jsonify({
            'success': True,
            'count': len(top_recommendations),
            'total_matches': len(recommendations),
            'user_profile': data,
            'recommendations': top_recommendations
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/countries', methods=['GET'])
def get_countries():
    """
    Get list of all unique countries in the dataset.
    """
    try:
        universities = recommender.get_all_universities()
        countries = sorted(set(u.get('country') for u in universities if u.get('country')))
        
        return jsonify({
            'success': True,
            'count': len(countries),
            'countries': countries
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/stats', methods=['GET'])
def get_stats():
    """
    Get dataset statistics.
    
    Returns statistics about:
    - Total universities
    - Number of countries
    - Tuition range
    - GPA range
    - Test score range
    - IELTS range
    """
    try:
        universities = recommender.get_all_universities()
        
        tuitions = [u.get('tuition_usd', 0) for u in universities]
        gpas_min = [u.get('gpa_min', 0) for u in universities]
        gpas_competitive = [u.get('gpa_competitive', 0) for u in universities]
        test_scores = [u.get('test_benchmark', 0) for u in universities]
        ielts_scores = [u.get('ielts_min', 0) for u in universities]
        countries = set(u.get('country') for u in universities if u.get('country'))
        
        stats = {
            'success': True,
            'total_universities': len(universities),
            'countries_count': len(countries),
            'tuition_range': {
                'min': min(tuitions) if tuitions else 0,
                'max': max(tuitions) if tuitions else 0,
                'average': round(sum(tuitions) / len(tuitions), 2) if tuitions else 0
            },
            'gpa_min_range': {
                'min': min(gpas_min) if gpas_min else 0,
                'max': max(gpas_min) if gpas_min else 0,
                'average': round(sum(gpas_min) / len(gpas_min), 2) if gpas_min else 0
            },
            'gpa_competitive_range': {
                'min': min(gpas_competitive) if gpas_competitive else 0,
                'max': max(gpas_competitive) if gpas_competitive else 0,
                'average': round(sum(gpas_competitive) / len(gpas_competitive), 2) if gpas_competitive else 0
            },
            'test_score_range': {
                'min': min(test_scores) if test_scores else 0,
                'max': max(test_scores) if test_scores else 0,
                'average': round(sum(test_scores) / len(test_scores), 2) if test_scores else 0
            },
            'ielts_range': {
                'min': min(ielts_scores) if ielts_scores else 0,
                'max': max(ielts_scores) if ielts_scores else 0,
                'average': round(sum(ielts_scores) / len(ielts_scores), 2) if ielts_scores else 0
            }
        }
        
        return jsonify(stats)
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({
        'success': False,
        'error': 'Endpoint not found'
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500


if __name__ == '__main__':
    # Debug mode should only be enabled for development
    # Set to False in production to prevent security risks
    import os
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(debug=debug_mode, port=5000)
