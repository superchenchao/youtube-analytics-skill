---
name: youtube-analytics
description: YouTube频道数据分析工具，获取视频的选择观看率、平均观看时长、观众地理位置、播放量、订阅数、互动播放次数等数据。使用YouTube Analytics API和YouTube Data API v3。当用户需要分析YouTube频道数据、获取视频统计信息、查看观众分析、导出频道报告时触发。关键词：YouTube分析、频道数据、视频统计、观看时长、观众画像、播放量。
---

# YouTube Analytics 数据获取工具

## 概述

本Skill帮助你获取YouTube频道的详细分析数据，包括视频表现和观众洞察。

## 新手安装

**首次使用请阅读：** [安装指南](references/installation-guide.md)

包含完整的：
- Python 安装
- Google Cloud 配置
- OAuth 认证设置
- 代理配置（中国大陆用户）

## 支持的数据类型

| 类别 | 指标 |
|-----|------|
| 视频表现 | 播放量、选择观看率、平均观看时长 |
| 观众分析 | 地理位置分布、观众留存率 |
| 频道数据 | 订阅数变化、订阅者来源 |
| 互动数据 | 点赞、评论、分享次数 |

## 快速开始

### 1. 安装依赖

```bash
pip install google-api-python-client google-auth-oauthlib pandas PySocks
```

### 2. 配置凭据

将 Google Cloud 下载的 `client_secret.json` 放到：
```
assets/client_secret.json
```

### 3. OAuth 认证

```bash
python scripts/youtube_analytics.py --auth
```

### 4. 获取数据

```bash
# 获取频道总览
python scripts/youtube_analytics.py --summary

# 获取单个视频数据
python scripts/youtube_analytics.py --video VIDEO_ID

# 获取观众地理位置
python scripts/youtube_analytics.py --geo

# 导出完整报告
python scripts/youtube_analytics.py --export report.csv
```

## 命令参考

```
python scripts/youtube_analytics.py [OPTIONS]

选项:
  --auth          执行OAuth认证
  --summary       获取频道概览数据
  --video ID      获取指定视频的详细数据
  --geo           获取观众地理位置分布
  --period DAYS   设置数据时间范围(默认30天)
  --export FILE   导出数据到CSV文件
  --list-videos   列出频道所有视频
```

## 代理配置

中国大陆用户需要配置代理。编辑 `scripts/youtube_analytics.py`：

```python
# 修改代理端口
PROXY_HTTP = os.environ.get('HTTP_PROXY', 'http://127.0.0.1:你的端口')
PROXY_HTTPS = os.environ.get('HTTPS_PROXY', 'http://127.0.0.1:你的端口')
```

## 指标说明

详细指标定义见 [references/metrics.md](references/metrics.md)

## 故障排除

| 错误 | 解决方案 |
|-----|---------|
| Access blocked | 在 OAuth consent screen 添加自己为测试用户 |
| 连接超时 | 检查代理是否开启，端口是否正确 |
| 找不到频道 | 确保已创建 YouTube 频道并上传过视频 |
| 认证失败 | 删除 `token.json` 后重新运行 `--auth` |
| API配额超限 | 等待24小时或申请更高配额 |
