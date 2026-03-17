#include <fstream>
#include <iostream>
#include <sstream>
#include <vector>
#include <string>
#include "../include/student.h"
#include "../include/file_handler.h"
#include "../include/grade_calculator.h"

std::string DATA_DIR = "src/data";

static std::string students_file() { return DATA_DIR + "/students.txt"; }
static std::string grades_file()   { return DATA_DIR + "/grades.txt"; }
static std::string attendance_file(){ return DATA_DIR + "/attendance.txt"; }

void add_student(Student s) {
    std::ofstream file(students_file(), std::ios::app);
    if (!file) { std::cerr << "ERROR:Cannot open students file\n"; return; }
    file << s.roll << "|" << s.name << "|" << s.className << "|" << s.contact << "\n";
}

void view_students() {
    std::ifstream file(students_file());
    if (!file) { std::cerr << "ERROR:Students file not found\n"; return; }
    std::string line;
    while (getline(file, line))
        if (!line.empty()) std::cout << line << "\n";
}

void search_student(int roll) {
    std::ifstream file(students_file());
    if (!file) { std::cerr << "ERROR:Students file not found\n"; return; }
    std::string line;
    std::string rollStr = std::to_string(roll);
    while (getline(file, line)) {
        // Exact match: first field before '|' must equal rollStr
        std::string firstField = line.substr(0, line.find('|'));
        if (firstField == rollStr) { std::cout << line << "\n"; return; }
    }
    std::cerr << "ERROR:Student not found\n";
}

void update_student(Student s) {
    std::ifstream file(students_file());
    if (!file) { std::cerr << "ERROR:Students file not found\n"; return; }
    std::vector<std::string> lines;
    std::string line;
    bool found = false;
    std::string rollStr = std::to_string(s.roll);
    while (getline(file, line)) {
        std::string firstField = line.substr(0, line.find('|'));
        if (firstField == rollStr) {
            lines.push_back(rollStr + "|" + s.name + "|" + s.className + "|" + s.contact);
            found = true;
        } else {
            lines.push_back(line);
        }
    }
    file.close();
    if (!found) { std::cerr << "ERROR:Student not found\n"; return; }
    std::ofstream out(students_file());
    for (auto& l : lines) out << l << "\n";
    std::cout << "Student Updated\n";
}

void delete_student(int roll) {
    std::ifstream file(students_file());
    if (!file) { std::cerr << "ERROR:Students file not found\n"; return; }
    std::vector<std::string> lines;
    std::string line;
    bool found = false;
    std::string rollStr = std::to_string(roll);
    while (getline(file, line)) {
        std::string firstField = line.substr(0, line.find('|'));
        if (firstField == rollStr) { found = true; continue; }
        if (!line.empty()) lines.push_back(line);
    }
    file.close();
    if (!found) { std::cerr << "ERROR:Student not found\n"; return; }
    std::ofstream out(students_file());
    for (auto& l : lines) out << l << "\n";
    std::cout << "Student Deleted\n";
}

void add_grades(int roll, int math, int english, int science) {
    // Remove existing grade for this roll then append new
    std::ifstream file(grades_file());
    std::vector<std::string> lines;
    std::string line;
    std::string rollStr = std::to_string(roll);
    if (file) {
        while (getline(file, line)) {
            std::string firstField = line.substr(0, line.find('|'));
            if (firstField != rollStr && !line.empty()) lines.push_back(line);
        }
        file.close();
    }
    std::ofstream out(grades_file());
    for (auto& l : lines) out << l << "\n";
    out << roll << "|" << math << "|" << english << "|" << science << "\n";
    std::cout << "Grades Saved\n";
}

void view_grades() {
    std::ifstream file(grades_file());
    if (!file) { std::cerr << "ERROR:Grades file not found\n"; return; }
    std::string line;
    while (getline(file, line))
        if (!line.empty()) std::cout << line << "\n";
}

void view_student_grades(int roll) {
    std::ifstream file(grades_file());
    if (!file) { std::cerr << "ERROR:Grades file not found\n"; return; }
    std::string line;
    std::string rollStr = std::to_string(roll);
    while (getline(file, line)) {
        std::string firstField = line.substr(0, line.find('|'));
        if (firstField == rollStr) { std::cout << line << "\n"; return; }
    }
    std::cerr << "ERROR:Grades not found\n";
}

