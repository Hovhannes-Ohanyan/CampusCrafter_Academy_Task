# CampusCrafter_Academy_Task
CampusCrafter is a cutting-edge, web-based platform designed to streamline and enhance the educational experience for students, educators, and administrators alike. At its core, CampusCrafter serves as an all-encompassing solution for managing academic processes, offering a suite of tools tailored to the unique needs of the educational sector.

#Installation

Clone the repository:

cd your-project


Create and activate a virtual environment (optional but recommended):

      virtualenv venv
      source venv/bin/activate 


Install dependencies:

      pip install -r requirements.txt


Initialize the database:

      python init_db.py
      
Run the application:
      python run.py



API Endpoints


Authentication


Register
URL: /register
Method: POST

Request:
    {
      "name": "your_name",
      "email": "your_email@example.com",
      "password": "your_password",
      "role": "student"   
    }
Response:
    {
      "message": "Account created successfully"
    }



Login

URL: /login
Method: POST

Request:
    {
      "email": "your_email@example.com",
      "password": "your_password"
    }

Response:
    {
      "access_token": "your_access_token"
    }


Courses

Create Course
URL: /api/courses
Method: POST
Authentication: JWT required with teacher or admin role.

Request:
    {
      "title": "Course Title",
      "description": "Course Description",
      "start_date": "YYYY-MM-DD",
      "credits": 3,
      "enrollment_limit": 50,
      "status": "active"   
    }
    
Response:
    {
      "message": "Course created successfully",
      "course_id": 1
    }


Get All Courses
Endpoint: /api/courses

Method: GET

Description: Retrieve a list of all courses.

Response:
    {
      "id": 1,
      "title": "Course Title",
      "description": "Course Description",
      "teacher_id": 2,
      "start_date": "2023-01-01T00:00:00",
      "credits": 3,
      "enrollment_limit": 30,
      "status": "active"
    }


Get Single Course
Endpoint: /api/courses/{courseId}

Method: GET

Description: Retrieve details for a specific course.

Response:
    {
      "id": 1,
      "title": "Course Title",
      "description": "Course Description",
      "teacher_id": 2,
      "start_date": "2023-01-01T00:00:00",
      "credits": 3,
      "enrollment_limit": 30,
      "status": "active"
    }


Update Course
Endpoint: /api/courses/{courseId}

Method: PUT

Description: Update details for a specific course.

Request:
      {
        "title": "Updated Course Title",
        "description": "Updated Course Description"
      }
      
Reponse:
      {
        "message": "Course updated successfully"
      }


Delete Course
Endpoint: /api/courses/{courseId}

Method: DELETE

Description: Delete a specific course.

Response:

      {
        "message": "Course deleted successfully"
      }


Assignments
Get Assignments for a Course
Endpoint: /api/courses/{courseId}/assignments

Method: GET

Description: Retrieve a list of assignments for a specific course.

Response:

      {
        "id": 1,
        "title": "Assignment Title",
        "content": "Assignment Content",
        "due_date": "2023-01-15T23:59:59",
        "posted_date": "2023-01-01T12:00:00",
        "max_score": 100,
        "submission_format": "PDF"
      }


Create Assignment
Endpoint: /api/courses/{courseId}/assignments

Method: POST

Description: Create a new assignment for a specific course.

Request:

      {
        "title": "Assignment Title",
        "content": "Assignment Content",
        "due_date": "2023-01-15T23:59:59",
        "max_score": 100,
        "submission_format": "PDF"
      }
Resoponse:
      {
        "message": "Assignment created successfully"
      }


Update Assignment
Endpoint: /api/assignments/{assignmentId}

Method: PUT

Description: Update details for a specific assignment.

Request:

      {
        "title": "Updated Assignment Title",
        "content": "Updated Assignment Content"
      }
Response:
      {
        "message": "Assignment updated successfully"
      }



Delete Assignment
Endpoint: /api/assignments/{assignmentId}

Method: DELETE

Description: Delete a specific assignment.

Response:
      {
        "message": "Assignment deleted successfully"
      }



Grades
Submit Grade
Endpoint: /api/assignments/{assignmentId}/grades

Method: POST

Description: Submit a grade for a specific assignment.

Request:

      {
        "student_id": 3,
        "score": 90
      }

Response:
      {
        "message": "Grade submitted successfully"
      }



Get Grades for Student
Endpoint: /api/students/{studentId}/grades

Method: GET

Description: Retrieve a list of grades for a specific student.

Response:
      {
        "id": 1,
        "assignment_id": 1,
        "score": 90
      }


User Profile
Get User Profile
Endpoint: /api/users/{userId}

Method: GET

Description: Retrieve user profile details.

Response:
      {
        "id": 1,
        "name": "John Doe",
        "email": "john.doe@example.com",
        "role": "student"
      }


Update User Profile
Endpoint: /api/users/{userId}

Method: PUT

Description: Update user profile details.

Request:
      {
        "name": "Updated Name",
        "email": "updated.email@example.com"
      }
Reesponse:
      {
        "message": "User profile updated successfully"
      }


Create User
Endpoint: /api/users

Method: POST

Description: Create a new user account.

Request:
      {
        "name": "New User",
        "email": "new.user@example.com",
        "password": "password123",
        "role": "student"
      }
Response:

      {
        "message": "User created successfully",
        "user_id": 2
      }


Delete User
Endpoint: /api/users/{userId}

Method: DELETE

Description: Delete a specific user.

Response:
      {
        "message": "User deleted successfully"
      }

