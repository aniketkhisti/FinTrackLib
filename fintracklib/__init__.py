"""
FinTrackLib - Personal Finance Tracking for Indian Users

A comprehensive expense tracking library with INR support,
Indian categories, and budget management.
"""

__version__ = "0.8.0"

from fintracklib.models import Transaction, Budget, RecurringExpense, SavingsGoal
from fintracklib.logger import ExpenseLogger
from fintracklib.budgeter import BudgetManager
from fintracklib.categorizer import Categorizer
from fintracklib.reporter import Reporter
from fintracklib.analytics import Analytics
from fintracklib.exporter import TransactionExporter, BudgetExporter
from fintracklib.recurring import RecurringExpenseManager
from fintracklib.savings import SavingsGoalManager
from fintracklib.tax import TaxCalculator
from fintracklib.filter import TransactionFilter, filter_transactions
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
    'RecurringExpense',
    'SavingsGoal',
    'ExpenseLogger',
    'BudgetManager',
    'Categorizer',
    'Reporter',
    'Analytics',
    'TransactionExporter',
    'BudgetExporter',
    'RecurringExpenseManager',
    'SavingsGoalManager',
    'TaxCalculator',
    'TransactionFilter',
    'filter_transactions',
    'format_inr',
    'get_fiscal_year',
    'format_amount_in_words',
    'parse_inr',
    'validate_inr_format',
    'convert_to_lakhs',
    'convert_to_crores',
    'paise_to_rupees',
]

