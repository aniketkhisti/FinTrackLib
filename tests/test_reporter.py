"""Tests for report generation."""
import pytest
from datetime import datetime
from fintracklib.models import Transaction, Budget
from fintracklib.reporter import Reporter


@pytest.fixture
def reporter():
    """Create a Reporter instance."""
    return Reporter()


@pytest.fixture
def sample_transactions():
    """Create sample transactions for testing."""
    return [
        Transaction(amount=20.0, description="Chai", category="Street Food", 
                   date=datetime(2024, 10, 15)),
        Transaction(amount=15.0, description="Samosa", category="Street Food",
                   date=datetime(2024, 10, 15)),
        Transaction(amount=150.0, description="Auto fare", category="Transport",
                   date=datetime(2024, 10, 16)),
        Transaction(amount=5000.0, description="Groceries", category="Groceries",
                   date=datetime(2024, 10, 20)),
    ]


@pytest.fixture
def sample_budgets():
    """Create sample budgets for testing."""
    budget1 = Budget(category="Street Food", amount=1000.0, period="monthly")
    budget1.spent = 500.0
    
    budget2 = Budget(category="Transport", amount=2000.0, period="monthly")
    budget2.spent = 2500.0  # Exceeded
    
    return [budget1, budget2]


def test_expense_summary_basic(reporter, sample_transactions):
    """Test basic expense summary generation."""
    report = reporter.expense_summary(sample_transactions)
    
    assert "EXPENSE SUMMARY" in report
    assert "Street Food:" in report
    assert "Chai: ₹20.00" in report
    assert "Samosa: ₹15.00" in report
    assert "Transport:" in report
    assert "Auto fare: ₹150.00" in report
    assert "Groceries:" in report
    assert "Total Expenses: ₹5,185.00" in report


def test_expense_summary_empty(reporter):
    """Test expense summary with no transactions."""
    report = reporter.expense_summary([])
    assert report == "No transactions to report."


def test_expense_summary_with_gst(reporter, sample_transactions):
    """Test expense summary with GST calculation."""
    report = reporter.expense_summary(sample_transactions, include_gst=True)
    
    assert "Total Expenses: ₹5,185.00" in report
    assert "GST (18%)" in report
    assert "Total with GST:" in report
    # 5185 * 1.18 = 6118.30
    assert "₹6,118.30" in report


def test_expense_summary_categorization(reporter):
    """Test that expenses are properly grouped by category."""
    transactions = [
        Transaction(amount=100.0, description="Item 1", category="Shopping"),
        Transaction(amount=200.0, description="Item 2", category="Shopping"),
        Transaction(amount=50.0, description="Item 3", category="Food"),
    ]
    
    report = reporter.expense_summary(transactions)
    
    assert "Shopping:" in report
    assert "Subtotal: ₹300.00" in report
    assert "Food:" in report
    assert "Subtotal: ₹50.00" in report
    assert "Total Expenses: ₹350.00" in report


def test_expense_summary_uncategorized(reporter):
    """Test that uncategorized expenses are properly labeled."""
    transactions = [
        Transaction(amount=100.0, description="Mystery expense"),
    ]
    
    report = reporter.expense_summary(transactions)
    assert "Uncategorized:" in report


def test_budget_report_basic(reporter, sample_budgets):
    """Test basic budget report generation."""
    report = reporter.budget_report(sample_budgets)
    
    assert "BUDGET REPORT" in report
    assert "Category: Street Food" in report
    assert "Allocated: ₹1,000.00" in report
    assert "Spent: ₹500.00" in report
    assert "Remaining: ₹500.00" in report
    assert "Utilization: 50.0%" in report


def test_budget_report_exceeded(reporter, sample_budgets):
    """Test budget report shows exceeded budgets."""
    report = reporter.budget_report(sample_budgets)
    
    assert "Category: Transport" in report
    assert "Allocated: ₹2,000.00" in report
    assert "Spent: ₹2,500.00" in report
    assert "Remaining: -₹500.00" in report  # Negative remaining
    assert "BUDGET EXCEEDED" in report


def test_budget_report_empty(reporter):
    """Test budget report with no budgets."""
    report = reporter.budget_report([])
    assert report == "No budgets to report."


def test_monthly_report_basic(reporter):
    """Test monthly report for specific month."""
    transactions = [
        Transaction(amount=100.0, description="Oct expense", 
                   category="Shopping", date=datetime(2024, 10, 15)),
        Transaction(amount=200.0, description="Oct expense 2", 
                   category="Shopping", date=datetime(2024, 10, 20)),
        Transaction(amount=50.0, description="Nov expense", 
                   category="Shopping", date=datetime(2024, 11, 5)),
    ]
    
    report = reporter.monthly_report(transactions, 2024, 10)
    
    assert "MONTHLY REPORT - October 2024" in report
    assert "Oct expense: ₹100.00" in report
    assert "Oct expense 2: ₹200.00" in report
    assert "Nov expense" not in report  # Should not include November
    assert "Total Expenses: ₹300.00" in report


def test_monthly_report_no_transactions(reporter):
    """Test monthly report when no transactions exist for month."""
    transactions = [
        Transaction(amount=100.0, description="Oct expense", 
                   date=datetime(2024, 10, 15)),
    ]
    
    report = reporter.monthly_report(transactions, 2024, 11)
    assert "No transactions found for 11/2024" in report


def test_monthly_report_different_months(reporter):
    """Test monthly reports for different months."""
    transactions = [
        Transaction(amount=1000.0, description="Diwali shopping", 
                   category="Festivals", date=datetime(2024, 10, 25)),
        Transaction(amount=2000.0, description="Holi colors", 
                   category="Festivals", date=datetime(2025, 3, 15)),
    ]
    
    oct_report = reporter.monthly_report(transactions, 2024, 10)
    assert "October 2024" in oct_report
    assert "Diwali" in oct_report
    assert "Holi" not in oct_report
    
    mar_report = reporter.monthly_report(transactions, 2025, 3)
    assert "March 2025" in mar_report
    assert "Holi" in mar_report
    assert "Diwali" not in mar_report

