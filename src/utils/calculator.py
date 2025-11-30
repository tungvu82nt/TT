"""
Calculator utility for SoNoBot
Handles simple arithmetic operations and money expressions
"""

import re
from typing import Optional, Tuple, Union
from .parser import parse_money, format_money

def parse_calculation(text: str) -> Optional[Tuple[int, str, Optional[str]]]:
    """
    Parse calculation expression and return (amount, operation, note)
    
    Supported formats:
    +50 -> (50000, "add", None)
    +30+30 -> (60000, "add", None) - **NEW**: Compound expressions
    -100k -> (100000, "subtract", None) 
    +50k cafe -> (50000, "add_debt", "cafe")
    -200k -> (200000, "payment", None)
    
    Args:
        text: Calculation expression to parse
        
    Returns:
        Tuple of (amount, operation_type, note) or None if invalid
    """
    if not text or not isinstance(text, str):
        return None
    
    text = text.strip()
    
    # Handle compound expressions like +30+30 or +1.5tr+500k - CHỮA LỖI: thêm số lẻ không đơn vị
    compound_pattern = r'^([+\-])\s*([0-9]+(?:\.[0-9]+)?(?:triệu|tr|[kmtm]|million)?)([+\-]\s*[0-9]+(?:\.[0-9]+)?(?:triệu|tr|[kmtm]|million)?)+'
    compound_match = re.match(compound_pattern, text.lower())
    
    if not compound_match:
        # CHỮA LỖI: Xử lý compound với số lẻ không đơn vị như +10.1+5.5
        compound_pattern_new = r'^([+\-])\s*([0-9]+(?:\.[0-9]+)?)([+\-]\s*[0-9]+(?:\.[0-9]+)?)+'
        compound_match = re.match(compound_pattern_new, text.lower())
    
    if compound_match:
        # CHỮA LỖI: Xử lý compound expression đúng logic
        
        # Extract all parts with their operation signs
        parts_pattern = r'([+\-])\s*([0-9]+(?:\.[0-9]+)?(?:triệu|tr|[kmtm]|million)?)'
        parts_matches = re.findall(parts_pattern, text.lower())
        
        if not parts_matches:
            return None
        
        # Calculate total amount by applying operations sequentially
        total_amount = 0
        first_operation = parts_matches[0][0]  # First operation determines the type
        
        for sign, amount_str in parts_matches:
            try:
                amount = parse_money(amount_str)
                if sign == '+':
                    total_amount += amount
                else:  # sign == '-'
                    total_amount -= amount
            except ValueError:
                continue
        
        # CHỮA LỖI: Logic đơn giản hơn - dựa vào dấu đầu tiên
        if first_operation == '+':
            operation = 'add'  # Bắt đầu bằng + là NẠP
        else:  # first_operation == '-'
            operation = 'subtract'  # Bắt đầu bằng - là RÚT
            
        return abs(total_amount), operation, None
    
    # Pattern for simple arithmetic with money
    patterns = [
        # Simple add/subtract with money - CHỮA LỖI: thêm số lẻ
        (r'^\+\s*([0-9]+(?:\.[0-9]+)?[ktr]?)$', 'add'),
        (r'^\-\s*([0-9]+(?:\.[0-9]+)?[ktr]?)$', 'subtract'),
        
        # Add/subtract with money and note - CHỮA LỖI: thêm số lẻ
        (r'^\+\s*([0-9]+(?:\.[0-9]+)?[ktr]?)\s+(.+)$', 'add_debt'),
        (r'^\-\s*([0-9]+(?:\.[0-9]+)?[ktr]?)\s+(.+)$', 'payment'),
        
        # Just money amount (assume add) - CHỮA LỖI: thêm số lẻ
        (r'^([0-9]+(?:\.[0-9]+)?[ktr]?)$', 'add'),
    ]
    
    for pattern, operation in patterns:
        match = re.match(pattern, text.lower())
        if match:
            money_part = match.group(1)
            try:
                amount = parse_money(money_part)
                note = match.group(2) if len(match.groups()) > 1 else None
                return amount, operation, note
            except ValueError:
                continue
    
    return None

def generate_calculation_help() -> str:
    """Generate help text for calculation expressions"""
    return """
🧮 **Nhập liệu nhanh với công thức**

**Định dạng hỗ trợ:**
• `+50k` - NẠP tiền 50,000đ
• `-50k` - RÚT tiền 50,000đ  
• `+100k cafe` - NẠP tiền 100,000đ (ghi chú)
• `-200k` - RÚT tiền 200,000đ
• `+50k+30k` - NẠP tiền tổng 80,000đ ⭐ **MỚI!**
• `+100k+50k` - NẠP tiền tổng 150,000đ ⭐ **MỚI!**

**Ví dụ thực tế:**
• `+50k` → NẠP tiền 50,000đ
• `-50k` → RÚT tiền 50,000đ
• `+1.5tr trưa` → NẠP tiền 1,500,000đ (trưa)
• `+50k+30k` → NẠP tiền 80,000đ (tính tổng nhiều số)

💡 **Mẹo:** 
• Dùng dấu + để NẠP tiền, - để RÚT tiền!
• **MỚI**: Có thể cộng nhiều số tiền cùng lúc như +50k+30k!
• **Lưu ý**: Với số nhỏ không có k, chỉ tính đơn vị đồng (ví dụ: +30 = 30đ)
    """.strip()

def format_calculation_result(amount: int, operation: str, note: str = None) -> str:
    """Format calculation result into user-friendly message"""
    amount_formatted = format_money(amount)
    note_text = f" ({note})" if note else ""
    
    if operation in ['add', 'add_debt']:
        return f"Nạp : {amount_formatted}{note_text}"
    elif operation in ['subtract', 'payment']:
        return f"Rút : {amount_formatted}{note_text}"
    else:
        return f"Giao dịch: {amount_formatted}{note_text}"