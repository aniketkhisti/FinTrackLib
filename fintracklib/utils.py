"""Utility functions for formatting and calculations."""
from datetime import datetime
from typing import Optional


def format_inr(amount: float) -> str:
    """Format amount in Indian Rupee notation with lakhs and crores.
    
    Indian numbering system:
    - First comma after 3 digits from right
    - Subsequent commas every 2 digits
    - Examples: ₹1,00,000 (1 lakh), ₹1,00,00,000 (1 crore)
    
    Args:
        amount: Amount to format
        
    Returns:
        Formatted string with ₹ symbol and proper comma placement
        
    Examples:
        >>> format_inr(1000)
        '₹1,000.00'
        >>> format_inr(100000)
        '₹1,00,000.00'
        >>> format_inr(10000000)
        '₹1,00,00,000.00'
    """
    # Handle negative amounts
    is_negative = amount < 0
    amount = abs(amount)
    
    # Split into integer and decimal parts
    integer_part = int(amount)
    decimal_part = f"{amount - integer_part:.2f}"[2:]  # Get decimal digits
    
    # Convert to string for manipulation
    num_str = str(integer_part)
    
    # For numbers less than 1000, no special formatting needed
    if integer_part < 1000:
        result = f"₹{num_str}.{decimal_part}"
        return f"-{result}" if is_negative else result
    
    # Format according to Indian system
    # Place first comma after last 3 digits, then every 2 digits
    result_parts = []
    
    # Take last 3 digits
    result_parts.append(num_str[-3:])
    num_str = num_str[:-3]
    
    # Take remaining digits in groups of 2 from right
    while num_str:
        if len(num_str) >= 2:
            result_parts.append(num_str[-2:])
            num_str = num_str[:-2]
        else:
            result_parts.append(num_str)
            break
    
    # Reverse and join with commas
    formatted = ','.join(reversed(result_parts))
    result = f"₹{formatted}.{decimal_part}"
    
    return f"-{result}" if is_negative else result


def get_fiscal_year(date: Optional[datetime] = None) -> str:
    """Get Indian fiscal year (April to March) for a given date.
    
    Indian fiscal year runs from April 1st to March 31st.
    Format: FY2024-25 means April 2024 to March 2025.
    
    Args:
        date: Date to get fiscal year for (defaults to now)
        
    Returns:
        Fiscal year string in FY2024-25 format
        
    Examples:
        >>> get_fiscal_year(datetime(2024, 10, 15))
        'FY2024-25'
        >>> get_fiscal_year(datetime(2025, 2, 10))
        'FY2024-25'
    """
    if date is None:
        date = datetime.now()
    
    if date.month >= 4:
        # April onwards: current year to next year
        start_year = date.year
        end_year = date.year + 1
    else:
        # Jan-March: previous year to current year
        start_year = date.year - 1
        end_year = date.year
    
    return f"FY{start_year}-{str(end_year)[-2:]}"


def format_amount_in_words(amount: float) -> str:
    """Convert amount to Indian word format for readability.
    
    Converts amounts to shorthand Indian notation:
    - Below 1000: Exact amount
    - 1K to 99K: Thousands
    - 1L to 99L: Lakhs
    - 1Cr+: Crores
    
    Args:
        amount: Amount to format
        
    Returns:
        Human-readable amount string
        
    Examples:
        >>> format_amount_in_words(500)
        '₹500'
        >>> format_amount_in_words(25000)
        '₹25.0K'
        >>> format_amount_in_words(250000)
        '₹2.5 lakhs'
    """
    if amount < 1000:
        return f"₹{amount:.0f}"
    elif amount < 100000:
        # Thousands
        return f"₹{amount/1000:.1f}K"
    elif amount < 10000000:
        # Lakhs
        return f"₹{amount/100000:.1f} lakhs"
    else:
        # Crores
        return f"₹{amount/10000000:.1f} crores"

