"""Tests for transaction filtering and search."""
import pytest
from datetime import datetime, timedelta
from fintracklib.models import Transaction
from fintracklib.filter import TransactionFilter, filter_transactions


class TestTransactionFilterBasic:
    """Test basic TransactionFilter functionality."""
    
    def test_create_filter(self):
        """Test creating a filter with transactions."""
        transactions = [
            Transaction(amount=20.0, description="Chai", date=datetime(2024, 10, 1)),
            Transaction(amount=150.0, description="Auto fare", date=datetime(2024, 10, 2)),
        ]
        filter_obj = TransactionFilter(transactions)
        assert len(filter_obj) == 2
    
    def test_get_results_no_filter(self):
        """Test getting results without applying any filters."""
        transactions = [
            Transaction(amount=20.0, description="Chai", date=datetime(2024, 10, 1)),
            Transaction(amount=150.0, description="Auto fare", date=datetime(2024, 10, 2)),
        ]
        filter_obj = TransactionFilter(transactions)
        results = filter_obj.get_results()
        assert len(results) == 2
        assert results == transactions
    
    def test_reset_filter(self):
        """Test resetting filters."""
        transactions = [
            Transaction(amount=20.0, description="Chai", date=datetime(2024, 10, 1)),
            Transaction(amount=150.0, description="Auto fare", date=datetime(2024, 10, 2)),
        ]
        filter_obj = TransactionFilter(transactions)
        filter_obj.filter_by_amount_range(min_amount=100.0)
        assert len(filter_obj) == 1
        
        filter_obj.reset()
        assert len(filter_obj) == 2


class TestSearchDescription:
    """Test search by description functionality."""
    
    def test_search_description_case_insensitive(self):
        """Test case-insensitive description search."""
        transactions = [
            Transaction(amount=20.0, description="Chai"),
            Transaction(amount=150.0, description="Auto Rickshaw"),
            Transaction(amount=15.0, description="Chai at station"),
        ]
        filter_obj = TransactionFilter(transactions)
        filter_obj.search_description("chai")
        results = filter_obj.get_results()
        
        assert len(results) == 2
        assert all("chai" in r.description.lower() for r in results)
    
    def test_search_description_case_sensitive(self):
        """Test case-sensitive description search."""
        transactions = [
            Transaction(amount=20.0, description="Chai"),
            Transaction(amount=15.0, description="chai at station"),
        ]
        filter_obj = TransactionFilter(transactions)
        filter_obj.search_description("chai", case_sensitive=True)
        results = filter_obj.get_results()
        
        assert len(results) == 1
        assert results[0].description == "chai at station"
    
    def test_search_description_empty_term(self):
        """Test search with empty term returns all."""
        transactions = [
            Transaction(amount=20.0, description="Chai"),
            Transaction(amount=150.0, description="Auto"),
        ]
        filter_obj = TransactionFilter(transactions)
        filter_obj.search_description("")
        results = filter_obj.get_results()
        
        assert len(results) == 2
    
    def test_search_description_partial_match(self):
        """Test fuzzy matching with partial words."""
        transactions = [
            Transaction(amount=500.0, description="Diwali lights"),
            Transaction(amount=3000.0, description="Diwali sweets"),
            Transaction(amount=150.0, description="Auto fare"),
        ]
        filter_obj = TransactionFilter(transactions)
        filter_obj.search_description("diwali")
        results = filter_obj.get_results()
        
        assert len(results) == 2
        assert all("diwali" in r.description.lower() for r in results)


