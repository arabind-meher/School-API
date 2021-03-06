from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager, jwt_required, create_access_token

from sqlalchemy import Column, Integer, String, Float, Date

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
    pass


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
    s_passed = Column(String(25))
    s_name = Column(String(50))
    dob = Column(Date)
    s_phone = Column(Integer, unique=True)
    s_email = Column(String(25), unique=True)


class Class(db.Model):
    __tablename__ = 'class'
    s_id = Column(Integer, primary_key=True, autoincrement=False)
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
    t_passed = Column(String(25))
    t_name = Column(String(50))
    t_phone = Column(Integer, unique=True)
    t_email = Column(String(25), unique=True)


class Admin(db.Model):
    __tablename__ = 'admin'
    a_id = Column(Integer, primary_key=True, autoincrement=False)
    a_passwd = Column(String(25))


class StudentSchema(ma.Schema):
    class Meta:
        fields = ('s_id', 's_passwd', 's_name', 'dob', 's_phone', 's_email')


class ClassSchema(ma.Schema):
    class Meta:
        fields = ('s_id', 'subject_1', 'subject_2', 'subject_3', 'subject_4', 'subject_5', 'total', 'percent', 'grade')


class TeacherSchema(ma.Schema):
    class Meta:
        fields = ('t_id', 't_passwd', 't_name', 't_phone', 't_email')


class AdminSchema(ma.Schema):
    class Meta:
        fields = ('a_id', 'a_passwd')


student_schema = StudentSchema()
students_schema = StudentSchema(many=True)

class_schema = ClassSchema()
classes_schema = ClassSchema(many=True)

teacher_schema = TeacherSchema()
teachers_schema = TeacherSchema(many=True)

admin_schema = AdminSchema()
admins_schema = AdminSchema(many=True)

if __name__ == '__main__':
    app.run(debug=True)
