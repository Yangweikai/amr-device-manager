# AMR 设备信息记录工具

一个用于记录和管理 AMR（自主移动机器人）设备信息的 Web 应用。

## 功能特性

- 📋 **设备信息管理**：记录车端、手臂、TSC、E-Rack、充电桩等详细信息
- 📝 **更新记录追踪**：记录设备更新历史，包括更新原因、内容和结果
- 🖼️ **图片上传**：支持上传设备相关图片（AGVWEB）
- 🔍 **搜索功能**：快速搜索设备和更新记录
- 📱 **响应式设计**：适配各种设备屏幕

## 技术栈

- **后端**: Flask (Python)
- **数据库**: SQLite (本地) / PostgreSQL (生产环境)
- **前端**: HTML + CSS + JavaScript (原生)

## 快速开始

### 本地开发

1. **克隆仓库**：
   ```bash
   git clone <仓库地址>
   cd <项目目录>
   ```

2. **安装依赖**：
   ```bash
   pip install -r requirements.txt
   ```

3. **运行应用**：
   ```bash
   python app.py
   ```

4. **访问应用**：
   打开浏览器访问 `http://localhost:5000`

### 在线部署

详细部署步骤请参考 [DEPLOY.md](./DEPLOY.md)

## 项目结构

```
.
├── app.py              # Flask 应用主文件
├── requirements.txt    # Python 依赖
├── Procfile           # Render 部署配置
├── runtime.txt        # Python 版本
├── templates/         # HTML 模板
│   └── index.html
├── uploads/           # 上传文件目录
└── instance/         # 数据库文件（本地开发）
```

## 环境变量

- `DATABASE_URL`: 数据库连接 URL（可选，默认使用 SQLite）
- `PORT`: 服务端口（可选，默认 5000）

## 许可证

本项目仅供内部使用。

