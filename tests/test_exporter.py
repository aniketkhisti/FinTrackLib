"""Tests for data export functionality."""
import pytest
import json
from datetime import datetime
from fintracklib.models import Transaction, Budget
from fintracklib.exporter import TransactionExporter, BudgetExporter


@pytest.fixture
def sample_transactions():
    """Create sample transactions for testing."""
    return [
        Transaction(amount=2500.0, description="Diwali lights", category="Festivals",
                   date=datetime(2024, 10, 25)),
        Transaction(amount=3000.0, description="Sweets", category="Festivals",
                   date=datetime(2024, 10, 26)),
        Transaction(amount=150.0, description="Auto fare", category="Transport",
                   date=datetime(2024, 10, 28)),
    ]


@pytest.fixture
def sample_budgets():
    """Create sample budgets for testing."""
    budget1 = Budget(category="Groceries", amount=5000.0, period="monthly")
    budget1.spent = 3500.0
    
    budget2 = Budget(category="Transport", amount=2000.0, period="monthly")
    budget2.spent = 1800.0
    
    return [budget1, budget2]


# Transaction CSV Export Tests
def test_transaction_csv_export_basic(sample_transactions):
    """Test basic CSV export of transactions."""
    exporter = TransactionExporter(sample_transactions)
    csv_data = exporter.to_csv()
    
    assert "Date,Description,Amount (₹),Category" in csv_data
    assert "25-10-2024" in csv_data
    assert "Diwali lights" in csv_data
    assert "₹2,500.00" in csv_data
    assert "Festivals" in csv_data


def test_transaction_csv_custom_date_format(sample_transactions):
    """Test CSV export with custom date format."""
    exporter = TransactionExporter(sample_transactions)
    csv_data = exporter.to_csv(date_format="%Y/%m/%d")
    
    assert "2024/10/25" in csv_data
    assert "2024/10/26" in csv_data


def test_transaction_csv_default_date_format_dd_mm_yyyy(sample_transactions):
    """Test CSV export uses DD-MM-YYYY format by default."""
    exporter = TransactionExporter(sample_transactions)
    csv_data = exporter.to_csv()
    
    # Should use DD-MM-YYYY format
    assert "25-10-2024" in csv_data
    assert "26-10-2024" in csv_data
    assert "28-10-2024" in csv_data
    # Should NOT contain ISO format
    assert "2024-10-25" not in csv_data


def test_transaction_csv_readable_headers(sample_transactions):
    """Test CSV export has readable column headers."""
    exporter = TransactionExporter(sample_transactions)
    csv_data = exporter.to_csv()
    
    # Headers should be properly capitalized
    assert "Date,Description,Amount (₹),Category" in csv_data
    # Should not have lowercase headers
    assert "date,description,amount" not in csv_data


def test_transaction_csv_timezone_preservation():
    """Test CSV export preserves date regardless of timezone/time component."""
    from datetime import datetime, timezone, timedelta
    
    # Create transaction with time component
    txn_with_time = Transaction(
        amount=100.0,
        description="Test with time",
        date=datetime(2024, 10, 25, 14, 30, 0)  # 2:30 PM
    )
    
    # Create transaction with timezone
    ist_timezone = timezone(timedelta(hours=5, minutes=30))
    txn_with_tz = Transaction(
        amount=200.0,
        description="Test with timezone",
        date=datetime(2024, 10, 26, 0, 0, 0, tzinfo=ist_timezone)
    )
    
    exporter = TransactionExporter([txn_with_time, txn_with_tz])
    csv_data = exporter.to_csv()
    
    # Dates should be preserved correctly (DD-MM-YYYY format)
    assert "25-10-2024" in csv_data
    assert "26-10-2024" in csv_data
    # Should not include time component
    assert "14:30" not in csv_data


def test_transaction_csv_iso_format_option(sample_transactions):
    """Test CSV export can use ISO format when explicitly requested."""
    exporter = TransactionExporter(sample_transactions)
    csv_data = exporter.to_csv(date_format="%Y-%m-%d")
    
    # Should use ISO format when explicitly requested
    assert "2024-10-25" in csv_data
    assert "2024-10-26" in csv_data


def test_transaction_csv_uncategorized(sample_transactions):
    """Test CSV export handles uncategorized transactions."""
    uncategorized_txn = Transaction(amount=500.0, description="Random expense")
    sample_transactions.append(uncategorized_txn)
    
    exporter = TransactionExporter(sample_transactions)
    csv_data = exporter.to_csv()
    
    assert "Uncategorized" in csv_data


def test_transaction_csv_empty_list():
    """Test CSV export with empty transaction list."""
    exporter = TransactionExporter([])
    csv_data = exporter.to_csv()
    
    # Should still have header
    assert "Date,Description,Amount (₹),Category" in csv_data
    lines = csv_data.strip().split('\n')
    assert len(lines) == 1  # Only header


