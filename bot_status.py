#!/usr/bin/env python3
"""
SoNoBot Status Check
Check all components and configuration
"""

import asyncio
import sys
import os
from pathlib import Path

def check_environment():
    """Check environment setup"""
    print("🔧 Checking Environment...")
    
    # Check Python version
    print(f"   Python: {sys.version}")
    
    # Check current directory
    print(f"   Directory: {os.getcwd()}")
    
    # Check required files
    required_files = [
        '.env',
        'main.py', 
        'start_bot.py',
        'requirements.txt',
        'src/',
        'src/config.py',
        'src/bot.py', 
        'src/database.py'
    ]
    
    for file in required_files:
        path = Path(file)
        status = "✅" if path.exists() else "❌"
        print(f"   {file}: {status}")
    
    return True

async def check_configuration():
    """Check configuration"""
    print("\n⚙️ Checking Configuration...")
    
    try:
        from src.config import config
        
        # Check token
        if config.BOT_TOKEN:
            print(f"   BOT_TOKEN: ✅ ({config.BOT_TOKEN[:10]}...)")
        else:
            print("   BOT_TOKEN: ❌ Missing")
            return False
        
        # Check admin ID
        if config.ADMIN_ID:
            print(f"   ADMIN_ID: ✅ ({config.ADMIN_ID})")
        else:
            print("   ADMIN_ID: ⚠️ Not set")
        
        # Check other settings
        print(f"   DB_PATH: ✅ ({config.DB_PATH})")
        print(f"   LOG_LEVEL: ✅ ({config.LOG_LEVEL})")
        
        return True
    except Exception as e:
        print(f"   Config error: ❌ {e}")
        return False

async def check_database():
    """Check database connection"""
    print("\n🗄️ Checking Database...")
    
    try:
        from src.database import database
        from src.config import config
        await database.init_db()
        
        # Check if database file exists
        if Path(config.DB_PATH).exists():
            size = Path(config.DB_PATH).stat().st_size
            print(f"   Database: ✅ ({size} bytes)")
        else:
            print("   Database: ⚠️ Will be created")
        
        await database.close()
        return True
    except Exception as e:
        print(f"   Database error: ❌ {e}")
        return False

async def check_bot_connection():
    """Check SafeW API connection"""
    print("\n🤖 Checking SafeW API...")
    
    try:
        from src.bot import bot
        await bot.start()
        
        bot_info = await bot.get_me()
        if bot_info and bot_info.get('ok'):
            result = bot_info['result']
            print(f"   Connection: ✅")
            print(f"   Bot Name: ✅ {result.get('username')}")
            print(f"   Bot ID: ✅ {result.get('id')}")
            print(f"   Bot Name: ✅ {result.get('first_name')}")
        else:
            print("   Connection: ❌ Failed to get bot info")
            return False
        
        await bot.close()
        return True
    except Exception as e:
        print(f"   API error: ❌ {e}")
        return False

def check_dependencies():
    """Check Python dependencies"""
    print("\n📦 Checking Dependencies...")
    
    try:
        import aiohttp
        print(f"   aiohttp: ✅ ({aiohttp.__version__})")
    except ImportError:
        print("   aiohttp: ❌ Missing")
        return False
    
    try:
        import aiosqlite
        print(f"   aiosqlite: ✅")
    except ImportError:
        print("   aiosqlite: ❌ Missing")
        return False
    
    try:
        import dotenv
        print(f"   python-dotenv: ✅")
    except ImportError:
        print("   python-dotenv: ❌ Missing")
        return False
    
    return True

def check_parser():
    """Check money parser"""
    print("\n💰 Checking Parser...")
    
    try:
        from src.utils.parser import parse_money, format_money
        
        test_cases = [
            ("50k", 50000),
            ("1.5tr", 1500000),
            ("200", 200),
            ("100k", 100000)
        ]
        
        for input_val, expected in test_cases:
            try:
                result = parse_money(input_val)
                formatted = format_money(result)
                status = "✅" if result == expected else "❌"
                print(f"   '{input_val}' -> {result} -> {formatted} {status}")
            except Exception as e:
                print(f"   '{input_val}' -> ❌ {e}")
                return False
        
        return True
    except Exception as e:
        print(f"   Parser error: ❌ {e}")
        return False

async def main():
    """Main status check"""
    print("🔍 SoNoBot Status Check\n")
    
    checks = [
        ("Environment", check_environment),
        ("Dependencies", check_dependencies), 
        ("Parser", check_parser),
        ("Configuration", check_configuration),
        ("Database", check_database),
        ("SafeW API", check_bot_connection)
    ]
    
    results = []
    for name, check_func in checks:
        try:
            if asyncio.iscoroutinefunction(check_func):
                result = await check_func()
            else:
                result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"   {name} check failed: ❌ {e}")
            results.append((name, False))
    
    # Summary
    print("\n" + "="*50)
    print("📋 SUMMARY")
    print("="*50)
    
    all_passed = True
    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{name:20s} {status}")
        if not passed:
            all_passed = False
    
    print("="*50)
    if all_passed:
        print("🎉 ALL CHECKS PASSED - Bot is ready!")
        print("\n🚀 To start bot: python start_bot.py")
        print("📱 Or use main.py: python main.py")
    else:
        print("⚠️ SOME CHECKS FAILED - Fix issues before starting")
    
    return all_passed

if __name__ == "__main__":
    result = asyncio.run(main())
    sys.exit(0 if result else 1)