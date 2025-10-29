"""Recurring expense management for common bills and subscriptions."""
from datetime import datetime
from typing import List, Optional
from fintracklib.models import RecurringExpense, Transaction


class RecurringExpenseManager:
    """Manages recurring expenses like rent and utility bills.
    
    Handles automatic transaction generation for due expenses.
    """
    
    def __init__(self):
        """Initialize the recurring expense manager."""
        self.recurring_expenses: List[RecurringExpense] = []
        self._next_id = 1
    
    def add_recurring_expense(
        self,
        amount: float,
        description: str,
        frequency: str,
        next_due_date: datetime,
        category: Optional[str] = None
    ) -> RecurringExpense:
        """Add a new recurring expense.
        
        Args:
            amount: Expense amount
            description: Description (e.g., "Monthly rent")
            frequency: How often it recurs (daily, weekly, monthly, yearly)
            next_due_date: When it's next due
            category: Optional category
            
        Returns:
            The created RecurringExpense
        """
        recurring = RecurringExpense(
            amount=amount,
            description=description,
            frequency=frequency,
            next_due_date=next_due_date,
            category=category,
            id=self._next_id
        )
        self._next_id += 1
        self.recurring_expenses.append(recurring)
        return recurring
    
    def get_due_expenses(self, check_date: Optional[datetime] = None) -> List[RecurringExpense]:
        """Get all recurring expenses that are due.
        
        Args:
            check_date: Date to check against (defaults to now)
            
        Returns:
            List of due recurring expenses
        """
        if check_date is None:
            check_date = datetime.now()
        
        return [exp for exp in self.recurring_expenses if exp.is_due(check_date)]
    
    def generate_transaction(self, recurring_id: int) -> Transaction:
        """Generate a transaction from a recurring expense.
        
        Args:
            recurring_id: ID of the recurring expense
            
        Returns:
            Generated Transaction object
            
        Raises:
            ValueError: If recurring expense not found
        """
        recurring = self.get_recurring_expense(recurring_id)
        if not recurring:
            raise ValueError(f"Recurring expense with ID {recurring_id} not found")
        
        transaction = Transaction(
            amount=recurring.amount,
            description=recurring.description,
            date=recurring.next_due_date,
            category=recurring.category
        )
        
        return transaction
    
    def mark_as_paid(self, recurring_id: int):
        """Mark a recurring expense as paid and update next due date.
        
        Args:
            recurring_id: ID of the recurring expense
            
        Raises:
            ValueError: If recurring expense not found
        """
        recurring = self.get_recurring_expense(recurring_id)
        if not recurring:
            raise ValueError(f"Recurring expense with ID {recurring_id} not found")
        
        # Update to next due date
        recurring.next_due_date = recurring.calculate_next_due_date()
    
    def get_recurring_expense(self, recurring_id: int) -> Optional[RecurringExpense]:
        """Get a recurring expense by ID.
        
        Args:
            recurring_id: ID to search for
            
        Returns:
            RecurringExpense if found, None otherwise
        """
        for exp in self.recurring_expenses:
            if exp.id == recurring_id:
                return exp
        return None
    
    def list_all_recurring(self) -> List[RecurringExpense]:
        """Get all recurring expenses.
        
        Returns:
            List of all recurring expenses
        """
        return self.recurring_expenses.copy()
    
    def remove_recurring_expense(self, recurring_id: int):
        """Remove a recurring expense.
        
        Args:
            recurring_id: ID of recurring expense to remove
            
        Raises:
            ValueError: If recurring expense not found
        """
        recurring = self.get_recurring_expense(recurring_id)
        if not recurring:
            raise ValueError(f"Recurring expense with ID {recurring_id} not found")
        
        self.recurring_expenses.remove(recurring)

