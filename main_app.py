import streamlit as st
import sqlite3
import pandas as pd

# Database Connection
conn = sqlite3.connect("students.db", check_same_thread=False)
c = conn.cursor()

# Create Table
c.execute("""
CREATE TABLE IF NOT EXISTS students(
    RollNo TEXT PRIMARY KEY,
    Name TEXT,
    Course TEXT,
    Marks INTEGER
)
""")
conn.commit()

# Title
st.title("🎓 Student Record Management System")

# Menu
menu = ["Add Student", "View Students", "Search Student", "Delete Student"]
choice = st.sidebar.selectbox("Menu", menu)

# Add Student
if choice == "Add Student":
    st.subheader("Add Student")

    roll = st.text_input("Roll Number")
    name = st.text_input("Student Name")
    course = st.text_input("Course")
    marks = st.number_input("Marks", 0, 100)

    if st.button("Add"):
        try:
            c.execute(
                "INSERT INTO students VALUES (?,?,?,?)",
                (roll, name, course, marks)
            )
            conn.commit()
            st.success("Student Added Successfully")
        except:
            st.error("Roll Number Already Exists")

# View Students
elif choice == "View Students":
    st.subheader("Student Records")

    c.execute("SELECT * FROM students")
    data = c.fetchall()

    df = pd.DataFrame(
        data,
        columns=["Roll No", "Name", "Course", "Marks"]
    )

    st.dataframe(df)

# Search Student
elif choice == "Search Student":
    st.subheader("Search Student")

    roll = st.text_input("Enter Roll Number")

    if st.button("Search"):
        c.execute(
            "SELECT * FROM students WHERE RollNo=?",
            (roll,)
        )

        student = c.fetchone()

        if student:
            st.write("Roll No :", student[0])
            st.write("Name :", student[1])
            st.write("Course :", student[2])
            st.write("Marks :", student[3])
        else:
            st.error("Student Not Found")

# Delete Student
elif choice == "Delete Student":
    st.subheader("Delete Student")

    roll = st.text_input("Enter Roll Number")

    if st.button("Delete"):
        c.execute(
            "DELETE FROM students WHERE RollNo=?",
            (roll,)
        )
        conn.commit()
        st.success("Student Deleted Successfully")
