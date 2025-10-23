"""Core data models for financial transactions."""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Transaction:
    """Represents a single expense transaction.
    
    Attributes:
        amount: Transaction amount in INR
        description: Description of the expense
        date: Transaction date (defaults to now)
        id: Unique identifier (assigned by logger)
    """
    amount: float
    description: str
    date: datetime = field(default_factory=datetime.now)
    id: Optional[int] = None
    
    def __post_init__(self):
        """Validate transaction data."""
        if self.amount < 0:
            raise ValueError("Amount cannot be negative")
    
    def to_dict(self):
        """Convert transaction to dictionary."""
        return {
            'id': self.id,
            'amount': self.amount,
            'description': self.description,
            'date': self.date.isoformat()
        }
    
    def matches(self, other):
        """Check if this transaction is a duplicate of another.
        
        Two transactions are considered duplicates if they have the same
        amount, description, and occur on the same day.
        
        Args:
            other: Another Transaction object
            
        Returns:
            True if transactions are duplicates, False otherwise
        """
        if not isinstance(other, Transaction):
            return False
        return (
            self.amount == other.amount and
            self.description == other.description and
            self.date.date() == other.date.date()
        )


@dataclass
class Budget:
    """Budget allocation for a specific category.
    
    Attributes:
        category: Budget category name
        amount: Total budget amount in INR
        period: Budget period (monthly, yearly, weekly)
        spent: Amount spent against this budget
    """
    category: str
    amount: float
    period: str = "monthly"
    spent: float = 0.0
    
    def __post_init__(self):
        """Validate budget data."""
        if self.amount <= 0:
            raise ValueError("Budget amount must be positive")
        if self.period not in ["monthly", "yearly", "weekly"]:
            raise ValueError(f"Invalid period: {self.period}")
    
    def remaining(self):
        """Calculate remaining budget amount.
        
        Returns:
            Remaining amount (can be negative if exceeded)
        """
        return self.amount - self.spent
    
    def is_exceeded(self):
        """Check if budget has been exceeded.
        
        Returns:
            True if spent exceeds budget
        """
        return self.spent > self.amount
    
    def utilization_percentage(self):
        """Get budget utilization as a percentage.
        
        Returns:
            Utilization percentage (0-100+)
        """
        return (self.spent / self.amount) * 100 if self.amount > 0 else 0
    
    def add_expense(self, amount: float):
        """Add an expense to this budget's spent amount.
        
        Args:
            amount: Expense amount to add
        """
        self.spent += amount

