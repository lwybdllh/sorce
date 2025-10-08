import sqlite3
import json
import os
from typing import Optional, List, Dict, Any

class BotDatabase:
    def __init__(self, db_path='bot_data.db'):
        """Initialize database connection and create tables"""
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        self.connect()
        self.create_tables()
    
    def connect(self):
        """Connect to SQLite database"""
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()
    
    def create_tables(self):
        """Create all necessary tables"""
        
        # Groups table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS groups (
                chat_id INTEGER PRIMARY KEY,
                title TEXT,
                is_active INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Group settings table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS group_settings (
                chat_id INTEGER PRIMARY KEY,
                photo_lock TEXT DEFAULT 'o',
                sticker_lock TEXT DEFAULT 'o',
                contact_lock TEXT DEFAULT 'o',
                doc_lock TEXT DEFAULT 'o',
                fwd_lock TEXT DEFAULT 'o',
                voice_lock TEXT DEFAULT 'o',
                link_lock TEXT DEFAULT 'o',
                audio_lock TEXT DEFAULT 'o',
                video_lock TEXT DEFAULT 'o',
                tag_lock TEXT DEFAULT 'o',
                markdown_lock TEXT DEFAULT 'o',
                bots_lock TEXT DEFAULT 'o',
                FOREIGN KEY (chat_id) REFERENCES groups(chat_id) ON DELETE CASCADE
            )
        ''')
        
        # Messages count table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS message_counts (
                chat_id INTEGER,
                user_id INTEGER,
                count INTEGER DEFAULT 0,
                PRIMARY KEY (chat_id, user_id)
            )
        ''')
        
        # Private members table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS private_members (
                user_id INTEGER PRIMARY KEY,
                joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Filters table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS filters (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id INTEGER,
                trigger_text TEXT,
                response_text TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(chat_id, trigger_text)
            )
        ''')
        
        # User points table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_points (
                chat_id INTEGER,
                user_id INTEGER,
                points INTEGER DEFAULT 0,
                PRIMARY KEY (chat_id, user_id)
            )
        ''')
        
        # Custom roles table (developers, creators, managers, admins, distinguished members)
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS custom_roles (
                chat_id INTEGER,
                user_id INTEGER,
                role TEXT,
                PRIMARY KEY (chat_id, user_id, role)
            )
        ''')
        
        # Bot configuration table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS bot_config (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        ''')
        
        # Broadcast mode table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS broadcast_mode (
                user_id INTEGER PRIMARY KEY,
                mode TEXT
            )
        ''')
        
        self.conn.commit()
    
    # ==================== Groups Management ====================
    
    def add_group(self, chat_id: int, title: str = ""):
        """Add a new group"""
        try:
            self.cursor.execute('''
                INSERT OR IGNORE INTO groups (chat_id, title, is_active)
                VALUES (?, ?, 1)
            ''', (chat_id, title))
            self.conn.commit()
            # Also create default settings
            self.cursor.execute('''
                INSERT OR IGNORE INTO group_settings (chat_id)
                VALUES (?)
            ''', (chat_id,))
            self.conn.commit()
        except Exception as e:
            print(f"Error adding group: {e}")
    
    def remove_group(self, chat_id: int):
        """Remove a group"""
        try:
            self.cursor.execute('DELETE FROM groups WHERE chat_id = ?', (chat_id,))
            self.conn.commit()
        except Exception as e:
            print(f"Error removing group: {e}")
    
    def get_all_groups(self) -> List[int]:
        """Get all active group IDs"""
        try:
            self.cursor.execute('SELECT chat_id FROM groups WHERE is_active = 1')
            return [row[0] for row in self.cursor.fetchall()]
        except Exception as e:
            print(f"Error getting groups: {e}")
            return []
    
    def is_group_active(self, chat_id: int) -> bool:
        """Check if group is active"""
        try:
            self.cursor.execute('SELECT is_active FROM groups WHERE chat_id = ?', (chat_id,))
            result = self.cursor.fetchone()
            return result[0] == 1 if result else False
        except Exception as e:
            print(f"Error checking group status: {e}")
            return False
    
    # ==================== Group Settings ====================
    
    def get_group_settings(self, chat_id: int) -> Dict[str, str]:
        """Get group settings"""
        try:
            self.cursor.execute('SELECT * FROM group_settings WHERE chat_id = ?', (chat_id,))
            result = self.cursor.fetchone()
            if result:
                return {
                    'photo_lock': result[1],
                    'sticker_lock': result[2],
                    'contact_lock': result[3],
                    'doc_lock': result[4],
                    'fwd_lock': result[5],
                    'voice_lock': result[6],
                    'link_lock': result[7],
                    'audio_lock': result[8],
                    'video_lock': result[9],
                    'tag_lock': result[10],
                    'markdown_lock': result[11],
                    'bots_lock': result[12]
                }
            else:
                # Return default settings
                return {
                    'photo_lock': 'o', 'sticker_lock': 'o', 'contact_lock': 'o',
                    'doc_lock': 'o', 'fwd_lock': 'o', 'voice_lock': 'o',
                    'link_lock': 'o', 'audio_lock': 'o', 'video_lock': 'o',
                    'tag_lock': 'o', 'markdown_lock': 'o', 'bots_lock': 'o'
                }
        except Exception as e:
            print(f"Error getting group settings: {e}")
            return {}
    
    def update_group_settings(self, chat_id: int, settings: Dict[str, str]):
        """Update group settings"""
        try:
            self.cursor.execute('''
                INSERT OR REPLACE INTO group_settings 
                (chat_id, photo_lock, sticker_lock, contact_lock, doc_lock, fwd_lock,
                 voice_lock, link_lock, audio_lock, video_lock, tag_lock, markdown_lock, bots_lock)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                chat_id,
                settings.get('photo_lock', 'o'),
                settings.get('sticker_lock', 'o'),
                settings.get('contact_lock', 'o'),
                settings.get('doc_lock', 'o'),
                settings.get('fwd_lock', 'o'),
                settings.get('voice_lock', 'o'),
                settings.get('link_lock', 'o'),
                settings.get('audio_lock', 'o'),
                settings.get('video_lock', 'o'),
                settings.get('tag_lock', 'o'),
                settings.get('markdown_lock', 'o'),
                settings.get('bots_lock', 'o')
            ))
            self.conn.commit()
        except Exception as e:
            print(f"Error updating group settings: {e}")
    
    # ==================== Message Counts ====================
    
    def increment_message_count(self, chat_id: int, user_id: int):
        """Increment message count for user in group"""
        try:
            self.cursor.execute('''
                INSERT INTO message_counts (chat_id, user_id, count)
                VALUES (?, ?, 1)
                ON CONFLICT(chat_id, user_id) DO UPDATE SET count = count + 1
            ''', (chat_id, user_id))
            self.conn.commit()
        except Exception as e:
            print(f"Error incrementing message count: {e}")
    
    def get_message_count(self, chat_id: int, user_id: int) -> int:
        """Get message count for user in group"""
        try:
            self.cursor.execute('''
                SELECT count FROM message_counts WHERE chat_id = ? AND user_id = ?
            ''', (chat_id, user_id))
            result = self.cursor.fetchone()
            return result[0] if result else 0
        except Exception as e:
            print(f"Error getting message count: {e}")
            return 0
    
    # ==================== Private Members ====================
    
    def add_private_member(self, user_id: int):
        """Add a private chat member"""
        try:
            self.cursor.execute('''
                INSERT OR IGNORE INTO private_members (user_id) VALUES (?)
            ''', (user_id,))
            self.conn.commit()
        except Exception as e:
            print(f"Error adding private member: {e}")
    
    def get_all_private_members(self) -> List[int]:
        """Get all private members"""
        try:
            self.cursor.execute('SELECT user_id FROM private_members')
            return [row[0] for row in self.cursor.fetchall()]
        except Exception as e:
            print(f"Error getting private members: {e}")
            return []
    
    # ==================== Filters ====================
    
    def add_filter(self, chat_id: int, trigger: str, response: str):
        """Add a filter"""
        try:
            self.cursor.execute('''
                INSERT OR REPLACE INTO filters (chat_id, trigger_text, response_text)
                VALUES (?, ?, ?)
            ''', (chat_id, trigger, response))
            self.conn.commit()
        except Exception as e:
            print(f"Error adding filter: {e}")
    
    def get_filter(self, chat_id: int, trigger: str) -> Optional[str]:
        """Get filter response"""
        try:
            self.cursor.execute('''
                SELECT response_text FROM filters WHERE chat_id = ? AND trigger_text = ?
            ''', (chat_id, trigger))
            result = self.cursor.fetchone()
            return result[0] if result else None
        except Exception as e:
            print(f"Error getting filter: {e}")
            return None
    
    def delete_filter(self, chat_id: int, trigger: str):
        """Delete a filter"""
        try:
            self.cursor.execute('''
                DELETE FROM filters WHERE chat_id = ? AND trigger_text = ?
            ''', (chat_id, trigger))
            self.conn.commit()
        except Exception as e:
            print(f"Error deleting filter: {e}")
    
    def get_all_filters(self, chat_id: int) -> List[tuple]:
        """Get all filters for a group"""
        try:
            self.cursor.execute('''
                SELECT trigger_text, response_text FROM filters WHERE chat_id = ?
            ''', (chat_id,))
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error getting all filters: {e}")
            return []
    
    def delete_all_filters(self, chat_id: int):
        """Delete all filters for a group"""
        try:
            self.cursor.execute('DELETE FROM filters WHERE chat_id = ?', (chat_id,))
            self.conn.commit()
        except Exception as e:
            print(f"Error deleting all filters: {e}")
    
    # ==================== User Points ====================
    
    def add_points(self, chat_id: int, user_id: int, points: int = 1):
        """Add points to user"""
        try:
            self.cursor.execute('''
                INSERT INTO user_points (chat_id, user_id, points)
                VALUES (?, ?, ?)
                ON CONFLICT(chat_id, user_id) DO UPDATE SET points = points + ?
            ''', (chat_id, user_id, points, points))
            self.conn.commit()
        except Exception as e:
            print(f"Error adding points: {e}")
    
    def get_points(self, chat_id: int, user_id: int) -> int:
        """Get user points"""
        try:
            self.cursor.execute('''
                SELECT points FROM user_points WHERE chat_id = ? AND user_id = ?
            ''', (chat_id, user_id))
            result = self.cursor.fetchone()
            return result[0] if result else 0
        except Exception as e:
            print(f"Error getting points: {e}")
            return 0
    
    def reset_points(self, chat_id: int, user_id: int):
        """Reset user points"""
        try:
            self.cursor.execute('''
                UPDATE user_points SET points = 0 WHERE chat_id = ? AND user_id = ?
            ''', (chat_id, user_id))
            self.conn.commit()
        except Exception as e:
            print(f"Error resetting points: {e}")
    
    # ==================== Custom Roles ====================
    
    def add_role(self, chat_id: int, user_id: int, role: str):
        """Add custom role to user"""
        try:
            self.cursor.execute('''
                INSERT OR IGNORE INTO custom_roles (chat_id, user_id, role)
                VALUES (?, ?, ?)
            ''', (chat_id, user_id, role))
            self.conn.commit()
        except Exception as e:
            print(f"Error adding role: {e}")
    
    def remove_role(self, chat_id: int, user_id: int, role: str):
        """Remove custom role from user"""
        try:
            self.cursor.execute('''
                DELETE FROM custom_roles WHERE chat_id = ? AND user_id = ? AND role = ?
            ''', (chat_id, user_id, role))
            self.conn.commit()
        except Exception as e:
            print(f"Error removing role: {e}")
    
    def has_role(self, chat_id: int, user_id: int, role: str) -> bool:
        """Check if user has role"""
        try:
            self.cursor.execute('''
                SELECT 1 FROM custom_roles WHERE chat_id = ? AND user_id = ? AND role = ?
            ''', (chat_id, user_id, role))
            return self.cursor.fetchone() is not None
        except Exception as e:
            print(f"Error checking role: {e}")
            return False
    
    def get_users_by_role(self, chat_id: int, role: str) -> List[int]:
        """Get all users with specific role"""
        try:
            self.cursor.execute('''
                SELECT user_id FROM custom_roles WHERE chat_id = ? AND role = ?
            ''', (chat_id, role))
            return [row[0] for row in self.cursor.fetchall()]
        except Exception as e:
            print(f"Error getting users by role: {e}")
            return []
    
    def delete_all_roles(self, chat_id: int, role: str):
        """Delete all users with specific role"""
        try:
            self.cursor.execute('''
                DELETE FROM custom_roles WHERE chat_id = ? AND role = ?
            ''', (chat_id, role))
            self.conn.commit()
        except Exception as e:
            print(f"Error deleting all roles: {e}")
    
    # ==================== Bot Configuration ====================
    
    def set_config(self, key: str, value: str):
        """Set configuration value"""
        try:
            self.cursor.execute('''
                INSERT OR REPLACE INTO bot_config (key, value) VALUES (?, ?)
            ''', (key, value))
            self.conn.commit()
        except Exception as e:
            print(f"Error setting config: {e}")
    
    def get_config(self, key: str, default: str = "") -> str:
        """Get configuration value"""
        try:
            self.cursor.execute('SELECT value FROM bot_config WHERE key = ?', (key,))
            result = self.cursor.fetchone()
            return result[0] if result else default
        except Exception as e:
            print(f"Error getting config: {e}")
            return default
    
    def delete_config(self, key: str):
        """Delete configuration value"""
        try:
            self.cursor.execute('DELETE FROM bot_config WHERE key = ?', (key,))
            self.conn.commit()
        except Exception as e:
            print(f"Error deleting config: {e}")
    
    # ==================== Broadcast Mode ====================
    
    def set_broadcast_mode(self, user_id: int, mode: str):
        """Set broadcast mode for user"""
        try:
            self.cursor.execute('''
                INSERT OR REPLACE INTO broadcast_mode (user_id, mode) VALUES (?, ?)
            ''', (user_id, mode))
            self.conn.commit()
        except Exception as e:
            print(f"Error setting broadcast mode: {e}")
    
    def get_broadcast_mode(self, user_id: int) -> Optional[str]:
        """Get broadcast mode for user"""
        try:
            self.cursor.execute('SELECT mode FROM broadcast_mode WHERE user_id = ?', (user_id,))
            result = self.cursor.fetchone()
            return result[0] if result else None
        except Exception as e:
            print(f"Error getting broadcast mode: {e}")
            return None
    
    def clear_broadcast_mode(self, user_id: int):
        """Clear broadcast mode for user"""
        try:
            self.cursor.execute('DELETE FROM broadcast_mode WHERE user_id = ?', (user_id,))
            self.conn.commit()
        except Exception as e:
            print(f"Error clearing broadcast mode: {e}")
    
    # ==================== Banned Words ====================
    
    def add_banned_word(self, chat_id: int, word: str):
        """Add banned word for chat"""
        try:
            self.cursor.execute('''
                INSERT OR IGNORE INTO custom_filters (chat_id, trigger, response)
                VALUES (?, ?, ?)
            ''', (chat_id, f"__banned__{word}", "__BANNED__"))
            self.conn.commit()
        except Exception as e:
            print(f"Error adding banned word: {e}")
    
    def remove_banned_word(self, chat_id: int, word: str):
        """Remove banned word for chat"""
        try:
            self.cursor.execute('''
                DELETE FROM custom_filters WHERE chat_id = ? AND trigger = ?
            ''', (chat_id, f"__banned__{word}"))
            self.conn.commit()
        except Exception as e:
            print(f"Error removing banned word: {e}")
    
    def get_all_banned_words(self, chat_id: int) -> list:
        """Get all banned words for chat"""
        try:
            self.cursor.execute('''
                SELECT trigger FROM custom_filters WHERE chat_id = ? AND response = ?
            ''', (chat_id, "__BANNED__"))
            return [row[0].replace("__banned__", "") for row in self.cursor.fetchall()]
        except Exception as e:
            print(f"Error getting banned words: {e}")
            return []
    
    def delete_all_banned_words(self, chat_id: int):
        """Delete all banned words for chat"""
        try:
            self.cursor.execute('''
                DELETE FROM custom_filters WHERE chat_id = ? AND response = ?
            ''', (chat_id, "__BANNED__"))
            self.conn.commit()
        except Exception as e:
            print(f"Error deleting all banned words: {e}")
    
    # ==================== Global Ban ====================
    
    def ban_user_global(self, user_id: int):
        """Ban user globally"""
        try:
            self.cursor.execute('''
                INSERT OR IGNORE INTO global_bans (user_id) VALUES (?)
            ''', (user_id,))
            self.conn.commit()
        except Exception as e:
            print(f"Error banning user globally: {e}")
    
    def unban_user_global(self, user_id: int):
        """Unban user globally"""
        try:
            self.cursor.execute('''
                DELETE FROM global_bans WHERE user_id = ?
            ''', (user_id,))
            self.conn.commit()
        except Exception as e:
            print(f"Error unbanning user globally: {e}")
    
    def is_banned_global(self, user_id: int) -> bool:
        """Check if user is banned globally"""
        try:
            self.cursor.execute('SELECT user_id FROM global_bans WHERE user_id = ?', (user_id,))
            return self.cursor.fetchone() is not None
        except Exception as e:
            print(f"Error checking global ban: {e}")
            return False
    
    def get_all_banned_users(self) -> list:
        """Get all globally banned users"""
        try:
            self.cursor.execute('SELECT user_id FROM global_bans')
            return [row[0] for row in self.cursor.fetchall()]
        except Exception as e:
            print(f"Error getting banned users: {e}")
            return []
    
    def clear_all_banned_users(self):
        """Clear all globally banned users"""
        try:
            self.cursor.execute('DELETE FROM global_bans')
            self.conn.commit()
        except Exception as e:
            print(f"Error clearing banned users: {e}")
    
    # ==================== Utility Methods ====================
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()