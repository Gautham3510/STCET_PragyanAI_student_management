import streamlit as st
import sqlite3
import pandas as pd

# -----------------------------
# Database
# -----------------------------
conn = sqlite3.connect("students.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    roll TEXT UNIQUE,
    department TEXT,
    semester INTEGER,
    marks REAL
)
""")
conn.commit()


# -----------------------------
# Functions
# -----------------------------

def add_student(name, roll, dept, sem, marks):
    try:
        cursor.execute(
            """
            INSERT INTO students
            (name, roll, department, semester, marks)
            VALUES(?,?,?,?,?)
            """,
            (name, roll, dept, sem, marks),
        )
        conn.commit()
        return True
    except:
        return False


def view_students():
    cursor.execute("SELECT * FROM students")
    return cursor.fetchall()


def delete_student(roll):
    cursor.execute(
        "DELETE FROM students WHERE roll=?",
        (roll,),
    )
    conn.commit()


def update_student(name, dept, sem, marks, roll):
    cursor.execute(
        """
        UPDATE students
        SET name=?,
        department=?,
        semester=?,
        marks=?
        WHERE roll=?
        """,
        (name, dept, sem, marks, roll),
    )
    conn.commit()


def search_student(roll):
    cursor.execute(
        "SELECT * FROM students WHERE roll=?",
        (roll,),
    )
    return cursor.fetchone()


def total_students():
    cursor.execute("SELECT COUNT(*) FROM students")
    return cursor.fetchone()[0]


def average_marks():
    cursor.execute("SELECT AVG(marks) FROM students")
    value = cursor.fetchone()[0]
    if value is None:
        return 0
    return round(value, 2)


# -----------------------------
# UI
# -----------------------------

st.set_page_config(
    page_title="Student Record Management",
    page_icon="🎓",
    layout="wide",
)

st.title("🎓 Student Record Management System")

menu = [
    "Dashboard",
    "Add Student",
    "View Students",
    "Search Student",
    "Update Student",
    "Delete Student",
]

choice = st.sidebar.selectbox("Menu", menu)

# -----------------------------
# Dashboard
# -----------------------------

if choice == "Dashboard":

    c1, c2 = st.columns(2)

    c1.metric("Total Students", total_students())
    c2.metric("Average Marks", average_marks())

    data = pd.DataFrame(
        view_students(),
        columns=[
            "ID",
            "Name",
            "Roll",
            "Department",
            "Semester",
            "Marks",
        ],
    )

    if not data.empty:
        st.subheader("Department Distribution")
        st.bar_chart(data["Department"].value_counts())

        st.subheader("Marks")
        st.line_chart(data["Marks"])

# -----------------------------
# Add Student
# -----------------------------

elif choice == "Add Student":

    st.subheader("Add Student")

    name = st.text_input("Student Name")

    roll = st.text_input("Roll Number")

    dept = st.selectbox(
        "Department",
        [
            "Computer Science",
            "Information Technology",
            "Mechanical",
            "Civil",
            "Electrical",
            "Electronics",
        ],
    )

    sem = st.number_input(
        "Semester",
        1,
        8,
        1,
    )

    marks = st.number_input(
        "Marks",
        0.0,
        100.0,
        50.0,
    )

    if st.button("Add"):

        if add_student(
            name,
            roll,
            dept,
            sem,
            marks,
        ):
            st.success("Student Added Successfully")

        else:
            st.error("Roll Number Already Exists")

# -----------------------------
# View Students
# -----------------------------

elif choice == "View Students":

    st.subheader("Student Records")

    data = pd.DataFrame(
        view_students(),
        columns=[
            "ID",
            "Name",
            "Roll",
            "Department",
            "Semester",
            "Marks",
        ],
    )

    st.dataframe(
        data,
        use_container_width=True,
    )

# -----------------------------
# Search
# -----------------------------

elif choice == "Search Student":

    st.subheader("Search Student")

    roll = st.text_input("Enter Roll Number")

    if st.button("Search"):

        student = search_student(roll)

        if student:

            st.success("Student Found")

            st.write("Name:", student[1])
            st.write("Roll:", student[2])
            st.write("Department:", student[3])
            st.write("Semester:", student[4])
            st.write("Marks:", student[5])

            gpa = round(student[5] / 10, 2)

            st.write("GPA:", gpa)

        else:
            st.error("Student Not Found")

# -----------------------------
# Update
# -----------------------------

elif choice == "Update Student":

    st.subheader("Update Student")

    roll = st.text_input("Enter Roll Number")

    if st.button("Load Student"):

        student = search_student(roll)

        if student:

            st.session_state.student = student

        else:
            st.error("Student Not Found")

    if "student" in st.session_state:

        student = st.session_state.student

        name = st.text_input(
            "Name",
            value=student[1],
        )

        dept = st.text_input(
            "Department",
            value=student[3],
        )

        sem = st.number_input(
            "Semester",
            1,
            8,
            value=int(student[4]),
        )

        marks = st.number_input(
            "Marks",
            0.0,
            100.0,
            value=float(student[5]),
        )

        if st.button("Update"):

            update_student(
                name,
                dept,
                sem,
                marks,
                roll,
            )

            st.success("Updated Successfully")

# -----------------------------
# Delete
# -----------------------------

elif choice == "Delete Student":

    st.subheader("Delete Student")

    roll = st.text_input("Roll Number")

    if st.button("Delete"):

        delete_student(roll)

        st.success("Student Deleted")
