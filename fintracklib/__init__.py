"""
FinTrackLib - Personal Finance Tracking for Indian Users

A comprehensive expense tracking library with INR support,
Indian categories, and budget management.
"""

__version__ = "0.4.0"

from fintracklib.models import Transaction, Budget
from fintracklib.logger import ExpenseLogger
from fintracklib.budgeter import BudgetManager
from fintracklib.categorizer import Categorizer
from fintracklib.reporter import Reporter
from fintracklib.utils import format_inr

__all__ = [
    'Transaction',
    'Budget',
    'ExpenseLogger',
    'BudgetManager',
    'Categorizer',
    'Reporter',
    'format_inr',
]

