#!/usr/bin/env python3
"""
Test script for calculator functionality
"""

import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from utils.calculator import parse_calculation, generate_calculation_help, format_calculation_result
from utils.parser import parse_money, format_money

def test_calculator():
    """Test calculator functionality"""
    print("🧮 Testing calculator functionality...")
    
    # Test cases
    test_cases = [
        "+50k",
        "-100k", 
        "+1.5tr cafe",
        "-200k",
        "+1000000",
        "+50k trưa sáng",
        "-50000",
    ]
    
    print("\n📝 Test Cases:")
    for case in test_cases:
        result = parse_calculation(case)
        if result:
            amount, operation, note = result
            formatted = format_money(amount)
            print(f"✅ '{case}' -> {operation}: {formatted} (note: {note})")
        else:
            print(f"❌ '{case}' -> Failed to parse")
    
    # Test help
    print("\n📖 Help Text:")
    print(generate_calculation_help())
    
    print("\n✅ Calculator test completed!")

if __name__ == "__main__":
    test_calculator()