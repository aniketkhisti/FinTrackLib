"""Analytics and insights for expense data."""
from typing import List, Dict
from datetime import datetime, timedelta
from collections import defaultdict
from fintracklib.models import Transaction
from fintracklib.utils import format_inr


class Analytics:
    """Provides analytics and insights for spending patterns.
    
    Analyzes transactions to provide insights about spending habits,
    especially useful for festival seasons and monthly trends.
    """
    
    def __init__(self, transactions: List[Transaction]):
        """Initialize analytics with transaction data.
        
        Args:
            transactions: List of Transaction objects to analyze
        """
        self.transactions = transactions
    
    def average_daily_spending(self, days: int = 30) -> float:
        """Calculate average daily spending over recent period.
        
        Args:
            days: Number of days to look back (default 30)
            
        Returns:
            Average daily spending amount
        """
        cutoff_date = datetime.now() - timedelta(days=days)
        recent = [t for t in self.transactions if t.date >= cutoff_date]
        
        if not recent:
            return 0.0
        
        total = sum(t.amount for t in recent)
        return total / days
    
    def spending_by_category(self) -> Dict[str, float]:
        """Get total spending grouped by category.
        
        Returns:
            Dictionary mapping category names to total amounts
        """
        by_category = defaultdict(float)
        
        for txn in self.transactions:
            category = txn.category or "Uncategorized"
            by_category[category] += txn.amount
        
        return dict(by_category)
    
    def festival_spending_analysis(self, festival_category: str = "Festivals") -> Dict:
        """Analyze spending on festivals like Diwali, Holi, etc.
        
        Args:
            festival_category: Category name for festival expenses
            
        Returns:
            Dictionary with festival spending statistics
        """
        festival_txns = [t for t in self.transactions 
                        if t.category == festival_category]
        
        if not festival_txns:
            return {
                'total': 0.0,
                'count': 0,
                'average': 0.0,
                'formatted_total': format_inr(0.0),
                'transactions': []
            }
        
        total = sum(t.amount for t in festival_txns)
        count = len(festival_txns)
        avg = total / count if count > 0 else 0.0
        
        return {
            'total': total,
            'count': count,
            'average': avg,
            'formatted_total': format_inr(total),
            'transactions': festival_txns
        }
    
    def get_insights(self) -> List[str]:
        """Generate textual insights about spending patterns.
        
        Returns:
            List of insight strings with INR formatting
        """
        insights = []
        
        if not self.transactions:
            return ["No transaction data available for analysis."]
        
        # Total spending
        total = sum(t.amount for t in self.transactions)
        insights.append(f"Total spending: {format_inr(total)}")
        
        # Average transaction
        avg_txn = total / len(self.transactions)
        insights.append(f"Average transaction: {format_inr(avg_txn)}")
        
        # Top category
        by_cat = self.spending_by_category()
        if by_cat:
            top_cat = max(by_cat.items(), key=lambda x: x[1])
            insights.append(f"Highest spending category: {top_cat[0]} ({format_inr(top_cat[1])})")
        
        return insights

