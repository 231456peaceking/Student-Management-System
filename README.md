# Student Management System

A simple **console-based Student Management System** built using **Python (Frontend UI)** and **C++ (Backend processing)** with **text files for data storage**.

The system allows teachers to manage **student information, grades, and attendance** through a simple menu-driven interface.

---

# Project Overview

This project demonstrates **cross-language integration**, where:

- **Python** handles the **user interface and input validation**
- **C++** performs **data processing and file operations**
- **Text files** store student records

The goal is to create a **lightweight and beginner-friendly system** that demonstrates **basic software architecture and modular programming**.

---

# Technologies Used

- **C++** – Backend logic and file handling  
- **Python 3** – User interface and menu system  
- **Text Files** – Data storage  
- **Ubuntu / Linux Terminal** – Build and run environment  

---

# System Architecture

The application follows a simple **two-layer architecture**.

User → Python UI → C++ Backend → Text Files → Output → Python Display

### Communication Flow

1. User selects an option in the **Python menu**
2. Python validates the input
3. Python calls the **C++ executable using subprocess**
4. C++ performs the requested operation
5. Data is read or written to **text files**
6. Results are returned and displayed to the user

---

# Visual Diagram

```
+------------------+
|   Python UI      |
|   main.py        |
+------------------+
        |
        | subprocess.run()
        v
+------------------+
|   C++ Backend    |
| student_management|
+------------------+
        |
        v
+------------------+
|   Text Files     |
| students.txt     |
| grades.txt       |
| attendance.txt   |
+------------------+
        |
        v
+------------------+
|  Results Shown   |
|  in Python UI    |
+------------------+
```

---

# Project Folder Structure

```
STUDENT_MANAGEMENT_SYSTEM

backend/
    main.cpp
    student.h
    student.cpp
    file_handler.cpp
    grade_calculator.cpp

frontend/
    main.py
    ui_menu.py
    backend_connector.py
    display_formatter.py

data/
    students.txt
    grades.txt
    attendance.txt

backup/

tests/
    test_student.cpp
    test_ui.py

scripts/
    backup_data.py

README.md
.gitignore
```

---

# Data Storage Format

### students.txt

```
RollNumber|Name|Class|Contact
```

Example:

```
101|Spongebob Squarepants|10A|0712345678
```

---

### grades.txt

```
RollNumber|Math|English|Science
```

Example:

```
101|85|90|88
```

---

### attendance.txt

```
RollNumber|Date|Status
```

Example:

```
101|2026-03-06|Present
```

---

# Features

### Student Management

- Add Student
- View Students
- Search Student
- Update Student
- Delete Student

Student fields:

- Roll Number
- Name
- Class
- Contact Number

---

### Academic Management

Subjects:

- Math
- English
- Science

The system can:

- Store student marks
- Calculate **total marks**
- Calculate **percentage**
- Determine **grade**

Grade system:

| Percentage | Grade |
|------------|------|
| 90 – 100 | A |
| 80 – 89 | B |
| 70 – 79 | C |
| 60 – 69 | D |
| Below 60 | F |

---

### Attendance Management

Functions include:

- Mark attendance
- View attendance
- Calculate attendance percentage

Formula:

```
Attendance % = (Present / Total Classes) × 100
```

---

# Login Credentials

Teacher login is required to access the system.

```
Username: admin
Password: 1234
```

---

# Ubuntu Build and Run Commands

### Navigate to project folder

```bash
cd STUDENT_MANAGEMENT_SYSTEM
```

### Compile C++ Backend

```bash
g++ backend/main.cpp backend/student.cpp backend/file_handler.cpp backend/grade_calculator.cpp -o student_management
```

### Make executable (optional)

```bash
chmod +x student_management
```

### Run Python UI

```bash
python3 frontend/main.py
```

---

# Testing Before Submission

## Test 1: Add Student

Input:

```
Name: Spongebob Squarepants
Roll: 101
Class: 10A
```

Expected Result:

```
students.txt updated
```

---

## Test 2: Search Student

Input:

```
Roll: 101
```

Expected Output:

```
101|Spongebob Squarepants|10A|0712345678
```

---

## Test 3: View Students

Expected Output:

```
Roll:101 Name:Spongebob Squarepants Class:10A Contact:0712345678
```

---

## Test 4: Backup Script

Run:

```bash
python3 scripts/backup_data.py
```

Expected Result:

```
backup/students_backup.txt created
```

---

# Example Report Card (Optional Extension)

Example output file:

```
report_101.txt
```

Example content:

```
STUDENT REPORT CARD

Name: Spongebob Squarepants
Roll: 101

Math: 85
English: 90
Science: 88

Total: 263
Percentage: 87.6%
Grade: B
```

---

# Why This Project Is Good for Learning

This project demonstrates:

- C++ backend programming
- Python frontend programming
- File handling with text files
- Cross-language integration
- Basic software architecture
- Modular project structure

The system is designed to be **simple, readable, and beginner-friendly** while still showing **real software development concepts**.

---# Student-Management-System
