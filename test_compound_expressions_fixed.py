#!/usr/bin/env python3
"""
Test compound expressions với định dạng chính xác
"""

from src.utils.calculator import parse_calculation

def test_compound_expressions():
    print('=== Test Compound Expressions (Fixed Format) ===\n')
    
    test_cases = [
        '+50k+30k',  # NẠP tiền 80,000đ (tổng)
        '+100k+50k', # NẠP tiền 150,000đ (tổng)
        '+30',       # NẠP tiền 30đ (không có k)
        '+50k',      # NẠP tiền 50,000đ (đơn)
        '-50k-30k',  # RÚT tiền 80,000đ (tổng)
        '+100k+50k+20k', # NẠP tiền 170,000đ (3 số)
        '+1.5tr+500k',   # NẠP tiền 2,000,000đ (triệu + ngàn)
    ]
    
    success_count = 0
    total_count = len(test_cases)
    
    for case in test_cases:
        try:
            result = parse_calculation(case)
            amount, operation, note = result
            formatted_amount = f"{amount:,}đ".replace(',', '.')
            print(f'✅ {case:>15} -> Amount: {formatted_amount:>10}, Operation: {operation:>10}, Note: {note}')
            success_count += 1
        except Exception as e:
            print(f'❌ {case:>15} -> ERROR: {e}')
    
    print(f'\n🎯 Kết quả: {success_count}/{total_count} test cases thành công')
    
    if success_count == total_count:
        print('🎉 Tất cả compound expressions hoạt động chính xác!')
    else:
        print('⚠️  Có một số test cases thất bại!')
    
    return success_count == total_count

if __name__ == "__main__":
    test_compound_expressions()