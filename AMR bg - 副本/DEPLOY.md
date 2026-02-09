# Render.com 部署指南

本指南将帮助你将 AMR 设备信息记录工具部署到 Render.com。

## 📋 前置要求

1. **GitHub 账号**：需要将代码推送到 GitHub
2. **Render.com 账号**：免费注册 [https://render.com](https://render.com)

## 🚀 部署步骤

### 第一步：准备代码并推送到 GitHub

1. **初始化 Git 仓库**（如果还没有）：
   ```bash
   git init
   git add .
   git commit -m "Initial commit: AMR device management tool"
   ```

2. **在 GitHub 创建新仓库**：
   - 访问 [GitHub](https://github.com)
   - 点击右上角 "+" → "New repository"
   - 输入仓库名称（如：`amr-device-manager`）
   - 选择 Public 或 Private
   - **不要**勾选 "Initialize this repository with a README"
   - 点击 "Create repository"

3. **推送代码到 GitHub**：
   ```bash
   git remote add origin https://github.com/你的用户名/仓库名.git
   git branch -M main
   git push -u origin main
   ```

### 第二步：在 Render.com 创建 Web Service

1. **登录 Render.com**：
   - 访问 [https://dashboard.render.com](https://dashboard.render.com)
   - 使用 GitHub 账号登录（推荐）

2. **创建新的 Web Service**：
   - 点击 "New +" → "Web Service"
   - 选择你的 GitHub 仓库
   - 如果看不到仓库，点击 "Configure account" 授权访问

3. **配置服务**：
   - **Name**: 输入服务名称（如：`amr-device-manager`）
   - **Region**: 选择离你最近的区域（如：Singapore）
   - **Branch**: 选择 `main` 或 `master`
   - **Root Directory**: 留空（如果代码在根目录）
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Plan**: 选择 **Free**（免费计划）

4. **点击 "Create Web Service"**

### 第三步：创建 PostgreSQL 数据库（推荐）

虽然应用可以使用 SQLite，但 Render 的免费层文件系统是临时的，数据会在重启后丢失。建议使用 PostgreSQL：

1. **创建数据库**：
   - 在 Render Dashboard 点击 "New +" → "PostgreSQL"
   - **Name**: 输入数据库名称（如：`amr-db`）
   - **Database**: 留空（使用默认）
   - **User**: 留空（使用默认）
   - **Region**: 选择与 Web Service 相同的区域
   - **Plan**: 选择 **Free**
   - 点击 "Create Database"

2. **获取数据库连接信息**：
   - 创建后，在数据库页面可以看到 "Internal Database URL"
   - 复制这个 URL（格式类似：`postgres://user:password@host:port/dbname`）

3. **配置环境变量**：
   - 回到你的 Web Service 页面
   - 点击 "Environment" 标签
   - 点击 "Add Environment Variable"
   - **Key**: `DATABASE_URL`
   - **Value**: 粘贴刚才复制的数据库 URL
   - 点击 "Save Changes"

### 第四步：部署和测试

1. **手动部署**（如果需要）：
   - 在 Web Service 页面，点击 "Manual Deploy" → "Deploy latest commit"
   - 或者推送新的代码到 GitHub，Render 会自动部署

2. **查看部署日志**：
   - 在 "Logs" 标签页查看部署和运行日志
   - 如果有错误，会在这里显示

3. **访问应用**：
   - 部署成功后，Render 会提供一个 URL（格式：`https://你的服务名.onrender.com`）
   - 点击这个 URL 访问你的应用

## ⚙️ 重要配置说明

### 环境变量

如果需要，可以添加以下环境变量：

- `DATABASE_URL`: PostgreSQL 数据库连接 URL（如果使用 PostgreSQL）
- `PORT`: 端口号（Render 会自动设置，通常不需要手动配置）

### 文件上传限制

- 免费层上传的文件会存储在临时文件系统中
- 如果服务重启，上传的文件可能会丢失
- 如果需要持久化存储，可以考虑：
  - 升级到付费计划使用持久化磁盘
  - 使用云存储服务（如 AWS S3、Cloudinary 等）

### 免费层限制

- **休眠机制**：免费服务在 15 分钟无活动后会休眠
- **首次访问**：休眠后首次访问需要约 30 秒唤醒时间
- **资源限制**：512MB RAM，0.5 CPU

## 🔧 故障排除

### 部署失败

1. **检查日志**：
   - 在 Render Dashboard 的 "Logs" 标签查看错误信息

2. **常见问题**：
   - **依赖安装失败**：检查 `requirements.txt` 是否正确
   - **启动失败**：检查 `Procfile` 中的命令是否正确
   - **数据库连接失败**：检查 `DATABASE_URL` 环境变量是否正确设置

### 应用无法访问

1. **检查服务状态**：
   - 在 Dashboard 查看服务是否正在运行（绿色状态）

2. **等待唤醒**：
   - 如果服务已休眠，首次访问需要等待约 30 秒

3. **检查 URL**：
   - 确保使用正确的 URL（`https://你的服务名.onrender.com`）

## 📝 后续更新

当你修改代码后：

1. **提交到 GitHub**：
   ```bash
   git add .
   git commit -m "更新说明"
   git push
   ```

2. **自动部署**：
   - Render 会自动检测到新的提交并开始部署
   - 在 Dashboard 的 "Events" 标签可以查看部署进度

## 🎉 完成！

部署完成后，你的应用就可以在线访问了！团队成员可以通过 Render 提供的 URL 访问应用。

---

**提示**：建议将应用的 URL 保存下来，方便团队成员访问。

