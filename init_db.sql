-- init_db.sql
-- 学生信息管理系统数据库初始化脚本

-- 创建数据库（如果不存在）
CREATE DATABASE IF NOT EXISTS student_db 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

USE student_db;

-- 创建学生表
CREATE TABLE IF NOT EXISTS students (
    student_id VARCHAR(20) PRIMARY KEY COMMENT '学号',
    name VARCHAR(50) NOT NULL COMMENT '姓名',
    gender ENUM('男', '女', '其他') NOT NULL COMMENT '性别',
    age INT COMMENT '年龄',
    major VARCHAR(100) COMMENT '专业',
    phone VARCHAR(20) COMMENT '电话',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='学生信息表';

-- 创建成绩表
CREATE TABLE IF NOT EXISTS scores (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '记录ID',
    student_id VARCHAR(20) NOT NULL COMMENT '学号',
    course_name VARCHAR(100) NOT NULL COMMENT '课程名称',
    score DECIMAL(5,2) COMMENT '分数',
    credit INT DEFAULT 0 COMMENT '学分',
    semester VARCHAR(20) COMMENT '学期',
    exam_date DATE COMMENT '考试日期',
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
    INDEX idx_student (student_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='成绩表';

-- 插入示例数据
INSERT INTO students (student_id, name, gender, age, major, phone) VALUES
('2024001', '张三', '男', 20, '计算机科学', '13800138001'),
('2024002', '李四', '女', 19, '软件工程', '13800138002'),
('2024003', '王五', '男', 21, '人工智能', '13800138003'),
('2024004', '赵六', '女', 20, '数据科学', '13800138004'),
('2024005', '钱七', '男', 22, '计算机科学', '13800138005');

-- 插入示例成绩
INSERT INTO scores (student_id, course_name, score, credit, semester, exam_date) VALUES
('2024001', '高等数学', 85.5, 4, '2024-2025-1', '2024-12-20'),
('2024001', 'Python编程', 92.0, 3, '2024-2025-1', '2024-12-25'),
('2024002', '高等数学', 78.0, 4, '2024-2025-1', '2024-12-20'),
('2024003', '数据结构', 88.5, 4, '2024-2025-1', '2024-12-22'),
('2024004', '数据库系统', 91.0, 3, '2024-2025-1', '2024-12-23');

-- 创建视图：学生成绩视图
CREATE OR REPLACE VIEW student_scores_view AS
SELECT 
    s.student_id,
    s.name,
    s.major,
    sc.course_name,
    sc.score,
    sc.credit,
    sc.semester,
    sc.exam_date
FROM students s
LEFT JOIN scores sc ON s.student_id = sc.student_id
ORDER BY s.student_id, sc.semester;

-- 创建存储过程：按专业统计学生人数
DELIMITER //
CREATE PROCEDURE GetStudentCountByMajor()
BEGIN
    SELECT 
        major,
        COUNT(*) as student_count
    FROM students
    WHERE major IS NOT NULL AND major != ''
    GROUP BY major
    ORDER BY student_count DESC;
END //
DELIMITER ;