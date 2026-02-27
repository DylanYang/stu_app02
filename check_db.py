# check_db.py
import sys
import os
from pathlib import Path

print("="*50)
print("🔍 数据库连接诊断工具")
print("="*50)

# 添加项目路径到系统路径
sys.path.insert(0, str(Path(__file__).parent))

# 首先检查 .env 文件
env_path = Path('.env')
if not env_path.exists():
    print("\n❌ .env 文件不存在！")
    print("请创建 .env 文件并设置数据库密码")
    print("可以从 .env.example 复制：")
    print("cp .env.example .env")
    sys.exit(1)

try:
    from config import Config
    print("\n📋 配置文件检查:")
    print(f"  MYSQL_HOST: {Config.MYSQL_HOST}")
    print(f"  MYSQL_PORT: {Config.MYSQL_PORT} (类型: {type(Config.MYSQL_PORT).__name__})")
    print(f"  MYSQL_USER: {Config.MYSQL_USER}")
    print(f"  MYSQL_DB: {Config.MYSQL_DB}")
    
    # 检查密码是否设置
    if Config.MYSQL_PASSWORD:
        print(f"  MYSQL_PASSWORD: {'*' * len(Config.MYSQL_PASSWORD)} (已设置)")
    else:
        print(f"  ⚠️ MYSQL_PASSWORD: 未设置！请在 .env 文件中设置数据库密码")
        print(f"  请编辑 .env 文件，修改 MYSQL_PASSWORD=你的密码")
        sys.exit(1)
        
except Exception as e:
    print(f"❌ 配置加载失败: {e}")
    sys.exit(1)

try:
    from models.database import test_connection, init_db, execute_query
    print("\n🔌 测试数据库连接:")
    
    # 测试连接
    if test_connection():
        print("  ✅ 数据库连接成功")
        
        print("\n📊 初始化数据库表:")
        if init_db():
            print("  ✅ 数据库表初始化成功")
            
            # 测试查询
            print("\n🔍 测试查询:")
            result = execute_query("SELECT COUNT(*) as count FROM students")
            if result is not None:
                print(f"  ✅ 查询成功，当前学生数: {result[0]['count'] if result else 0}")
            else:
                print("  ❌ 查询失败")
        else:
            print("  ❌ 数据库表初始化失败")
    else:
        print("  ❌ 数据库连接失败")
        print("\n可能的原因:")
        print("  1. MySQL 服务未启动")
        print("  2. 数据库密码错误")
        print("  3. 数据库 'student_db' 不存在")
        print("\n解决方法:")
        print("  1. 启动 MySQL: brew services start mysql")
        print("  2. 检查密码: mysql -u root -p")
        print("  3. 创建数据库: CREATE DATABASE student_db;")
        
except ImportError as e:
    print(f"❌ 导入错误: {e}")
    import traceback
    traceback.print_exc()
except Exception as e:
    print(f"❌ 数据库测试失败: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*50)