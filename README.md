# WanderAI - 智能旅行计划助手

基于 **CrewAI 多智能体协作框架** + **Django REST Framework** + **Vue.js** 的全栈旅行计划生成平台。用户只需输入出发地、目的地、日期和兴趣偏好，系统会派出多个 AI 智能体协同工作，自动生成包含交通、住宿、行程、美食、天气和预算的完整旅行方案。

***

## 项目架构

```
Trip_Planner.egg-info/
├── travel_project/          # Django 后端
│   ├── travel_project/      # 项目配置（settings、urls、wsgi）
│   ├── agents/              # AI 智能体定义（CrewAI）
│   ├── tasks/               # AI 任务编排
│   ├── tools/               # 工具集（搜索、浏览器抓取、计算器、文件IO）
│   ├── trip/                # 行程应用（models、views、urls）
│   ├── auth_app/            # 认证应用（注册、登录、JWT）
│   ├── user/                # 用户应用（收藏行程）
│   ├── main.py              # CrewAI 行程生成核心逻辑
│   ├── manage.py            # Django 管理入口
│   ├── .env.example         # 环境变量模板
│   └── requirements.txt     # Python 依赖
│
├── my-travel-app/           # Vue.js 前端
│   ├── src/
│   │   ├── components/      # Vue 组件（Home、login、plan、register、history）
│   │   ├── router/          # 前端路由
│   │   ├── store/           # Vuex 状态管理
│   │   ├── api/             # API 请求封装（axios）
│   │   └── assets/          # 静态资源（CSS、图片、视频）
│   ├── public/              # 公共静态文件
│   └── package.json         # Node.js 依赖
│
├── .gitignore               # 根 Git 忽略规则
└── README.md                # 本文件
```

***

## AI 智能体协作流程

系统由 **7 个专业 AI Agent** 协同工作，由 CrewAI 框架编排：

| Agent                               | 职责                            |
| ----------------------------------- | ----------------------------- |
| **Trip\_Planner\_Agent** 🗺️        | 总行程规划负责人，汇总各 Agent 结果生成最终旅行计划 |
| **Destination\_Research\_Agent** 🔍 | 目的地研究专家，推荐景点、体验和当地文化          |
| **Accommodation\_Agent** 🏨         | 住宿资源专家，推荐酒店/民宿并对比价格           |
| **Transportation\_Agent** 🚗        | 交通规划专家，规划城际 + 市内交通方案          |
| **Weather\_Agent** 🌤️              | 天气预报专家，提供每日/每小时天气和预警          |
| **Itinerary\_Planner\_Agent** 📋    | 日程规划专家，制定每日详细行程               |
| **Budget\_Analyst\_Agent** 💰       | 预算分析师，拆解费用并提供省钱建议             |

所有 Agent 基于 **DeepSeek / OpenAI 兼容 API** 驱动，具备搜索互联网和计算能力。

***

## 功能特性

- **AI 行程生成** — 输入目的地和日期，自动生成完整旅行计划（Markdown 格式）
- **行程修订** — 对已生成的计划提出反馈，AI 自动修订
- **行程导出** — 支持导出为 Markdown / TXT / PDF
- **用户系统** — 注册、登录（JWT 认证）、邮箱验证码
- **行程收藏** — 登录后可以保存和查看历史行程
- **响应式 UI** — Vue.js 前端，视频背景，动画效果

***

## API 接口概览

