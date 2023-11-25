from datetime import datetime

import bcrypt
from flask import request, jsonify, abort
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

from app import app, db
from app.models import UserProfile, Course, Assignment, Grade


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role', 'student')

    existing_user = UserProfile.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({'message': 'Email address is already registered'}), 400

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    new_user = UserProfile(name=name, email=email, password=hashed_password, role=role)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'Account created successfully'}), 201


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')

    user = UserProfile.query.filter_by(email=email).first()
    if user and bcrypt.checkpw(password.encode('utf-8'), user.password):
        access_token = create_access_token(identity={'id': user.id, 'email': user.email, 'role': user.role})
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({'message': 'Invalid email or password'}), 401


@app.route('/api/courses', methods=['POST'])
@jwt_required()
def create_course():
    current_user = get_jwt_identity()

    if current_user['role'] not in ['teacher', 'admin']:
        abort(403, description="Permission denied")

    data = request.get_json()

    title = data.get('title')
    description = data.get('description')
    start_date = datetime.strptime(data.get('start_date'), '%Y-%m-%d')
    credits = data.get('credits')
    enrollment_limit = data.get('enrollment_limit')
    status = data.get('status', 'active')

    new_course = Course(
        title=title,
        description=description,
        teacher_id=current_user['id'],
        start_date=start_date,
        credits=credits,
        enrollment_limit=enrollment_limit,
        status=status
    )

    db.session.add(new_course)
    db.session.commit()

    return jsonify({'message': 'Course created successfully', 'course_id': new_course.id}), 201


@app.route('/api/courses', methods=['GET'])
@jwt_required()
def get_all_courses():
    courses = Course.query.all()
    courses_data = [
        {
            'id': course.id,
            'title': course.title,
            'description': course.description,
            'teacher_id': course.teacher_id,
            'start_date': course.start_date.isoformat(),
            'credits': course.credits,
            'enrollment_limit': course.enrollment_limit,
            'status': course.status
        }
        for course in courses
    ]
    return jsonify(courses_data), 200


@app.route('/api/courses/<int:course_id>', methods=['GET'])
@jwt_required()
def get_single_course(course_id):
    course = Course.query.get(course_id)
    if not course:
        abort(404, description="Course not found")
    course_data = {
        'id': course.id,
        'title': course.title,
        'description': course.description,
        'teacher_id': course.teacher_id,
        'start_date': course.start_date.isoformat(),
        'credits': course.credits,
        'enrollment_limit': course.enrollment_limit,
        'status': course.status
    }
    return jsonify(course_data), 200


@app.route('/api/courses/<int:course_id>', methods=['PUT'])
@jwt_required()
def update_course(course_id):
    current_user = get_jwt_identity()
    updated_course_data = request.get_json()
    updated_course = Course.query.get(course_id)

    if not updated_course:
        abort(404, description="Course not found")
    if current_user['role'] != 'admin' and updated_course.teacher_id != current_user['id']:
        abort(403, description="Permission denied")

    updated_course.title = updated_course_data.get('title', updated_course.title)
    updated_course.description = updated_course_data.get('description', updated_course.description)

    db.session.commit()

    return jsonify({'message': 'Course updated successfully'}), 200


@app.route('/api/courses/<int:course_id>', methods=['DELETE'])
@jwt_required()
def delete_course(course_id):
    current_user = get_jwt_identity()

    course = Course.query.get(course_id)

    if not course:
        abort(404, description="Course not found")
    if current_user['role'] != 'admin' and course.teacher_id != current_user['id']:
        abort(403, description="Permission denied")

    db.session.delete(course)
    db.session.commit()

    return jsonify({'message': 'Course deleted successfully'}), 200


@app.route('/api/courses/<int:course_id>/assignments', methods=['GET'])
@jwt_required()
def get_assignments_for_course(course_id):
    assignments = Assignment.query.filter_by(course_id=course_id).all()
    assignments_data = [
        {
            'id': assignment.id,
            'title': assignment.title,
            'content': assignment.content,
            'due_date': assignment.due_date.isoformat(),
            'posted_date': assignment.posted_date.isoformat(),
            'max_score': assignment.max_score,
            'submission_format': assignment.submission_format
        }
        for assignment in assignments
    ]
    return jsonify(assignments_data), 200


@app.route('/api/courses/<int:course_id>/assignments', methods=['POST'])
@jwt_required()
def create_assignment(course_id):
    current_user = get_jwt_identity()

    new_assignment_data = request.get_json()
    course = Course.query.get(course_id)

    if not course:
        abort(404, description="Course not found")

    if current_user['role'] != 'admin' and course.teacher_id != current_user['id']:
        abort(403, description="Permission denied")

    new_assignment = Assignment(
        title=new_assignment_data.get('title'),
        content=new_assignment_data.get('content'),
        due_date=datetime.strptime(new_assignment_data['due_date'], "%Y-%m-%dT%H:%M:%S.%fZ"),
        course_id=course_id,
        max_score=new_assignment_data.get('max_score'),
        submission_format=new_assignment_data.get('submission_format')
    )
    db.session.add(new_assignment)
    db.session.commit()

    return jsonify({'message': 'Assignment created successfully'}), 201


