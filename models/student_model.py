# models/student_model.py
from typing import List, Dict, Optional, Any
from models.database import get_db_connection

class StudentModel:
    """学生模型 - 处理所有学生相关的数据操作"""
    
    @staticmethod
    def get_all_students() -> List[Dict[str, Any]]:
        """获取所有学生"""
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute('SELECT * FROM students ORDER BY student_id')
                students = cursor.fetchall()
                return students
        except Exception as e:
            print(f"❌ 数据库查询错误: {e}")
            return []
        finally:
            connection.close()
    
    @staticmethod
    def get_student_by_id(student_id: str) -> Optional[Dict[str, Any]]:
        """根据ID获取单个学生"""
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute('SELECT * FROM students WHERE student_id = %s', (student_id,))
                student = cursor.fetchone()
                return student
        except Exception as e:
            print(f"❌ 数据库查询错误: {e}")
            return None
        finally:
            connection.close()
    
    @staticmethod
    def add_student(student_data: Dict[str, Any]) -> bool:
        """添加学生"""
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute('''
                    INSERT INTO students (student_id, name, gender, age, major, phone)
                    VALUES (%s, %s, %s, %s, %s, %s)
                ''', (
                    student_data['student_id'],
                    student_data['name'],
                    student_data['gender'],
                    student_data.get('age'),
                    student_data.get('major'),
                    student_data.get('phone')
                ))
            connection.commit()
            return True
        except Exception as e:
            connection.rollback()
            print(f"❌ 添加学生错误: {e}")
            return False
        finally:
            connection.close()
    
    @staticmethod
    def update_student(student_id: str, student_data: Dict[str, Any]) -> bool:
        """更新学生信息"""
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute('''
                    UPDATE students 
                    SET name=%s, gender=%s, age=%s, major=%s, phone=%s
                    WHERE student_id=%s
                ''', (
                    student_data['name'],
                    student_data['gender'],
                    student_data.get('age'),
                    student_data.get('major'),
                    student_data.get('phone'),
                    student_id
                ))
            connection.commit()
            return cursor.rowcount > 0
        except Exception as e:
            connection.rollback()
            print(f"❌ 更新学生错误: {e}")
            return False
        finally:
            connection.close()
    
    @staticmethod
    def delete_student(student_id: str) -> bool:
        """删除学生"""
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute('DELETE FROM students WHERE student_id = %s', (student_id,))
            connection.commit()
            return cursor.rowcount > 0
        except Exception as e:
            connection.rollback()
            print(f"❌ 删除学生错误: {e}")
            return False
        finally:
            connection.close()
    
    @staticmethod
    def search_students(keyword: str) -> List[Dict[str, Any]]:
        """搜索学生"""
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                pattern = f"%{keyword}%"
                cursor.execute('''
                    SELECT * FROM students 
                    WHERE student_id LIKE %s OR name LIKE %s OR major LIKE %s
                    ORDER BY student_id
                ''', (pattern, pattern, pattern))
                return cursor.fetchall()
        except Exception as e:
            print(f"❌ 搜索错误: {e}")
            return []
        finally:
            connection.close()
    
    @staticmethod
    def get_statistics() -> Dict[str, Any]:
        """获取统计信息"""
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                # 总学生数
                cursor.execute('SELECT COUNT(*) as total FROM students')
                result = cursor.fetchone()
                total = result['total'] if result else 0
                
                # 性别分布
                cursor.execute('''
                    SELECT gender, COUNT(*) as count 
                    FROM students 
                    GROUP BY gender
                ''')
                gender_stats = cursor.fetchall()
                
                # 专业分布
                cursor.execute('''
                    SELECT major, COUNT(*) as count 
                    FROM students 
                    WHERE major IS NOT NULL AND major != ''
                    GROUP BY major
                    ORDER BY count DESC
                    LIMIT 5
                ''')
                major_stats = cursor.fetchall()
                
                # 年龄统计 - 使用 COALESCE 处理 NULL 值
                cursor.execute('''
                    SELECT 
                        COALESCE(AVG(age), 0) as avg_age,
                        COALESCE(MIN(age), 0) as min_age,
                        COALESCE(MAX(age), 0) as max_age
                    FROM students 
                    WHERE age IS NOT NULL
                ''')
                age_stats = cursor.fetchone()
                
                # 确保 age_stats 有默认值
                if not age_stats:
                    age_stats = {'avg_age': 0, 'min_age': 0, 'max_age': 0}
                
                return {
                    'total_students': total,
                    'gender_distribution': gender_stats if gender_stats else [],
                    'major_distribution': major_stats if major_stats else [],
                    'age_stats': age_stats
                }
        except Exception as e:
            print(f"❌ 统计错误: {e}")
            # 返回默认值
            return {
                'total_students': 0,
                'gender_distribution': [],
                'major_distribution': [],
                'age_stats': {'avg_age': 0, 'min_age': 0, 'max_age': 0}
            }
        finally:
            connection.close()
    
    @staticmethod
    def check_student_exists(student_id: str) -> bool:
        """检查学生是否存在"""
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute('SELECT COUNT(*) as count FROM students WHERE student_id = %s', (student_id,))
                result = cursor.fetchone()
                return result['count'] > 0
        except Exception as e:
            print(f"❌ 检查学生错误: {e}")
            return False
        finally:
            connection.close()