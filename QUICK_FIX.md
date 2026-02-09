# Railway 构建失败 - 快速修复指南

## 立即检查事项

### 1. 查看 Railway 构建日志
在 Railway 项目页面：
- 点击失败的服务（红色警告图标）
- 查看 "Deployments" 或 "Logs" 标签
- **复制最后的错误信息**

### 2. 常见错误及快速修复

#### ❌ 错误：`ModuleNotFoundError` 或 `No module named`
**修复**：检查 `requirements.txt` 是否包含所有依赖

#### ❌ 错误：`gunicorn: command not found`
**修复**：确保 `requirements.txt` 包含 `gunicorn==21.2.0`

#### ❌ 错误：Python 版本问题
**修复**：
- 删除 `runtime.txt`，或
- 改为：`python-3.11`（使用主版本号）

#### ❌ 错误：端口绑定失败
**修复**：已更新 `Procfile` 使用 `$PORT` 环境变量

## 已修复的配置

✅ 已更新 `Procfile`：使用 `$PORT` 环境变量
✅ 已简化 `railway.json`：移除可能导致问题的配置
✅ 已确认 `runtime.txt` 格式正确

## 下一步操作

1. **提交更改到 GitHub**：
   ```bash
   git add .
   git commit -m "修复 Railway 构建配置"
   git push
   ```

2. **在 Railway 重新部署**：
   - Railway 会自动检测到新的提交并重新部署
   - 或手动点击 "Redeploy"

3. **查看新的构建日志**：
   - 如果仍然失败，查看新的错误信息
   - 根据具体错误信息进一步修复

## 如果仍然失败

请提供 Railway 构建日志中的**最后几行错误信息**，我可以帮你进一步诊断。

常见需要检查的地方：
- 构建日志的最后 20-30 行
- 是否有特定的 Python 包安装失败
- 是否有文件路径问题
- 是否有权限问题