@app.route('/api/assignments/<int:assignment_id>', methods=['PUT'])
@jwt_required()
def update_assignment(assignment_id):
    current_user = get_jwt_identity()

    updated_assignment_data = request.get_json()
    updated_assignment = Assignment.query.get(assignment_id)

    if not updated_assignment:
        abort(404, description="Assignment not found")

    course = Course.query.get(updated_assignment.course_id)

    if not course:
        abort(404, description="Course not found")

    if current_user['role'] != 'admin' and course.teacher_id != current_user['id']:
        abort(403, description="Permission denied")

    updated_assignment.title = updated_assignment_data.get('title', updated_assignment.title)
    updated_assignment.content = updated_assignment_data.get('content', updated_assignment.content)
    updated_assignment.due_date = datetime.strptime(updated_assignment_data['due_date'], "%Y-%m-%dT%H:%M:%S.%fZ")
    updated_assignment.max_score = updated_assignment_data.get('max_score', updated_assignment.max_score)
    updated_assignment.submission_format = updated_assignment_data.get('submission_format',
                                                                       updated_assignment.submission_format)

    db.session.commit()

    return jsonify({'message': 'Assignment updated successfully'}), 200


@app.route('/api/assignments/<int:assignment_id>', methods=['DELETE'])
@jwt_required()
def delete_assignment(assignment_id):
    current_user = get_jwt_identity()

    assignment = Assignment.query.get(assignment_id)

    if not assignment:
        abort(404, description="Assignment not found")

    course = Course.query.get(assignment.course_id)

    if not course:
        abort(404, description="Course not found")

    if current_user['role'] != 'admin' and course.teacher_id != current_user['id']:
        abort(403, description="Permission denied")

    db.session.delete(assignment)
    db.session.commit()

    return jsonify({'message': 'Assignment deleted successfully'}), 200


@app.route('/api/assignments/<int:assignment_id>/grades', methods=['POST'])
@jwt_required()
def submit_grade(assignment_id):
    current_user = get_jwt_identity()

    if current_user['role'] not in ['teacher', 'admin']:
        abort(403, description="Permission denied")

    grade_data = request.get_json()


    assignment = Assignment.query.get(assignment_id)

    if not assignment:
        abort(404, description="Assignment not found")

    course = Course.query.get(assignment.course_id)
    if not course or (current_user['role'] != 'admin' and course.teacher_id != current_user['id']):
        abort(403, description="Permission denied")

    new_grade = Grade(
        assignment_id=assignment_id,
        student_id=grade_data.get('student_id'),
        score=grade_data.get('score')
    )

    db.session.add(new_grade)
    db.session.commit()

    return jsonify({'message': 'Grade submitted successfully'}), 201


@app.route('/api/students/<int:student_id>/grades', methods=['GET'])
@jwt_required()
def get_grades_for_student(student_id):
    current_user = get_jwt_identity()

    if current_user['role'] == 'student' and current_user['id'] != student_id:
        abort(403, description="Permission denied")

    grades = Grade.query.filter_by(student_id=student_id).all()

    grades_data = [
        {
            'id': grade.id,
            'assignment_id': grade.assignment_id,
            'score': grade.score,
        }
        for grade in grades
    ]

    return jsonify(grades_data), 200


@app.route('/api/users/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user_profile(user_id):
    current_user = get_jwt_identity()

    if current_user['role'] == 'user' and current_user['id'] != user_id:
        abort(403, description="Permission denied")

    user_profile = UserProfile.query.get(user_id)

    if not user_profile:
        abort(404, description="User not found")

    user_profile_data = {
        'id': user_profile.id,
        'name': user_profile.name,
        'email': user_profile.email,
        'role': user_profile.role,
    }

    return jsonify(user_profile_data), 200


@app.route('/api/users/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user_profile(user_id):
    current_user = get_jwt_identity()

    if current_user['role'] == 'user' and current_user['id'] != user_id:
        abort(403, description="Permission denied")

    user_profile = UserProfile.query.get(user_id)

    if not user_profile:
        abort(404, description="User not found")

    if current_user['role'] == 'user' and current_user['id'] != user_id:
        abort(403, description="Permission denied")

    updated_data = request.get_json()
    user_profile.name = updated_data.get('name', user_profile.name)
    user_profile.email = updated_data.get('email', user_profile.email)

    db.session.commit()

    return jsonify({'message': 'User profile updated successfully'}), 200


@app.route('/api/users', methods=['POST'])
@jwt_required()
def create_user():
    current_user = get_jwt_identity()

    if current_user['role'] != 'admin':
        abort(403, description="Permission denied")

    user_data = request.get_json()

    new_user = UserProfile(
        name=user_data.get('name'),
        email=user_data.get('email'),
        password=user_data.get('password'),
        role=user_data.get('role', 'user')
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User created successfully', 'user_id': new_user.id}), 201


@app.route('/api/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    current_user = get_jwt_identity()

    if current_user['role'] != 'admin':
        abort(403, description="Permission denied")

    user_profile = UserProfile.query.get(user_id)

    if not user_profile:
        abort(404, description="User not found")

    db.session.delete(user_profile)
    db.session.commit()

    return jsonify({'message': 'User deleted successfully'}), 200
