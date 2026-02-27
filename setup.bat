@echo off
REM setup.bat - Windows安装脚本

echo 🚀 开始安装学生信息管理系统...
echo =================================

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 未找到Python，请先安装Python
    exit /b 1
)

REM 创建虚拟环境
echo 📦 创建虚拟环境...
python -m venv venv

REM 激活虚拟环境
echo 🔧 激活虚拟环境...
call venv\Scripts\activate.bat

REM 安装依赖
echo 📚 安装依赖包...
python -m pip install --upgrade pip
pip install -r requirements.txt

REM 检查.env文件
if not exist .env (
    echo ⚠️ 未找到.env文件，从模板创建...
    copy .env.example .env
    echo ✅ 已创建.env文件，请编辑并填入你的数据库密码
)

echo =================================
echo ✅ 安装完成！
echo.
echo 下一步：
echo 1. 编辑 .env 文件，设置你的数据库密码
echo 2. 运行应用: python app.py
echo 3. 访问 http://127.0.0.1:5000