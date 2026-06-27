"""
工具函数模块
提供各种辅助功能
"""

from datetime import datetime
from tabulate import tabulate


def format_datetime(datetime_str: str) -> str:
    """格式化日期时间"""
    try:
        dt = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except:
        return datetime_str


def print_success(message: str):
    """打印成功消息"""
    print(f"✅ {message}")


def print_error(message: str):
    """打印错误消息"""
    print(f"❌ {message}")


def print_info(message: str):
    """打印信息消息"""
    print(f"ℹ️  {message}")


def print_table(data: list, headers: list):
    """打印表格"""
    if not data:
        print_info("暂无数据")
        return
    print(tabulate(data, headers=headers, tablefmt="grid"))


def print_separator():
    """打印分隔线"""
    print("-" * 50)


def get_current_date() -> str:
    """获取当前日期"""
    return datetime.now().strftime("%Y-%m-%d")


def get_current_time() -> str:
    """获取当前时间"""
    return datetime.now().strftime("%H:%M:%S")


def get_current_datetime() -> str:
    """获取当前日期时间"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
