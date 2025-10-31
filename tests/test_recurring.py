"""Tests for recurring expense management."""
import pytest
from datetime import datetime, timedelta
from fintracklib.models import RecurringExpense
from fintracklib.recurring import RecurringExpenseManager


@pytest.fixture
def manager():
    """Create a recurring expense manager for testing."""
    return RecurringExpenseManager()


@pytest.fixture
def sample_due_date():
    """Sample due date for testing."""
    return datetime(2024, 11, 1, 10, 0)


def test_recurring_expense_creation():
    """Test creating a recurring expense."""
    due_date = datetime(2024, 11, 1)
    recurring = RecurringExpense(
        amount=15000.0,
        description="Monthly rent",
        frequency="monthly",
        next_due_date=due_date,
        category="Housing"
    )
    
    assert recurring.amount == 15000.0
    assert recurring.description == "Monthly rent"
    assert recurring.frequency == "monthly"
    assert recurring.next_due_date == due_date
    assert recurring.category == "Housing"


def test_recurring_expense_validation():
    """Test validation of recurring expense data."""
    due_date = datetime(2024, 11, 1)
    
    # Negative amount should fail
    with pytest.raises(ValueError, match="Amount must be positive"):
        RecurringExpense(
            amount=-100.0,
            description="Test",
            frequency="monthly",
            next_due_date=due_date
        )
    
    # Invalid frequency should fail
    with pytest.raises(ValueError, match="Frequency must be one of"):
        RecurringExpense(
            amount=100.0,
            description="Test",
            frequency="biweekly",
            next_due_date=due_date
        )


def test_is_due():
    """Test checking if recurring expense is due."""
    due_date = datetime(2024, 10, 25)
    recurring = RecurringExpense(
        amount=800.0,
        description="Electricity bill",
        frequency="monthly",
        next_due_date=due_date
    )
    
    # Before due date
    assert not recurring.is_due(datetime(2024, 10, 20))
    
    # On due date
    assert recurring.is_due(datetime(2024, 10, 25))
    
    # After due date
    assert recurring.is_due(datetime(2024, 10, 30))


def test_calculate_next_due_date_daily():
    """Test calculating next due date for daily frequency."""
    due_date = datetime(2024, 10, 25, 10, 0)
    recurring = RecurringExpense(
        amount=50.0,
        description="Daily expense",
        frequency="daily",
        next_due_date=due_date
    )
    
    next_date = recurring.calculate_next_due_date()
    expected = datetime(2024, 10, 26, 10, 0)
    assert next_date == expected


def test_calculate_next_due_date_weekly():
    """Test calculating next due date for weekly frequency."""
    due_date = datetime(2024, 10, 25, 10, 0)
    recurring = RecurringExpense(
        amount=200.0,
        description="Weekly shopping",
        frequency="weekly",
        next_due_date=due_date
    )
    
    next_date = recurring.calculate_next_due_date()
    expected = datetime(2024, 11, 1, 10, 0)
    assert next_date == expected


def test_calculate_next_due_date_monthly():
    """Test calculating next due date for monthly frequency."""
    due_date = datetime(2024, 10, 15, 10, 0)
    recurring = RecurringExpense(
        amount=15000.0,
        description="Rent",
        frequency="monthly",
        next_due_date=due_date
    )
    
    next_date = recurring.calculate_next_due_date()
    expected = datetime(2024, 11, 15, 10, 0)
    assert next_date == expected


def test_calculate_next_due_date_monthly_edge_case():
    """Test monthly calculation handles months with different days."""
    # Jan 31 -> should become Feb 28 (or 29)
    due_date = datetime(2024, 1, 31, 10, 0)
    recurring = RecurringExpense(
        amount=15000.0,
        description="Rent",
        frequency="monthly",
        next_due_date=due_date
    )
    
    next_date = recurring.calculate_next_due_date()
    # 2024 is a leap year, so Feb has 29 days
    expected = datetime(2024, 2, 29, 10, 0)
    assert next_date == expected


