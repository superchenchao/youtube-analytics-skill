# YouTube Analytics Skill 新手安装指南

## 第一步：安装 Python

1. 访问 https://www.python.org/downloads/
2. 下载最新版 Python（3.10 或更高版本）
3. 安装时**勾选 "Add Python to PATH"**
4. 完成安装后，打开命令提示符验证：
   ```
   python --version
   ```

## 第二步：安装依赖

打开命令提示符（CMD），运行：

```bash
pip install google-api-python-client google-auth-oauthlib pandas PySocks
```

## 第三步：配置 Google Cloud

### 3.1 创建项目

1. 访问 https://console.cloud.google.com
2. 登录 Google 账户
3. 点击顶部项目选择器 → "NEW PROJECT"
4. 项目名称：`YouTube Analytics`
5. 点击 "CREATE"
6. 创建完成后点击 "SELECT PROJECT"

### 3.2 启用 API

1. 左侧菜单 → "APIs & Services" → "Library"
2. 搜索 `YouTube Data API v3` → 点击 → "ENABLE"
3. 返回库，搜索 `YouTube Analytics API` → 点击 → "ENABLE"

### 3.3 配置 OAuth

1. 左侧菜单 → "APIs & Services" → "OAuth consent screen"
2. 选择 "External" → "CREATE"
3. 填写：
   - App name: `YouTube Analytics Tool`
   - User support email: 选择你的邮箱
   - Developer contact: 填写你的邮箱
4. 点击 "SAVE AND CONTINUE"
5. Scopes 页面直接点击 "SAVE AND CONTINUE"
6. Test users 页面点击 "ADD USERS" → 输入你的 Gmail → "ADD"
7. 点击 "SAVE AND CONTINUE" → "BACK TO DASHBOARD"

### 3.4 创建凭据

1. 左侧菜单 → "APIs & Services" → "Credentials"
2. 点击 "CREATE CREDENTIALS" → "OAuth client ID"
3. Application type: 选择 "Desktop app"
4. Name: `YouTube Analytics Client`
5. 点击 "CREATE"
6. 点击 "DOWNLOAD JSON"
7. 将下载的文件重命名为 `client_secret.json`

### 3.5 放置凭据文件

将 `client_secret.json` 复制到：
```
你的Skill目录/assets/client_secret.json
```

例如：
```
C:\Users\你的用户名\.claude\skills\youtube-analytics\assets\client_secret.json
```

## 第四步：配置代理（中国大陆用户）

如果你在中国大陆，需要配置代理：

1. 打开 `scripts/youtube_analytics.py` 文件
2. 找到以下行，修改端口号为你的代理端口：
   ```python
   PROXY_HTTP = os.environ.get('HTTP_PROXY', 'http://127.0.0.1:7897')
   PROXY_HTTPS = os.environ.get('HTTPS_PROXY', 'http://127.0.0.1:7897')
   ```
3. 同时修改 `get_services` 函数中的端口：
   ```python
   proxy_info = httplib2.ProxyInfo(
       httplib2.socks.PROXY_TYPE_HTTP,
       '127.0.0.1',
       7897  # 改成你的代理端口
   )
   ```

## 第五步：首次认证

```bash
cd 你的Skill目录
python scripts/youtube_analytics.py --auth
```

浏览器会打开授权页面：
1. 选择你的 Google 账户
2. 如果显示"未验证应用"，点击"高级" → "前往 YouTube Analytics Tool"
3. 点击"允许"授权
4. 看到"认证成功"提示

## 第六步：开始使用

```bash
# 查看频道概览
python scripts/youtube_analytics.py --summary

# 查看单个视频数据
python scripts/youtube_analytics.py --video VIDEO_ID

# 查看观众地理位置
python scripts/youtube_analytics.py --geo

# 导出数据到CSV
python scripts/youtube_analytics.py --export report.csv

# 列出所有视频
python scripts/youtube_analytics.py --list-videos
```

## 常见问题

### Q: 提示 "Access blocked" 错误
A: 你需要把自己添加为测试用户。回到 OAuth consent screen → Test users → ADD USERS

### Q: 连接超时
A: 检查代理是否开启，端口是否正确

### Q: 找不到频道信息
A: 确保你已创建 YouTube 频道并上传过视频

### Q: API 配额用完
A: 每天有配额限制，第二天会重置
