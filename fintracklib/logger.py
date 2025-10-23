"""Expense logging functionality."""
from typing import List, Optional
from datetime import datetime
from fintracklib.models import Transaction


class ExpenseLogger:
    """Manages expense transaction logging.
    
    Provides functionality to log expenses, retrieve transactions,
    and calculate totals. Each transaction is assigned a unique ID.
    """
    
    def __init__(self):
        """Initialize the expense logger."""
        self.transactions: List[Transaction] = []
        self._next_id = 1
    
    def log_expense(self, amount: float, description: str, 
                    category: Optional[str] = None,
                    date: Optional[datetime] = None,
                    allow_duplicates: bool = False):
        """Log a new expense transaction.
        
        Args:
            amount: Expense amount in INR
            description: Expense description
            category: Expense category (optional)
            date: Transaction date (defaults to now)
            allow_duplicates: If False, raises error for duplicate transactions
            
        Returns:
            The created Transaction object
            
        Raises:
            ValueError: If amount is negative or duplicate detected
        """
        if date is None:
            date = datetime.now()
        
        txn = Transaction(
            amount=amount,
            description=description,
            category=category,
            date=date,
            id=self._next_id
        )
        
        # Check for duplicates
        if not allow_duplicates:
            for existing in self.transactions:
                if txn.matches(existing):
                    raise ValueError(
                        f"Duplicate transaction detected: {description} for ₹{amount}"
                    )
        
        self.transactions.append(txn)
        self._next_id += 1
        return txn
    
    def get_all_transactions(self):
        """Get all logged transactions.
        
        Returns:
            Copy of the transactions list
        """
        return self.transactions.copy()
    
    def total_expenses(self):
        """Calculate total of all expenses.
        
        Returns:
            Sum of all transaction amounts
        """
        return sum(t.amount for t in self.transactions)

