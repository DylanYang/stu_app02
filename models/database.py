# models/database.py
import pymysql
from pymysql.cursors import DictCursor
from config import Config

def get_db_connection():
    """获取数据库连接"""
    try:
        # 打印连接信息（调试用）
        print(f"🔌 尝试连接数据库: {Config.MYSQL_HOST}:{Config.MYSQL_PORT}/{Config.MYSQL_DB}")
        
        connection = pymysql.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            database=Config.MYSQL_DB,
            port=Config.MYSQL_PORT,
            cursorclass=DictCursor,
            charset='utf8mb4',
            autocommit=False,
            connect_timeout=5
        )
        print("✅ 数据库连接成功")
        return connection
    except pymysql.Error as e:
        print(f"❌ 数据库连接错误: {e}")
        raise e

def init_db():
    """初始化数据库表"""
    connection = None
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            # 创建students表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS students (
                    student_id VARCHAR(20) PRIMARY KEY,
                    name VARCHAR(50) NOT NULL,
                    gender ENUM('男', '女', '其他') NOT NULL,
                    age INT,
                    major VARCHAR(100),
                    phone VARCHAR(20),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """)
            
            # 创建scores表（可选）
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS scores (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    student_id VARCHAR(20) NOT NULL,
                    course_name VARCHAR(100) NOT NULL,
                    score DECIMAL(5,2),
                    credit INT DEFAULT 0,
                    semester VARCHAR(20),
                    exam_date DATE,
                    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
                    INDEX idx_student (student_id)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """)
            
        connection.commit()
        print("✅ 数据库表初始化成功")
        return True
    except Exception as e:
        print(f"❌ 初始化数据库表失败: {e}")
        if connection:
            connection.rollback()
        return False
    finally:
        if connection:
            connection.close()

def test_connection():
    """测试数据库连接"""
    connection = None
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            print("✅ 数据库连接测试成功")
            return True
    except Exception as e:
        print(f"❌ 数据库连接测试失败: {e}")
        return False
    finally:
        if connection:
            connection.close()

def execute_query(query, params=None):
    """执行查询并返回结果"""
    connection = None
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            # 如果是SELECT查询，返回结果
            if query.strip().upper().startswith('SELECT'):
                result = cursor.fetchall()
                return result
            else:
                # 如果是INSERT/UPDATE/DELETE，提交事务
                connection.commit()
                return cursor.rowcount
    except Exception as e:
        print(f"❌ 执行查询失败: {e}")
        if connection:
            connection.rollback()
        return None
    finally:
        if connection:
            connection.close()

def execute_insert(query, params=None):
    """执行插入操作，返回最后插入的ID"""
    connection = None
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            connection.commit()
            return cursor.lastrowid
    except Exception as e:
        print(f"❌ 执行插入失败: {e}")
        if connection:
            connection.rollback()
        return None
    finally:
        if connection:
            connection.close()