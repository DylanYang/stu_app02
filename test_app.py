# test_app.py
import unittest
import pymysql
from config import Config
from models.student_model import StudentModel

class TestStudentModel(unittest.TestCase):
    """测试学生模型"""
    
    @classmethod
    def setUpClass(cls):
        """测试前准备"""
        # 检查数据库连接
        try:
            from models.database import get_db_connection
            conn = get_db_connection()
            conn.close()
            print("✅ 数据库连接正常")
        except Exception as e:
            print(f"❌ 数据库连接失败: {e}")
            raise e
    
    def test_get_all_students(self):
        """测试获取所有学生"""
        students = StudentModel.get_all_students()
        self.assertIsInstance(students, list)
        print(f"✅ 获取学生列表成功，共 {len(students)} 条记录")
    
    def test_add_and_delete_student(self):
        """测试添加和删除学生"""
        # 添加测试学生
        test_student = {
            'student_id': 'TEST001',
            'name': '测试学生',
            'gender': '男',
            'age': 20,
            'major': '测试专业',
            'phone': '13800138000'
        }
        
        # 添加
        result = StudentModel.add_student(test_student)
        self.assertTrue(result)
        print("✅ 添加学生成功")
        
        # 验证添加
        student = StudentModel.get_student_by_id('TEST001')
        self.assertIsNotNone(student)
        self.assertEqual(student['name'], '测试学生')
        
        # 删除
        result = StudentModel.delete_student('TEST001')
        self.assertTrue(result)
        print("✅ 删除学生成功")
        
        # 验证删除
        student = StudentModel.get_student_by_id('TEST001')
        self.assertIsNone(student)

if __name__ == '__main__':
    unittest.main(verbosity=2)