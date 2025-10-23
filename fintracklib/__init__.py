"""
FinTrackLib - Personal Finance Tracking for Indian Users

A comprehensive expense tracking library with INR support,
Indian categories, and budget management.
"""

__version__ = "0.1.0"

from fintracklib.models import Transaction
from fintracklib.logger import ExpenseLogger

__all__ = [
    'Transaction',
    'ExpenseLogger',
]