void mark_attendance(int roll, const std::string& date, const std::string& status) {
    // Remove existing record for same roll+date, then append
    std::ifstream file(attendance_file());
    std::vector<std::string> lines;
    std::string line;
    std::string rollStr = std::to_string(roll);
    if (file) {
        while (getline(file, line)) {
            if (line.empty()) continue;
            std::istringstream ss(line);
            std::string r, d, s;
            getline(ss, r, '|'); getline(ss, d, '|'); getline(ss, s, '|');
            if (r == rollStr && d == date) continue;
            lines.push_back(line);
        }
        file.close();
    }
    std::ofstream out(attendance_file());
    for (auto& l : lines) out << l << "\n";
    out << roll << "|" << date << "|" << status << "\n";
    std::cout << "Attendance Marked\n";
}

void view_attendance() {
    std::ifstream file(attendance_file());
    if (!file) { std::cerr << "ERROR:Attendance file not found\n"; return; }
    std::string line;
    while (getline(file, line))
        if (!line.empty()) std::cout << line << "\n";
}

void attendance_percentage(int roll) {
    std::ifstream file(attendance_file());
    if (!file) { std::cerr << "ERROR:Attendance file not found\n"; return; }
    std::string line;
    std::string rollStr = std::to_string(roll);
    int total = 0, present = 0;
    while (getline(file, line)) {
        if (line.empty()) continue;
        std::istringstream ss(line);
        std::string r, d, s;
        getline(ss, r, '|'); getline(ss, d, '|'); getline(ss, s, '|');
        if (r == rollStr) {
            total++;
            if (s == "Present") present++;
        }
    }
    if (total == 0) { std::cerr << "ERROR:No attendance records\n"; return; }
    float pct = (float)present / total * 100.0f;
    std::cout << rollStr << "|" << present << "|" << total << "|" << pct << "\n";
}

void generate_report(int roll, const std::string& reports_dir) {
    // Fetch student info
    std::ifstream sf(students_file());
    if (!sf) { std::cerr << "ERROR:Students file not found\n"; return; }
    std::string line, rollStr = std::to_string(roll);
    std::string name, cls, contact;
    bool found = false;
    while (getline(sf, line)) {
        std::istringstream ss(line);
        std::string r; getline(ss, r, '|');
        if (r == rollStr) {
            getline(ss, name, '|'); getline(ss, cls, '|'); getline(ss, contact, '|');
            found = true; break;
        }
    }
    if (!found) { std::cerr << "ERROR:Student not found\n"; return; }

    // Fetch grades
    std::ifstream gf(grades_file());
    int math = 0, english = 0, science = 0;
    bool hasGrades = false;
    if (gf) {
        while (getline(gf, line)) {
            std::istringstream ss(line);
            std::string r; getline(ss, r, '|');
            if (r == rollStr) {
                std::string m, e, s;
                getline(ss, m, '|'); getline(ss, e, '|'); getline(ss, s, '|');
                math = std::stoi(m); english = std::stoi(e); science = std::stoi(s);
                hasGrades = true; break;
            }
        }
    }

    float pct = hasGrades ? calculate_percentage(math, english, science) : 0;
    char grade = hasGrades ? calculate_grade(pct) : 'N';

    std::string outPath = reports_dir + "/report_" + rollStr + ".txt";
    std::ofstream out(outPath);
    if (!out) { std::cerr << "ERROR:Cannot write report\n"; return; }

    out << "STUDENT REPORT CARD\n";
    out << "===================\n";
    out << "Name: " << name << "\n";
    out << "Roll: " << roll << "\n";
    out << "Class: " << cls << "\n";
    out << "Contact: " << contact << "\n\n";
    if (hasGrades) {
        out << "Math: " << math << "\n";
        out << "English: " << english << "\n";
        out << "Science: " << science << "\n\n";
        out << "Total: " << (math + english + science) << "/300\n";
        out << "Percentage: " << pct << "%\n";
        out << "Grade: " << grade << "\n";
    } else {
        out << "No grades recorded.\n";
    }
    std::cout << outPath << "\n";
}
