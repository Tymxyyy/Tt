#!/usr/bin/env python3
"""
打卡工具 - 每日打卡管理系统
使用 SQLite 本地存储，支持命令行操作
"""

import click
import sys
from datetime import datetime
from db import init_db, add_checkin, get_today_checkin, get_history, get_stats
from utils import (
    print_success, print_error, print_info, print_table, 
    print_separator, get_current_datetime
)


@click.group()
def cli():
    """🎯 打卡工具 - 每日打卡管理系统"""
    init_db()


@cli.command()
@click.option('--note', '-n', default='', help='打卡备注')
def check(note):
    """📍 记录打卡"""
    if add_checkin(note):
        now = get_current_datetime()
        print_success(f"打卡成功！时间：{now}")
        if note:
            print_info(f"备注：{note}")
    else:
        print_error("打卡失败，请重试")
        sys.exit(1)


@cli.command()
def today():
    """👁️  查看今天的打卡记录"""
    checkin = get_today_checkin()
    
    if checkin:
        date, time, note = checkin
        print_info(f"今天的打卡记录")
        print_separator()
        print(f"📅 日期：{date}")
        print(f"🕐 时间：{time}")
        if note:
            print(f"📝 备注：{note}")
        else:
            print(f"📝 备注：无")
    else:
        print_info("今天还没有打卡记录")


@cli.command()
@click.option('--days', '-d', default=30, help='查看天数，默认 30 天')
def history(days):
    """📊 查看打卡历史"""
    records = get_history(days)
    
    if records:
        print_info(f"最近 {days} 天的打卡记录")
        print_separator()
        
        # 准备表格数据
        table_data = []
        for i, (date, time, note) in enumerate(records, 1):
            note_text = note if note else "-"
            table_data.append([date, time, note_text])
        
        print_table(table_data, ["日期", "时间", "备注"])
        print(f"\n📈 共 {len(records)} 条记录")
    else:
        print_info(f"最近 {days} 天没有打卡记录")


@cli.command()
def stats():
    """📈 查看打卡统计"""
    stats_data = get_stats()
    
    if not stats_data:
        print_error("获取统计信息失败")
        sys.exit(1)
    
    print_info("📊 打卡统计信息")
    print_separator()
    print(f"总打卡次数：{stats_data['total']} 次")
    print(f"本月打卡：{stats_data['month']} 次")
    print(f"本月天数：{stats_data['days_in_month']} 天")
    print(f"打卡率：{stats_data['rate']:.1f}%")
    print(f"连续打卡：{stats_data['consecutive']} 天")
    print_separator()


@cli.command()
def reset():
    """🔄 重置所有数据（谨慎使用）"""
    if click.confirm('⚠️  确定要清空所有打卡记录吗？此操作不可撤销'):
        from db import clear_all
        if clear_all():
            print_success("已清空所有打卡记录")
        else:
            print_error("清空失败")
            sys.exit(1)
    else:
        print_info("已取消操作")


@cli.command()
def version():
    """📌 显示版本信息"""
    print("打卡工具 (Tt) v1.0.0")
    print("一个简洁高效的每日打卡工具")


if __name__ == '__main__':
    try:
        cli()
    except KeyboardInterrupt:
        print("\n")
        print_info("已中断")
        sys.exit(0)
    except Exception as e:
        print_error(f"发生错误：{e}")
        sys.exit(1)
