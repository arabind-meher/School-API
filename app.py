from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager, jwt_required, create_access_token

from sqlalchemy import Column, Integer, String, Float, Date
from datetime import datetime

import yaml


package = yaml.load(open('package.yaml'), Loader=yaml.FullLoader)


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql://{package['username']}:{package['passwd']}@localhost/school"

db = SQLAlchemy(app)
ma = Marshmallow(app)
jwt = JWTManager(app)


@app.cli.command('create_db')
def create_db():
    db.create_all()
    print('Database Created!')


@app.cli.command('seed_db')
def seed_db():
    student_1 = Student(
        s_id=10001,
        s_passwd='student1',
        s_name='Student 1',
        dob=datetime(2000, 5, 17).strftime('%Y-%m-%d'),
        s_email='student_1@gmail.com',
        subject_1=80,
        subject_2=86,
        subject_3=71,
        subject_4=92,
        subject_5=88,
        total=417,
        percent=83.4,
        grade='A'
    )

    student_2 = Student(
        s_id=10002,
        s_passwd='student2',
        s_name='Student 2',
        dob=datetime(2000, 2, 6).strftime('%Y-%m-%d'),
        s_email='student_2@gmail.com',
        subject_1=69,
        subject_2=63,
        subject_3=77,
        subject_4=52,
        subject_5=80,
        total=341,
        percent=68.2,
        grade='B'
    )

    teacher_1 = Teacher(
        t_id=1001,
        t_passwd='teacher1',
        t_name='Teacher 1',
        t_email='teacher_1@gmail.com'
    )

    admin_1 = Admin(
        a_id=101,
        a_passwd='admin1'
    )

    db.session.add(student_1)
    db.session.add(student_2)
    db.session.add(teacher_1)
    db.session.add(admin_1)

    db.session.commit()

    print('Database Seeded!')


@app.cli.command('drop_db')
def drop_db():
    db.drop_all()
    print('Database Dropped!')


@app.route('/admin/<int:a_id>', methods=['GET'])
def admin(a_id: int):
    a = Admin.query.filter_by(a_id=a_id).first()
    r = admin_schema.dump(a)
    return jsonify(r), 200


@app.route('/admin_list', methods=['GET'])
def admin_list():
    a = Admin.query.all()
    print(a)
    r = admins_schema.dump(a)
    return jsonify(r), 200


class Student(db.Model):
    __tablename__ = 'student'
    s_id = Column(Integer, primary_key=True, autoincrement=False)
    s_passwd = Column(String(25))
    s_name = Column(String(50))
    dob = Column(Date)
    s_email = Column(String(25))
    subject_1 = Column(Float)
    subject_2 = Column(Float)
    subject_3 = Column(Float)
    subject_4 = Column(Float)
    subject_5 = Column(Float)
    total = Column(Float)
    percent = Column(Float)
    grade = Column(String(3))


class Teacher(db.Model):
    __tablename__ = 'teacher'
    t_id = Column(Integer, primary_key=True, autoincrement=False)
    t_passwd = Column(String(25))
    t_name = Column(String(50))
    t_email = Column(String(25))


class Admin(db.Model):
    __tablename__ = 'admin'
    a_id = Column(Integer, primary_key=True, autoincrement=False)
    a_passwd = Column(String(25))


class StudentSchema(ma.Schema):
    class Meta:
        fields = (
            's_id', 's_passwd', 's_name', 'dob', 's_email',
            'subject_1', 'subject_2', 'subject_3', 'subject_4', 'subject_5',
            'total', 'percent', 'grade'
        )


class TeacherSchema(ma.Schema):
    class Meta:
        fields = ('t_id', 't_passwd', 't_name', 't_email')


class AdminSchema(ma.Schema):
    class Meta:
        fields = ('a_id', 'a_passwd')


student_schema = StudentSchema()
students_schema = StudentSchema(many=True)

teacher_schema = TeacherSchema()
teachers_schema = TeacherSchema(many=True)

admin_schema = AdminSchema()
admins_schema = AdminSchema(many=True)

if __name__ == '__main__':
    app.run(debug=True)