def test_calculate_next_due_date_monthly_31st_non_leap_feb():
    """Test monthly calculation: Jan 31 -> Feb 28 in non-leap year."""
    due_date = datetime(2023, 1, 31, 10, 0)
    recurring = RecurringExpense(
        amount=15000.0,
        description="Rent",
        frequency="monthly",
        next_due_date=due_date
    )
    
    next_date = recurring.calculate_next_due_date()
    # 2023 is not a leap year, so Feb has 28 days
    expected = datetime(2023, 2, 28, 10, 0)
    assert next_date == expected


def test_calculate_next_due_date_monthly_31st_to_30_day_month():
    """Test monthly calculation: Mar 31 -> Apr 30."""
    due_date = datetime(2024, 3, 31, 10, 0)
    recurring = RecurringExpense(
        amount=15000.0,
        description="Rent",
        frequency="monthly",
        next_due_date=due_date
    )
    
    next_date = recurring.calculate_next_due_date()
    # April has 30 days
    expected = datetime(2024, 4, 30, 10, 0)
    assert next_date == expected


def test_calculate_next_due_date_monthly_31st_to_nov():
    """Test monthly calculation: Oct 31 -> Nov 30."""
    due_date = datetime(2024, 10, 31, 10, 0)
    recurring = RecurringExpense(
        amount=15000.0,
        description="Rent",
        frequency="monthly",
        next_due_date=due_date
    )
    
    next_date = recurring.calculate_next_due_date()
    # November has 30 days
    expected = datetime(2024, 11, 30, 10, 0)
    assert next_date == expected


def test_calculate_next_due_date_monthly_30th_to_feb():
    """Test monthly calculation: Jan 30 -> Feb 28/29."""
    # Test with non-leap year
    due_date = datetime(2023, 1, 30, 10, 0)
    recurring = RecurringExpense(
        amount=15000.0,
        description="Rent",
        frequency="monthly",
        next_due_date=due_date
    )
    
    next_date = recurring.calculate_next_due_date()
    # Feb 30 doesn't exist, should use Feb 28 (non-leap year)
    expected = datetime(2023, 2, 28, 10, 0)
    assert next_date == expected


def test_calculate_next_due_date_monthly_29th_to_feb():
    """Test monthly calculation: Jan 29 -> Feb 29 (leap year) or Feb 28 (non-leap)."""
    # Test with leap year
    due_date = datetime(2024, 1, 29, 10, 0)
    recurring = RecurringExpense(
        amount=15000.0,
        description="Rent",
        frequency="monthly",
        next_due_date=due_date
    )
    
    next_date = recurring.calculate_next_due_date()
    # 2024 is a leap year, so Feb has 29 days
    expected = datetime(2024, 2, 29, 10, 0)
    assert next_date == expected
    
    # Test with non-leap year
    recurring.next_due_date = datetime(2023, 1, 29, 10, 0)
    next_date = recurring.calculate_next_due_date()
    # 2023 is not a leap year, so Feb has 28 days
    expected = datetime(2023, 2, 28, 10, 0)
    assert next_date == expected


def test_calculate_next_due_date_monthly_31st_all_edge_months():
    """Test monthly calculation for all months that don't have 31 days."""
    # May 31 -> Jun 30
    due_date = datetime(2024, 5, 31, 10, 0)
    recurring = RecurringExpense(
        amount=15000.0,
        description="Rent",
        frequency="monthly",
        next_due_date=due_date
    )
    assert recurring.calculate_next_due_date() == datetime(2024, 6, 30, 10, 0)
    
    # Aug 31 -> Sep 30
    recurring.next_due_date = datetime(2024, 8, 31, 10, 0)
    assert recurring.calculate_next_due_date() == datetime(2024, 9, 30, 10, 0)
    
    # Dec 31 -> Jan 31 (year rollover)
    recurring.next_due_date = datetime(2024, 12, 31, 10, 0)
    assert recurring.calculate_next_due_date() == datetime(2025, 1, 31, 10, 0)