| 模块 | 方法     | 路径                               | 说明      |
| -- | ------ | -------------------------------- | ------- |
| 认证 | POST   | `/api/auth/register`             | 用户注册    |
| 认证 | POST   | `/api/auth/login`                | 用户登录    |
| 认证 | POST   | `/api/auth/send_email_code`      | 发送邮箱验证码 |
| 行程 | POST   | `/api/trip/generate`             | 生成旅行计划  |
| 行程 | GET    | `/api/trip/<trip_id>/summary`    | 获取行程总结  |
| 行程 | GET    | `/api/trip/<trip_id>/weather`    | 获取天气信息  |
| 行程 | GET    | `/api/trip/<trip_id>/transport`  | 获取交通安排  |
| 行程 | GET    | `/api/trip/<trip_id>/hotel`      | 获取住宿信息  |
| 行程 | GET    | `/api/trip/<trip_id>/food`       | 获取美食推荐  |
| 行程 | GET    | `/api/trip/<trip_id>/itinerary`  | 获取每日行程  |
| 行程 | GET    | `/api/trip/<trip_id>/budget`     | 获取预算明细  |
| 行程 | GET    | `/api/trip/<trip_id>/download`   | 下载行程文件  |
| 行程 | POST   | `/api/trip/<trip_id>/regenerate` | 重新生成行程  |
| 行程 | POST   | `/api/trip/<trip_id>/revise`     | 修订行程    |
| 行程 | DELETE | `/api/trip/<trip_id>/delete`     | 删除行程    |

***

## 快速开始

### 环境要求

- **Python** >= 3.11
- **Node.js** >= 16
- **MySQL** >= 5.7（或 SQLite 用于开发）

### 1. 克隆仓库

```bash
git clone <your-repo-url>
cd Trip_Planner.egg-info
```

### 2. 配置后端

```bash
cd travel_project

# 创建虚拟环境
python -m venv .venv
.venv\Scripts\activate    # Windows
# source .venv/bin/activate  # macOS/Linux

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
# 将 .env.example 复制为 .env，并填入你的 API 密钥和数据库信息
copy .env.example .env    # Windows
# cp .env.example .env    # macOS/Linux

# 数据库迁移
python manage.py makemigrations
python manage.py migrate

# 启动后端（默认 http://127.0.0.1:8000）
python manage.py runserver
```

### 3. 配置前端

```bash
cd my-travel-app

# 安装依赖
npm install

# 启动开发服务器（默认 http://localhost:8080）
npm run serve
```

### 4. 环境变量说明

编辑 `travel_project/.env`，必须配置以下变量：

| 变量                    | 说明                 | 获取方式                                                        |
| --------------------- | ------------------ | ----------------------------------------------------------- |
| `DJANGO_SECRET_KEY`   | Django 密钥          | 可使用 `django.core.management.utils.get_random_secret_key` 生成 |
| `DB_PASSWORD`         | 数据库密码              | 你的 MySQL 密码                                                 |
| `SERPER_API_KEY`      | Google 搜索 API      | [serper.dev](https://serper.dev) 注册获取                       |
| `OPENAI_API_KEY`      | OpenAI / 代理 API 密钥 | [platform.openai.com](https://platform.openai.com)          |
| `DEEPSEEK_API_KEY`    | DeepSeek API 密钥    | [platform.deepseek.com](https://platform.deepseek.com)      |
| `EMAIL_HOST_USER`     | QQ 邮箱地址            | 用于发送验证码                                                     |
| `EMAIL_HOST_PASSWORD` | QQ 邮箱授权码           | QQ 邮箱 → 设置 → 账户 → POP3/SMTP 服务 → 生成授权码                      |

***

## 技术栈

### 后端

| 技术                            | 用途           |
| ----------------------------- | ------------ |
| Django 5.2                    | Web 框架       |
| Django REST Framework         | RESTful API  |
| djangorestframework-simplejwt | JWT 认证       |
| CrewAI                        | 多智能体 AI 协作框架 |
| LangChain                     | LLM 调用抽象层    |
| bcrypt                        | 密码哈希         |
| MySQL / SQLite                | 数据持久化        |
| ReportLab                     | PDF 生成       |

### 前端

| 技术           | 用途       |
| ------------ | -------- |
| Vue.js 2.6   | 前端框架     |
| Vue Router   | 前端路由     |
| Vuex         | 状态管理     |
| Element UI   | UI 组件库   |
| Axios        | HTTP 请求  |
| Tailwind CSS | 原子化 CSS  |
| Less         | CSS 预处理器 |

***

## License

本项目仅供学习和个人使用。
