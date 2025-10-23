"""Tests for data models."""
import pytest
from datetime import datetime
from fintracklib.models import Transaction, Budget


def test_transaction_creation():
    """Test basic transaction creation with Indian example."""
    txn = Transaction(amount=20.0, description="Chai")
    assert txn.amount == 20.0
    assert txn.description == "Chai"
    assert txn.id is None
    assert isinstance(txn.date, datetime)


def test_transaction_negative_amount():
    """Test that negative amounts are rejected."""
    with pytest.raises(ValueError, match="Amount cannot be negative"):
        Transaction(amount=-50.0, description="Invalid")


def test_transaction_to_dict():
    """Test transaction serialization."""
    txn = Transaction(amount=150.0, description="Auto Rickshaw fare", id=1)
    data = txn.to_dict()
    assert data['id'] == 1
    assert data['amount'] == 150.0
    assert data['description'] == "Auto Rickshaw fare"
    assert 'date' in data


def test_transaction_custom_date():
    """Test transaction with custom date."""
    custom_date = datetime(2024, 10, 15, 10, 30)
    txn = Transaction(amount=15.0, description="Samosa", date=custom_date)
    assert txn.date == custom_date


def test_transaction_zero_amount():
    """Test that zero amounts are allowed."""
    txn = Transaction(amount=0.0, description="Free sample")
    assert txn.amount == 0.0


# Budget tests

def test_budget_creation():
    """Test basic budget creation with Indian example."""
    budget = Budget(category="Festivals", amount=10000.0, period="monthly")
    assert budget.category == "Festivals"
    assert budget.amount == 10000.0
    assert budget.period == "monthly"
    assert budget.spent == 0.0


def test_budget_remaining():
    """Test remaining budget calculation."""
    budget = Budget(category="Groceries", amount=5000.0)
    budget.add_expense(2000.0)
    assert budget.remaining() == 3000.0


def test_budget_exceeded():
    """Test budget exceeded detection."""
    budget = Budget(category="Transport", amount=1000.0)
    budget.add_expense(1500.0)
    assert budget.is_exceeded() is True


def test_budget_not_exceeded():
    """Test budget not exceeded when within limit."""
    budget = Budget(category="Healthcare", amount=5000.0)
    budget.add_expense(3000.0)
    assert budget.is_exceeded() is False


def test_budget_utilization():
    """Test utilization percentage calculation."""
    budget = Budget(category="Street Food", amount=500.0)
    budget.add_expense(250.0)
    assert budget.utilization_percentage() == 50.0


def test_budget_invalid_amount():
    """Test that negative budgets are rejected."""
    with pytest.raises(ValueError, match="Budget amount must be positive"):
        Budget(category="Invalid", amount=-100.0)


def test_budget_invalid_period():
    """Test that invalid periods are rejected."""
    with pytest.raises(ValueError, match="Invalid period"):
        Budget(category="Test", amount=1000.0, period="daily")


def test_budget_multiple_expenses():
    """Test adding multiple expenses to a budget."""
    budget = Budget(category="Entertainment", amount=3000.0)
    budget.add_expense(500.0)
    budget.add_expense(800.0)
    budget.add_expense(600.0)
    assert budget.spent == 1900.0
    assert budget.remaining() == 1100.0

