"""Utility functions for formatting and calculations."""


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