class TestFilterByCategory:
    """Test filtering by category."""
    
    def test_filter_by_category(self):
        """Test filtering by single category."""
        transactions = [
            Transaction(amount=20.0, description="Chai", category="Street Food"),
            Transaction(amount=150.0, description="Auto", category="Transport"),
            Transaction(amount=15.0, description="Samosa", category="Street Food"),
        ]
        filter_obj = TransactionFilter(transactions)
        filter_obj.filter_by_category("Street Food")
        results = filter_obj.get_results()
        
        assert len(results) == 2
        assert all(r.category == "Street Food" for r in results)
    
    def test_filter_by_category_no_match(self):
        """Test filtering by category with no matches."""
        transactions = [
            Transaction(amount=20.0, description="Chai", category="Street Food"),
        ]
        filter_obj = TransactionFilter(transactions)
        filter_obj.filter_by_category("Transport")
        results = filter_obj.get_results()
        
        assert len(results) == 0
    
    def test_filter_by_categories(self):
        """Test filtering by multiple categories."""
        transactions = [
            Transaction(amount=20.0, description="Chai", category="Street Food"),
            Transaction(amount=150.0, description="Auto", category="Transport"),
            Transaction(amount=500.0, description="Festival", category="Festivals"),
        ]
        filter_obj = TransactionFilter(transactions)
        filter_obj.filter_by_categories(["Street Food", "Transport"])
        results = filter_obj.get_results()
        
        assert len(results) == 2
        assert all(r.category in ["Street Food", "Transport"] for r in results)
    
    def test_filter_uncategorized(self):
        """Test filtering for uncategorized transactions."""
        transactions = [
            Transaction(amount=20.0, description="Chai", category="Street Food"),
            Transaction(amount=150.0, description="Auto"),
            Transaction(amount=15.0, description="Unknown"),
        ]
        filter_obj = TransactionFilter(transactions)
        filter_obj.filter_uncategorized()
        results = filter_obj.get_results()
        
        assert len(results) == 2
        assert all(r.category is None for r in results)
    
    def test_filter_categorized(self):
        """Test filtering for categorized transactions."""
        transactions = [
            Transaction(amount=20.0, description="Chai", category="Street Food"),
            Transaction(amount=150.0, description="Auto"),
            Transaction(amount=15.0, description="Samosa", category="Street Food"),
        ]
        filter_obj = TransactionFilter(transactions)
        filter_obj.filter_categorized()
        results = filter_obj.get_results()
        
        assert len(results) == 2
        assert all(r.category is not None for r in results)


class TestFilterByDateRange:
    """Test filtering by date range."""
    
    def test_filter_by_date_range(self):
        """Test filtering by date range."""
        start = datetime(2024, 10, 1)
        end = datetime(2024, 10, 15)
        
        transactions = [
            Transaction(amount=20.0, description="Chai", date=datetime(2024, 9, 30)),
            Transaction(amount=150.0, description="Auto", date=datetime(2024, 10, 5)),
            Transaction(amount=15.0, description="Samosa", date=datetime(2024, 10, 20)),
        ]
        filter_obj = TransactionFilter(transactions)
        filter_obj.filter_by_date_range(start_date=start, end_date=end)
        results = filter_obj.get_results()
        
        assert len(results) == 1
        assert results[0].description == "Auto"
    
    def test_filter_by_start_date_only(self):
        """Test filtering with only start date."""
        start = datetime(2024, 10, 1)
        
        transactions = [
            Transaction(amount=20.0, description="Chai", date=datetime(2024, 9, 30)),
            Transaction(amount=150.0, description="Auto", date=datetime(2024, 10, 5)),
            Transaction(amount=15.0, description="Samosa", date=datetime(2024, 10, 20)),
        ]
        filter_obj = TransactionFilter(transactions)
        filter_obj.filter_by_date_range(start_date=start)
        results = filter_obj.get_results()
        
        assert len(results) == 2
    
    def test_filter_by_end_date_only(self):
        """Test filtering with only end date."""
        end = datetime(2024, 10, 15)
        
        transactions = [
            Transaction(amount=20.0, description="Chai", date=datetime(2024, 9, 30)),
            Transaction(amount=150.0, description="Auto", date=datetime(2024, 10, 5)),
            Transaction(amount=15.0, description="Samosa", date=datetime(2024, 10, 20)),
        ]
        filter_obj = TransactionFilter(transactions)
        filter_obj.filter_by_date_range(end_date=end)
        results = filter_obj.get_results()
        
        assert len(results) == 2
    
    def test_filter_by_date_range_inclusive(self):
        """Test that date range is inclusive."""
        start = datetime(2024, 10, 1)
        end = datetime(2024, 10, 5)
        
        transactions = [
            Transaction(amount=20.0, description="Chai", date=datetime(2024, 10, 1)),
            Transaction(amount=150.0, description="Auto", date=datetime(2024, 10, 5)),
            Transaction(amount=15.0, description="Samosa", date=datetime(2024, 10, 6)),
        ]
        filter_obj = TransactionFilter(transactions)
        filter_obj.filter_by_date_range(start_date=start, end_date=end)
        results = filter_obj.get_results()
        
        assert len(results) == 2
    
    def test_filter_by_date_range_invalid(self):
        """Test error when start_date > end_date."""
        transactions = [
            Transaction(amount=20.0, description="Chai", date=datetime(2024, 10, 1)),
        ]
        filter_obj = TransactionFilter(transactions)
        
        with pytest.raises(ValueError, match="start_date cannot be after end_date"):
            filter_obj.filter_by_date_range(
                start_date=datetime(2024, 10, 10),
                end_date=datetime(2024, 10, 1)
            )


