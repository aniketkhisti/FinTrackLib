"""Tests for analytics and insights."""
import pytest
from datetime import datetime, timedelta
from fintracklib.models import Transaction
from fintracklib.analytics import Analytics
from fintracklib.utils import get_fiscal_year, format_amount_in_words


@pytest.fixture
def sample_transactions():
    """Create sample transactions for testing."""
    # Use recent dates to ensure they're within the analysis window
    now = datetime.now()
    return [
        Transaction(amount=5000.0, description="Diwali lights", category="Festivals",
                   date=now - timedelta(days=5)),
        Transaction(amount=3000.0, description="Diwali sweets", category="Festivals",
                   date=now - timedelta(days=4)),
        Transaction(amount=150.0, description="Auto fare", category="Transport",
                   date=now - timedelta(days=2)),
        Transaction(amount=20.0, description="Chai", category="Street Food",
                   date=now - timedelta(days=1)),
        Transaction(amount=1000.0, description="Groceries", category="Groceries",
                   date=now),
    ]


def test_analytics_initialization(sample_transactions):
    """Test Analytics class initialization."""
    analytics = Analytics(sample_transactions)
    assert len(analytics.transactions) == 5


def test_average_daily_spending(sample_transactions):
    """Test average daily spending calculation."""
    analytics = Analytics(sample_transactions)
    # All transactions are within last 30 days
    avg = analytics.average_daily_spending(days=30)
    total = 5000 + 3000 + 150 + 20 + 1000  # 9170
    expected = 9170 / 30
    assert avg == expected


def test_average_daily_spending_no_recent_transactions():
    """Test average daily spending with no recent transactions."""
    old_txn = [
        Transaction(amount=100.0, description="Old expense", 
                   date=datetime(2020, 1, 1))
    ]
    analytics = Analytics(old_txn)
    assert analytics.average_daily_spending(days=30) == 0.0


def test_spending_by_category(sample_transactions):
    """Test spending breakdown by category."""
    analytics = Analytics(sample_transactions)
    by_category = analytics.spending_by_category()
    
    assert by_category['Festivals'] == 8000.0  # 5000 + 3000
    assert by_category['Transport'] == 150.0
    assert by_category['Street Food'] == 20.0
    assert by_category['Groceries'] == 1000.0


def test_spending_by_category_with_uncategorized():
    """Test spending breakdown with uncategorized transactions."""
    transactions = [
        Transaction(amount=100.0, description="Item 1", category="Shopping"),
        Transaction(amount=50.0, description="Item 2"),  # No category
    ]
    analytics = Analytics(transactions)
    by_category = analytics.spending_by_category()
    
    assert by_category['Shopping'] == 100.0
    assert by_category['Uncategorized'] == 50.0


def test_festival_spending_analysis(sample_transactions):
    """Test festival spending analysis."""
    analytics = Analytics(sample_transactions)
    festival_stats = analytics.festival_spending_analysis("Festivals")
    
    assert festival_stats['total'] == 8000.0
    assert festival_stats['count'] == 2
    assert festival_stats['average'] == 4000.0
    assert "₹8,000.00" in festival_stats['formatted_total']
    assert len(festival_stats['transactions']) == 2


def test_festival_spending_no_festivals():
    """Test festival spending with no festival transactions."""
    transactions = [
        Transaction(amount=100.0, description="Groceries", category="Groceries"),
    ]
    analytics = Analytics(transactions)
    festival_stats = analytics.festival_spending_analysis("Festivals")
    
    assert festival_stats['total'] == 0.0
    assert festival_stats['count'] == 0
    assert festival_stats['average'] == 0.0
    assert len(festival_stats['transactions']) == 0


def test_get_insights(sample_transactions):
    """Test insights generation."""
    analytics = Analytics(sample_transactions)
    insights = analytics.get_insights()
    
    assert len(insights) >= 3
    assert "Total spending: ₹9,170.00" in insights[0]
    assert "Average transaction:" in insights[1]
    assert "Highest spending category: Festivals" in insights[2]


def test_get_insights_no_transactions():
    """Test insights with no transactions."""
    analytics = Analytics([])
    insights = analytics.get_insights()
    
    assert len(insights) == 1
    assert "No transaction data available" in insights[0]


def test_get_fiscal_year_april_onwards():
    """Test fiscal year calculation for April onwards."""
    date = datetime(2024, 10, 15)
    fy = get_fiscal_year(date)
    assert fy == "FY2024-25"


def test_get_fiscal_year_jan_march():
    """Test fiscal year calculation for Jan-March."""
    date = datetime(2025, 2, 10)
    fy = get_fiscal_year(date)
    assert fy == "FY2024-25"


def test_format_amount_in_words_small():
    """Test amount formatting for small amounts."""
    assert format_amount_in_words(500) == "₹500"
    assert format_amount_in_words(999) == "₹999"


def test_format_amount_in_words_thousands():
    """Test amount formatting for thousands."""
    assert format_amount_in_words(25000) == "₹25.0K"
    assert format_amount_in_words(50000) == "₹50.0K"


def test_format_amount_in_words_lakhs():
    """Test amount formatting for lakhs."""
    assert format_amount_in_words(250000) == "₹2.5 lakhs"
    assert format_amount_in_words(1000000) == "₹10.0 lakhs"


def test_format_amount_in_words_crores():
    """Test amount formatting for crores."""
    assert format_amount_in_words(50000000) == "₹5.0 crores"
    assert format_amount_in_words(100000000) == "₹10.0 crores"

