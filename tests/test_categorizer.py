"""Tests for expense categorizer."""
import pytest
from fintracklib.models import Transaction
from fintracklib.categorizer import Categorizer
from fintracklib.config import DEFAULT_CATEGORIES


def test_categorizer_initialization():
    """Test categorizer initializes with default categories."""
    categorizer = Categorizer()
    assert len(categorizer.valid_categories) == 10
    assert "Groceries" in categorizer.valid_categories
    assert "Street Food" in categorizer.valid_categories


def test_categorizer_custom_categories():
    """Test categorizer with custom categories."""
    custom = ["Food", "Travel", "Bills"]
    categorizer = Categorizer(valid_categories=custom)
    assert categorizer.valid_categories == custom


def test_is_valid_category():
    """Test category validation."""
    categorizer = Categorizer()
    assert categorizer.is_valid_category("Groceries") is True
    assert categorizer.is_valid_category("Transport") is True
    assert categorizer.is_valid_category("Invalid") is False


def test_get_valid_categories():
    """Test getting list of valid categories."""
    categorizer = Categorizer()
    categories = categorizer.get_valid_categories()
    assert categories == DEFAULT_CATEGORIES
    # Ensure it returns a copy
    categories.append("New Category")
    assert "New Category" not in categorizer.valid_categories


def test_categorize_transaction_valid():
    """Test manually categorizing a transaction."""
    categorizer = Categorizer()
    txn = Transaction(amount=100.0, description="Weekly shopping")
    
    categorizer.categorize_transaction(txn, "Groceries")
    assert txn.category == "Groceries"


def test_categorize_transaction_invalid():
    """Test that invalid category raises error."""
    categorizer = Categorizer()
    txn = Transaction(amount=100.0, description="Test")
    
    with pytest.raises(ValueError, match="Invalid category"):
        categorizer.categorize_transaction(txn, "InvalidCategory")


def test_auto_categorize_street_food():
    """Test auto-categorization for street food."""
    categorizer = Categorizer()
    
    # Test various street food items
    txn1 = Transaction(amount=20.0, description="Morning chai")
    assert categorizer.auto_categorize(txn1) is True
    assert txn1.category == "Street Food"
    
    txn2 = Transaction(amount=30.0, description="Samosa for evening snack")
    assert categorizer.auto_categorize(txn2) is True
    assert txn2.category == "Street Food"
    
    txn3 = Transaction(amount=200.0, description="Biryani from corner shop")
    assert categorizer.auto_categorize(txn3) is True
    assert txn3.category == "Street Food"


def test_auto_categorize_transport():
    """Test auto-categorization for transport."""
    categorizer = Categorizer()
    
    txn1 = Transaction(amount=50.0, description="Auto Rickshaw fare")
    assert categorizer.auto_categorize(txn1) is True
    assert txn1.category == "Transport"
    
    txn2 = Transaction(amount=200.0, description="Ola cab to airport")
    assert categorizer.auto_categorize(txn2) is True
    assert txn2.category == "Transport"
    
    txn3 = Transaction(amount=100.0, description="Metro card recharge")
    assert categorizer.auto_categorize(txn3) is True
    assert txn3.category == "Transport"


def test_auto_categorize_festivals():
    """Test auto-categorization for festivals."""
    categorizer = Categorizer()
    
    txn1 = Transaction(amount=5000.0, description="Diwali shopping")
    assert categorizer.auto_categorize(txn1) is True
    assert txn1.category == "Festivals"
    
    txn2 = Transaction(amount=500.0, description="Holi colors and pichkari")
    assert categorizer.auto_categorize(txn2) is True
    assert txn2.category == "Festivals"


def test_auto_categorize_groceries():
    """Test auto-categorization for groceries."""
    categorizer = Categorizer()
    
    txn1 = Transaction(amount=500.0, description="Rice and Atta")
    assert categorizer.auto_categorize(txn1) is True
    assert txn1.category == "Groceries"
    
    txn2 = Transaction(amount=200.0, description="Fresh vegetables")
    assert categorizer.auto_categorize(txn2) is True
    assert txn2.category == "Groceries"


def test_auto_categorize_utilities():
    """Test auto-categorization for utilities."""
    categorizer = Categorizer()
    
    txn1 = Transaction(amount=1500.0, description="Electricity bill payment")
    assert categorizer.auto_categorize(txn1) is True
    assert txn1.category == "Utilities"
    
    txn2 = Transaction(amount=800.0, description="Gas cylinder")
    assert categorizer.auto_categorize(txn2) is True
    assert txn2.category == "Utilities"


def test_auto_categorize_no_match():
    """Test auto-categorization when no keywords match."""
    categorizer = Categorizer()
    
    txn = Transaction(amount=1000.0, description="Random expense XYZ")
    assert categorizer.auto_categorize(txn) is False
    assert txn.category is None


def test_auto_categorize_case_insensitive():
    """Test that auto-categorization is case insensitive."""
    categorizer = Categorizer()
    
    txn1 = Transaction(amount=20.0, description="CHAI")
    assert categorizer.auto_categorize(txn1) is True
    assert txn1.category == "Street Food"
    
    txn2 = Transaction(amount=100.0, description="Auto Fare")
    assert categorizer.auto_categorize(txn2) is True
    assert txn2.category == "Transport"


def test_categorize_then_auto_categorize():
    """Test manual categorization followed by auto-categorization."""
    categorizer = Categorizer()
    
    txn = Transaction(amount=50.0, description="chai at cafe")
    categorizer.categorize_transaction(txn, "Entertainment")
    assert txn.category == "Entertainment"
    
    # Auto-categorize should overwrite
    categorizer.auto_categorize(txn)
    assert txn.category == "Street Food"


def test_overwrite_protection():
    """Test that categorizing an already-categorized transaction raises error."""
    categorizer = Categorizer()
    
    txn = Transaction(amount=150.0, description="Auto fare", category="Transport")
    
    # Should raise error when trying to change category without overwrite=True
    with pytest.raises(ValueError, match="already has category"):
        categorizer.categorize_transaction(txn, "Shopping")
    
    # Category should remain unchanged
    assert txn.category == "Transport"


def test_overwrite_allowed_with_flag():
    """Test that overwrite=True allows changing category."""
    categorizer = Categorizer()
    
    txn = Transaction(amount=150.0, description="Auto fare", category="Transport")
    
    # Should work with overwrite=True
    categorizer.categorize_transaction(txn, "Shopping", overwrite=True)
    assert txn.category == "Shopping"

