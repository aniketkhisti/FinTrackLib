"""Tests for budget manager."""
import pytest
from fintracklib.budgeter import BudgetManager


def test_create_budget():
    """Test creating a budget with Indian example."""
    manager = BudgetManager()
    budget = manager.create_budget("Festivals", 10000.0, period="monthly")
    
    assert budget.category == "Festivals"
    assert budget.amount == 10000.0
    assert budget.period == "monthly"


def test_get_budget():
    """Test retrieving a budget."""
    manager = BudgetManager()
    manager.create_budget("Groceries", 5000.0)
    
    budget = manager.get_budget("Groceries")
    assert budget is not None
    assert budget.category == "Groceries"


def test_get_nonexistent_budget():
    """Test getting budget that doesn't exist."""
    manager = BudgetManager()
    budget = manager.get_budget("NonExistent")
    assert budget is None


def test_duplicate_budget_rejected():
    """Test that duplicate budgets are rejected."""
    manager = BudgetManager()
    manager.create_budget("Transport", 2000.0)
    
    with pytest.raises(ValueError, match="Budget already exists"):
        manager.create_budget("Transport", 3000.0)


def test_record_expense():
    """Test recording expense against budget."""
    manager = BudgetManager()
    manager.create_budget("Street Food", 1000.0)
    manager.record_expense("Street Food", 250.0)
    
    budget = manager.get_budget("Street Food")
    assert budget.spent == 250.0


def test_record_expense_no_budget():
    """Test recording expense for non-existent budget."""
    manager = BudgetManager()
    # Should not raise error, just silently ignore
    manager.record_expense("NonExistent", 100.0)


def test_get_all_budgets():
    """Test getting all budgets."""
    manager = BudgetManager()
    manager.create_budget("Groceries", 5000.0)
    manager.create_budget("Transport", 2000.0)
    manager.create_budget("Festivals", 10000.0)
    
    budgets = manager.get_all_budgets()
    assert len(budgets) == 3
    categories = [b.category for b in budgets]
    assert "Groceries" in categories
    assert "Transport" in categories
    assert "Festivals" in categories


def test_multiple_expenses_same_budget():
    """Test recording multiple expenses against same budget."""
    manager = BudgetManager()
    manager.create_budget("Entertainment", 3000.0)
    manager.record_expense("Entertainment", 500.0)
    manager.record_expense("Entertainment", 800.0)
    manager.record_expense("Entertainment", 400.0)
    
    budget = manager.get_budget("Entertainment")
    assert budget.spent == 1700.0
    assert budget.remaining() == 1300.0

