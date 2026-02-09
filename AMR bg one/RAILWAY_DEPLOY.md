# Railway 部署指南

## 前置要求

1. GitHub 账号（用于代码托管）
2. Railway 账号（https://railway.app）

## 部署步骤

### 第一步：准备代码仓库

1. **初始化 Git 仓库**（如果还没有）：
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   ```

2. **推送到 GitHub**：
   - 在 GitHub 创建新仓库
   - 将代码推送到 GitHub：
     ```bash
     git remote add origin https://github.com/你的用户名/仓库名.git
     git branch -M main
     git push -u origin main
     ```

### 第二步：在 Railway 部署

1. **注册/登录 Railway**：
   - 访问 https://railway.app
   - 使用 GitHub 账号登录

2. **创建新项目**：
   - 点击 "New Project"
   - 选择 "Deploy from GitHub repo"
   - 选择你的仓库

3. **配置服务**：
   - Railway 会自动检测到 Flask 应用
   - 会自动使用 `Procfile` 中的配置
   - 构建和部署会自动开始

4. **添加数据库（可选）**：
   - 如果需要使用 PostgreSQL（推荐生产环境）：
     - 在项目页面点击 "New" → "Database" → "Add PostgreSQL"
     - Railway 会自动创建数据库并设置 `DATABASE_URL` 环境变量
   - 如果使用 SQLite（免费但数据不持久）：
     - 无需额外配置，但注意 Railway 的临时文件系统会清空数据

5. **设置环境变量（如果需要）**：
   - 在服务设置中找到 "Variables" 标签
   - 可以添加自定义环境变量
   - `DATABASE_URL` 会在添加 PostgreSQL 后自动设置

6. **获取访问地址**：
   - 部署完成后，Railway 会提供一个 `.railway.app` 域名
   - 在服务设置中可以查看和自定义域名

### 第三步：验证部署

1. 访问 Railway 提供的域名
2. 测试应用功能：
   - 创建设备记录
   - 上传图片
   - 查看更新记录

## 重要提示

### 关于文件存储

⚠️ **重要**：Railway 使用临时文件系统，重启后 `uploads/` 目录的文件会丢失。

**解决方案**：
1. **使用外部存储**（推荐）：
   - 集成 Cloudinary、AWS S3 或其他对象存储服务
   - 修改代码将上传的文件保存到外部存储

2. **使用 Railway Volume**（需要付费计划）：
   - 可以创建持久化卷来存储文件

3. **使用数据库存储**（小文件）：
   - 将图片转换为 base64 存储在数据库中

### 关于数据库

- **SQLite**：免费但数据不持久，重启可能丢失
- **PostgreSQL**：推荐，Railway 提供免费 PostgreSQL 数据库

### 免费额度

Railway 免费层提供：
- $5/月 免费额度
- 足够小团队使用
- 超出后需要升级到付费计划

## 故障排查

### 部署失败

1. 检查构建日志：
   - 在 Railway 项目页面查看构建日志
   - 确认所有依赖都正确安装

2. 检查启动命令：
   - 确认 `Procfile` 中的命令正确
   - 确认 `gunicorn` 在 `requirements.txt` 中

3. 检查 Python 版本：
   - 确认 `runtime.txt` 中的版本 Railway 支持

### 应用无法访问

1. 检查服务状态：
   - 在 Railway 项目页面确认服务正在运行

2. 检查端口配置：
   - Railway 会自动设置 `PORT` 环境变量
   - 应用代码已支持从环境变量读取端口

3. 查看日志：
   - 在 Railway 项目页面查看实时日志

## 更新部署

每次推送到 GitHub 的 main 分支，Railway 会自动重新部署。

也可以手动触发部署：
- 在 Railway 项目页面点击 "Redeploy"

## 自定义域名

1. 在服务设置中找到 "Settings"
2. 在 "Domains" 部分添加自定义域名
3. 按照提示配置 DNS 记录

## 监控和日志

- Railway 提供实时日志查看
- 可以查看资源使用情况
- 可以设置告警通知

