import mysql.connector
from datetime import datetime

# Database creation block
try:
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root"
    )
    cursor = mydb.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS stdmngsys4")
    print("Database created or exists.")
except mysql.connector.Error as e:
    print("Database error:", e)

class DatabaseConnection:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root',
            database='stdmngsys4'
        )
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS students (
                                student_id INT AUTO_INCREMENT PRIMARY KEY,
                                name VARCHAR(255) UNIQUE,
                                age INT,
                                class VARCHAR(50),
                                phone_no BIGINT,
                                password VARCHAR(255))''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS faculty (
                                faculty_id INT AUTO_INCREMENT PRIMARY KEY,
                                name VARCHAR(255),
                                phone_no BIGINT,
                                username VARCHAR(255) UNIQUE,
                                password VARCHAR(255),
                                assigned_class VARCHAR(50))''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS courses (
                                course_id VARCHAR(50) PRIMARY KEY,
                                course_name VARCHAR(255))''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS classes (
                                class_name VARCHAR(50) UNIQUE,
                                student_id INT,
                                student_name VARCHAR(255),
                                attended_classes INT DEFAULT 30,
                                total_classes INT DEFAULT 120,
                                attendance_percentage DECIMAL(5, 2) GENERATED ALWAYS AS (
                                    (attended_classes / total_classes) * 100
                                ) STORED,
                                PRIMARY KEY (class_name, student_id),
                                FOREIGN KEY (student_id) REFERENCES students(student_id))''')
        
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS activities (
                                class_name VARCHAR(50),
                                activity_name VARCHAR(255),
                                given_date DATE,
                                submission_date DATE,
                                total_marks INT,
                                FOREIGN KEY (class_name) REFERENCES classes(class_name))''')
        
    def execute_query(self, query, params=None):
        try:
            self.cursor.execute(query, params)
            self.conn.commit()
        except mysql.connector.Error as e:
            print("MySQL Error:", e)

    def fetch_all(self, query, params=None):
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def close(self):
        self.cursor.close()
        self.conn.close()

# Admin functionalities
def add_student(db):
    name = input("Enter Name: ")
    age = int(input("Enter Age: "))
    student_class = input("Enter Class (e.g., 12A): ")
    phone = int(input("Enter the Phone No: "))
    password = input("Enter Password: ")
    student_query = "INSERT INTO students (name, age, class, phone_no, password) VALUES (%s, %s, %s, %s, %s)"
    db.execute_query(student_query, (name, age, student_class, phone, password))
    
    db.cursor.execute("SELECT student_id FROM students WHERE name=%s AND class=%s", (name, student_class))
    student_id = db.cursor.fetchone()[0]
    class_query = "INSERT INTO classes (class_name, student_id, student_name, attended_classes, total_classes) VALUES (%s, %s, %s, %s, %s)"
    db.execute_query(class_query, (student_class, student_id, name, 30, 120))
    print("Student and class information added.")

def view_students(db):
    query = "SELECT * FROM students"
    students = db.fetch_all(query)
    if not students:
        print("No students found.")
    else:
        print("\nStudents List:")
        for student in students:
            print(student)

def update_student(db):
    student_id = int(input("Enter Student ID to update: "))
    name = input("Enter new Name: ")
    age = int(input("Enter new Age: "))
    student_class = input("Enter new Class: ")
    phone = int(input("Enter new Phone No: "))
    password = input("Enter new Password: ")
    student_query = "UPDATE students SET name=%s, age=%s, class=%s, phone_no=%s, password=%s WHERE student_id=%s"
    db.execute_query(student_query, (name, age, student_class, phone, password, student_id))

    class_query = "UPDATE classes SET class_name=%s, student_name=%s WHERE student_id=%s"
    db.execute_query(class_query, (student_class, name, student_id))
    print("Student updated.")

def delete_student(db):
    student_id = int(input("Enter Student ID to delete: "))
    student_query = "DELETE FROM students WHERE student_id=%s"
    db.execute_query(student_query, (student_id,))
    
    class_query = "DELETE FROM classes WHERE student_id=%s"
    db.execute_query(class_query, (student_id,))
    print("Student deleted.")

def add_faculty(db):
    name = input("Enter Faculty Name: ")
    phone = int(input("Enter Faculty Phone No: "))
    username = input("Enter Username for Faculty: ")
    password = input("Enter Password for Faculty: ")
    assigned_class = input("Enter Assigned Class: ")
    query = "INSERT INTO faculty (name, phone_no, username, password, assigned_class) VALUES (%s, %s, %s, %s, %s)"
    db.execute_query(query, (name, phone, username, password, assigned_class))
    print("Faculty added.")

