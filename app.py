# app.py
import os
from flask import Flask
from config import Config
from controllers.student_controller import student_bp

def create_app():
    """应用工厂函数"""
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # 确保templates文件夹存在
    if not os.path.exists('templates'):
        os.makedirs('templates')
    
    # 注册蓝图
    app.register_blueprint(student_bp)
    
    return app

if __name__ == '__main__':
    app = create_app()
    print("="*50)
    print("学生信息管理系统 (MVC模式) 启动成功！")
    print(f"访问地址：http://127.0.0.1:5000")
    print("="*50)
    app.run(debug=Config.DEBUG)