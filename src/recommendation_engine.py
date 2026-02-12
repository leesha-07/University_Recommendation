"""
University Recommendation Engine
Provides filtering and ranking logic for university recommendations.
"""

import json
import os


class UniversityRecommender:
    """
    A recommendation engine that filters and ranks universities based on user profiles.
    """

    def __init__(self, data_path):
        """
        Initialize the recommender with university data.
        
        Args:
            data_path: Path to the JSON file containing university data
        """
        self.data_path = data_path
        self.universities = self._load_universities()

    def _load_universities(self):
        """Load universities from JSON file."""
        try:
            # Handle relative paths from src directory
            if not os.path.isabs(self.data_path):
                # Get the directory of this file
                current_dir = os.path.dirname(os.path.abspath(__file__))
                self.data_path = os.path.join(current_dir, self.data_path)
            
            with open(self.data_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"University data file not found at {self.data_path}")
        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON in data file: {self.data_path}")

    def get_all_universities(self):
        """
        Return all universities in the dataset.
        
        Returns:
            list: All universities
        """
        return self.universities

    def filter_by_gpa(self, universities, gpa):
        """
        Filter universities where user's GPA meets minimum requirement.
        
        Args:
            universities: List of universities to filter
            gpa: User's GPA
            
        Returns:
            list: Filtered universities
        """
        return [u for u in universities if gpa >= u.get('gpa_min', 0)]

    def filter_by_budget(self, universities, budget):
        """
        Filter universities where tuition is within budget.
        
        Args:
            universities: List of universities to filter
            budget: Maximum tuition user can afford
            
        Returns:
            list: Filtered universities
        """
        return [u for u in universities if u.get('tuition_usd', 0) <= budget]

    def filter_by_test_score(self, universities, test_score, tolerance=50):
        """
        Filter universities within test score range (with tolerance).
        
        Args:
            universities: List of universities to filter
            test_score: User's test score (SAT/equivalent)
            tolerance: Score tolerance range
            
        Returns:
            list: Filtered universities
        """
        return [
            u for u in universities 
            if abs(u.get('test_benchmark', 0) - test_score) <= tolerance or 
               test_score >= u.get('test_benchmark', 0)
        ]

    def filter_by_ielts(self, universities, ielts_score):
        """
        Filter universities where user's IELTS meets minimum requirement.
        
        Args:
            universities: List of universities to filter
            ielts_score: User's IELTS score
            
        Returns:
            list: Filtered universities
        """
        return [u for u in universities if ielts_score >= u.get('ielts_min', 0)]

    def filter_by_country(self, universities, countries):
        """
        Filter universities by specified countries.
        
        Args:
            universities: List of universities to filter
            countries: List of country names
            
        Returns:
            list: Filtered universities
        """
        if not countries:
            return universities
        return [u for u in universities if u.get('country') in countries]

    def filter_by_sectors(self, universities, sectors):
        """
        Filter universities by top sectors.
        
        Args:
            universities: List of universities to filter
            sectors: List of sector keywords
            
        Returns:
            list: Filtered universities
        """
        if not sectors:
            return universities
        
        filtered = []
        for u in universities:
            top_sectors = u.get('top_sectors', '').lower()
            if any(sector.lower() in top_sectors for sector in sectors):
                filtered.append(u)
        return filtered

    def calculate_match_score(self, university, user_profile):
        """
        Calculate how well the university matches the user profile.
        
        Scoring factors:
        - GPA proximity to competitive GPA (0-30 points)
        - Budget affordability (0-25 points)
        - Test score proximity (0-20 points)
        - World rank (0-25 points)
        
        Args:
            university: University dictionary
            user_profile: User profile dictionary
            
        Returns:
            float: Match score (0-100)
        """
        score = 0
        
        # GPA score (30 points max)
        # Higher user GPA relative to competitive GPA is better
        gpa = user_profile.get('gpa', 0)
        gpa_competitive = university.get('gpa_competitive', 0)
        if gpa_competitive > 0:
            gpa_ratio = min(gpa / gpa_competitive, 1.1)  # Cap at 110%
            score += gpa_ratio * 30
        
        # Budget score (25 points max)
        # More affordable relative to budget is better
        budget = user_profile.get('budget', 0)
        tuition = university.get('tuition_usd', 0)
        if budget > 0:
            affordability = 1 - (tuition / budget) if tuition <= budget else 0
            score += affordability * 25
        
        # Test score proximity (20 points max)
        test_score = user_profile.get('test_score', 0)
        test_benchmark = university.get('test_benchmark', 0)
        if test_benchmark > 0:
            score_diff = abs(test_score - test_benchmark)
            proximity = max(0, 1 - (score_diff / 200))  # 200 point range
            score += proximity * 20
        
        # World rank score (25 points max)
        # Lower rank number is better
        world_rank = university.get('world_rank', 100)
        rank_score = max(0, 1 - (world_rank / 100))
        score += rank_score * 25
        
        return round(score, 2)

    def rank_universities(self, universities, user_profile):
        """
        Sort universities by match score (highest first).
        
        Args:
            universities: List of universities to rank
            user_profile: User profile dictionary
            
        Returns:
            list: Universities sorted by match score with scores included
        """
        ranked = []
        for university in universities:
            match_score = self.calculate_match_score(university, user_profile)
            university_with_score = university.copy()
            university_with_score['match_score'] = match_score
            ranked.append(university_with_score)
        
        # Sort by match score (descending)
        ranked.sort(key=lambda x: x['match_score'], reverse=True)
        return ranked

    def recommend(self, user_profile):
        """
        Generate university recommendations based on user profile.
        
        The recommendation process:
        1. Filter by minimum requirements (GPA, test scores, IELTS)
        2. Filter by budget
        3. Filter by preferred countries (if specified)
        4. Filter by preferred sectors (if specified)
        5. Calculate match scores
        6. Rank and return top recommendations
        
        Args:
            user_profile: Dictionary containing:
                - gpa (float): User's GPA
                - budget (float): Max tuition they can afford
                - test_score (int): SAT/equivalent score
                - ielts_score (float): IELTS score
                - preferred_countries (list, optional): List of country names
                - preferred_sectors (list, optional): List of sector keywords
                
        Returns:
            list: Top recommended universities with match scores
        """
        universities = self.universities.copy()
        
        # Apply filters
        universities = self.filter_by_gpa(universities, user_profile.get('gpa', 0))
        universities = self.filter_by_budget(universities, user_profile.get('budget', float('inf')))
        universities = self.filter_by_test_score(
            universities, 
            user_profile.get('test_score', 0),
            tolerance=100  # More lenient tolerance for recommendations
        )
        universities = self.filter_by_ielts(universities, user_profile.get('ielts_score', 0))
        
        # Optional filters
        preferred_countries = user_profile.get('preferred_countries', [])
        if preferred_countries:
            universities = self.filter_by_country(universities, preferred_countries)
        
        preferred_sectors = user_profile.get('preferred_sectors', [])
        if preferred_sectors:
            universities = self.filter_by_sectors(universities, preferred_sectors)
        
        # Rank and return
        return self.rank_universities(universities, user_profile)