def view_faculties(db):
    query = "SELECT * FROM faculty"
    faculties = db.fetch_all(query)
    if not faculties:
        print("No faculties found.")
    else:
        print("\nFaculty List:")
        for faculty in faculties:
            print(faculty)

def update_faculty(db):
    faculty_id = int(input("Enter Faculty ID to update: "))
    name = input("Enter new Name: ")
    phone = int(input("Enter new Phone No: "))
    username = input("Enter new Username: ")
    password = input("Enter new Password: ")
    assigned_class = input("Enter new Assigned Class: ")
    query = "UPDATE faculty SET name=%s, phone_no=%s, username=%s, password=%s, assigned_class=%s WHERE faculty_id=%s"
    db.execute_query(query, (name, phone, username, password, assigned_class, faculty_id))
    print("Faculty updated.")

def delete_faculty(db):
    faculty_id = int(input("Enter Faculty ID to delete: "))
    query = "DELETE FROM faculty WHERE faculty_id=%s"
    db.execute_query(query, (faculty_id,))
    print("Faculty deleted.")

def add_course(db):
    course_id = input("Enter Course ID: ")
    course_name = input("Enter Course Name: ")
    query = "INSERT INTO courses (course_id, course_name) VALUES (%s, %s)"
    db.execute_query(query, (course_id, course_name))
    print("Course added.")

def view_courses(db):
    query = "SELECT * FROM courses"
    courses = db.fetch_all(query)
    if not courses:
        print("No courses found.")
    else:
        print("\nCourses List:")
        for course in courses:
            print(course)

def update_course(db):
    course_id = input("Enter Course ID to update: ")
    course_name = input("Enter new Course Name: ")
    query = "UPDATE courses SET course_name=%s WHERE course_id=%s"
    db.execute_query(query, (course_name, course_id))
    print("Course updated.")

def delete_course(db):
    course_id = input("Enter Course ID to delete: ")
    query = "DELETE FROM courses WHERE course_id=%s"
    db.execute_query(query, (course_id,))
    print("Course deleted.")

# Faculty functionalities
def view_class_profile(db, assigned_class):
    query = "SELECT s.student_id, s.name, s.age, s.phone_no FROM students s JOIN classes c ON s.student_id = c.student_id WHERE c.class_name = %s"
    students = db.fetch_all(query, (assigned_class,))
    if not students:
        print("No students found in your class.")
    else:
        print("\nStudents in Your Class:")
        for student in students:
            print(student)

def mark_attendance(db, assigned_class):
    student_id = int(input("Enter Student ID: "))
    attendance_status = int(input("Enter attendance status (1 for Present, 0 for Absent): "))
    if attendance_status == 1:
        query = "UPDATE classes SET attended_classes = attended_classes + 1 WHERE student_id=%s AND class_name=%s"
        db.execute_query(query, (student_id, assigned_class))
        print("Attendance marked as present.")
    else:
        print("Attendance marked as absent (no change in attendance count).")

def assign_activity(db, assigned_class):
    activity_name = input("Enter Activity Name: ")
    try:
        given_date_str = input("Enter the Given Date (DD-MM-YYYY): ")
        given_date = datetime.strptime(given_date_str, "%d-%m-%Y").date()
        submission_date_str = input("Enter Submission Date (DD-MM-YYYY): ")
        submission_date = datetime.strptime(submission_date_str, "%d-%m-%Y").date()
    except ValueError:
        print("Incorrect date format. Use DD-MM-YYYY.")
        return
    total_marks = int(input("Enter Total Marks: "))
    query = "INSERT INTO activities (class_name, activity_name, given_date, submission_date, total_marks) VALUES (%s, %s, %s, %s, %s)"
    db.execute_query(query, (assigned_class, activity_name, given_date, submission_date, total_marks))
    print("Activity assigned to class.")


# Student functionalities
def view_attendance(db, student_id):
    query = "SELECT attendance_percentage FROM classes WHERE student_id=%s"
    result = db.fetch_all(query, (student_id,))
    if result:
        attendance_percentage = result[0][0]
        print(f"Attendance Percentage: {attendance_percentage:.2f}%")
    else:
        print("No attendance record found for this student.")

