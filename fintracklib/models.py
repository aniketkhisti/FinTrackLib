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

