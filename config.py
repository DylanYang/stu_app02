# config.py
import os
from pathlib import Path
from dotenv import load_dotenv

# 获取项目根目录
basedir = Path(__file__).parent.absolute()
env_path = basedir / '.env'

# 加载环境变量
if env_path.exists():
    load_dotenv(dotenv_path=env_path)
    print(f"✅ 加载配置文件: {env_path}")
else:
    print(f"⚠️ 警告: 找不到 .env 文件，使用默认配置")
    print(f"   期望路径: {env_path}")

class Config:
    """应用配置类"""
    
    # Flask 配置
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # MySQL 配置
    MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
    MYSQL_USER = os.getenv('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', '')
    MYSQL_DB = os.getenv('MYSQL_DB', 'student_db')
    
    # 处理 MySQL 端口 - 确保是整数
    mysql_port = os.getenv('MYSQL_PORT', '3306')
    try:
        MYSQL_PORT = int(mysql_port)
    except ValueError:
        print(f"⚠️ MYSQL_PORT 不是有效的数字: {mysql_port}，使用默认值 3306")
        MYSQL_PORT = 3306
    
    # 应用配置
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    
    @classmethod
    def validate(cls):
        """验证必要配置"""
        if not cls.MYSQL_PASSWORD:
            print("⚠️ 警告: MYSQL_PASSWORD 未设置")
            return False
        print(f"✅ 数据库配置: {cls.MYSQL_HOST}:{cls.MYSQL_PORT}/{cls.MYSQL_DB}")
        return True

# 创建配置实例
config = Config()

# 验证配置
config.validate()