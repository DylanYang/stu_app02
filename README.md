# 🎓 学生信息管理系统 (Student Information Management System)

基于 Python Flask + MySQL 的 MVC 架构学生信息管理系统。

## 📋 项目简介

这是一个功能完善的学生信息管理系统，采用 MVC 设计模式，提供学生信息的增删改查、搜索、统计等功能。系统界面美观，操作简单，适合用于课程设计或小型教育机构使用。

### ✨ 主要功能

- ✅ **学生管理**：添加、编辑、删除学生信息
- 🔍 **搜索功能**：支持按学号、姓名、专业模糊搜索
- 📊 **数据统计**：学生总数、性别分布、专业分布、平均年龄等
- 💾 **数据库管理**：自动创建表结构，支持数据库初始化
- 🎨 **响应式界面**：适配电脑、平板、手机等多种设备
- 🔒 **安全配置**：使用环境变量管理敏感信息

## 🛠️ 技术栈

| 技术 | 用途 |
|------|------|
| Python 3.8+ | 编程语言 |
| Flask 2.3+ | Web 框架 |
| MySQL 5.7+ | 数据库 |
| PyMySQL | MySQL 驱动 |
| Bootstrap 5 | 前端框架 |
| Font Awesome | 图标库 |
| Jinja2 | 模板引擎 |

## 📁 项目结构

```
stu_app_02/
├── .env                    # 环境变量配置（请勿提交）
├── .env.example            # 环境变量示例
├── .gitignore              # Git 忽略文件
├── requirements.txt        # 项目依赖
├── README.md               # 项目说明文档
├── app.py                  # 应用入口
├── config.py               # 配置文件
├── check_db.py             # 数据库诊断工具
├── init_db.sql             # 数据库初始化脚本
├── controllers/            # 控制器层
│   ├── __init__.py
│   └── student_controller.py
├── models/                 # 模型层
│   ├── __init__.py
│   ├── database.py
│   └── student_model.py
└── templates/              # 视图层（模板文件）
    ├── index.html
    ├── add.html
    └── edit.html
```

## 🚀 快速开始

### 环境要求

- Python 3.8 或更高版本
- MySQL 5.7 或更高版本
- pip 包管理工具

### 安装步骤

#### 1. 克隆项目

```bash
git clone <项目地址>
cd stu_app_02
```

#### 2. 创建虚拟环境（推荐）

```bash
# macOS/Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

#### 3. 安装依赖

```bash
pip install -r requirements.txt
```

#### 4. 配置数据库

复制环境变量示例文件并编辑：

```bash
cp .env.example .env
```

编辑 `.env` 文件，填入你的数据库信息：

```env
# Flask 配置
SECRET_KEY=your-secret-key-here

# MySQL 数据库配置
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=你的数据库密码
MYSQL_DB=student_db
MYSQL_PORT=3306

# 应用配置
DEBUG=True
```

#### 5. 创建数据库

```bash
# 登录 MySQL
mysql -u root -p

# 创建数据库
CREATE DATABASE student_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;

# 或者运行初始化脚本
mysql -u root -p < init_db.sql
```

#### 6. 运行诊断工具（可选）

```bash
python check_db.py
```

#### 7. 启动应用

```bash
python app.py
```

访问 http://127.0.0.1:5000 即可使用系统。

## 📖 使用指南

### 首页功能

- **统计卡片**：显示总学生数、男女比例、平均年龄
- **搜索框**：输入关键词搜索学生
- **添加按钮**：跳转到添加学生页面
- **初始化数据库**：创建必要的数据库表
- **测试连接**：测试数据库连接状态

### 学生管理

#### 添加学生
1. 点击首页的"添加学生"按钮
2. 填写学生信息（学号、姓名、性别为必填）
3. 点击"保存"完成添加

#### 编辑学生
1. 在学生列表中找到目标学生
2. 点击"编辑"按钮
3. 修改信息后点击"更新"

#### 删除学生
1. 在学生列表中找到目标学生
2. 点击"删除"按钮
3. 确认删除操作

#### 搜索学生
1. 在首页搜索框输入关键词
2. 支持学号、姓名、专业模糊搜索
3. 显示匹配的所有学生

## 🗄️ 数据库设计

### students 表

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| student_id | VARCHAR(20) | PRIMARY KEY | 学号 |
| name | VARCHAR(50) | NOT NULL | 姓名 |
| gender | ENUM('男','女','其他') | NOT NULL | 性别 |
| age | INT | | 年龄 |
| major | VARCHAR(100) | | 专业 |
| phone | VARCHAR(20) | | 电话 |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | 创建时间 |
| updated_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP ON UPDATE | 更新时间 |

### scores 表（可选）

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | INT | AUTO_INCREMENT PRIMARY KEY | 记录ID |
| student_id | VARCHAR(20) | FOREIGN KEY | 学号 |
| course_name | VARCHAR(100) | NOT NULL | 课程名称 |
| score | DECIMAL(5,2) | | 分数 |
| credit | INT | DEFAULT 0 | 学分 |
| semester | VARCHAR(20) | | 学期 |
| exam_date | DATE | | 考试日期 |

## 🔧 常见问题解决

### Q1: 数据库连接失败

**症状**：应用启动时显示数据库连接错误
**解决**：
1. 检查 MySQL 服务是否运行：`brew services list` (macOS) 或 `systemctl status mysql` (Linux)
2. 验证 `.env` 中的密码是否正确
3. 运行诊断工具：`python check_db.py`

### Q2: 模板找不到变量

**症状**：访问页面时显示 `UndefinedError`
**解决**：确保控制器中传递了所有模板需要的变量，特别是 `stats` 变量

### Q3: 添加学生时学号重复

**症状**：添加学生时提示学号已存在
**解决**：学号是主键，必须唯一。请使用不同的学号。

### Q4: 中文显示乱码

**症状**：页面或数据库中的中文显示为乱码
**解决**：
1. 确保数据库使用 utf8mb4 字符集
2. 连接时指定 charset='utf8mb4'

## 🧪 测试数据

系统启动后，可以通过以下 SQL 插入测试数据：

```sql
INSERT INTO students (student_id, name, gender, age, major, phone) VALUES
('2024001', '张三', '男', 20, '计算机科学', '13800138001'),
('2024002', '李四', '女', 19, '软件工程', '13800138002'),
('2024003', '王五', '男', 21, '人工智能', '13800138003'),
('2024004', '赵六', '女', 20, '数据科学', '13800138004');
```

## 📝 开发计划

- [ ] 添加成绩管理功能
- [ ] 导入/导出 Excel 功能
- [ ] 数据可视化图表
- [ ] 用户登录和权限管理
- [ ] 分页显示学生列表
- [ ] 批量删除学生

## 🤝 贡献指南

欢迎贡献代码或提出改进建议！

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 提交 Pull Request

## 📄 许可证

本项目采用 MIT 许可证。详见 `LICENSE` 文件。

## 📧 联系方式

如有问题，请联系：

- 作者：[你的名字]
- 邮箱：[你的邮箱]
- 项目地址：[项目 GitHub 地址]

## 🙏 致谢

- Flask 框架文档
- Bootstrap 5 文档
- Font Awesome 图标库
- 所有贡献者和用户

---

**Happy Coding!** 🚀