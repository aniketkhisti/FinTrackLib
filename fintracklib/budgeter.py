"""Budget management and tracking."""
from typing import Dict, List, Optional
from fintracklib.models import Budget


class BudgetManager:
    """Manages budgets for different expense categories.
    
    Allows creating budgets, recording expenses against them,
    and retrieving budget information.
    """
    
    def __init__(self):
        """Initialize the budget manager."""
        self.budgets: Dict[str, Budget] = {}
    
    def create_budget(self, category: str, amount: float, period: str = "monthly"):
        """Create a new budget for a category.
        
        Args:
            category: Budget category name
            amount: Budget amount in INR
            period: Budget period (monthly, yearly, weekly)
            
        Returns:
            The created Budget object
            
        Raises:
            ValueError: If budget already exists for category
        """
        if category in self.budgets:
            raise ValueError(f"Budget already exists for category: {category}")
        
        budget = Budget(category=category, amount=amount, period=period)
        self.budgets[category] = budget
        return budget
    
    def get_budget(self, category: str) -> Optional[Budget]:
        """Get budget for a category.
        
        Args:
            category: Category name
            
        Returns:
            Budget object or None if not found
        """
        return self.budgets.get(category)
    
    def record_expense(self, category: str, amount: float):
        """Record an expense against a budget.
        
        Args:
            category: Category name
            amount: Expense amount
        """
        if category in self.budgets:
            self.budgets[category].add_expense(amount)
    
    def get_all_budgets(self) -> List[Budget]:
        """Get list of all budgets.
        
        Returns:
            List of Budget objects
        """
        return list(self.budgets.values())

