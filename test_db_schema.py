#!/usr/bin/env python3
"""
Test script để kiểm tra database schema
"""
import sqlite3

def check_database():
    """Kiểm tra database schema và dữ liệu"""
    
    print("=== Database Schema Check ===")
    
    try:
        conn = sqlite3.connect('sonobot.db')
        cursor = conn.cursor()
        
        # Lấy schema của transactions table
        cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='transactions'")
        schema = cursor.fetchone()
        
        if schema:
            print("Transactions table schema:")
            print(schema[0])
            print()
            
            # Lấy column info
            cursor.execute("PRAGMA table_info(transactions)")
            columns = cursor.fetchall()
            print("Columns:")
            for col in columns:
                print(f"  {col[1]}: {col[2]}")
                
            print()
            
            # Đếm số records
            cursor.execute("SELECT COUNT(*) FROM transactions")
            count = cursor.fetchone()[0]
            print(f"Total transactions: {count}")
            
            # Lấy một vài records gần đây
            cursor.execute("SELECT * FROM transactions ORDER BY created_at DESC LIMIT 5")
            recent = cursor.fetchall()
            
            if recent:
                print("\nRecent transactions:")
                for record in recent:
                    print(f"  {record}")
                    
        else:
            print("Table transactions not found")
            
        conn.close()
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_database()