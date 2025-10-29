# FinTrackLib

A personal finance tracking library built for Indian users. Handles INR formatting with lakhs/crores, Indian fiscal year, GST calculations, and tax slabs.

## Overview

This library helps you track expenses and income with proper Indian context - meaning it understands that we write ₹1,00,000 (not ₹100,000), that our fiscal year runs April to March, and that GST splits into CGST/SGST for intra-state transactions.

Built this because most finance tools don't get Indian formats right.

## What it does

**Core features:**
- Track expenses and income with unique IDs
- Set budgets and get warnings when you're close to limits
- Auto-categorize transactions (Festivals, Street Food, Transport, etc.)
- Prevents duplicate entries by default

**Reports and analytics:**
- Generate expense reports with GST breakdown (CGST/SGST/IGST)
- Track festival spending separately (Diwali, Holi, etc.)
- Monthly summaries with proper INR formatting
- Spending trends and insights

**Indian-specific stuff:**
- Formats amounts properly: ₹1,00,000 for 1 lakh, ₹1,00,00,000 for 1 crore
- Parses INR strings back to numbers
- Indian fiscal year calculations (FY2024-25 means April 2024 to March 2025)
- Income tax calculator for both old and new regimes
- GST breakdown (9% CGST + 9% SGST or 18% IGST)

**Data handling:**
- Export to CSV with DD-MM-YYYY format (not the American way)
- JSON export with metadata including fiscal year
- Import from CSV/JSON with validation
- Tag transactions (UPI, cash, credit-card, tax-deductible)
- Search and filter by category, date, amount

**Future features** (in progress):
- Recurring expense tracking (rent, electricity bills)
- Savings goals for weddings, house down payment, etc.
- More detailed tax calculations

## Installation

```bash
pip install -e .
```

## Quick examples

```python
from fintracklib import ExpenseLogger, BudgetManager, format_inr
from fintracklib import Reporter, Analytics, TransactionExporter

# Log expenses with Indian context
logger = ExpenseLogger()
logger.log_expense(20.0, "Chai", category="Street Food")
logger.log_expense(150.0, "Auto fare", category="Transport")
logger.log_expense(5000.0, "Diwali lights", category="Festivals")

# Create and track budgets
budget_mgr = BudgetManager()
budget_mgr.create_budget("Festivals", 10000.0, period="monthly")
budget_mgr.record_expense("Festivals", 5000.0)

# Generate reports with GST
reporter = Reporter()
transactions = logger.get_all_transactions()
print(reporter.expense_summary(transactions, include_gst=True))

# Analytics for festival spending
analytics = Analytics(transactions)
festival_stats = analytics.festival_spending_analysis()
print(f"Festival spending: {festival_stats['formatted_total']}")

# Export data with Indian date format
exporter = TransactionExporter(transactions)
exporter.to_csv("expenses.csv")  # DD-MM-YYYY format
exporter.to_json("expenses.json", include_metadata=True)

# Format amounts in Indian notation
print(format_inr(125000))  # ₹1,25,000.00
print(format_inr(10000000))  # ₹1,00,00,000.00
```

More examples:

```python
from fintracklib import parse_inr, get_fiscal_year, convert_to_lakhs

# Parse INR strings
amount = parse_inr("₹1,00,000.00")  # Returns 100000.0

# Get current fiscal year
fy = get_fiscal_year()  # Returns "FY2024-25"

# Unit conversions
lakhs = convert_to_lakhs(250000)  # Returns 2.5
```

## Testing

```bash
pytest                              # Run all tests
pytest --cov=fintracklib tests/    # With coverage
pytest tests/test_reporter.py -v   # Specific module
```
## Why Indian context matters

Most finance libraries assume US/Western formats. This causes issues:
- They write ₹100,000 instead of ₹1,00,000 (confusing for Indians)
- Fiscal year assumed as Jan-Dec, not Apr-Mar
- No GST breakdown (we need CGST/SGST or IGST)
- Categories don't match Indian spending (no "Street Food" or "Festivals")
- Tax calculations don't match Indian slabs

This library fixes that. Examples:
```python
# We write lakhs and crores properly
₹1,00,000      # 1 lakh
₹1,00,00,000   # 1 crore

# Fiscal year follows Indian calendar
FY2024-25      # April 2024 to March 2025

# GST splits correctly
CGST 9% + SGST 9% = 18%  # intra-state (Maharashtra to Maharashtra)
IGST 18%                  # inter-state (Maharashtra to Delhi)

# Categories that make sense
"Festivals"    # Diwali, Holi expenses
"Street Food"  # Chai, samosa, vada pav
"Transport"    # Auto rickshaw, metro, cab
```

## License

MIT License

