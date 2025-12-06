"""
Money parser for SoNoBot
Handles Vietnamese shorthand money formats: 50k -> 50000, 1.5m -> 1500000
"""

import re
from typing import Optional

def parse_money(text: str) -> int:
    """
    Parse Vietnamese shorthand money format to integer amount
    
    Supported formats:
    - 50k -> 50000
    - 1.5m -> 1500000
    - 200 -> 200
    - 1.2tr -> 1200000 (triệu)
    - 100k, 50k (with commas and dots)
    
    Args:
        text: Money string to parse
        
    Returns:
        int: Amount in VND
        
    Raises:
        ValueError: If format is invalid
    """
    if not text or not isinstance(text, str):
        raise ValueError("Input must be a non-empty string")
    
    # Clean the input - remove spaces, commas, dots (except decimal dots)
    cleaned = text.strip().lower().replace(' ', '').replace(',', '')
    
    # Handle different unit separators
    patterns = [
        # Millions (m, triệu, tr)
        (r'^(\d+\.?\d*)\s*m$', lambda m: int(float(m.group(1)) * 1000000)),  # 1.5m
        (r'^(\d+\.?\d*)\s*triệu$', lambda m: int(float(m.group(1)) * 1000000)),  # 1.5triệu
        (r'^(\d+\.?\d*)\s*tr$', lambda m: int(float(m.group(1)) * 1000000)),    # 1.5tr
        
        # Thousands (k, ngàn, n)
        (r'^(\d+\.?\d*)\s*k$', lambda m: int(float(m.group(1)) * 1000)),         # 50k
        (r'^(\d+\.?\d*)\s*ngàn$', lambda m: int(float(m.group(1)) * 1000)),      # 50ngàn
        (r'^(\d+\.?\d*)\s*n$', lambda m: int(float(m.group(1)) * 1000)),         # 50n
        
        # Plain numbers (treat as VND) - SỬA LỖI: số lẻ parse thành đồng thật
        (r'^(\d+\.\d+)$', lambda m: int(float(m.group(1)))),               # 10.1 -> 10 đồng
        (r'^(\d+)$', lambda m: int(float(m.group(1)))),                    # 200 -> 200 đồng
    ]
    
    for pattern, converter in patterns:
        match = re.match(pattern, cleaned)
        if match:
            try:
                result = converter(match)
                if result <= 0:
                    raise ValueError("Amount must be positive")
                return result
            except (ValueError, OverflowError) as e:
                raise ValueError(f"Invalid number format: {text}")
    
    raise ValueError(f"Cannot parse money format: {text}")


def format_money(amount: int) -> str:
    """
    Format integer amount to simple Vietnamese currency format
    
    Args:
        amount: Amount in VND
        
    Returns:
        str: Formatted money string (đơn giản, hiển thị theo đơn vị k/tr khi phù hợp)
    """
    # Nếu số >= 1 triệu, hiển thị theo triệu
    if amount >= 1000000:
        trieu = amount / 1000000.0
        # Làm tròn đến 1 chữ số thập phân, bỏ số 0 thừa
        trieu_str = f"{trieu:.1f}".rstrip('0').rstrip('.')
        return f"{trieu_str}tr" if trieu_str else "0"
    
    # Nếu số >= 1000, hiển thị theo k (ngàn)
    elif amount >= 1000:
        ngan = amount / 1000.0
        # Làm tròn đến 1 chữ số thập phân, bỏ số 0 thừa
        ngan_str = f"{ngan:.1f}".rstrip('0').rstrip('.')
        return f"{ngan_str}k" if ngan_str else "0"
    
    # Số nhỏ hơn 1000, hiển thị trực tiếp
    else:
        return str(amount)


def extract_mentions(text: str) -> list:
    """
    Extract Telegram mentions from text
    
    Args:
        text: Text to extract mentions from
        
    Returns:
        list: List of usernames (without @)
    """
    # Pattern to match @username
    pattern = r'@(\w+)'
    mentions = re.findall(pattern, text)
    return mentions


def validate_username(username: str) -> bool:
    """
    Validate Telegram username format
    
    Args:
        username: Username to validate
        
    Returns:
        bool: True if valid username
    """
    if not username:
        return False
    
    # Remove @ if present
    username = username.lstrip('@')
    
    # Telegram username rules: 5-32 characters, letters, numbers, underscores
    pattern = r'^[a-zA-Z0-9_]{5,32}$'
    return bool(re.match(pattern, username))


def sanitize_text(text: str) -> str:
    """
    Sanitize text for database storage
    
    Args:
        text: Text to sanitize
        
    Returns:
        str: Sanitized text
    """
    if not text:
        return ""
    
    # Remove potential harmful characters but keep Vietnamese characters
    # Basic sanitization - can be enhanced based on needs
    text = text.strip()
    # Limit length
    text = text[:500] if len(text) > 500 else text
    return text


def parse_command_args(command: str) -> list:
    """
    Parse command arguments from message text
    
    Args:
        command: Command text (e.g., "/no @user 50k coffee")
        
    Returns:
        list: List of arguments
    """
    # Split by spaces but keep quoted text together
    parts = re.findall(r'(?:(?:"[^"]*")|(?:"[^"]*$)|(?:[^\s"])+)', command)
    
    # Remove quotes from quoted parts
    parsed_parts = []
    for part in parts:
        if part.startswith('"') and part.endswith('"'):
            parsed_parts.append(part[1:-1])
        elif part.startswith('"') and not part.endswith('"'):
            parsed_parts.append(part[1:])
        else:
            parsed_parts.append(part)
    
    # Remove the command itself (first part if it starts with /)
    if parsed_parts and parsed_parts[0].startswith('/'):
        # Extract command name and keep the rest as args
        command_name = parsed_parts[0].split()[0]
        args = parsed_parts[1:]
        return [command_name] + args
    
    return parsed_parts