class TestFilterByAmountRange:
    """Test filtering by amount range."""
    
    def test_filter_by_amount_range(self):
        """Test filtering by amount range."""
        transactions = [
            Transaction(amount=20.0, description="Chai"),
            Transaction(amount=150.0, description="Auto"),
            Transaction(amount=500.0, description="Festival"),
        ]
        filter_obj = TransactionFilter(transactions)
        filter_obj.filter_by_amount_range(min_amount=100.0, max_amount=200.0)
        results = filter_obj.get_results()
        
        assert len(results) == 1
        assert results[0].description == "Auto"
    
    def test_filter_by_min_amount_only(self):
        """Test filtering with only minimum amount."""
        transactions = [
            Transaction(amount=20.0, description="Chai"),
            Transaction(amount=150.0, description="Auto"),
            Transaction(amount=500.0, description="Festival"),
        ]
        filter_obj = TransactionFilter(transactions)
        filter_obj.filter_by_amount_range(min_amount=100.0)
        results = filter_obj.get_results()
        
        assert len(results) == 2
    
    def test_filter_by_max_amount_only(self):
        """Test filtering with only maximum amount."""
        transactions = [
            Transaction(amount=20.0, description="Chai"),
            Transaction(amount=150.0, description="Auto"),
            Transaction(amount=500.0, description="Festival"),
        ]
        filter_obj = TransactionFilter(transactions)
        filter_obj.filter_by_amount_range(max_amount=200.0)
        results = filter_obj.get_results()
        
        assert len(results) == 2
    
    def test_filter_by_amount_range_inclusive(self):
        """Test that amount range is inclusive."""
        transactions = [
            Transaction(amount=100.0, description="Min"),
            Transaction(amount=200.0, description="Max"),
            Transaction(amount=50.0, description="Below"),
        ]
        filter_obj = TransactionFilter(transactions)
        filter_obj.filter_by_amount_range(min_amount=100.0, max_amount=200.0)
        results = filter_obj.get_results()
        
        assert len(results) == 2
    
    def test_filter_by_amount_range_invalid(self):
        """Test error when min_amount > max_amount."""
        transactions = [
            Transaction(amount=20.0, description="Chai"),
        ]
        filter_obj = TransactionFilter(transactions)
        
        with pytest.raises(ValueError, match="min_amount cannot be greater"):
            filter_obj.filter_by_amount_range(min_amount=200.0, max_amount=100.0)
    
    def test_filter_by_amount_range_negative_min(self):
        """Test error when min_amount is negative."""
        transactions = [
            Transaction(amount=20.0, description="Chai"),
        ]
        filter_obj = TransactionFilter(transactions)
        
        with pytest.raises(ValueError, match="min_amount cannot be negative"):
            filter_obj.filter_by_amount_range(min_amount=-10.0)
    
    def test_filter_by_amount_range_negative_max(self):
        """Test error when max_amount is negative."""
        transactions = [
            Transaction(amount=20.0, description="Chai"),
        ]
        filter_obj = TransactionFilter(transactions)
        
        with pytest.raises(ValueError, match="max_amount cannot be negative"):
            filter_obj.filter_by_amount_range(max_amount=-10.0)


