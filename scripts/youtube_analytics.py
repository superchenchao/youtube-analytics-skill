#!/usr/bin/env python3
"""
YouTube Analytics Data Fetcher
获取YouTube频道分析数据
"""

import os
import sys
import json
import argparse
from datetime import datetime, timedelta
from pathlib import Path

# 代理设置 - 如果需要代理，修改这里的地址
PROXY_HTTP = os.environ.get('HTTP_PROXY', 'http://127.0.0.1:7897')
PROXY_HTTPS = os.environ.get('HTTPS_PROXY', 'http://127.0.0.1:7897')

# 设置环境变量代理
os.environ['HTTP_PROXY'] = PROXY_HTTP
os.environ['HTTPS_PROXY'] = PROXY_HTTPS

try:
    import httplib2
    import google_auth_httplib2
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build
    from googleapiclient.http import build_http
    import pandas as pd
except ImportError:
    print("请先安装依赖: pip install google-api-python-client google-auth-oauthlib pandas")
    sys.exit(1)

# OAuth配置
SCOPES = [
    'https://www.googleapis.com/auth/youtube.readonly',
    'https://www.googleapis.com/auth/yt-analytics.readonly',
    'https://www.googleapis.com/auth/yt-analytics-monetary.readonly'
]

# 获取脚本所在目录
SCRIPT_DIR = Path(__file__).parent
SKILL_DIR = SCRIPT_DIR.parent
ASSETS_DIR = SKILL_DIR / 'assets'

# 凭据文件路径
CLIENT_SECRETS_FILE = ASSETS_DIR / 'client_secret.json'
TOKEN_FILE = SKILL_DIR / 'token.json'


def get_credentials():
    """获取OAuth凭据"""
    creds = None

    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not CLIENT_SECRETS_FILE.exists():
                print(f"""
错误: 未找到OAuth客户端配置文件

请按以下步骤操作:
1. 访问 Google Cloud Console: https://console.cloud.google.com
2. 创建项目并启用 YouTube Data API v3 和 YouTube Analytics API
3. 创建 OAuth 2.0 客户端 ID (桌面应用)
4. 下载凭据文件并保存到:
   {CLIENT_SECRETS_FILE}

详细说明见: references/google-cloud-setup.md
""")
                sys.exit(1)

            flow = InstalledAppFlow.from_client_secrets_file(
                str(CLIENT_SECRETS_FILE), SCOPES)
            creds = flow.run_local_server(port=0)

        with open(TOKEN_FILE, 'w') as f:
            f.write(creds.to_json())

    return creds


def get_services(creds):
    """获取YouTube API服务（支持代理）"""
    # 配置代理
    proxy_info = httplib2.ProxyInfo(
        httplib2.socks.PROXY_TYPE_HTTP,
        '127.0.0.1',
        7897
    )
    http = httplib2.Http(proxy_info=proxy_info)
    # 使用 credentials 授权 http
    authed_http = google_auth_httplib2.AuthorizedHttp(creds, http=http)

    youtube = build('youtube', 'v3', http=authed_http)
    analytics = build('youtubeAnalytics', 'v2', http=authed_http)
    return youtube, analytics


def get_channel_info(youtube):
    """获取频道基本信息"""
    response = youtube.channels().list(
        part='snippet,statistics,contentDetails',
        mine=True
    ).execute()

    if not response.get('items'):
        return None

    channel = response['items'][0]
    return {
        'id': channel['id'],
        'title': channel['snippet']['title'],
        'subscribers': int(channel['statistics'].get('subscriberCount', 0)),
        'views': int(channel['statistics'].get('viewCount', 0)),
        'videos': int(channel['statistics'].get('videoCount', 0))
    }


def get_analytics_report(analytics, metrics, dimensions=None, start_date=None, end_date=None, filters=None):
    """获取分析报告"""
    if not start_date:
        start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
    if not end_date:
        end_date = datetime.now().strftime('%Y-%m-%d')

    request_params = {
        'ids': 'channel==MINE',
        'startDate': start_date,
        'endDate': end_date,
        'metrics': metrics
    }

    if dimensions:
        request_params['dimensions'] = dimensions
    if filters:
        request_params['filters'] = filters

    response = analytics.reports().query(**request_params).execute()
    return response


