# controllers/student_controller.py
from flask import render_template, request, redirect, url_for, flash, Blueprint
from models.student_model import StudentModel
from models.database import init_db, test_connection

# 创建蓝图
student_bp = Blueprint('student', __name__, url_prefix='/')

class StudentController:
    """学生控制器 - 处理业务逻辑和HTTP请求"""
    
    @staticmethod
    @student_bp.route('/')
    def index():
        """首页：显示所有学生"""
        try:
            # 测试数据库连接
            if not test_connection():
                flash('数据库连接失败，请检查配置', 'danger')
                return render_template('index.html', students=[], stats={}, title='学生列表')
            
            students = StudentModel.get_all_students()
            stats = StudentModel.get_statistics()
            return render_template('index.html', 
                                 students=students, 
                                 stats=stats,
                                 title='学生列表')
        except Exception as e:
            print(f"❌ 系统错误: {e}")
            flash(f'系统错误：{str(e)}', 'danger')
            return render_template('index.html', students=[], stats={}, title='学生列表')
    
    @staticmethod
    @student_bp.route('/init-db')
    def init_database():
        """初始化数据库"""
        try:
            if init_db():
                flash('数据库初始化成功！', 'success')
            else:
                flash('数据库初始化失败，请检查配置', 'danger')
        except Exception as e:
            flash(f'数据库初始化失败：{str(e)}', 'danger')
        return redirect(url_for('student.index'))
    
    @staticmethod
    @student_bp.route('/test-db')
    def test_database():
        """测试数据库连接"""
        if test_connection():
            flash('数据库连接成功！', 'success')
        else:
            flash('数据库连接失败，请检查配置', 'danger')
        return redirect(url_for('student.index'))
    
    @staticmethod
    @student_bp.route('/add', methods=['GET', 'POST'])
    def add():
        """添加学生"""
        if request.method == 'POST':
            # 验证输入
            error = StudentController._validate_student_data(request.form)
            if error:
                flash(error, 'danger')
                return render_template('add.html', title='添加学生')
            
            # 检查学号是否已存在
            if StudentModel.check_student_exists(request.form['student_id'].strip()):
                flash('学号已存在，请使用其他学号', 'danger')
                return render_template('add.html', title='添加学生')
            
            # 准备数据
            student_data = {
                'student_id': request.form['student_id'].strip(),
                'name': request.form['name'].strip(),
                'gender': request.form['gender'],
                'age': int(request.form['age']) if request.form.get('age') else None,
                'major': request.form.get('major', '').strip() or None,
                'phone': request.form.get('phone', '').strip() or None
            }
            
            # 调用模型添加
            if StudentModel.add_student(student_data):
                flash(f'学生 {student_data["name"]} 添加成功！', 'success')
                return redirect(url_for('student.index'))
            else:
                flash('添加失败，请重试', 'danger')
        
        return render_template('add.html', title='添加学生')
    
    @staticmethod
    @student_bp.route('/edit/<student_id>', methods=['GET', 'POST'])
    def edit(student_id):
        """编辑学生"""
        if request.method == 'POST':
            # 验证输入
            error = StudentController._validate_student_data(request.form, edit_mode=True)
            if error:
                flash(error, 'danger')
                return redirect(url_for('student.edit', student_id=student_id))
            
            # 准备数据
            student_data = {
                'name': request.form['name'].strip(),
                'gender': request.form['gender'],
                'age': int(request.form['age']) if request.form.get('age') else None,
                'major': request.form.get('major', '').strip() or None,
                'phone': request.form.get('phone', '').strip() or None
            }
            
            # 调用模型更新
            if StudentModel.update_student(student_id, student_data):
                flash('学生信息更新成功！', 'success')
                return redirect(url_for('student.index'))
            else:
                flash('更新失败', 'danger')
        
        # GET请求：获取学生信息
        student = StudentModel.get_student_by_id(student_id)
        if not student:
            flash('学生不存在！', 'danger')
            return redirect(url_for('student.index'))
        
        return render_template('edit.html', student=student, title='编辑学生')
    
    @staticmethod
    @student_bp.route('/delete/<student_id>')
    def delete(student_id):
        """删除学生"""
        if StudentModel.delete_student(student_id):
            flash('学生删除成功！', 'success')
        else:
            flash('删除失败，学生不存在', 'danger')
        
        return redirect(url_for('student.index'))
    
    @staticmethod
    @student_bp.route('/search')
    def search():
        """搜索学生"""
        keyword = request.args.get('q', '').strip()
        
        # 获取默认的 stats 结构
        default_stats = {
            'total_students': 0,
            'gender_distribution': [],
            'major_distribution': [],
            'age_stats': {'avg_age': 0, 'min_age': 0, 'max_age': 0}
        }
        
        if keyword:
            try:
                students = StudentModel.search_students(keyword)
                
                # 获取统计信息（可选，如果不需要统计可以传空字典）
                try:
                    stats = StudentModel.get_statistics()
                except:
                    stats = default_stats
                
                return render_template('index.html', 
                                    students=students, 
                                    stats=stats,
                                    search_keyword=keyword,
                                    title=f'搜索: {keyword}')
            except Exception as e:
                print(f"❌ 搜索错误: {e}")
                flash(f'搜索失败：{str(e)}', 'danger')
                return redirect(url_for('student.index'))
        
        return redirect(url_for('student.index'))
    
    @staticmethod
    def _validate_student_data(form_data, edit_mode=False):
        """验证学生数据"""
        if not edit_mode and not form_data.get('student_id'):
            return '学号不能为空'
        
        if not edit_mode and len(form_data.get('student_id', '').strip()) < 3:
            return '学号至少需要3个字符'
        
        if not form_data.get('name'):
            return '姓名不能为空'
        
        if len(form_data.get('name', '').strip()) < 2:
            return '姓名至少需要2个字符'
        
        if not form_data.get('gender'):
            return '请选择性别'
        
        # 验证年龄
        age = form_data.get('age')
        if age:
            try:
                age_int = int(age)
                if age_int < 1 or age_int > 150:
                    return '年龄必须在1-150之间'
            except ValueError:
                return '年龄必须是数字'
        
        # 验证电话（如果填写）
        phone = form_data.get('phone')
        if phone:
            # 简单的电话验证
            import re
            if not re.match(r'^[\d\s\-+()]{7,20}$', phone.strip()):
                return '电话号码格式不正确'
        
        return None