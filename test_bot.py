#!/usr/bin/env python3
"""
Simple test script for SoNoBot
"""

import asyncio
from src.config import config
from src.bot import bot
from src.database import database
from src.utils.parser import parse_money, format_money

async def test_all():
    """Test all components"""
    print("🧪 Testing SoNoBot components...")
    
    # Test configuration
    print("\n1. Testing configuration...")
    if config.validate():
        print("✅ Configuration valid")
    else:
        print("❌ Configuration invalid")
        return False
    
    # Test parser
    print("\n2. Testing money parser...")
    test_cases = ['50k', '1.5tr', '200', '1000']
    for case in test_cases:
        try:
            parsed = parse_money(case)
            formatted = format_money(parsed)
            print(f"   {case} -> {parsed} -> {formatted}")
        except Exception as e:
            print(f"   ❌ {case}: {e}")
    
    # Test database
    print("\n3. Testing database...")
    try:
        await database.init_db()
        print("✅ Database initialized")
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False
    
    # Test SafeW API
    print("\n4. Testing SafeW API...")
    try:
        await bot.start()
        bot_info = await bot.get_me()
        if bot_info and bot_info.get('ok'):
            result = bot_info['result']
            print(f"✅ Connected to: {result.get('username')}")
            print(f"   Name: {result.get('first_name')}")
        else:
            print("❌ Failed to get bot info")
            return False
    except Exception as e:
        print(f"❌ API error: {e}")
        return False
    finally:
        await bot.close()
    
    print("\n🎉 All tests passed!")
    return True

if __name__ == "__main__":
    result = asyncio.run(test_all())
    print(f"\nFinal result: {'SUCCESS' if result else 'FAILED'}")