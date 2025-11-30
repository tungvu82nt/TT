#!/usr/bin/env python3
"""Test script for decimal money parsing fix"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.utils.parser import parse_money, format_money
from src.utils.calculator import parse_calculation, format_calculation_result

def test_decimal_parsing():
    """Test decimal money parsing"""
    print("🔧 Testing Decimal Money Parsing Fix...")
    
    # Test cases
    test_cases = [
        # Format: (input, expected_output, description)
        ("10.1", 10.1, "Số lẻ không đơn vị"),
        ("50.5", 50.5, "Số lẻ lớn hơn"),
        ("100.25", 100.25, "Số lẻ có 2 chữ số thập phân"),
        ("+10.1", 10.1, "Với dấu +"),
        ("-10.1", 10.1, "Với dấu -"),
    ]
    
    print("\n📊 Test Results:")
    all_passed = True
    
    for input_text, expected, desc in test_cases:
        try:
            result = parse_money(input_text.replace('+', '').replace('-', ''))
            status = "✅ PASS" if result == int(expected * 1000) or abs(result - expected) < 0.1 else "❌ FAIL"
            if status == "❌ FAIL":
                all_passed = False
            print(f"{status} {desc}: '{input_text}' → {result} (expected ~{expected})")
        except Exception as e:
            print(f"❌ FAIL {desc}: '{input_text}' → Error: {e}")
            all_passed = False
    
    return all_passed

def test_calculation_formatting():
    """Test calculation result formatting"""
    print("\n💰 Testing Calculation Result Formatting...")
    
    test_cases = [
        # Format: (amount, operation, note, expected_contains)
        (10100, "add", None, "Nạp : 10.1k"),
        (10100, "add", "test", "Nạp : 10.1k (test)"),
        (5050, "subtract", None, "Rút : 5.05k"),
    ]
    
    print("\n📊 Test Results:")
    all_passed = True
    
    for amount, operation, note, expected in test_cases:
        try:
            result = format_calculation_result(amount, operation, note)
            status = "✅ PASS" if expected in result else "❌ FAIL"
            if status == "❌ FAIL":
                all_passed = False
            print(f"{status} Amount {amount}: '{result}' (expected contains '{expected}')")
        except Exception as e:
            print(f"❌ FAIL Amount {amount}: Error: {e}")
            all_passed = False
    
    return all_passed

def test_compound_expressions():
    """Test compound expressions with decimals"""
    print("\n🔄 Testing Compound Expressions with Decimals...")
    
    test_cases = [
        ("+10.1+5.5", "add", 15600),  # 10.1 + 5.5 = 15.6k
        ("+10.1+5.5", "add", 15600),
        ("-10.1+2.5", "subtract", 7600),  # -(10.1 - 2.5) = -7.6k
    ]
    
    print("\n📊 Test Results:")
    all_passed = True
    
    for expr, expected_op, expected_amount in test_cases:
        try:
            result = parse_calculation(expr)
            if result:
                amount, operation, note = result
                status = "✅ PASS" if operation == expected_op and abs(amount - expected_amount) < 100 else "❌ FAIL"
                if status == "❌ FAIL":
                    all_passed = False
                print(f"{status} Expression '{expr}': {amount} {operation} (expected {expected_amount} {expected_op})")
            else:
                print(f"❌ FAIL Expression '{expr}': Could not parse")
                all_passed = False
        except Exception as e:
            print(f"❌ FAIL Expression '{expr}': Error: {e}")
            all_passed = False
    
    return all_passed

if __name__ == "__main__":
    print("🚀 SoNoBot Decimal Fix Test Suite")
    print("=" * 50)
    
    parser_pass = test_decimal_parsing()
    formatting_pass = test_calculation_formatting()
    compound_pass = test_compound_expressions()
    
    print("\n" + "=" * 50)
    print("📈 FINAL RESULTS:")
    print(f"Parser Tests: {'✅ PASS' if parser_pass else '❌ FAIL'}")
    print(f"Formatting Tests: {'✅ PASS' if formatting_pass else '❌ FAIL'}")
    print(f"Compound Tests: {'✅ PASS' if compound_pass else '❌ FAIL'}")
    
    overall_pass = parser_pass and formatting_pass and compound_pass
    print(f"\n🎯 OVERALL: {'✅ ALL TESTS PASSED' if overall_pass else '❌ SOME TESTS FAILED'}")
    
    if overall_pass:
        print("\n🎉 Số lẻ đã được hỗ trợ! Test bot với +10.1 để xem kết quả.")
    else:
        print("\n⚠️  Vẫn còn lỗi cần sửa.")
    
    sys.exit(0 if overall_pass else 1)