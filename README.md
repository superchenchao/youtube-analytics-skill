# YouTube Analytics Skill 使用说明

## 文件说明

- `youtube-analytics.skill` - Skill 安装包
- 本文件 - 使用说明

## 安装步骤

### 1. 安装 Skill

将 `youtube-analytics.skill` 文件放到你的 Skills 目录：

```
C:\Users\你的用户名\.claude\skills\
```

解压后得到 `youtube-analytics` 文件夹。

### 2. 安装 Python 依赖

打开命令提示符（CMD），运行：

```bash
pip install google-api-python-client google-auth-oauthlib pandas PySocks
```

### 3. 配置 Google Cloud（首次使用）

#### 3.1 创建项目
1. 访问 https://console.cloud.google.com
2. 登录 Google 账户
3. 点击 "新建项目" → 名称填写 `YouTube Analytics` → 创建

#### 3.2 启用 API
1. 左侧菜单 → "API和服务" → "库"
2. 搜索 `YouTube Data API v3` → 启用
3. 搜索 `YouTube Analytics API` → 启用

#### 3.3 配置 OAuth
1. 左侧菜单 → "API和服务" → "OAuth 同意屏幕"
2. 选择 "外部" → 创建
3. 应用名称：`YouTube Analytics Tool`
4. 用户支持电子邮件：选择你的邮箱
5. 开发者联系信息：填写你的邮箱
6. 保存并继续（Scopes 页面直接跳过）
7. 测试用户页面 → 添加用户 → 输入你的 Gmail

#### 3.4 创建凭据
1. 左侧菜单 → "API和服务" → "凭据"
2. 创建凭据 → OAuth 客户端 ID
3. 应用类型：桌面应用
4. 创建 → 下载 JSON

#### 3.5 放置凭据
将下载的 JSON 文件重命名为 `client_secret.json`，放到：
```
youtube-analytics/assets/client_secret.json
```

### 4. 配置代理（中国大陆用户必看）

编辑 `youtube-analytics/scripts/youtube_analytics.py`：

找到这两处，修改端口号：
```python
# 第12-13行
PROXY_HTTP = os.environ.get('HTTP_PROXY', 'http://127.0.0.1:你的端口')
PROXY_HTTPS = os.environ.get('HTTPS_PROXY', 'http://127.0.0.1:你的端口')

# 第94-97行
proxy_info = httplib2.ProxyInfo(
    httplib2.socks.PROXY_TYPE_HTTP,
    '127.0.0.1',
    你的端口  # 改这里
)
```

### 5. 首次认证

```bash
cd youtube-analytics
python scripts/youtube_analytics.py --auth
```

浏览器会打开授权页面，完成授权。

## 使用方法

```bash
# 查看频道概览
python scripts/youtube_analytics.py --summary

# 查看单个视频数据
python scripts/youtube_analytics.py --video VIDEO_ID

# 查看观众地理位置
python scripts/youtube_analytics.py --geo

# 导出数据到 CSV
python scripts/youtube_analytics.py --export report.csv

# 列出所有视频
python scripts/youtube_analytics.py --list-videos

# 指定时间范围（天数）
python scripts/youtube_analytics.py --summary --period 7
```

## 常见问题

**Q: 提示 "Access blocked"**
A: 回到 OAuth 同意屏幕 → 测试用户 → 添加你的 Gmail

**Q: 连接超时**
A: 检查代理是否开启，端口号是否正确

**Q: 找不到频道信息**
A: 需要先创建 YouTube 频道并上传视频

**Q: 认证失败**
A: 删除 `token.json` 文件，重新运行 `--auth`

## 注意事项

- 每个 Google Cloud 项目每天有 API 配额限制
- 需要 YouTube 频道才能获取分析数据
- `client_secret.json` 是你的私密凭据，不要分享给他人
