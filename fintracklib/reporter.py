"""Report generation for expenses and budgets."""
from typing import List, Optional
from datetime import datetime
from fintracklib.models import Transaction, Budget
from fintracklib.utils import format_inr


class Reporter:
    """Generate formatted reports for expenses and budgets.
    
    Provides various report formats including expense summaries,
    budget reports, and monthly breakdowns with proper INR formatting.
    """
    
    def __init__(self):
        """Initialize the reporter."""
        pass
    
    def expense_summary(self, transactions: List[Transaction], 
                       include_gst: bool = False) -> str:
        """Generate a formatted expense summary report.
        
        Groups transactions by category and calculates totals.
        
        Args:
            transactions: List of Transaction objects
            include_gst: If True, adds GST calculation (18%)
            
        Returns:
            Formatted report string
        """
        if not transactions:
            return "No transactions to report."
        
        # Group transactions by category
        by_category = {}
        for txn in transactions:
            category = txn.category or "Uncategorized"
            if category not in by_category:
                by_category[category] = []
            by_category[category].append(txn)
        
        # Build report
        lines = []
        lines.append("=" * 50)
        lines.append("EXPENSE SUMMARY")
        lines.append("=" * 50)
        lines.append("")
        
        total = 0.0
        for category in sorted(by_category.keys()):
            txns = by_category[category]
            lines.append(f"{category}:")
            
            category_total = 0.0
            for txn in txns:
                lines.append(f"  - {txn.description}: {format_inr(txn.amount)}")
                category_total += txn.amount
            
            lines.append(f"  Subtotal: {format_inr(category_total)}")
            lines.append("")
            total += category_total
        
        lines.append("-" * 50)
        lines.append(f"Total Expenses: {format_inr(total)}")
        
        if include_gst:
            gst_amount = total * 0.18
            total_with_gst = total + gst_amount
            lines.append(f"GST (18%): {format_inr(gst_amount)}")
            lines.append(f"Total with GST: {format_inr(total_with_gst)}")
        
        lines.append("=" * 50)
        
        return "\n".join(lines)
    
    def budget_report(self, budgets: List[Budget]) -> str:
        """Generate a budget utilization report.
        
        Shows each budget's allocation, spent amount, remaining amount,
        and utilization percentage.
        
        Args:
            budgets: List of Budget objects
            
        Returns:
            Formatted budget report string
        """
        if not budgets:
            return "No budgets to report."
        
        lines = []
        lines.append("=" * 50)
        lines.append("BUDGET REPORT")
        lines.append("=" * 50)
        lines.append("")
        
        for budget in budgets:
            lines.append(f"Category: {budget.category}")
            lines.append(f"Period: {budget.period.capitalize()}")
            lines.append(f"Allocated: {format_inr(budget.amount)}")
            lines.append(f"Spent: {format_inr(budget.spent)}")
            lines.append(f"Remaining: {format_inr(budget.remaining())}")
            lines.append(f"Utilization: {budget.utilization_percentage():.1f}%")
            
            if budget.is_exceeded():
                lines.append("⚠️  BUDGET EXCEEDED!")
            
            lines.append("")
        
        lines.append("=" * 50)
        
        return "\n".join(lines)
    
    def monthly_report(self, transactions: List[Transaction], 
                      year: int, month: int) -> str:
        """Generate a report for a specific month.
        
        Filters transactions for the given month and year,
        then generates an expense summary.
        
        Args:
            transactions: List of all transactions
            year: Year to filter (e.g., 2024)
            month: Month to filter (1-12)
            
        Returns:
            Formatted monthly report string
        """
        # Filter transactions for the specified month
        filtered = [
            txn for txn in transactions
            if txn.date.year == year and txn.date.month == month
        ]
        
        if not filtered:
            return f"No transactions found for {month:02d}/{year}"
        
        # Generate header
        month_names = [
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ]
        month_name = month_names[month - 1]
        
        lines = []
        lines.append("=" * 50)
        lines.append(f"MONTHLY REPORT - {month_name} {year}")
        lines.append("=" * 50)
        lines.append("")
        
        # Generate summary for filtered transactions
        summary = self.expense_summary(filtered)
        # Remove the header from summary since we have our own
        summary_lines = summary.split("\n")[4:]  # Skip header lines
        
        lines.extend(summary_lines)
        
        return "\n".join(lines)

