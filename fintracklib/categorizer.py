"""Expense categorization functionality."""
from typing import List, Optional
from fintracklib.models import Transaction
from fintracklib.config import DEFAULT_CATEGORIES


class Categorizer:
    """Manages categorization of expense transactions.
    
    Provides functionality to manually categorize transactions or
    automatically categorize based on keywords in the description.
    """
    
    def __init__(self, valid_categories: Optional[List[str]] = None):
        """Initialize the categorizer.
        
        Args:
            valid_categories: List of valid category names.
                            Defaults to DEFAULT_CATEGORIES if not provided.
        """
        self.valid_categories = valid_categories or DEFAULT_CATEGORIES.copy()
    
    def is_valid_category(self, category: str) -> bool:
        """Check if a category is valid.
        
        Args:
            category: Category name to check
            
        Returns:
            True if category is valid, False otherwise
        """
        return category in self.valid_categories
    
    def get_valid_categories(self) -> List[str]:
        """Get list of valid categories.
        
        Returns:
            Copy of the valid categories list
        """
        return self.valid_categories.copy()
    
    def categorize_transaction(self, transaction: Transaction, category: str,
                              overwrite: bool = False):
        """Manually assign a category to a transaction.
        
        Args:
            transaction: Transaction to categorize
            category: Category to assign
            overwrite: If False and transaction already has a category,
                      raises ValueError. Set to True to allow category changes.
            
        Raises:
            ValueError: If category is not valid or if transaction already
                       has a category and overwrite=False
        """
        if not self.is_valid_category(category):
            raise ValueError(
                f"Invalid category '{category}'. "
                f"Valid categories: {', '.join(self.valid_categories)}"
            )
        
        if transaction.category is not None and not overwrite:
            raise ValueError(
                f"Transaction already has category '{transaction.category}'. "
                f"Use overwrite=True to change it."
            )
        
        transaction.category = category
    
    def auto_categorize(self, transaction: Transaction) -> bool:
        """Automatically categorize a transaction based on description keywords.
        
        Args:
            transaction: Transaction to categorize
            
        Returns:
            True if transaction was categorized, False otherwise
        """
        desc_lower = transaction.description.lower()
        
        # Street Food keywords
        if any(word in desc_lower for word in [
            'chai', 'tea', 'samosa', 'biryani', 'vada pav', 
            'pani puri', 'pav bhaji', 'dosa', 'idli', 'chaat'
        ]):
            transaction.category = 'Street Food'
            return True
        
        # Transport keywords
        if any(word in desc_lower for word in [
            'auto', 'rickshaw', 'cab', 'ola', 'uber', 
            'metro', 'bus', 'train', 'taxi', 'fare'
        ]):
            transaction.category = 'Transport'
            return True
        
        # Festivals keywords
        if any(word in desc_lower for word in [
            'diwali', 'holi', 'rakhi', 'dussehra', 'ganesh', 
            'navratri', 'eid', 'christmas', 'puja', 'festival'
        ]):
            transaction.category = 'Festivals'
            return True
        
        # Groceries keywords
        if any(word in desc_lower for word in [
            'rice', 'atta', 'wheat', 'dal', 'vegetables', 'veggies',
            'grocery', 'groceries', 'milk', 'bread', 'eggs'
        ]):
            transaction.category = 'Groceries'
            return True
        
        # Utilities keywords
        if any(word in desc_lower for word in [
            'electricity', 'electric', 'water', 'gas', 'cylinder',
            'bill', 'recharge', 'broadband', 'internet', 'wifi'
        ]):
            transaction.category = 'Utilities'
            return True
        
        # Entertainment keywords
        if any(word in desc_lower for word in [
            'movie', 'cinema', 'theater', 'concert', 'show',
            'restaurant', 'netflix', 'spotify', 'game'
        ]):
            transaction.category = 'Entertainment'
            return True
        
        # Healthcare keywords
        if any(word in desc_lower for word in [
            'medicine', 'medical', 'doctor', 'hospital', 'clinic',
            'pharmacy', 'health', 'insurance', 'checkup'
        ]):
            transaction.category = 'Healthcare'
            return True
        
        # Education keywords
        if any(word in desc_lower for word in [
            'book', 'books', 'tuition', 'course', 'class',
            'school', 'college', 'university', 'education', 'study'
        ]):
            transaction.category = 'Education'
            return True
        
        # Shopping keywords
        if any(word in desc_lower for word in [
            'clothes', 'clothing', 'shoes', 'electronics', 'phone',
            'laptop', 'shopping', 'amazon', 'flipkart', 'myntra'
        ]):
            transaction.category = 'Shopping'
            return True
        
        # If no match found, return False
        return False

