"""Tests for utility functions."""
import pytest
from fintracklib.utils import (
    format_inr,
    parse_inr,
    validate_inr_format,
    convert_to_lakhs,
    convert_to_crores,
    paise_to_rupees,
)


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


# Tests for parse_inr
def test_parse_inr_basic():
    """Test basic INR parsing."""
    assert parse_inr("₹100.00") == 100.0
    assert parse_inr("₹1,000.00") == 1000.0


def test_parse_inr_lakhs():
    """Test parsing lakhs format."""
    assert parse_inr("₹1,00,000.00") == 100000.0
    assert parse_inr("₹5,50,000") == 550000.0


def test_parse_inr_crores():
    """Test parsing crores format."""
    assert parse_inr("₹1,00,00,000.00") == 10000000.0
    assert parse_inr("₹2,50,00,000") == 25000000.0


def test_parse_inr_without_decimals():
    """Test parsing amounts without decimal places."""
    assert parse_inr("₹100") == 100.0
    assert parse_inr("₹1,000") == 1000.0


def test_parse_inr_with_spaces():
    """Test parsing with extra whitespace."""
    assert parse_inr("  ₹1,00,000.00  ") == 100000.0
    assert parse_inr("₹ 50,000") == 50000.0


def test_parse_inr_invalid():
    """Test parsing invalid INR strings."""
    with pytest.raises(ValueError):
        parse_inr("invalid")
    
    with pytest.raises(ValueError):
        parse_inr("")
    
    with pytest.raises(ValueError):
        parse_inr("₹abc")


# Tests for validate_inr_format
def test_validate_inr_format_valid():
    """Test validation of valid INR formats."""
    assert validate_inr_format("₹100.00") == True
    assert validate_inr_format("₹1,000.00") == True
    assert validate_inr_format("₹1,00,000.00") == True
    assert validate_inr_format("₹50,000") == True


def test_validate_inr_format_invalid():
    """Test validation of invalid INR formats."""
    assert validate_inr_format("100.00") == False  # Missing rupee symbol
    assert validate_inr_format("$100") == False  # Wrong currency symbol
    assert validate_inr_format("") == False  # Empty string
    assert validate_inr_format("₹abc") == False  # Non-numeric


def test_validate_inr_format_edge_cases():
    """Test validation edge cases."""
    assert validate_inr_format("₹0") == True
    assert validate_inr_format("₹999") == True
    assert validate_inr_format("₹-100.00") == True  # Negative amounts


# Tests for convert_to_lakhs
def test_convert_to_lakhs():
    """Test conversion to lakhs."""
    assert convert_to_lakhs(100000) == 1.0
    assert convert_to_lakhs(250000) == 2.5
    assert convert_to_lakhs(1000000) == 10.0
    assert convert_to_lakhs(50000) == 0.5


# Tests for convert_to_crores
def test_convert_to_crores():
    """Test conversion to crores."""
    assert convert_to_crores(10000000) == 1.0
    assert convert_to_crores(5000000) == 0.5
    assert convert_to_crores(25000000) == 2.5
    assert convert_to_crores(100000000) == 10.0


# Tests for paise_to_rupees
def test_paise_to_rupees():
    """Test conversion from paise to rupees."""
    assert paise_to_rupees(100) == 1.0
    assert paise_to_rupees(250) == 2.5
    assert paise_to_rupees(50) == 0.5
    assert paise_to_rupees(1000) == 10.0


# Integration tests
def test_parse_and_format_roundtrip():
    """Test that parse and format are inverses."""
    original = 125000.0
    formatted = format_inr(original)
    parsed = parse_inr(formatted)
    assert parsed == original


def test_conversion_consistency():
    """Test conversions are consistent."""
    amount = 1000000  # 10 lakhs
    lakhs = convert_to_lakhs(amount)
    crores = convert_to_crores(amount)
    
    assert lakhs == 10.0
    assert crores == 0.1
    assert lakhs == crores * 100  # 1 crore = 100 lakhs

