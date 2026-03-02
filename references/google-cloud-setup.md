# Google Cloud 项目设置指南

本指南帮助没有Google Cloud项目的用户完成完整配置。

## 步骤概览

1. 创建Google Cloud项目
2. 启用API
3. 配置OAuth同意屏幕
4. 创建OAuth客户端
5. 下载凭据文件

---

## Step 1: 创建Google Cloud项目

1. 访问 [Google Cloud Console](https://console.cloud.google.com)
2. 点击顶部导航栏的项目选择器
3. 点击 **"新建项目"**
4. 填写项目名称 (如: "YouTube Analytics")
5. 点击 **"创建"**
6. 等待项目创建完成，选择该项目

## Step 2: 启用API

### 2.1 启用 YouTube Data API v3

1. 在左侧菜单选择 **"API和服务" → "库"**
2. 搜索 **"YouTube Data API v3"**
3. 点击进入，然后点击 **"启用"**

### 2.2 启用 YouTube Analytics API

1. 返回API库
2. 搜索 **"YouTube Analytics API"**
3. 点击进入，然后点击 **"启用"**

## Step 3: 配置OAuth同意屏幕

1. 在左侧菜单选择 **"API和服务" → "OAuth同意屏幕"**
2. 选择用户类型:
   - **外部** - 适合个人使用(推荐)
   - **内部** - 仅限Google Workspace组织
3. 点击 **"创建"**

### 填写应用信息

| 字段 | 填写内容 |
|-----|---------|
| 应用名称 | YouTube Analytics Tool |
| 用户支持电子邮件 | 你的邮箱 |
| 应用Logo | 可选 |
| 应用首页 | 可选 |
| 应用隐私权政策 | 可选 |
| 应用服务条款 | 可选 |
| 已获授权的网域 | 留空 |
| 开发者联系信息 | 你的邮箱 |

4. 点击 **"保存并继续"**

### 配置作用域

1. 点击 **"添加或移除作用域"**
2. 搜索并勾选以下作用域:
   - `https://www.googleapis.com/auth/youtube.readonly`
   - `https://www.googleapis.com/auth/yt-analytics.readonly`
3. 点击 **"更新"**
4. 点击 **"保存并继续"**

### 测试用户

1. 点击 **"添加用户"**
2. 输入你的Gmail地址
3. 点击 **"添加"**
4. 点击 **"保存并继续"**

## Step 4: 创建OAuth客户端

1. 在左侧菜单选择 **"API和服务" → "凭据"**
2. 点击顶部的 **"创建凭据" → "OAuth客户端ID"**
3. 应用类型选择 **"桌面应用"**
4. 名称填写: `YouTube Analytics Client`
5. 点击 **"创建"**

## Step 5: 下载凭据文件

1. 创建完成后会弹出对话框
2. 点击 **"下载JSON"**
3. 将下载的文件重命名为 `client_secret.json`
4. 复制到 Skill 的 assets 目录:
   ```
   ~/.claude/skills/youtube-analytics/assets/client_secret.json
   ```

## 验证配置

运行认证命令验证配置是否正确:

```bash
python scripts/youtube_analytics.py --auth
```

浏览器会打开授权页面:
1. 选择你的Google账户
2. 点击 "继续" (可能会显示未验证应用警告，这是正常的)
3. 授权请求的权限
4. 看到 "认证成功" 提示

---

## 常见问题

### Q: 显示"未验证应用"警告?
A: 这是正常的。因为应用处于测试模式，点击"高级"→"前往(应用名)"继续。

### Q: API配额是多少?
A:
- YouTube Data API: 每天10,000单位
- YouTube Analytics API: 每天约50,000查询

### Q: 如何申请更高配额?
A: 在Google Cloud Console的"IAM和管理"→"配额"中申请。

### Q: token.json是什么?
A: 首次认证后生成的访问令牌，有效期约1小时，会自动刷新。不要分享此文件。

---

## 参考链接

- [YouTube Data API 文档](https://developers.google.com/youtube/v3)
- [YouTube Analytics API 文档](https://developers.google.com/youtube/analytics)
- [Google Cloud Console](https://console.cloud.google.com)
