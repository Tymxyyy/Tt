# 打卡工具 (Tt)

一个简洁高效的每日打卡工具，用于记录和管理日常打卡任务。

## ✨ 功能特性

- ✅ **每日打卡** - 快速记录打卡时间
- 📝 **打卡备注** - 支持添加打卡说明
- 📊 **查看历史** - 浏览所有打卡记录
- 📈 **统计信息** - 显示连续打卡天数、本月打卡率等
- 💾 **本地存储** - 使用 SQLite 数据库，数据完全本地化

## 🚀 快速开始

### 安装

```bash
# 克隆仓库
git clone https://github.com/Tymxyyy/Tt.git
cd Tt

# 安装依赖
pip install -r requirements.txt
```

### 使用

```bash
# 打卡
python checkin.py check

# 查看今天的打卡记录
python checkin.py today

# 查看最近 7 天的记录
python checkin.py history --days 7

# 查看统计信息
python checkin.py stats

# 打卡并添加备注
python checkin.py check --note "完成日常工作"

# 查看帮助
python checkin.py --help
```

## 📁 项目结构

```
Tt/
├── checkin.py           # 主程序入口
├── db.py               # 数据库操作模块
├── utils.py            # 工具函数
├── requirements.txt    # 依赖文件
└── README.md          # 说明文档
```

## 🗄️ 数据库

数据存储在本地 `checkin.db` SQLite 数据库中，包含以下信息：
- 打卡时间
- 打卡备注
- 打卡状态

## 📋 示例

```bash
# 记录打卡
$ python checkin.py check --note "按时完成"
✅ 打卡成功！时间：2026-06-27 10:30:45

# 查看统计
$ python checkin.py stats
📊 打卡统计信息
---
连续打卡: 5 天
本月打卡: 20 次
打卡率: 66.7%
```

## 📝 许可证

MIT

## 👤 作者

Tymxyyy