class TestFilterChaining:
    """Test chaining filters together."""
    
    def test_chain_filters_and_logic(self):
        """Test that chained filters use AND logic."""
        transactions = [
            Transaction(amount=150.0, description="Auto", category="Transport",
                       date=datetime(2024, 10, 5)),
            Transaction(amount=20.0, description="Chai", category="Street Food",
                       date=datetime(2024, 10, 5)),
            Transaction(amount=200.0, description="Taxi", category="Transport",
                       date=datetime(2024, 10, 15)),
        ]
        filter_obj = TransactionFilter(transactions)
        filter_obj.filter_by_category("Transport").filter_by_amount_range(min_amount=100.0)
        results = filter_obj.get_results()
        
        assert len(results) == 2
        assert all(r.category == "Transport" for r in results)
        assert all(r.amount >= 100.0 for r in results)
    
    def test_chain_multiple_filters(self):
        """Test chaining multiple filters."""
        transactions = [
            Transaction(amount=150.0, description="Diwali lights", category="Festivals",
                       date=datetime(2024, 10, 25)),
            Transaction(amount=500.0, description="Diwali sweets", category="Festivals",
                       date=datetime(2024, 10, 26)),
            Transaction(amount=3000.0, description="Diwali gifts", category="Shopping",
                       date=datetime(2024, 10, 25)),
        ]
        filter_obj = TransactionFilter(transactions)
        filter_obj.filter_by_category("Festivals").filter_by_amount_range(min_amount=100.0).search_description("diwali")
        results = filter_obj.get_results()
        
        assert len(results) == 2
        assert all(r.category == "Festivals" for r in results)
        assert all("diwali" in r.description.lower() for r in results)
    
    def test_chain_filters_with_date_range(self):
        """Test chaining filters with date range."""
        start = datetime(2024, 10, 1)
        end = datetime(2024, 10, 15)
        
        transactions = [
            Transaction(amount=150.0, description="Auto", category="Transport",
                       date=datetime(2024, 10, 5)),
            Transaction(amount=200.0, description="Taxi", category="Transport",
                       date=datetime(2024, 10, 20)),
            Transaction(amount=20.0, description="Chai", category="Street Food",
                       date=datetime(2024, 10, 10)),
        ]
        filter_obj = TransactionFilter(transactions)
        filter_obj.filter_by_category("Transport").filter_by_date_range(start_date=start, end_date=end)
        results = filter_obj.get_results()
        
        assert len(results) == 1
        assert results[0].description == "Auto"


class TestSorting:
    """Test sorting functionality."""
    
    def test_sort_by_date_ascending(self):
        """Test sorting by date in ascending order."""
        transactions = [
            Transaction(amount=150.0, description="Auto", date=datetime(2024, 10, 5)),
            Transaction(amount=20.0, description="Chai", date=datetime(2024, 10, 1)),
            Transaction(amount=500.0, description="Festival", date=datetime(2024, 10, 3)),
        ]
        filter_obj = TransactionFilter(transactions)
        filter_obj.sort_by('date')
        results = filter_obj.get_results()
        
        assert len(results) == 3
        assert results[0].date == datetime(2024, 10, 1)
        assert results[2].date == datetime(2024, 10, 5)
    
    def test_sort_by_date_descending(self):
        """Test sorting by date in descending order."""
        transactions = [
            Transaction(amount=150.0, description="Auto", date=datetime(2024, 10, 5)),
            Transaction(amount=20.0, description="Chai", date=datetime(2024, 10, 1)),
            Transaction(amount=500.0, description="Festival", date=datetime(2024, 10, 3)),
        ]
        filter_obj = TransactionFilter(transactions)
        filter_obj.sort_by('date', reverse=True)
        results = filter_obj.get_results()
        
        assert len(results) == 3
        assert results[0].date == datetime(2024, 10, 5)
        assert results[2].date == datetime(2024, 10, 1)
    
    def test_sort_by_amount_ascending(self):
        """Test sorting by amount in ascending order."""
        transactions = [
            Transaction(amount=500.0, description="Festival"),
            Transaction(amount=20.0, description="Chai"),
            Transaction(amount=150.0, description="Auto"),
        ]
        filter_obj = TransactionFilter(transactions)
        filter_obj.sort_by('amount')
        results = filter_obj.get_results()
        
        assert len(results) == 3
        assert results[0].amount == 20.0
        assert results[2].amount == 500.0
    
    def test_sort_by_category(self):
        """Test sorting by category."""
        transactions = [
            Transaction(amount=150.0, description="Auto", category="Transport"),
            Transaction(amount=20.0, description="Chai", category="Street Food"),
            Transaction(amount=500.0, description="Festival", category="Festivals"),
        ]
        filter_obj = TransactionFilter(transactions)
        filter_obj.sort_by('category')
        results = filter_obj.get_results()
        
        assert len(results) == 3
        assert results[0].category == "Festivals"
        assert results[1].category == "Street Food"
    
    def test_sort_by_category_with_none(self):
        """Test sorting by category handles None values."""
        transactions = [
            Transaction(amount=150.0, description="Auto", category="Transport"),
            Transaction(amount=20.0, description="Chai"),
            Transaction(amount=500.0, description="Festival", category="Festivals"),
        ]
        filter_obj = TransactionFilter(transactions)
        filter_obj.sort_by('category')
        results = filter_obj.get_results()
        
        assert len(results) == 3
    
    def test_sort_by_description(self):
        """Test sorting by description."""
        transactions = [
            Transaction(amount=150.0, description="Auto"),
            Transaction(amount=20.0, description="Chai"),
            Transaction(amount=500.0, description="Biryani"),
        ]
        filter_obj = TransactionFilter(transactions)
        filter_obj.sort_by('description')
        results = filter_obj.get_results()
        
        assert len(results) == 3
        assert results[0].description == "Auto"
    
    def test_sort_invalid_field(self):
        """Test error when sorting by invalid field."""
        transactions = [
            Transaction(amount=20.0, description="Chai"),
        ]
        filter_obj = TransactionFilter(transactions)
        
        with pytest.raises(ValueError, match="Invalid sort field"):
            filter_obj.sort_by('invalid_field')
    
    def test_sort_after_filtering(self):
        """Test sorting after applying filters."""
        transactions = [
            Transaction(amount=500.0, description="Festival", category="Festivals"),
            Transaction(amount=20.0, description="Chai", category="Street Food"),
            Transaction(amount=150.0, description="Auto", category="Transport"),
        ]
        filter_obj = TransactionFilter(transactions)
        filter_obj.filter_by_amount_range(min_amount=100.0).sort_by('amount')
        results = filter_obj.get_results()
        
        assert len(results) == 2
        assert results[0].amount == 150.0


