#!/usr/bin/env python3
"""
Digital Clock - 显示多个时区的数字时钟
实时显示不同时区的当前时间
"""

import click
import time
import sys
from datetime import datetime
from pytz import timezone, all_timezones
from typing import List, Dict


class DigitalClock:
    """数字时钟类"""
    
    def __init__(self, timezones: List[str] = None):
        """
        初始化时钟
        
        Args:
            timezones: 时区列表，默认为常用时区
        """
        if timezones is None:
            self.timezones = [
                'UTC',
                'Asia/Shanghai',      # 北京时间
                'Asia/Tokyo',         # 日本
                'Asia/Hong_Kong',     # 香港
                'America/New_York',   # 纽约
                'Europe/London',      # 伦敦
                'Europe/Paris',       # 巴黎
                'Australia/Sydney',   # 悉尼
            ]
        else:
            self.timezones = timezones
    
    def get_time_in_timezone(self, tz: str) -> Dict:
        """
        获取指定时区的时间
        
        Args:
            tz: 时区字符串
            
        Returns:
            dict: 包含时间信息的字典
        """
        try:
            tz_obj = timezone(tz)
            dt = datetime.now(tz_obj)
            
            return {
                'timezone': tz,
                'datetime': dt,
                'time': dt.strftime('%H:%M:%S'),
                'date': dt.strftime('%Y-%m-%d'),
                'day': dt.strftime('%A'),
                'utc_offset': dt.strftime('%z'),
            }
        except Exception as e:
            return None
    
    def display_clock(self, update_interval: float = 1.0):
        """
        显示实时时钟
        
        Args:
            update_interval: 更新间隔（秒）
        """
        try:
            while True:
                # 清屏（ANSI 转义码）
                click.clear()
                
                print("=" * 70)
                print("🕐 DIGITAL CLOCK - 数字时钟 (多时区)".center(70))
                print("=" * 70)
                print()
                
                # 显示每个时区的时间
                for tz in self.timezones:
                    time_info = self.get_time_in_timezone(tz)
                    
                    if time_info:
                        # 获取时区的友好名称
                        tz_display = self._get_tz_display_name(tz)
                        
                        print(f"📍 {tz_display:<20} │ {time_info['time']} │ {time_info['date']}")
                        print(f"   {tz:<20} │ {time_info['day']:<20} │ UTC {time_info['utc_offset']}")
                        print("-" * 70)
                
                print()
                print("💡 按 Ctrl+C 退出 | Press Ctrl+C to exit".center(70))
                
                # 等待指定的更新间隔
                time.sleep(update_interval)
                
        except KeyboardInterrupt:
            click.echo("\n✅ 时钟已关闭 | Clock stopped")
            sys.exit(0)
    
    def _get_tz_display_name(self, tz: str) -> str:
        """获取时区的显示名称"""
        tz_names = {
            'UTC': '协调世界时',
            'Asia/Shanghai': '北京（中国）',
            'Asia/Tokyo': '东京（日本）',
            'Asia/Hong_Kong': '香港',
            'America/New_York': '纽约（美国）',
            'Europe/London': '伦敦（英国）',
            'Europe/Paris': '巴黎（法国）',
            'Australia/Sydney': '悉尼（澳大利亚）',
        }
        return tz_names.get(tz, tz)
    
    def display_single_time(self, tz: str):
        """
        显示单个时区的时间
        
        Args:
            tz: 时区字符串
        """
        time_info = self.get_time_in_timezone(tz)
        
        if time_info:
            tz_display = self._get_tz_display_name(tz)
            print("=" * 50)
            print(f"🕐 {tz_display}".center(50))
            print("=" * 50)
            print(f"时区: {time_info['timezone']}")
            print(f"时间: {time_info['time']}")
            print(f"日期: {time_info['date']}")
            print(f"星期: {time_info['day']}")
            print(f"UTC偏移: {time_info['utc_offset']}")
            print("=" * 50)
        else:
            click.echo(f"❌ 无效的时区: {tz}")
            sys.exit(1)


@click.group()
def cli():
    """🕐 数字时钟 - 多时区时间显示"""
    pass


@cli.command()
@click.option('--interval', '-i', default=1.0, type=float, help='更新间隔（秒），默认 1 秒')
@click.option('--timezones', '-tz', multiple=True, help='指定时区列表')
def start(interval, timezones):
    """▶️  启动实时多时区时钟"""
    if timezones:
        timezones = list(timezones)
    else:
        timezones = None
    
    clock = DigitalClock(timezones)
    clock.display_clock(update_interval=interval)


@cli.command()
@click.argument('timezone', default='Asia/Shanghai')
def show(timezone):
    """👁️  显示指定时区的时间"""
    clock = DigitalClock()
    clock.display_single_time(timezone)


@cli.command()
@click.argument('query', default='')
def search(query):
    """🔍 搜索时区"""
    matching_tzs = [tz for tz in all_timezones if query.lower() in tz.lower()]
    
    if matching_tzs:
        print(f"\n📍 匹配 '{query}' 的时区（共 {len(matching_tzs)} 个）:\n")
        for tz in sorted(matching_tzs)[:50]:  # 显示前 50 个
            print(f"  • {tz}")
        
        if len(matching_tzs) > 50:
            print(f"\n  ... 还有 {len(matching_tzs) - 50} 个时区")
    else:
        click.echo(f"❌ 没有找到包含 '{query}' 的时区")


@cli.command()
def list():
    """📋 列出所有可用时区"""
    print(f"\n📍 所有可用时区（共 {len(all_timezones)} 个）:\n")
    
    for i, tz in enumerate(sorted(all_timezones), 1):
        if i % 2 == 1:
            print(f"  {tz:<40}", end="")
        else:
            print(f"  {tz}")
    
    if len(all_timezones) % 2 == 1:
        print()


@cli.command()
@click.argument('timezones', nargs=-1, required=True)
def custom(timezones):
    """⚙️  使用自定义时区列表启动时钟"""
    # 验证所有时区
    for tz in timezones:
        try:
            timezone(tz)
        except Exception:
            click.echo(f"❌ 无效的时区: {tz}")
            sys.exit(1)
    
    clock = DigitalClock(list(timezones))
    clock.display_clock(update_interval=1.0)


@cli.command()
def compare():
    """🌍 比较主要时区的时间差异"""
    clock = DigitalClock()
    
    print("\n" + "=" * 60)
    print("🌍 主要时区时间比较".center(60))
    print("=" * 60)
    
    times = []
    for tz in clock.timezones:
        time_info = clock.get_time_in_timezone(tz)
        if time_info:
            times.append((tz, time_info))
    
    # 按时间排序
    times.sort(key=lambda x: x[1]['datetime'])
    
    for tz, time_info in times:
        tz_display = clock._get_tz_display_name(tz)
        print(f"{tz_display:<20} {time_info['time']} ({time_info['utc_offset']})")
    
    print("=" * 60)


@cli.command()
def version():
    """📌 显示版本信息"""
    print("数字时钟 (Digital Clock) v1.0.0")
    print("多时区实时时间显示工具")


if __name__ == '__main__':
    try:
        cli()
    except KeyboardInterrupt:
        print("\n✅ 程序已退出")
        sys.exit(0)
    except Exception as e:
        click.echo(f"❌ 错误: {e}", err=True)
        sys.exit(1)
