# Railway 构建失败故障排查

## 常见构建失败原因及解决方案

### 1. 查看构建日志
在 Railway 项目页面：
- 点击失败的服务
- 查看 "Deployments" 标签页
- 点击失败的部署，查看详细日志

### 2. Python 版本问题

**问题**：`runtime.txt` 格式不正确

**解决方案**：
- 确保 `runtime.txt` 内容为：`python-3.11.7` 或 `3.11.7`
- Railway 会自动检测，也可以删除 `runtime.txt` 让 Railway 使用默认版本

### 3. 依赖安装失败

**问题**：某些包无法安装（特别是 `psycopg2-binary`）

**解决方案**：
- 检查 `requirements.txt` 中的包版本是否兼容
- 如果 `psycopg2-binary` 安装失败，可以尝试：
  ```txt
  psycopg2-binary==2.9.9
  ```
  或者使用：
  ```txt
  psycopg2==2.9.9
  ```

### 4. 启动命令问题

**问题**：`Procfile` 或启动命令不正确

**解决方案**：
- 确保 `Procfile` 内容为：`web: gunicorn app:app`
- 或者使用：`web: gunicorn app:app --bind 0.0.0.0:$PORT`

### 5. 缺少必要文件

**问题**：Railway 无法找到应用入口

**解决方案**：
- 确保 `app.py` 在项目根目录
- 确保 `templates/` 目录存在
- 确保 `uploads/` 目录存在（或创建 `.gitkeep` 文件）

### 6. 数据库初始化问题

**问题**：数据库连接或初始化失败

**解决方案**：
- 如果使用 PostgreSQL，确保已添加 PostgreSQL 服务
- 检查 `DATABASE_URL` 环境变量是否正确设置
- 如果使用 SQLite，确保有写入权限

## 快速修复步骤

### 步骤 1：检查构建日志
1. 在 Railway 项目页面找到失败的部署
2. 点击查看详细日志
3. 找到错误信息（通常在最后几行）

### 步骤 2：根据错误信息修复

#### 错误：`No module named 'xxx'`
- 检查 `requirements.txt` 是否包含该模块
- 确保版本号正确

#### 错误：`Python version not found`
- 检查 `runtime.txt` 格式
- 或删除 `runtime.txt` 使用默认版本

#### 错误：`gunicorn: command not found`
- 确保 `gunicorn` 在 `requirements.txt` 中
- 检查 `Procfile` 是否正确

#### 错误：`Port already in use` 或端口相关错误
- 确保使用 `$PORT` 环境变量
- 检查启动命令是否正确

### 步骤 3：重新部署
1. 修复问题后，提交代码到 GitHub
2. Railway 会自动重新部署
3. 或手动点击 "Redeploy"

## 推荐的配置

### 最小化配置（让 Railway 自动检测）
- 保留 `Procfile`
- 保留 `requirements.txt`
- 可以删除 `runtime.txt` 和 `railway.json`，让 Railway 自动检测

### 完整配置（明确指定）
- `Procfile`: `web: gunicorn app:app`
- `requirements.txt`: 包含所有依赖
- `runtime.txt`: `python-3.11.7`
- `railway.json`: 简化配置

## 测试本地构建

在部署前，可以在本地测试：

```bash
# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 测试启动
gunicorn app:app
```

如果本地可以运行，Railway 也应该可以。

## 联系支持

如果以上方法都无法解决：
1. 复制完整的构建日志
2. 在 Railway Discord 或 GitHub 社区寻求帮助
3. 检查 Railway 状态页面是否有服务问题

