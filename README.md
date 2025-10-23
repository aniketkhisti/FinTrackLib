# FinTrackLib

A personal finance tracking library for Indian users with full INR support, Indian categories, and budget management.

## Features

- **Expense Logging**: Track daily expenses with unique IDs
- **Indian Context**: Full INR support with Indian examples

## Installation

```bash
pip install -e .
```

## Quick Start

```python
from fintracklib import ExpenseLogger

# Log expenses
logger = ExpenseLogger()
logger.log_expense(20.0, "Chai")
logger.log_expense(150.0, "Auto Rickshaw fare")
logger.log_expense(15.0, "Samosa")

# Get total
print(f"Total expenses: ₹{logger.total_expenses()}")
```

## Testing

```bash
pytest
```

## Development Status

This is an active development project. More features coming soon:
- Budget management
- Expense categorization
- Reporting with INR formatting (lakhs/crores)
- Analytics for spending patterns

## License

MIT License

