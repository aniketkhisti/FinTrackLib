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


@dataclass
class SavingsGoal:
    """Represents a savings goal for major life events.
    
    Attributes:
        name: Goal name (e.g., "Wedding", "House down payment")
        target_amount: Target amount to save in INR
        current_saved: Amount currently saved
        deadline: Target date to achieve the goal
        id: Unique identifier
    """
    name: str
    target_amount: float
    current_saved: float = 0.0
    deadline: datetime = field(default_factory=lambda: datetime.now() + timedelta(days=365))
    id: Optional[int] = None
    
    def __post_init__(self):
        """Validate savings goal data."""
        if self.target_amount <= 0:
            raise ValueError("Target amount must be positive")
        if self.current_saved < 0:
            raise ValueError("Current saved amount cannot be negative")
        if self.deadline <= datetime.now():
            raise ValueError("Deadline must be in the future")
    
    def add_contribution(self, amount: float):
        """Add a contribution to this savings goal.
        
        Args:
            amount: Amount to add to current savings
        """
        if amount <= 0:
            raise ValueError("Contribution amount must be positive")
        self.current_saved += amount
    
    def progress_percentage(self) -> float:
        """Calculate progress as a percentage.
        
        Returns:
            Progress percentage (capped at 100.0)
        """
        if self.target_amount == 0:
            return 0.0
        progress = (self.current_saved / self.target_amount) * 100
        return min(progress, 100.0)
    
    def remaining_amount(self) -> float:
        """Calculate remaining amount to reach goal.
        
        Returns:
            Amount still needed (can be negative if exceeded)
        """
        return self.target_amount - self.current_saved
    
    def is_exceeded(self) -> bool:
        """Check if goal has been exceeded.
        
        Returns:
            True if current savings exceed target
        """
        return self.current_saved > self.target_amount
    
    def excess_amount(self) -> float:
        """Get amount by which goal is exceeded.
        
        Returns:
            Excess amount (0 if not exceeded)
        """
        return max(0, self.current_saved - self.target_amount)
    
    def months_remaining(self) -> int:
        """Calculate months remaining until deadline.
        
        Returns:
            Number of months remaining
        """
        now = datetime.now()
        if self.deadline <= now:
            return 0
        
        # Calculate months difference
        year_diff = self.deadline.year - now.year
        month_diff = self.deadline.month - now.month
        total_months = year_diff * 12 + month_diff
        
        # Adjust for day difference
        if self.deadline.day < now.day:
            total_months -= 1
        
        return max(0, total_months)
    
    def monthly_required(self) -> float:
        """Calculate monthly savings needed to meet deadline.
        
        Returns:
            Monthly amount needed (0 if deadline passed or goal met)
        """
        months_left = self.months_remaining()
        if months_left == 0 or self.is_exceeded():
            return 0.0
        
        remaining = self.remaining_amount()
        return remaining / months_left if months_left > 0 else 0.0
    
    def is_on_track(self, monthly_savings: float) -> bool:
        """Check if current monthly savings rate will meet the goal.
        
        Args:
            monthly_savings: Current monthly savings rate
            
        Returns:
            True if on track to meet goal by deadline
        """
        required = self.monthly_required()
        return monthly_savings >= required
    
    def to_dict(self):
        """Convert savings goal to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'target_amount': self.target_amount,
            'current_saved': self.current_saved,
            'deadline': self.deadline.isoformat(),
            'progress_percentage': self.progress_percentage(),
            'remaining_amount': self.remaining_amount(),
            'is_exceeded': self.is_exceeded(),
            'months_remaining': self.months_remaining(),
            'monthly_required': self.monthly_required()
        }