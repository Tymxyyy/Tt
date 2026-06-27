"""
数据库操作模块
处理 SQLite 数据库的初始化和操作
"""

import sqlite3
import os
from datetime import datetime
from typing import List, Tuple, Optional

DB_FILE = "checkin.db"


def init_db():
    """初始化数据库表"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS checkins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            note TEXT,
            UNIQUE(date)
        )
    ''')
    
    conn.commit()
    conn.close()


def add_checkin(note: str = "") -> bool:
    """
    添加打卡记录
    
    Args:
        note: 打卡备注
        
    Returns:
        bool: 是否成功
    """
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        today = datetime.now().strftime("%Y-%m-%d")
        current_time = datetime.now().strftime("%H:%M:%S")
        
        cursor.execute('''
            INSERT OR REPLACE INTO checkins (date, time, note)
            VALUES (?, ?, ?)
        ''', (today, current_time, note))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"❌ 数据库错误: {e}")
        return False


def get_today_checkin() -> Optional[Tuple]:
    """
    获取今天的打卡记录
    
    Returns:
        tuple: (date, time, note) 或 None
    """
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        today = datetime.now().strftime("%Y-%m-%d")
        cursor.execute('SELECT date, time, note FROM checkins WHERE date = ?', (today,))
        result = cursor.fetchone()
        
        conn.close()
        return result
    except Exception as e:
        print(f"❌ 数据库错误: {e}")
        return None


def get_history(days: int = 30) -> List[Tuple]:
    """
    获取最近 N 天的打卡记录
    
    Args:
        days: 天数
        
    Returns:
        list: 打卡记录列表
    """
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT date, time, note FROM checkins
            ORDER BY date DESC
            LIMIT ?
        ''', (days,))
        results = cursor.fetchall()
        
        conn.close()
        return results
    except Exception as e:
        print(f"❌ 数据库错误: {e}")
        return []


def get_stats() -> dict:
    """
    获取打卡统计信息
    
    Returns:
        dict: 包含各项统计数据
    """
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        # 总打卡次数
        cursor.execute('SELECT COUNT(*) FROM checkins')
        total_count = cursor.fetchone()[0]
        
        # 本月打卡次数
        cursor.execute('''
            SELECT COUNT(*) FROM checkins 
            WHERE date LIKE ?
        ''', (datetime.now().strftime("%Y-%m") + "%",))
        month_count = cursor.fetchone()[0]
        
        # 连续打卡天数
        cursor.execute('SELECT date FROM checkins ORDER BY date DESC LIMIT 100')
        dates = [row[0] for row in cursor.fetchall()]
        
        consecutive_days = 0
        if dates:
            from datetime import timedelta
            current_date = datetime.now().date()
            for i, date_str in enumerate(dates):
                date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
                expected_date = current_date - timedelta(days=i)
                if date_obj == expected_date:
                    consecutive_days += 1
                else:
                    break
        
        # 本月天数和打卡率
        import calendar
        year = datetime.now().year
        month = datetime.now().month
        days_in_month = calendar.monthrange(year, month)[1]
        checkin_rate = (month_count / days_in_month * 100) if days_in_month > 0 else 0
        
        conn.close()
        
        return {
            'total': total_count,
            'month': month_count,
            'consecutive': consecutive_days,
            'rate': checkin_rate,
            'days_in_month': days_in_month
        }
    except Exception as e:
        print(f"❌ 数据库错误: {e}")
        return {}


def clear_all() -> bool:
    """
    清空所有记录（仅用于测试）
    
    Returns:
        bool: 是否成功
    """
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM checkins')
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"❌ 数据库错误: {e}")
        return False
