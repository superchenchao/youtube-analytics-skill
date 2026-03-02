# YouTube Analytics 指标参考

## 核心指标说明

### 播放量 (Views)
视频被观看的次数。用户观看视频超过一定时长(约30秒)才计入。

### 选择观看率 (CTR - Click-Through Rate)
缩略图被点击的次数 / 缩略图展示次数。反映标题和缩略图的吸引力。

### 平均观看时长 (Average View Duration)
观众观看视频的平均时间，以秒为单位。

### 平均观看比例 (Average View Percentage)
观众平均观看了视频的百分之多少。

### 观众留存率 (Audience Retention)
视频每个时间点的观众留存情况。

---

## API指标对照表

| 中文名称 | API指标名称 | 说明 |
|---------|------------|------|
| 播放量 | views | 视频播放次数 |
| 观看时长 | estimatedMinutesWatched | 总观看分钟数 |
| 平均观看时长 | averageViewDuration | 平均观看秒数 |
| 平均观看比例 | averageViewPercentage | 平均观看百分比 |
| 新增订阅 | subscribersGained | 新增订阅者数 |
| 取消订阅 | subscribersLost | 取消订阅者数 |
| 点赞 | likes | 点赞数 |
| 踩 | dislikes | 踩数 |
| 评论 | comments | 评论数 |
| 分享 | shares | 分享次数 |

---

## 维度说明

### 时间维度
- `day` - 按天
- `month` - 按月

### 地理维度
- `country` - 国家/地区代码 (ISO 3166-1)
- `province` - 省份/州

### 内容维度
- `video` - 视频ID
- `playlist` - 播放列表ID
- `channel` - 频道ID

### 设备维度
- `deviceType` - 设备类型 (mobile, desktop, tv, etc.)
- `operatingSystem` - 操作系统

### 流量来源
- `insightTrafficSourceType` - 流量来源类型

---

## 常用查询组合

### 频道总览
```
metrics: views,estimatedMinutesWatched,averageViewDuration,subscribersGained
```

### 视频表现
```
metrics: views,averageViewPercentage,likes,comments,shares
dimensions: video
```

### 地理分布
```
metrics: views,estimatedMinutesWatched
dimensions: country
```

### 每日趋势
```
metrics: views,subscribersGained,estimatedMinutesWatched
dimensions: day
```

### 流量来源
```
metrics: views,estimatedMinutesWatched
dimensions: insightTrafficSourceType
```
