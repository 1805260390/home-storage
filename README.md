# 家庭收纳管理 - 云端部署指南

## 📦 项目文件

```
home-storage-manager-20260910T071035097Z/
├── server.py              # 服务器程序
├── 家庭收纳管理.html       # 前端页面
├── Procfile               # 云平台启动配置
├── runtime.txt            # Python 版本配置
└── README.md              # 本文件
```

## 🚀 部署到 Render（免费）

### 步骤 1：注册 GitHub 并上传代码

1. 访问 https://github.com 注册账号（如已有可跳过）
2. 点击右上角 `+` → `New repository`
3. 仓库名填 `home-storage`，选 `Public`，点 `Create repository`
4. 在仓库页面点 `uploading an existing file`
5. 把以下文件拖入上传区：
   - `server.py`
   - `家庭收纳管理.html`
   - `Procfile`
   - `runtime.txt`
6. 点 `Commit changes`

### 步骤 2：部署到 Render

1. 访问 https://render.com 注册账号（可用 GitHub 登录）
2. 登录后点 `New +` → `Web Service`
3. 选择 `Build and deploy from a Git repository`
4. 连接你的 GitHub，选择 `home-storage` 仓库
5. 配置页面填写：
   - **Name**: `home-storage`（随意）
   - **Region**: 选离你近的（如 Singapore）
   - **Branch**: `main`
   - **Runtime**: `Python`
   - **Build Command**: 留空
   - **Start Command**: 留空（Procfile 会自动处理）
   - **Instance Type**: 选 `Free`
6. 点 `Create Web Service`

### 步骤 3：等待部署完成

- Render 会自动构建和启动（约 2-3 分钟）
- 部署完成后会显示你的网址，如 `https://home-storage.onrender.com`
- 第一次访问可能需要 30 秒冷启动（免费版限制）

### 步骤 4：使用

1. 在电脑浏览器打开你的 Render 网址
2. 第一次输入一个密码（4位以上），这是你的家庭密码
3. 开始添加收纳位置和物品
4. 生成二维码打印贴在箱子上
5. 手机扫码打开同一个网址，输入密码即可查看和管理

## 💻 本地局域网使用（可选）

如果只想在家里用，也可以不部署到云端，直接在电脑上运行：

```bash
cd home-storage-manager-20260910T071035097Z
python server.py
```

启动后会显示局域网地址（如 `http://192.168.1.100:8080`），手机连同一 WiFi 后访问即可。

## ⚙️ 工作原理

- **前端**：单页 HTML 应用，电脑和手机共用
- **后端**：Python HTTP 服务器，提供 API 和静态文件
- **数据**：保存在服务器 `storage_data.json` 文件
- **密码**：SHA256 哈希保存在 `auth_hash.json`，所有设备用同一密码
- **同步**：前端每 5 秒自动检查数据更新，多设备实时同步

## 📝 注意事项

- Render 免费版有冷启动延迟（约 30 秒），属于正常现象
- 数据保存在 Render 服务器，重启后仍然存在
- 如需备份数据，可在页面导出 JSON 文件
- 建议定期导出备份，防止数据丢失