def test_calculate_next_due_date_yearly():
    """Test calculating next due date for yearly frequency."""
    due_date = datetime(2024, 10, 25, 10, 0)
    recurring = RecurringExpense(
        amount=5000.0,
        description="Annual subscription",
        frequency="yearly",
        next_due_date=due_date
    )
    
    next_date = recurring.calculate_next_due_date()
    expected = datetime(2025, 10, 25, 10, 0)
    assert next_date == expected


def test_calculate_next_due_date_leap_year():
    """Test yearly calculation handles leap year (Feb 29)."""
    # Feb 29, 2024 (leap year) -> Feb 28, 2025 (non-leap)
    due_date = datetime(2024, 2, 29, 10, 0)
    recurring = RecurringExpense(
        amount=1000.0,
        description="Anniversary",
        frequency="yearly",
        next_due_date=due_date
    )
    
    next_date = recurring.calculate_next_due_date()
    expected = datetime(2025, 2, 28, 10, 0)
    assert next_date == expected


def test_add_recurring_expense(manager, sample_due_date):
    """Test adding a recurring expense."""
    recurring = manager.add_recurring_expense(
        amount=15000.0,
        description="Monthly rent",
        frequency="monthly",
        next_due_date=sample_due_date,
        category="Housing"
    )
    
    assert recurring.id == 1
    assert recurring.amount == 15000.0
    assert len(manager.list_all_recurring()) == 1


def test_add_multiple_recurring_expenses(manager, sample_due_date):
    """Test adding multiple recurring expenses with unique IDs."""
    rent = manager.add_recurring_expense(
        amount=15000.0,
        description="Rent",
        frequency="monthly",
        next_due_date=sample_due_date
    )
    
    electricity = manager.add_recurring_expense(
        amount=800.0,
        description="Electricity",
        frequency="monthly",
        next_due_date=sample_due_date
    )
    
    mobile = manager.add_recurring_expense(
        amount=500.0,
        description="Mobile recharge",
        frequency="monthly",
        next_due_date=sample_due_date
    )
    
    assert rent.id == 1
    assert electricity.id == 2
    assert mobile.id == 3
    assert len(manager.list_all_recurring()) == 3


def test_get_due_expenses(manager):
    """Test getting expenses that are due."""
    # Add past due expense
    past_due = datetime(2024, 10, 20)
    manager.add_recurring_expense(
        amount=15000.0,
        description="Rent",
        frequency="monthly",
        next_due_date=past_due
    )
    
    # Add future expense
    future_due = datetime(2024, 11, 10)
    manager.add_recurring_expense(
        amount=800.0,
        description="Electricity",
        frequency="monthly",
        next_due_date=future_due
    )
    
    # Check what's due on Oct 25
    check_date = datetime(2024, 10, 25)
    due_expenses = manager.get_due_expenses(check_date)
    
    assert len(due_expenses) == 1
    assert due_expenses[0].description == "Rent"


def test_generate_transaction(manager, sample_due_date):
    """Test generating a transaction from recurring expense."""
    recurring = manager.add_recurring_expense(
        amount=800.0,
        description="Electricity bill",
        frequency="monthly",
        next_due_date=sample_due_date,
        category="Utilities"
    )
    
    transaction = manager.generate_transaction(recurring.id)
    
    assert transaction.amount == 800.0
    assert transaction.description == "Electricity bill"
    assert transaction.date == sample_due_date
    assert transaction.category == "Utilities"


def test_generate_transaction_not_found(manager):
    """Test generating transaction for non-existent recurring expense."""
    with pytest.raises(ValueError, match="not found"):
        manager.generate_transaction(999)


