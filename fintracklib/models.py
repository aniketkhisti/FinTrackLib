"""Core data models for financial transactions."""
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional


@dataclass
class Transaction:
    """Represents a single expense transaction.
    
    Attributes:
        amount: Transaction amount in INR
        description: Description of the expense
        date: Transaction date (defaults to now)
        category: Expense category (optional)
        id: Unique identifier (assigned by logger)
    """
    amount: float
    description: str
    date: datetime = field(default_factory=datetime.now)
    category: Optional[str] = None
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
            'category': self.category,
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


@dataclass
class RecurringExpense:
    """Represents a recurring expense like rent or bills.
    
    Attributes:
        amount: Expense amount
        description: Description of the recurring expense
        frequency: How often it recurs (daily, weekly, monthly, yearly)
        next_due_date: Next date when expense is due
        category: Optional expense category
        id: Unique identifier
    """
    amount: float
    description: str
    frequency: str  # daily, weekly, monthly, yearly
    next_due_date: datetime
    category: Optional[str] = None
    id: Optional[int] = None
    
    def __post_init__(self):
        """Validate recurring expense data."""
        if self.amount <= 0:
            raise ValueError("Amount must be positive")
        
        valid_frequencies = ['daily', 'weekly', 'monthly', 'yearly']
        if self.frequency.lower() not in valid_frequencies:
            raise ValueError(f"Frequency must be one of: {', '.join(valid_frequencies)}")
        
        self.frequency = self.frequency.lower()
    
    def is_due(self, check_date: Optional[datetime] = None) -> bool:
        """Check if this recurring expense is due.
        
        Args:
            check_date: Date to check against (defaults to now)
            
        Returns:
            True if expense is due on or before check_date
        """
        if check_date is None:
            check_date = datetime.now()
        return self.next_due_date <= check_date
    
    def calculate_next_due_date(self) -> datetime:
        """Calculate the next due date based on frequency.
        
        Returns:
            Next due date
        """
        current = self.next_due_date
        
        if self.frequency == 'daily':
            return current + timedelta(days=1)
        elif self.frequency == 'weekly':
            return current + timedelta(weeks=1)
        elif self.frequency == 'monthly':
            # Handle months with different days
            month = current.month + 1
            year = current.year
            if month > 12:
                month = 1
                year += 1
            
            # Handle day overflow (e.g., Jan 31 -> Feb 28)
            day = current.day
            while True:
                try:
                    return datetime(year, month, day, current.hour, current.minute)
                except ValueError:
                    # Day doesn't exist in this month, try previous day
                    day -= 1
                    if day < 1:
                        raise ValueError("Unable to calculate next monthly date")
        
        elif self.frequency == 'yearly':
            year = current.year + 1
            # Handle leap year (Feb 29 in non-leap year)
            if current.month == 2 and current.day == 29:
                # Check if next year is leap year
                try:
                    return datetime(year, 2, 29, current.hour, current.minute)
                except ValueError:
                    # Not a leap year, use Feb 28
                    return datetime(year, 2, 28, current.hour, current.minute)
            return datetime(year, current.month, current.day, current.hour, current.minute)
        
        return current