def format_number(num):
    """格式化数字"""
    if num >= 1000000:
        return f"{num/1000000:.2f}M"
    elif num >= 1000:
        return f"{num/1000:.1f}K"
    return str(num)


def format_duration(seconds):
    """格式化时长"""
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes}:{secs:02d}"


def cmd_auth(args):
    """执行OAuth认证"""
    print("正在启动OAuth认证...")
    creds = get_credentials()
    print("认证成功!")
    print(f"Token已保存到: {TOKEN_FILE}")


def cmd_summary(args):
    """获取频道概览"""
    creds = get_credentials()
    youtube, analytics = get_services(creds)

    # 获取频道信息
    channel = get_channel_info(youtube)
    if not channel:
        print("错误: 无法获取频道信息")
        return

    print(f"\n{'='*50}")
    print(f"频道: {channel['title']}")
    print(f"{'='*50}")
    print(f"订阅者: {format_number(channel['subscribers'])}")
    print(f"总播放量: {format_number(channel['views'])}")
    print(f"视频数: {channel['videos']}")

    # 获取时间范围内的分析数据
    start_date = (datetime.now() - timedelta(days=args.period)).strftime('%Y-%m-%d')
    end_date = datetime.now().strftime('%Y-%m-%d')

    print(f"\n--- 最近 {args.period} 天数据 ---")

    # 基础指标
    response = get_analytics_report(
        analytics,
        metrics='views,estimatedMinutesWatched,averageViewDuration,subscribersGained,subscribersLost,likes,dislikes,comments,shares',
        start_date=start_date,
        end_date=end_date
    )

    if response.get('rows'):
        row = response['rows'][0]
        data = {
            '播放量': row[0],
            '观看时长(分钟)': row[1],
            '平均观看时长': row[2],
            '新增订阅': row[3],
            '取消订阅': row[4],
            '点赞': row[5],
            '踩': row[6],
            '评论': row[7],
            '分享': row[8]
        }

        for key, value in data.items():
            if '时长' in key:
                print(f"{key}: {format_duration(value)}")
            else:
                print(f"{key}: {format_number(value)}")


def cmd_video(args):
    """获取单个视频数据"""
    creds = get_credentials()
    youtube, analytics = get_services(creds)

    video_id = args.video

    # 获取视频基本信息
    video_response = youtube.videos().list(
        part='snippet,statistics,contentDetails',
        id=video_id
    ).execute()

    if not video_response.get('items'):
        print(f"错误: 未找到视频 {video_id}")
        return

    video = video_response['items'][0]
    stats = video['statistics']

    print(f"\n{'='*50}")
    print(f"视频: {video['snippet']['title']}")
    print(f"{'='*50}")
    print(f"发布日期: {video['snippet']['publishedAt'][:10]}")
    print(f"播放量: {format_number(int(stats.get('viewCount', 0)))}")
    print(f"点赞: {format_number(int(stats.get('likeCount', 0)))}")
    print(f"评论: {format_number(int(stats.get('commentCount', 0)))}")

    # 获取分析数据
    start_date = (datetime.now() - timedelta(days=args.period)).strftime('%Y-%m-%d')
    end_date = datetime.now().strftime('%Y-%m-%d')

    response = get_analytics_report(
        analytics,
        metrics='views,estimatedMinutesWatched,averageViewDuration,averageViewPercentage,subscribersGained',
        filters=f'video=={video_id}',
        start_date=start_date,
        end_date=end_date
    )

    if response.get('rows'):
        row = response['rows'][0]
        print(f"\n--- 分析数据 (最近{args.period}天) ---")
        print(f"观看时长: {format_number(row[1])} 分钟")
        print(f"平均观看时长: {format_duration(row[2])}")
        print(f"平均观看比例: {row[3]:.1f}%")
        print(f"带来订阅: {row[4]}")


