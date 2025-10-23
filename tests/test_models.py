"""Tests for data models."""
import pytest
from datetime import datetime
from fintracklib.models import Transaction


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