# Transaction JSON Export Tests
def test_transaction_json_export_basic(sample_transactions):
    """Test basic JSON export of transactions."""
    exporter = TransactionExporter(sample_transactions)
    json_data = exporter.to_json()
    
    data = json.loads(json_data)
    assert 'transactions' in data
    assert len(data['transactions']) == 3
    assert data['transactions'][0]['description'] == 'Diwali lights'
    assert data['transactions'][0]['amount'] == 2500.0


def test_transaction_json_with_metadata(sample_transactions):
    """Test JSON export includes metadata."""
    exporter = TransactionExporter(sample_transactions)
    json_data = exporter.to_json(include_metadata=True)
    
    data = json.loads(json_data)
    assert 'metadata' in data
    assert data['metadata']['total_count'] == 3
    assert data['metadata']['total_amount'] == 5650.0
    assert 'fiscal_year' in data['metadata']
    assert 'export_date' in data['metadata']
    assert '₹' in data['metadata']['formatted_total']


def test_transaction_json_without_metadata(sample_transactions):
    """Test JSON export without metadata."""
    exporter = TransactionExporter(sample_transactions)
    json_data = exporter.to_json(include_metadata=False)
    
    data = json.loads(json_data)
    assert 'metadata' not in data
    assert 'transactions' in data


def test_transaction_json_date_format(sample_transactions):
    """Test JSON uses ISO date format."""
    exporter = TransactionExporter(sample_transactions)
    json_data = exporter.to_json()
    
    data = json.loads(json_data)
    assert data['transactions'][0]['date'] == '2024-10-25'


# Budget Export Tests
def test_budget_json_export_basic(sample_budgets):
    """Test basic budget JSON export."""
    exporter = BudgetExporter(sample_budgets)
    json_data = exporter.to_json()
    
    data = json.loads(json_data)
    assert 'budgets' in data
    assert len(data['budgets']) == 2
    assert data['budgets'][0]['category'] == 'Groceries'
    assert data['budgets'][0]['amount'] == 5000.0


def test_budget_json_includes_calculations(sample_budgets):
    """Test budget export includes calculated fields."""
    exporter = BudgetExporter(sample_budgets)
    json_data = exporter.to_json()
    
    data = json.loads(json_data)
    budget = data['budgets'][0]
    
    assert 'remaining' in budget
    assert 'exceeded' in budget
    assert 'utilization' in budget
    assert budget['remaining'] == 1500.0  # 5000 - 3500
    assert budget['exceeded'] == False
    assert budget['utilization'] == 70.0


def test_budget_json_with_metadata(sample_budgets):
    """Test budget export includes metadata."""
    exporter = BudgetExporter(sample_budgets)
    json_data = exporter.to_json(include_metadata=True)
    
    data = json.loads(json_data)
    assert 'metadata' in data
    assert data['metadata']['budget_count'] == 2
    assert data['metadata']['total_budget'] == 7000.0  # 5000 + 2000
    assert data['metadata']['total_spent'] == 5300.0  # 3500 + 1800
    assert 'formatted_budget' in data['metadata']
    assert 'formatted_spent' in data['metadata']


def test_budget_json_without_metadata(sample_budgets):
    """Test budget export without metadata."""
    exporter = BudgetExporter(sample_budgets)
    json_data = exporter.to_json(include_metadata=False)
    
    data = json.loads(json_data)
    assert 'metadata' not in data
    assert 'budgets' in data


# Edge Cases
def test_export_large_amounts():
    """Test export handles large INR amounts (lakhs/crores)."""
    transactions = [
        Transaction(amount=100000.0, description="Lakh expense"),
        Transaction(amount=10000000.0, description="Crore expense"),
    ]
    exporter = TransactionExporter(transactions)
    csv_data = exporter.to_csv()
    
    assert "₹1,00,000.00" in csv_data
    assert "₹1,00,00,000.00" in csv_data


def test_export_with_special_characters():
    """Test export handles special characters in descriptions."""
    transactions = [
        Transaction(amount=100.0, description="Chai & Samosa"),
        Transaction(amount=200.0, description='Item with "quotes"'),
    ]
    exporter = TransactionExporter(transactions)
    csv_data = exporter.to_csv()
    
    assert "Chai & Samosa" in csv_data


def test_export_unicode_rupee_symbol():
    """Test export properly handles rupee symbol (₹)."""
    transactions = [Transaction(amount=100.0, description="Test")]
    exporter = TransactionExporter(transactions)
    
    csv_data = exporter.to_csv()
    assert "₹" in csv_data
    
    json_data = exporter.to_json()
    assert "₹" in json_data

