"""
FinTrackLib - Personal Finance Tracking for Indian Users

A comprehensive expense tracking library with INR support,
Indian categories, and budget management.
"""

__version__ = "0.3.0"

from fintracklib.models import Transaction, Budget
from fintracklib.logger import ExpenseLogger
from fintracklib.budgeter import BudgetManager
from fintracklib.categorizer import Categorizer

__all__ = [
    'Transaction',
    'Budget',
    'ExpenseLogger',
    'BudgetManager',
    'Categorizer',
]

