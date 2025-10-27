"""Tests for utility functions."""
import pytest
from fintracklib.utils import format_inr


def test_format_inr_basic():
    """Test basic INR formatting for small amounts."""
    assert format_inr(100) == "₹100.00"
    assert format_inr(999) == "₹999.00"


def test_format_inr_thousands():
    """Test INR formatting for thousands (first comma)."""
    assert format_inr(1000) == "₹1,000.00"
    assert format_inr(9999) == "₹9,999.00"
    assert format_inr(99999) == "₹99,999.00"


def test_format_inr_lakhs():
    """Test INR formatting for lakhs (1 lakh = 1,00,000)."""
    assert format_inr(100000) == "₹1,00,000.00"
    assert format_inr(500000) == "₹5,00,000.00"
    assert format_inr(999999) == "₹9,99,999.00"


def test_format_inr_ten_lakhs():
    """Test INR formatting for ten lakhs."""
    assert format_inr(1000000) == "₹10,00,000.00"
    assert format_inr(5000000) == "₹50,00,000.00"
    assert format_inr(9999999) == "₹99,99,999.00"


def test_format_inr_crores():
    """Test INR formatting for crores (1 crore = 1,00,00,000)."""
    assert format_inr(10000000) == "₹1,00,00,000.00"
    assert format_inr(50000000) == "₹5,00,00,000.00"


def test_format_inr_ten_crores():
    """Test INR formatting for ten crores and above."""
    assert format_inr(100000000) == "₹10,00,00,000.00"
    assert format_inr(1000000000) == "₹1,00,00,00,000.00"


def test_format_inr_decimals():
    """Test INR formatting with decimal amounts."""
    assert format_inr(1234.56) == "₹1,234.56"
    assert format_inr(123456.78) == "₹1,23,456.78"
    assert format_inr(12345678.90) == "₹1,23,45,678.90"


def test_format_inr_zero():
    """Test INR formatting for zero."""
    assert format_inr(0) == "₹0.00"
    assert format_inr(0.0) == "₹0.00"


def test_format_inr_small_decimals():
    """Test INR formatting for amounts less than 1."""
    assert format_inr(0.50) == "₹0.50"
    assert format_inr(0.99) == "₹0.99"


def test_format_inr_negative():
    """Test INR formatting for negative amounts."""
    assert format_inr(-100) == "-₹100.00"
    assert format_inr(-1000) == "-₹1,000.00"
    assert format_inr(-100000) == "-₹1,00,000.00"


def test_format_inr_realistic_expenses():
    """Test INR formatting with realistic Indian expense amounts."""
    # Chai
    assert format_inr(20) == "₹20.00"
    # Samosa
    assert format_inr(15) == "₹15.00"
    # Biryani
    assert format_inr(180) == "₹180.00"
    # Auto fare
    assert format_inr(150) == "₹150.00"
    # Groceries budget
    assert format_inr(5000) == "₹5,000.00"
    # Diwali budget
    assert format_inr(10000) == "₹10,000.00"