class TestLimitAndCount:
    """Test limit and count functionality."""
    
    def test_limit_results(self):
        """Test limiting the number of results."""
        transactions = [
            Transaction(amount=20.0, description="Chai"),
            Transaction(amount=150.0, description="Auto"),
            Transaction(amount=500.0, description="Festival"),
        ]
        filter_obj = TransactionFilter(transactions)
        filter_obj.limit(2)
        results = filter_obj.get_results()
        
        assert len(results) == 2
    
    def test_limit_after_filtering(self):
        """Test limiting after filtering."""
        transactions = [
            Transaction(amount=20.0, description="Chai", category="Street Food"),
            Transaction(amount=150.0, description="Auto", category="Transport"),
            Transaction(amount=200.0, description="Taxi", category="Transport"),
            Transaction(amount=300.0, description="Bus", category="Transport"),
        ]
        filter_obj = TransactionFilter(transactions)
        filter_obj.filter_by_category("Transport").sort_by('amount').limit(2)
        results = filter_obj.get_results()
        
        assert len(results) == 2
        assert all(r.category == "Transport" for r in results)
    
    def test_limit_negative(self):
        """Test error when limit is negative."""
        transactions = [
            Transaction(amount=20.0, description="Chai"),
        ]
        filter_obj = TransactionFilter(transactions)
        
        with pytest.raises(ValueError, match="count cannot be negative"):
            filter_obj.limit(-1)
    
    def test_count_method(self):
        """Test count method."""
        transactions = [
            Transaction(amount=20.0, description="Chai"),
            Transaction(amount=150.0, description="Auto"),
        ]
        filter_obj = TransactionFilter(transactions)
        assert filter_obj.count() == 2
        
        filter_obj.filter_by_category("Transport")
        assert filter_obj.count() == 0
    
    def test_total_amount(self):
        """Test calculating total amount of filtered transactions."""
        transactions = [
            Transaction(amount=20.0, description="Chai"),
            Transaction(amount=150.0, description="Auto"),
            Transaction(amount=500.0, description="Festival"),
        ]
        filter_obj = TransactionFilter(transactions)
        total = filter_obj.total_amount()
        
        assert total == 670.0
    
    def test_total_amount_after_filtering(self):
        """Test total amount after filtering."""
        transactions = [
            Transaction(amount=20.0, description="Chai"),
            Transaction(amount=150.0, description="Auto"),
            Transaction(amount=500.0, description="Festival"),
        ]
        filter_obj = TransactionFilter(transactions)
        filter_obj.filter_by_amount_range(min_amount=100.0)
        total = filter_obj.total_amount()
        
        assert total == 650.0