def cmd_geo(args):
    """获取观众地理位置分布"""
    creds = get_credentials()
    _, analytics = get_services(creds)

    start_date = (datetime.now() - timedelta(days=args.period)).strftime('%Y-%m-%d')
    end_date = datetime.now().strftime('%Y-%m-%d')

    response = get_analytics_report(
        analytics,
        metrics='views,estimatedMinutesWatched',
        dimensions='country',
        start_date=start_date,
        end_date=end_date
    )

    if not response.get('rows'):
        print("无地理位置数据")
        return

    print(f"\n{'='*50}")
    print(f"观众地理位置分布 (最近{args.period}天)")
    print(f"{'='*50}")
    print(f"{'国家/地区':<20} {'播放量':>12} {'观看时长(分钟)':>15}")
    print("-" * 50)

    rows = sorted(response['rows'], key=lambda x: x[1], reverse=True)
    for row in rows[:20]:  # 显示前20个国家
        print(f"{row[0]:<20} {format_number(row[1]):>12} {format_number(row[2]):>15}")


def cmd_list_videos(args):
    """列出频道视频"""
    creds = get_credentials()
    youtube, _ = get_services(creds)

    # 获取频道上传播放列表
    channel = get_channel_info(youtube)
    if not channel:
        print("错误: 无法获取频道信息")
        return

    # 获取上传的视频
    response = youtube.search().list(
        part='snippet',
        channelId=channel['id'],
        type='video',
        order='date',
        maxResults=50
    ).execute()

    print(f"\n{'='*60}")
    print(f"频道视频列表")
    print(f"{'='*60}")

    for item in response.get('items', []):
        video_id = item['id']['videoId']
        title = item['snippet']['title'][:40]
        date = item['snippet']['publishedAt'][:10]
        print(f"{date} | {title:<40} | {video_id}")


def cmd_export(args):
    """导出数据到CSV"""
    creds = get_credentials()
    youtube, analytics = get_services(creds)

    start_date = (datetime.now() - timedelta(days=args.period)).strftime('%Y-%m-%d')
    end_date = datetime.now().strftime('%Y-%m-%d')

    # 获取详细数据
    response = get_analytics_report(
        analytics,
        metrics='views,estimatedMinutesWatched,averageViewDuration,subscribersGained,likes,comments,shares',
        dimensions='day',
        start_date=start_date,
        end_date=end_date
    )

    if not response.get('rows'):
        print("无数据可导出")
        return

    # 创建DataFrame
    columns = ['日期', '播放量', '观看时长(分钟)', '平均观看时长(秒)', '新增订阅', '点赞', '评论', '分享']
    df = pd.DataFrame(response['rows'], columns=columns)

    output_file = args.export
    df.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"数据已导出到: {output_file}")
    print(f"共 {len(df)} 条记录")


def main():
    parser = argparse.ArgumentParser(
        description='YouTube Analytics 数据获取工具'
    )

    parser.add_argument('--auth', action='store_true', help='执行OAuth认证')
    parser.add_argument('--summary', action='store_true', help='获取频道概览')
    parser.add_argument('--video', type=str, help='获取指定视频数据 (视频ID)')
    parser.add_argument('--geo', action='store_true', help='获取观众地理位置分布')
    parser.add_argument('--list-videos', action='store_true', help='列出频道视频')
    parser.add_argument('--export', type=str, metavar='FILE', help='导出数据到CSV')
    parser.add_argument('--period', type=int, default=30, help='数据时间范围(天), 默认30')
    parser.add_argument('--retention', action='store_true', help='获取观众留存数据')

    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        return

    if args.auth:
        cmd_auth(args)
    elif args.summary:
        cmd_summary(args)
    elif args.video:
        cmd_video(args)
    elif args.geo:
        cmd_geo(args)
    elif args.list_videos:
        cmd_list_videos(args)
    elif args.export:
        cmd_export(args)


if __name__ == '__main__':
    main()
