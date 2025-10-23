"""Tests for expense logger."""
import pytest
from datetime import datetime
from fintracklib.logger import ExpenseLogger


def test_log_expense():
    """Test logging an expense with Indian example."""
    logger = ExpenseLogger()
    txn = logger.log_expense(20.0, "Chai")
    
    assert txn.amount == 20.0
    assert txn.description == "Chai"
    assert txn.id == 1


def test_unique_ids():
    """Test that each transaction gets a unique ID."""
    logger = ExpenseLogger()
    txn1 = logger.log_expense(20.0, "Chai")
    txn2 = logger.log_expense(150.0, "Auto Rickshaw fare")
    txn3 = logger.log_expense(15.0, "Samosa")
    
    assert txn1.id == 1
    assert txn2.id == 2
    assert txn3.id == 3


def test_get_all_transactions():
    """Test retrieving all transactions."""
    logger = ExpenseLogger()
    logger.log_expense(20.0, "Chai")
    logger.log_expense(180.0, "Biryani")
    
    transactions = logger.get_all_transactions()
    assert len(transactions) == 2
    assert transactions[0].description == "Chai"
    assert transactions[1].description == "Biryani"


def test_total_expenses():
    """Test calculating total expenses."""
    logger = ExpenseLogger()
    logger.log_expense(20.0, "Chai")
    logger.log_expense(150.0, "Auto fare")
    logger.log_expense(15.0, "Samosa")
    
    total = logger.total_expenses()
    assert total == 185.0


def test_negative_amount_rejected():
    """Test that negative amounts are rejected."""
    logger = ExpenseLogger()
    with pytest.raises(ValueError):
        logger.log_expense(-50.0, "Invalid")


def test_custom_date():
    """Test logging with custom date."""
    logger = ExpenseLogger()
    custom_date = datetime(2024, 10, 15)
    txn = logger.log_expense(100.0, "Groceries", date=custom_date)
    assert txn.date == custom_date


def test_empty_logger():
    """Test empty logger total."""
    logger = ExpenseLogger()
    assert logger.total_expenses() == 0.0
    assert len(logger.get_all_transactions()) == 0