class TestConvenienceFunction:
    """Test convenience filter_transactions function."""
    
    def test_convenience_function_by_category(self):
        """Test convenience function with category filter."""
        transactions = [
            Transaction(amount=20.0, description="Chai", category="Street Food"),
            Transaction(amount=150.0, description="Auto", category="Transport"),
            Transaction(amount=15.0, description="Samosa", category="Street Food"),
        ]
        results = filter_transactions(transactions, category="Street Food")
        
        assert len(results) == 2
        assert all(r.category == "Street Food" for r in results)
    
    def test_convenience_function_by_date_range(self):
        """Test convenience function with date range."""
        transactions = [
            Transaction(amount=20.0, description="Chai", date=datetime(2024, 10, 1)),
            Transaction(amount=150.0, description="Auto", date=datetime(2024, 10, 15)),
            Transaction(amount=500.0, description="Festival", date=datetime(2024, 11, 1)),
        ]
        results = filter_transactions(
            transactions,
            start_date=datetime(2024, 10, 1),
            end_date=datetime(2024, 10, 31)
        )
        
        assert len(results) == 2
    
    def test_convenience_function_by_amount_range(self):
        """Test convenience function with amount range."""
        transactions = [
            Transaction(amount=20.0, description="Chai"),
            Transaction(amount=150.0, description="Auto"),
            Transaction(amount=500.0, description="Festival"),
        ]
        results = filter_transactions(
            transactions,
            min_amount=100.0,
            max_amount=200.0
        )
        
        assert len(results) == 1
        assert results[0].description == "Auto"
    
    def test_convenience_function_by_search_term(self):
        """Test convenience function with search term."""
        transactions = [
            Transaction(amount=500.0, description="Diwali lights"),
            Transaction(amount=3000.0, description="Diwali sweets"),
            Transaction(amount=150.0, description="Auto fare"),
        ]
        results = filter_transactions(transactions, search_term="diwali")
        
        assert len(results) == 2
    
    def test_convenience_function_combined(self):
        """Test convenience function with multiple filters."""
        transactions = [
            Transaction(amount=500.0, description="Diwali lights", category="Festivals",
                       date=datetime(2024, 10, 25)),
            Transaction(amount=3000.0, description="Diwali sweets", category="Festivals",
                       date=datetime(2024, 10, 26)),
            Transaction(amount=150.0, description="Auto", category="Transport",
                       date=datetime(2024, 10, 25)),
        ]
        results = filter_transactions(
            transactions,
            category="Festivals",
            start_date=datetime(2024, 10, 1),
            end_date=datetime(2024, 10, 31),
            min_amount=100.0,
            search_term="diwali"
        )
        
        assert len(results) == 2
        assert all(r.category == "Festivals" for r in results)