def view_activities(db, student_id):
    query = "SELECT class FROM students WHERE student_id=%s"
    result = db.fetch_all(query, (student_id,))
    if result:
        student_class = result[0][0]
        query_activities = "SELECT activity_name, given_date, submission_date, total_marks FROM activities WHERE class_name=%s"
        activities = db.fetch_all(query_activities, (student_class,))
        if activities:
            print(f"\nActivities for Class {student_class}:")
            for activity in activities:
                print(f"Activity: {activity[0]}, Given Date: {activity[1]}, Submission Date: {activity[2]}, Total Marks: {activity[3]}")
        else:
            print(f"No activities found for Class {student_class}.")
    else:
        print("Student record not found.")


# Main function to run the system
def main():
    db = DatabaseConnection()
    while True:
        print("\nWelcome to the Student Management System")
        print("1. Admin Login")
        print("2. Faculty Login")
        print("3. Student Login")
        print("4. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            admin_password = input("Enter Admin Password: ")
            if admin_password == 'admin123':
                while True:
                    print("\nAdmin Menu")
                    print("1. Add Student")
                    print("2. View Students")
                    print("3. Update Student")
                    print("4. Delete Student")
                    print("5. Add Faculty")
                    print("6. View Faculties")
                    print("7. Update Faculty")
                    print("8. Delete Faculty")
                    print("9. Add Course")
                    print("10. View Courses")
                    print("11. Update Course")
                    print("12. Delete Course")
                    print("13. Logout")
                    admin_choice = input("Choose an option: ")

                    if admin_choice == '1':
                        add_student(db)
                    elif admin_choice == '2':
                        view_students(db)
                    elif admin_choice == '3':
                        update_student(db)
                    elif admin_choice == '4':
                        delete_student(db)
                    elif admin_choice == '5':
                        add_faculty(db)
                    elif admin_choice == '6':
                        view_faculties(db)
                    elif admin_choice == '7':
                        update_faculty(db)
                    elif admin_choice == '8':
                        delete_faculty(db)
                    elif admin_choice == '9':
                        add_course(db)
                    elif admin_choice == '10':
                        view_courses(db)
                    elif admin_choice == '11':
                        update_course(db)
                    elif admin_choice == '12':
                        delete_course(db)
                    elif admin_choice == '13':
                        break
                    else:
                        print("Invalid option. Please try again.")
            else:
                print("Invalid admin password.")

        elif choice == '2':
            username = input("Enter Faculty Username: ")
            password = input("Enter Faculty Password: ")
            faculty = db.fetch_all("SELECT * FROM faculty WHERE username=%s AND password=%s", (username, password))
            if faculty:
                assigned_class = faculty[0][5]
                print(f"\nWelcome, {faculty[0][1]}")
                while True:
                    print("\nFaculty Menu")
                    print("1. View Class Profile")
                    print("2. Update Student Profile")
                    print("3. View Courses")
                    print("4. Mark Attendance")
                    print("5. Assign Activity to class")
                    print("6. Logout")
                    choice = input("Choose an option: ")
                    if choice == '1':
                        view_class_profile(db, assigned_class)
                    elif choice == '2':
                        update_student(db)
                    elif choice == '3':
                        view_courses(db)
                    elif choice == '4':
                        mark_attendance(db, faculty[0][4])
                    elif choice == '5':
                        assign_activity(db, assigned_class)
                    elif choice == '6':
                        break
                    else:
                        print("Invalid option. Try again.")
            else:
                print("Invalid login details.")

        elif choice == '3':
            student_id = int(input("Enter Student ID: "))
            password = input("Enter Password: ")
            student = db.fetch_all("SELECT * FROM students WHERE student_id=%s AND password=%s", (student_id, password))
            if student:
                print(f"\nWelcome, {student[0][1]}")
                while True:
                    print("\nStudent Menu")
                    print("1. View Attendance")
                    print("2. View Available Courses")
                    print("3. View Activities")
                    print("4. Logout")
                    choice = input("Choose an option: ")
                    if choice == '1':
                        view_attendance(db, student_id)
                    elif choice == '2':
                        view_courses(db)
                    elif choice == '3':
                        view_activities(db, student_id)
                    elif choice == '4':
                        break
                    else:
                        print("Invalid option. Try again.")
            else:
                print("Invalid Student ID.")

        elif choice == '4':
            db.close()
            print("Exiting the system. Goodbye!")
            break

        else:
            print("Invalid option. Please try again.")

# Run the main function
if __name__ == "__main__":
    main()
