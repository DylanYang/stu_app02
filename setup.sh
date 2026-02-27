#!/bin/bash
# setup.sh - 项目安装脚本

echo "🚀 开始安装学生信息管理系统..."
echo "================================="

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "❌ 未找到Python3，请先安装Python3"
    exit 1
fi

# 创建虚拟环境
echo "📦 创建虚拟环境..."
python3 -m venv venv

# 激活虚拟环境
echo "🔧 激活虚拟环境..."
source venv/bin/activate

# 安装依赖
echo "📚 安装依赖包..."
pip install --upgrade pip
pip install -r requirements.txt

# 检查.env文件
if [ ! -f .env ]; then
    echo "⚠️ 未找到.env文件，从模板创建..."
    cp .env.example .env
    echo "✅ 已创建.env文件，请编辑并填入你的数据库密码"
fi

echo "================================="
echo "✅ 安装完成！"
echo ""
echo "下一步："
echo "1. 编辑 .env 文件，设置你的数据库密码"
echo "2. 运行应用: python app.py"
echo "3. 访问 http://127.0.0.1:5000"