class TestRealWorldScenarios:
    """Test real-world Indian context scenarios."""
    
    def test_find_chai_expenses(self):
        """Test finding all chai expenses."""
        transactions = [
            Transaction(amount=20.0, description="Chai at station", date=datetime(2024, 10, 1)),
            Transaction(amount=25.0, description="Chai with friends", date=datetime(2024, 10, 5)),
            Transaction(amount=150.0, description="Auto fare", date=datetime(2024, 10, 2)),
        ]
        filter_obj = TransactionFilter(transactions)
        filter_obj.search_description("chai")
        results = filter_obj.get_results()
        
        assert len(results) == 2
        assert all("chai" in r.description.lower() for r in results)
    
    def test_transport_expenses_in_october_over_100(self):
        """Test finding transport expenses in October over ₹100."""
        transactions = [
            Transaction(amount=150.0, description="Auto", category="Transport",
                       date=datetime(2024, 10, 5)),
            Transaction(amount=80.0, description="Bus", category="Transport",
                       date=datetime(2024, 10, 10)),
            Transaction(amount=200.0, description="Taxi", category="Transport",
                       date=datetime(2024, 9, 20)),
        ]
        filter_obj = TransactionFilter(transactions)
        filter_obj.filter_by_category("Transport").filter_by_date_range(
            start_date=datetime(2024, 10, 1),
            end_date=datetime(2024, 10, 31)
        ).filter_by_amount_range(min_amount=100.0)
        results = filter_obj.get_results()
        
        assert len(results) == 1
        assert results[0].description == "Auto"
    
    def test_top_10_expenses_this_year(self):
        """Test finding top 10 expenses by amount this year."""
        transactions = [
            Transaction(amount=5000.0, description="Festival", date=datetime(2024, 6, 1)),
            Transaction(amount=3000.0, description="Shopping", date=datetime(2024, 7, 1)),
            Transaction(amount=2000.0, description="Gifts", date=datetime(2024, 8, 1)),
            Transaction(amount=1500.0, description="Groceries", date=datetime(2024, 9, 1)),
            Transaction(amount=1000.0, description="Utilities", date=datetime(2024, 10, 1)),
            Transaction(amount=800.0, description="Entertainment", date=datetime(2024, 11, 1)),
            Transaction(amount=600.0, description="Food", date=datetime(2024, 12, 1)),
            Transaction(amount=500.0, description="Transport", date=datetime(2024, 5, 1)),
            Transaction(amount=400.0, description="Bills", date=datetime(2024, 4, 1)),
            Transaction(amount=300.0, description="Other", date=datetime(2024, 3, 1)),
            Transaction(amount=200.0, description="Misc", date=datetime(2024, 2, 1)),
            Transaction(amount=100.0, description="Small", date=datetime(2024, 1, 1)),
        ]
        start_year = datetime(2024, 1, 1)
        end_year = datetime(2024, 12, 31)
        
        filter_obj = TransactionFilter(transactions)
        filter_obj.filter_by_date_range(start_date=start_year, end_date=end_year)
        filter_obj.sort_by('amount', reverse=True).limit(10)
        results = filter_obj.get_results()
        
        assert len(results) == 10
        assert results[0].amount == 5000.0
        assert results[9].amount == 300.0
    
    def test_all_uncategorized_transactions(self):
        """Test finding all uncategorized transactions."""
        transactions = [
            Transaction(amount=20.0, description="Chai", category="Street Food"),
            Transaction(amount=150.0, description="Auto"),
            Transaction(amount=15.0, description="Unknown"),
            Transaction(amount=500.0, description="Festival", category="Festivals"),
        ]
        filter_obj = TransactionFilter(transactions)
        filter_obj.filter_uncategorized()
        results = filter_obj.get_results()
        
        assert len(results) == 2
        assert all(r.category is None for r in results)
    
    def test_expenses_containing_diwali_in_last_3_months(self):
        """Test finding expenses containing 'diwali' in last 3 months."""
        now = datetime(2024, 11, 1)
        three_months_ago = now - timedelta(days=90)
        
        transactions = [
            Transaction(amount=500.0, description="Diwali lights", date=datetime(2024, 10, 25)),
            Transaction(amount=3000.0, description="Diwali sweets", date=datetime(2024, 10, 26)),
            Transaction(amount=2000.0, description="Diwali gifts", date=datetime(2024, 7, 1)),
        ]
        filter_obj = TransactionFilter(transactions)
        filter_obj.search_description("diwali").filter_by_date_range(
            start_date=three_months_ago,
            end_date=now
        )
        results = filter_obj.get_results()
        
        assert len(results) == 2
        assert all("diwali" in r.description.lower() for r in results)


class TestIteration:
    """Test iteration over filtered results."""
    
    def test_iterate_over_filtered_results(self):
        """Test iterating over filtered results."""
        transactions = [
            Transaction(amount=20.0, description="Chai"),
            Transaction(amount=150.0, description="Auto"),
            Transaction(amount=500.0, description="Festival"),
        ]
        filter_obj = TransactionFilter(transactions)
        filter_obj.filter_by_amount_range(min_amount=100.0)
        
        results = [txn for txn in filter_obj]
        assert len(results) == 2
    
    def test_len_method(self):
        """Test len() method on filter."""
        transactions = [
            Transaction(amount=20.0, description="Chai"),
            Transaction(amount=150.0, description="Auto"),
        ]
        filter_obj = TransactionFilter(transactions)
        assert len(filter_obj) == 2
        
        filter_obj.filter_by_category("Transport")
        assert len(filter_obj) == 0

