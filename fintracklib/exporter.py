"""Data export functionality for transactions and budgets."""
import csv
import json
from datetime import datetime
from typing import List, Optional
from io import StringIO
from fintracklib.models import Transaction, Budget
from fintracklib.utils import format_inr, get_fiscal_year


class TransactionExporter:
    """Export transactions to various formats."""
    
    def __init__(self, transactions: List[Transaction]):
        """Initialize exporter with transactions.
        
        Args:
            transactions: List of transactions to export
        """
        self.transactions = transactions
    
    def to_csv(self, filepath: Optional[str] = None,
               date_format: str = "%d-%m-%Y") -> str:
        """Export transactions to CSV format.
        
        Uses Indian date format (DD-MM-YYYY) by default.
        
        Args:
            filepath: Optional file path to write CSV
            date_format: Date format string (default: DD-MM-YYYY)
            
        Returns:
            CSV string if filepath is None, otherwise writes to file
            
        Examples:
            >>> exporter = TransactionExporter(transactions)
            >>> csv_data = exporter.to_csv()
            >>> exporter.to_csv("expenses.csv")
        """
        output = StringIO()
        writer = csv.writer(output)
        
        # Write header
        writer.writerow(['Date', 'Description', 'Amount (₹)', 'Category'])
        
        # Write data
        for txn in self.transactions:
            date_str = txn.date.strftime(date_format)
            amount_str = format_inr(txn.amount)
            category = txn.category or 'Uncategorized'
            writer.writerow([date_str, txn.description, amount_str, category])
        
        csv_content = output.getvalue()
        output.close()
        
        if filepath:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(csv_content)
            return filepath
        
        return csv_content
    
    def to_json(self, filepath: Optional[str] = None,
                include_metadata: bool = True) -> str:
        """Export transactions to JSON format with metadata.
        
        Args:
            filepath: Optional file path to write JSON
            include_metadata: Include export metadata (default: True)
            
        Returns:
            JSON string if filepath is None, otherwise writes to file
        """
        data = {
            'transactions': [
                {
                    'date': txn.date.strftime('%Y-%m-%d'),
                    'description': txn.description,
                    'amount': txn.amount,
                    'category': txn.category,
                    'id': txn.id
                }
                for txn in self.transactions
            ]
        }
        
        if include_metadata:
            total_amount = sum(t.amount for t in self.transactions)
            data['metadata'] = {
                'export_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'fiscal_year': get_fiscal_year(),
                'total_count': len(self.transactions),
                'total_amount': total_amount,
                'formatted_total': format_inr(total_amount)
            }
        
        json_content = json.dumps(data, indent=2, ensure_ascii=False)
        
        if filepath:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(json_content)
            return filepath
        
        return json_content


class BudgetExporter:
    """Export budgets to various formats."""
    
    def __init__(self, budgets: List[Budget]):
        """Initialize exporter with budgets.
        
        Args:
            budgets: List of budgets to export
        """
        self.budgets = budgets
    
    def to_json(self, filepath: Optional[str] = None,
                include_metadata: bool = True) -> str:
        """Export budgets to JSON format.
        
        Args:
            filepath: Optional file path to write JSON
            include_metadata: Include export metadata
            
        Returns:
            JSON string if filepath is None, otherwise writes to file
        """
        data = {
            'budgets': [
                {
                    'category': budget.category,
                    'amount': budget.amount,
                    'spent': budget.spent,
                    'period': budget.period,
                    'remaining': budget.remaining(),
                    'exceeded': budget.is_exceeded(),
                    'utilization': budget.utilization_percentage()
                }
                for budget in self.budgets
            ]
        }
        
        if include_metadata:
            total_budget = sum(b.amount for b in self.budgets)
            total_spent = sum(b.spent for b in self.budgets)
            
            data['metadata'] = {
                'export_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'fiscal_year': get_fiscal_year(),
                'budget_count': len(self.budgets),
                'total_budget': total_budget,
                'total_spent': total_spent,
                'formatted_budget': format_inr(total_budget),
                'formatted_spent': format_inr(total_spent)
            }
        
        json_content = json.dumps(data, indent=2, ensure_ascii=False)
        
        if filepath:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(json_content)
            return filepath
        
        return json_content