def test_mark_as_paid(manager):
    """Test marking a recurring expense as paid."""
    due_date = datetime(2024, 10, 1, 10, 0)
    recurring = manager.add_recurring_expense(
        amount=15000.0,
        description="Rent",
        frequency="monthly",
        next_due_date=due_date
    )
    
    original_due = recurring.next_due_date
    manager.mark_as_paid(recurring.id)
    
    # Due date should be updated to next month
    assert recurring.next_due_date > original_due
    expected_next = datetime(2024, 11, 1, 10, 0)
    assert recurring.next_due_date == expected_next


def test_mark_as_paid_not_found(manager):
    """Test marking non-existent recurring expense as paid."""
    with pytest.raises(ValueError, match="not found"):
        manager.mark_as_paid(999)


def test_get_recurring_expense(manager, sample_due_date):
    """Test getting a recurring expense by ID."""
    recurring = manager.add_recurring_expense(
        amount=500.0,
        description="Mobile recharge",
        frequency="monthly",
        next_due_date=sample_due_date
    )
    
    found = manager.get_recurring_expense(recurring.id)
    assert found == recurring
    
    not_found = manager.get_recurring_expense(999)
    assert not_found is None


def test_list_all_recurring(manager, sample_due_date):
    """Test listing all recurring expenses."""
    manager.add_recurring_expense(
        amount=15000.0,
        description="Rent",
        frequency="monthly",
        next_due_date=sample_due_date
    )
    
    manager.add_recurring_expense(
        amount=800.0,
        description="Electricity",
        frequency="monthly",
        next_due_date=sample_due_date
    )
    
    all_recurring = manager.list_all_recurring()
    assert len(all_recurring) == 2
    
    # Should return a copy
    all_recurring.clear()
    assert len(manager.list_all_recurring()) == 2


def test_remove_recurring_expense(manager, sample_due_date):
    """Test removing a recurring expense."""
    recurring = manager.add_recurring_expense(
        amount=500.0,
        description="Old subscription",
        frequency="monthly",
        next_due_date=sample_due_date
    )
    
    assert len(manager.list_all_recurring()) == 1
    
    manager.remove_recurring_expense(recurring.id)
    assert len(manager.list_all_recurring()) == 0


def test_remove_recurring_expense_not_found(manager):
    """Test removing non-existent recurring expense."""
    with pytest.raises(ValueError, match="not found"):
        manager.remove_recurring_expense(999)


def test_indian_recurring_examples(manager):
    """Test common Indian recurring expenses."""
    # Add typical Indian recurring expenses
    rent_date = datetime(2024, 11, 1)
    manager.add_recurring_expense(
        amount=18000.0,
        description="Flat rent",
        frequency="monthly",
        next_due_date=rent_date,
        category="Housing"
    )
    
    electricity_date = datetime(2024, 11, 5)
    manager.add_recurring_expense(
        amount=950.0,
        description="Electricity bill (MSEDCL)",
        frequency="monthly",
        next_due_date=electricity_date,
        category="Utilities"
    )
    
    mobile_date = datetime(2024, 11, 10)
    manager.add_recurring_expense(
        amount=599.0,
        description="Jio mobile recharge",
        frequency="monthly",
        next_due_date=mobile_date,
        category="Utilities"
    )
    
    broadband_date = datetime(2024, 11, 15)
    manager.add_recurring_expense(
        amount=799.0,
        description="Airtel Xstream Fiber",
        frequency="monthly",
        next_due_date=broadband_date,
        category="Utilities"
    )
    
    all_recurring = manager.list_all_recurring()
    assert len(all_recurring) == 4
    
    total_monthly = sum(r.amount for r in all_recurring)
    assert total_monthly == 20348.0


def test_frequency_case_insensitive():
    """Test that frequency is case insensitive."""
    due_date = datetime(2024, 11, 1)
    
    recurring1 = RecurringExpense(
        amount=100.0,
        description="Test 1",
        frequency="MONTHLY",
        next_due_date=due_date
    )
    assert recurring1.frequency == "monthly"
    
    recurring2 = RecurringExpense(
        amount=100.0,
        description="Test 2",
        frequency="Weekly",
        next_due_date=due_date
    )
    assert recurring2.frequency == "weekly"

