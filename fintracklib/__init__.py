"""
FinTrackLib - Personal Finance Tracking for Indian Users

A comprehensive expense tracking library with INR support,
Indian categories, and budget management.
"""

__version__ = "0.6.0"

from fintracklib.models import Transaction, Budget
from fintracklib.logger import ExpenseLogger
from fintracklib.budgeter import BudgetManager
from fintracklib.categorizer import Categorizer
from fintracklib.reporter import Reporter
from fintracklib.analytics import Analytics
from fintracklib.utils import (
    format_inr,
    get_fiscal_year,
    format_amount_in_words,
    parse_inr,
    validate_inr_format,
    convert_to_lakhs,
    convert_to_crores,
    paise_to_rupees,
)

__all__ = [
    'Transaction',
    'Budget',
    'ExpenseLogger',
    'BudgetManager',
    'Categorizer',
    'Reporter',
    'Analytics',
    'format_inr',
    'get_fiscal_year',
    'format_amount_in_words',
    'parse_inr',
    'validate_inr_format',
    'convert_to_lakhs',
    'convert_to_crores',
    'paise_to_rupees',
]

