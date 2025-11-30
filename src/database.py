"""
Database management for SoNoBot
Handles SQLite database operations with aiosqlite
"""

import aiosqlite
import asyncio
from datetime import datetime
from typing import List, Dict, Optional, Tuple
from .config import config

class Database:
    """Database manager for SoNoBot"""
    
    def __init__(self):
        self.db_path = config.DB_PATH
        self._connection = None
    
    async def init_db(self) -> None:
        """Initialize database tables"""
        async with aiosqlite.connect(self.db_path) as db:
            # Create users table
            await db.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT,
                    full_name TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create transactions table
            await db.execute('''
                CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    debtor_id INTEGER NOT NULL,
                    creditor_id INTEGER NOT NULL,
                    amount INTEGER NOT NULL,
                    note TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (debtor_id) REFERENCES users (user_id),
                    FOREIGN KEY (creditor_id) REFERENCES users (user_id)
                )
            ''')
            
            # Create indexes for better performance
            await db.execute('''
                CREATE INDEX IF NOT EXISTS idx_transactions_debtor 
                ON transactions (debtor_id)
            ''')
            await db.execute('''
                CREATE INDEX IF NOT EXISTS idx_transactions_creditor 
                ON transactions (creditor_id)
            ''')

            # Create System/Group user (ID 0)
            await db.execute('''
                INSERT OR IGNORE INTO users (user_id, username, full_name)
                VALUES (0, 'system', 'Quỹ/Nhóm')
            ''')
            
            await db.commit()
    
    async def get_connection(self) -> aiosqlite.Connection:
        """Get or create database connection"""
        if self._connection is None:
            self._connection = await aiosqlite.connect(self.db_path)
        return self._connection
    
    async def close(self) -> None:
        """Close database connection"""
        if self._connection:
            await self._connection.close()
            self._connection = None
    
    # User operations
    async def add_user(self, user_id: int, username: str = None, full_name: str = None) -> bool:
        """Add a new user or update existing user"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute('''
                    INSERT OR REPLACE INTO users (user_id, username, full_name)
                    VALUES (?, ?, ?)
                ''', (user_id, username, full_name))
                await db.commit()
                return True
        except Exception as e:
            print(f"Error adding user: {e}")
            return False
    
    async def get_user(self, user_id: int) -> Optional[Dict]:
        """Get user by ID"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                db.row_factory = aiosqlite.Row
                cursor = await db.execute(
                    'SELECT * FROM users WHERE user_id = ?', (user_id,)
                )
                row = await cursor.fetchone()
                return dict(row) if row else None
        except Exception as e:
            print(f"Error getting user: {e}")
            return None
    
    async def get_user_by_username(self, username: str) -> Optional[Dict]:
        """Get user by username (without @)"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                db.row_factory = aiosqlite.Row
                cursor = await db.execute(
                    'SELECT * FROM users WHERE username = ?', (username,)
                )
                row = await cursor.fetchone()
                return dict(row) if row else None
        except Exception as e:
            print(f"Error getting user by username: {e}")
            return None
    
    # Transaction operations
    async def add_transaction(self, debtor_id: int, creditor_id: int, amount: int, note: str = None) -> Optional[int]:
        """Add a new transaction"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                cursor = await db.execute('''
                    INSERT INTO transactions (debtor_id, creditor_id, amount, note)
                    VALUES (?, ?, ?, ?)
                ''', (debtor_id, creditor_id, amount, note))
                await db.commit()
                return cursor.lastrowid
        except Exception as e:
            print(f"Error adding transaction: {e}")
            return None
    
    async def get_transaction(self, transaction_id: int) -> Optional[Dict]:
        """Get transaction by ID"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                db.row_factory = aiosqlite.Row
                cursor = await db.execute('''
                    SELECT t.*, 
                           d.username as debtor_username,
                           d.full_name as debtor_name,
                           c.username as creditor_username,
                           c.full_name as creditor_name
                    FROM transactions t
                    JOIN users d ON t.debtor_id = d.user_id
                    JOIN users c ON t.creditor_id = c.user_id
                    WHERE t.id = ?
                ''', (transaction_id,))
                row = await cursor.fetchone()
                return dict(row) if row else None
        except Exception as e:
            print(f"Error getting transaction: {e}")
            return None
    
    async def delete_transaction(self, transaction_id: int, user_id: int) -> bool:
        """Delete transaction (only creditor can delete)"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                # Check if user is creditor
                cursor = await db.execute(
                    'SELECT creditor_id FROM transactions WHERE id = ?',
                    (transaction_id,)
                )
                row = await cursor.fetchone()
                
                if not row or row[0] != user_id:
                    return False
                
                # Delete the transaction
                await db.execute(
                    'DELETE FROM transactions WHERE id = ?', (transaction_id,)
                )
                await db.commit()
                return True
        except Exception as e:
            print(f"Error deleting transaction: {e}")
            return False
    
    async def get_user_debts(self, user_id: int) -> Dict[str, int]:
        """Get user's debt summary"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                # Amount others owe user (user is creditor)
                cursor = await db.execute('''
                    SELECT COALESCE(SUM(amount), 0) as total
                    FROM transactions 
                    WHERE creditor_id = ?
                ''', (user_id,))
                others_owe = (await cursor.fetchone())[0]
                
                # Amount user owes others (user is debtor)
                cursor = await db.execute('''
                    SELECT COALESCE(SUM(amount), 0) as total
                    FROM transactions 
                    WHERE debtor_id = ?
                ''', (user_id,))
                user_owes = (await cursor.fetchone())[0]
                
                return {
                    'others_owe_me': others_owe,
                    'i_owe_others': user_owes,
                    'net_balance': others_owe - user_owes
                }
        except Exception as e:
            print(f"Error getting user debts: {e}")
            return {'others_owe_me': 0, 'i_owe_others': 0, 'net_balance': 0}
    
    async def get_detailed_debts(self, user_id: int) -> Dict:
        """Get detailed debt information for a user"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                db.row_factory = aiosqlite.Row
                
                # People who owe user
                cursor = await db.execute('''
                    SELECT 
                        d.user_id,
                        d.username,
                        d.full_name,
                        COALESCE(SUM(t.amount), 0) as amount
                    FROM transactions t
                    JOIN users d ON t.debtor_id = d.user_id
                    WHERE t.creditor_id = ?
                    GROUP BY d.user_id, d.username, d.full_name
                ''', (user_id,))
                debtors = [dict(row) for row in await cursor.fetchall()]
                
                # People user owes
                cursor = await db.execute('''
                    SELECT 
                        c.user_id,
                        c.username,
                        c.full_name,
                        COALESCE(SUM(t.amount), 0) as amount
                    FROM transactions t
                    JOIN users c ON t.creditor_id = c.user_id
                    WHERE t.debtor_id = ?
                    GROUP BY c.user_id, c.username, c.full_name
                ''', (user_id,))
                creditors = [dict(row) for row in await cursor.fetchall()]
                
                return {
                    'debtors': debtors,  # People who owe user
                    'creditors': creditors  # People user owes
                }
        except Exception as e:
            print(f"Error getting detailed debts: {e}")
            return {'debtors': [], 'creditors': []}

    async def get_total_contribution(self, user_id: int) -> int:
        """
        Get total contribution of a user.
        Calculated as: (Total amount user is Creditor where Debtor is 0) - (Total amount user is Debtor where Creditor is 0)
        """
        try:
            async with aiosqlite.connect(self.db_path) as db:
                # Total Nạp (User -> System)
                cursor = await db.execute('''
                    SELECT COALESCE(SUM(amount), 0)
                    FROM transactions 
                    WHERE creditor_id = ? AND debtor_id = 0
                ''', (user_id,))
                total_nap = (await cursor.fetchone())[0]
                
                # Total Rút (System -> User)
                cursor = await db.execute('''
                    SELECT COALESCE(SUM(amount), 0)
                    FROM transactions 
                    WHERE debtor_id = ? AND creditor_id = 0
                ''', (user_id,))
                total_rut = (await cursor.fetchone())[0]
                
                return total_nap - total_rut
        except Exception as e:
            print(f"Error getting total contribution: {e}")
            return 0
    
    async def get_total_deposit_and_withdrawal(self, user_id: int) -> Dict[str, int]:
        """
        Get total deposit (Nạp) and total withdrawal (Rút) separately for a user.
        
        Returns:
            Dict with keys: 'total_nap', 'total_rut', 'total'
        """
        try:
            async with aiosqlite.connect(self.db_path) as db:
                # Total Nạp (User -> System)
                cursor = await db.execute('''
                    SELECT COALESCE(SUM(amount), 0)
                    FROM transactions 
                    WHERE creditor_id = ? AND debtor_id = 0
                ''', (user_id,))
                total_nap = (await cursor.fetchone())[0]
                
                # Total Rút (System -> User)
                cursor = await db.execute('''
                    SELECT COALESCE(SUM(amount), 0)
                    FROM transactions 
                    WHERE debtor_id = ? AND creditor_id = 0
                ''', (user_id,))
                total_rut = (await cursor.fetchone())[0]
                
                return {
                    'total_nap': total_nap,
                    'total_rut': total_rut,
                    'total': total_nap - total_rut
                }
        except Exception as e:
            print(f"Error getting total deposit and withdrawal: {e}")
            return {'total_nap': 0, 'total_rut': 0, 'total': 0}
    
    async def reset_all_transactions(self) -> bool:
        """
        Reset all transactions - Delete all transaction records (Admin only)
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            async with aiosqlite.connect(self.db_path) as db:
                # Delete all transactions
                await db.execute('DELETE FROM transactions')
                await db.commit()
                return True
        except Exception as e:
            print(f"Error resetting transactions: {e}")
            return False
    
    async def get_transaction_count(self) -> int:
        """
        Get total number of transactions
        
        Returns:
            int: Number of transactions
        """
        try:
            async with aiosqlite.connect(self.db_path) as db:
                cursor = await db.execute('SELECT COUNT(*) FROM transactions')
                count = (await cursor.fetchone())[0]
                return count
        except Exception as e:
            print(f"Error getting transaction count: {e}")
            return 0


# Global database instance
database = Database()