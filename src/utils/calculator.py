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
    +7.3 + 12.8 + 7.8 -> (27900, "add", None) - Expressions with spaces
    -100k -> (100000, "subtract", None) 
    +50k cafe -> (50000, "add_debt", "cafe")
    -200k -> (200000, "payment", None)
    nạp 50 -> (50000, "add", None) - **NEW**: Keyword support
    rút 100k -> (100000, "subtract", None) - **NEW**: Keyword support
    
    Args:
        text: Calculation expression to parse
        
    Returns:
        Tuple of (amount, operation_type, note) or None if invalid
    """
    if not text or not isinstance(text, str):
        return None
    
    text = text.strip().lower()
    
    # ------------------------
    # Kiểm tra từ khóa nạp/rút
    # ------------------------
    keyword_patterns = [
        # Từ khóa nạp/rút - chấp nhận cả nạp/nap và rút/rut
        (r'^(nap|nạp)\s+([0-9]+(?:\.[0-9]+)?(?:tr|triệu|k|r)?)$', 'add'),
        (r'^(rut|rút)\s+([0-9]+(?:\.[0-9]+)?(?:tr|triệu|k|r)?)$', 'subtract'),
        
        # Từ khóa nạp/rút với ghi chú - chấp nhận cả nạp/nap và rút/rut
        (r'^(nap|nạp)\s+([0-9]+(?:\.[0-9]+)?(?:tr|triệu|k|r)?)\s+(.+)$', 'add_debt'),
        (r'^(rut|rút)\s+([0-9]+(?:\.[0-9]+)?(?:tr|triệu|k|r)?)\s+(.+)$', 'payment'),
    ]
    
    for pattern, operation in keyword_patterns:
        match = re.match(pattern, text)
        if match:
            money_part = match.group(2)  # group(1) is the keyword, group(2) is the amount
            try:
                amount = parse_money(money_part)
                note = match.group(3) if len(match.groups()) > 2 else None
                return amount, operation, note
            except ValueError:
                continue
    
    # ------------------------
    # Xử lý các định dạng khác
    # ------------------------
    
    # ✅ Nếu không bắt đầu bằng +/-, tự động thêm + (mặc định là NẠP)
    if not text.startswith(('+', '-')):
        text = '+' + text
    
    # Check for compound expressions (multiple + or - signs)
    has_multiple_operations = len(re.findall(r'[+\-]', text)) > 1
    
    if has_multiple_operations:
        # Extract all parts with their operation signs, including spaces and decimal numbers
        parts_pattern = r'([+\-])\s*([0-9]+(?:\.[0-9]+)?(?:triệu|tr|k|r|million)?)'
        parts_matches = re.findall(parts_pattern, text)
        
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
        
        # Logic đơn giản hơn - dựa vào dấu đầu tiên
        if first_operation == '+':
            operation = 'add'  # Bắt đầu bằng + là NẠP
        else:  # first_operation == '-'
            operation = 'subtract'  # Bắt đầu bằng - là RÚT
            
        return abs(total_amount), operation, None
    
    # Pattern for simple arithmetic with money
    patterns = [
        # Simple add/subtract with money - hỗ trợ đầy đủ đơn vị k, tr, r
        (r'^\+\s*([0-9]+(?:\.[0-9]+)?(?:tr|triệu|k|r)?)$', 'add'),
        (r'^\-\s*([0-9]+(?:\.[0-9]+)?(?:tr|triệu|k|r)?)$', 'subtract'),
        
        # Add/subtract with money and note
        (r'^\+\s*([0-9]+(?:\.[0-9]+)?(?:tr|triệu|k|r)?)\s+(.+)$', 'add_debt'),
        (r'^\-\s*([0-9]+(?:\.[0-9]+)?(?:tr|triệu|k|r)?)\s+(.+)$', 'payment'),
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
• `10k` - NẠP tiền 10,000đ (không cần tiền tố, mặc định là nạp)
• `+50k` - NẠP tiền 50,000đ
• `-50k` - RÚT tiền 50,000đ  
• `nạp 10k` - NẠP tiền 10,000đ (từ khóa)
• `rút 50k` - RÚT tiền 50,000đ (từ khóa)
• `100k cafe` - NẠP tiền 100,000đ (ghi chú: cafe)
• `+100k cafe` - NẠP tiền 100,000đ (ghi chú: cafe)
• `nạp 100k cafe` - NẠP tiền 100,000đ (ghi chú: cafe)
• `-200k` - RÚT tiền 200,000đ
• `rút 200k` - RÚT tiền 200,000đ
• `50k+30k` - NẠP tiền tổng 80,000đ (không cần tiền tố)
• `+100k+50k` - NẠP tiền tổng 150,000đ

**Ví dụ thực tế:**
• `100k` → NẠP tiền 100,000đ
• `50` → NẠP tiền 50,000đ  
• `-50k` → RÚT tiền 50,000đ
• `nạp 50` → NẠP tiền 50,000đ
• `rút 50k` → RÚT tiền 50,000đ
• `1.5tr trưa` → NẠP tiền 1,500,000đ (trưa)
• `nạp 1.5tr trưa` → NẠP tiền 1,500,000đ (trưa)
• `100k+50k` → NẠP tiền 150,000đ (tính tổng nhiều số)

💡 **Mẹo:** 
• Không cần tiền tố cho nạp tiền (mặc định là nạp)
• Dùng dấu - hoặc từ "rút" để rút tiền!
• Dùng từ "nạp" để nạp tiền rõ ràng!
• Có thể cộng nhiều số tiền cùng lúc như 50k+30k!
• Lưu ý: Với số nhỏ không có k, chỉ tính đơn vị đồng (ví dụ: 30 = 30đ)
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