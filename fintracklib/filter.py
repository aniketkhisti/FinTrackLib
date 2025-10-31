"""Transaction filtering and search functionality."""
from typing import List, Optional, Tuple
from datetime import datetime, timedelta
from .models import Transaction


class TransactionFilter:
    """Filter and search through transactions with multiple criteria.
    
    Supports filtering by category, date range, amount range, and
    searching by description with fuzzy matching. Filters can be
    chained together with AND logic.
    """
    
    def __init__(self, transactions: List[Transaction]):
        """Initialize the filter with a list of transactions.
        
        Args:
            transactions: List of Transaction objects to filter
        """
        self.transactions = transactions.copy()
        self._filtered: Optional[List[Transaction]] = None
    
    def search_description(self, search_term: str, case_sensitive: bool = False) -> 'TransactionFilter':
        """Search transactions by description (fuzzy matching).
        
        Performs a case-insensitive substring search by default.
        Finds transactions where the description contains the search term.
        
        Args:
            search_term: Text to search for in descriptions
            case_sensitive: If True, perform case-sensitive search
            
        Returns:
            Self for method chaining
        """
        if not search_term:
            return self
        
        search_term = search_term if case_sensitive else search_term.lower()
        
        def matches(txn: Transaction) -> bool:
            desc = txn.description if case_sensitive else txn.description.lower()
            return search_term in desc
        
        self._apply_filter(matches)
        return self
    
    def filter_by_category(self, category: str) -> 'TransactionFilter':
        """Filter transactions by category.
        
        Args:
            category: Category name to filter by
            
        Returns:
            Self for method chaining
        """
        def matches(txn: Transaction) -> bool:
            return txn.category == category
        
        self._apply_filter(matches)
        return self
    
    def filter_by_categories(self, categories: List[str]) -> 'TransactionFilter':
        """Filter transactions by multiple categories (OR logic).
        
        Args:
            categories: List of category names to filter by
            
        Returns:
            Self for method chaining
        """
        if not categories:
            return self
        
        def matches(txn: Transaction) -> bool:
            return txn.category in categories
        
        self._apply_filter(matches)
        return self
    
    def filter_by_date_range(self, start_date: Optional[datetime] = None,
                            end_date: Optional[datetime] = None) -> 'TransactionFilter':
        """Filter transactions by date range.
        
        Args:
            start_date: Start date (inclusive). If None, no lower bound.
            end_date: End date (inclusive). If None, no upper bound.
            
        Returns:
            Self for method chaining
            
        Raises:
            ValueError: If start_date > end_date
        """
        if start_date and end_date and start_date > end_date:
            raise ValueError("start_date cannot be after end_date")
        
        def matches(txn: Transaction) -> bool:
            if start_date and txn.date < start_date:
                return False
            if end_date and txn.date > end_date:
                return False
            return True
        
        self._apply_filter(matches)
        return self
    
    def filter_by_amount_range(self, min_amount: Optional[float] = None,
                              max_amount: Optional[float] = None) -> 'TransactionFilter':
        """Filter transactions by amount range.
        
        Args:
            min_amount: Minimum amount (inclusive). If None, no lower bound.
            max_amount: Maximum amount (inclusive). If None, no upper bound.
            
        Returns:
            Self for method chaining
            
        Raises:
            ValueError: If min_amount > max_amount or negative amounts
        """
        if min_amount is not None and min_amount < 0:
            raise ValueError("min_amount cannot be negative")
        if max_amount is not None and max_amount < 0:
            raise ValueError("max_amount cannot be negative")
        if min_amount is not None and max_amount is not None and min_amount > max_amount:
            raise ValueError("min_amount cannot be greater than max_amount")
        
        def matches(txn: Transaction) -> bool:
            if min_amount is not None and txn.amount < min_amount:
                return False
            if max_amount is not None and txn.amount > max_amount:
                return False
            return True
        
        self._apply_filter(matches)
        return self
    
    def filter_uncategorized(self) -> 'TransactionFilter':
        """Filter for transactions without a category.
        
        Returns:
            Self for method chaining
        """
        def matches(txn: Transaction) -> bool:
            return txn.category is None
        
        self._apply_filter(matches)
        return self
    
    def filter_categorized(self) -> 'TransactionFilter':
        """Filter for transactions with a category.
        
        Returns:
            Self for method chaining
        """
        def matches(txn: Transaction) -> bool:
            return txn.category is not None
        
        self._apply_filter(matches)
        return self
    
    def sort_by(self, field: str = 'date', reverse: bool = False) -> 'TransactionFilter':
        """Sort filtered results by a field.
        
        Args:
            field: Field to sort by ('date', 'amount', 'category', 'description')
            reverse: If True, sort in descending order
            
        Returns:
            Self for method chaining
            
        Raises:
            ValueError: If field is invalid
        """
        valid_fields = ['date', 'amount', 'category', 'description']
        if field not in valid_fields:
            raise ValueError(f"Invalid sort field: {field}. Must be one of {valid_fields}")
        
        target_list = self._filtered if self._filtered is not None else self.transactions
        
        if field == 'date':
            target_list.sort(key=lambda t: t.date, reverse=reverse)
        elif field == 'amount':
            target_list.sort(key=lambda t: t.amount, reverse=reverse)
        elif field == 'category':
            target_list.sort(key=lambda t: t.category or '', reverse=reverse)
        elif field == 'description':
            target_list.sort(key=lambda t: t.description.lower(), reverse=reverse)
        
        return self
    
    def limit(self, count: int) -> 'TransactionFilter':
        """Limit the number of results returned.
        
        Args:
            count: Maximum number of results to return
            
        Returns:
            Self for method chaining
            
        Raises:
            ValueError: If count is negative
        """
        if count < 0:
            raise ValueError("count cannot be negative")
        
        target_list = self._filtered if self._filtered is not None else self.transactions
        self._filtered = target_list[:count]
        return self
    
    def get_results(self) -> List[Transaction]:
        """Get the filtered and sorted results.
        
        Returns:
            List of filtered Transaction objects
        """
        if self._filtered is not None:
            return self._filtered.copy()
        return self.transactions.copy()
    
    def reset(self) -> 'TransactionFilter':
        """Reset all filters and start fresh.
        
        Returns:
            Self for method chaining
        """
        self._filtered = None
        return self
    
    def count(self) -> int:
        """Get the count of filtered results.
        
        Returns:
            Number of transactions matching the filters
        """
        if self._filtered is not None:
            return len(self._filtered)
        return len(self.transactions)
    
    def total_amount(self) -> float:
        """Calculate total amount of filtered transactions.
        
        Returns:
            Sum of amounts for filtered transactions
        """
        results = self.get_results()
        return sum(txn.amount for txn in results)
    
    def _apply_filter(self, predicate):
        """Apply a filter predicate to current results.
        
        Args:
            predicate: Function that takes a Transaction and returns bool
        """
        source = self._filtered if self._filtered is not None else self.transactions
        self._filtered = [txn for txn in source if predicate(txn)]
    
    def __len__(self) -> int:
        """Return the count of filtered results."""
        return self.count()
    
    def __iter__(self):
        """Allow iteration over filtered results."""
        return iter(self.get_results())


# Convenience function for quick filtering
def filter_transactions(transactions: List[Transaction],
                       category: Optional[str] = None,
                       start_date: Optional[datetime] = None,
                       end_date: Optional[datetime] = None,
                       min_amount: Optional[float] = None,
                       max_amount: Optional[float] = None,
                       search_term: Optional[str] = None) -> List[Transaction]:
    """Convenience function to filter transactions with common criteria.
    
    Args:
        transactions: List of Transaction objects
        category: Filter by category (optional)
        start_date: Filter by start date (optional)
        end_date: Filter by end date (optional)
        min_amount: Minimum amount filter (optional)
        max_amount: Maximum amount filter (optional)
        search_term: Search description (optional)
        
    Returns:
        Filtered list of Transaction objects
    """
    filter_obj = TransactionFilter(transactions)
    
    if category:
        filter_obj.filter_by_category(category)
    
    if start_date or end_date:
        filter_obj.filter_by_date_range(start_date, end_date)
    
    if min_amount is not None or max_amount is not None:
        filter_obj.filter_by_amount_range(min_amount, max_amount)
    
    if search_term:
        filter_obj.search_description(search_term)
    
    return filter_obj.get_results()

