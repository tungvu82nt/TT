#!/usr/bin/env python3
"""Check format_money function output"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.utils.parser import format_money
from src.utils.calculator import parse_calculation, format_calculation_result

def check_format():
    """Test format_money directly"""
    print("🧪 Testing format_money function...")
    
    # Test cases
    test_amounts = [10100, 15600, 50250, 101000]
    
    print("\n📋 Direct format_money tests:")
    print("=" * 50)
    
    for amount in test_amounts:
        formatted = format_money(amount)
        print(f"Amount: {amount} VND")
        print(f"Formatted: '{formatted}'")
        print("-" * 30)
    
    print("\n📋 Full calculation tests:")
    print("=" * 50)
    
    test_expressions = ["+10.1", "+10.5", "+15.6"]
    
    for expr in test_expressions:
        result = parse_calculation(expr)
        if result:
            amount, operation, note = result
            formatted = format_calculation_result(amount, operation, note)
            print(f"Expression: {expr}")
            print(f"Full result: '{formatted}'")
            print("-" * 30)

if __name__ == "__main__":
    check_format()