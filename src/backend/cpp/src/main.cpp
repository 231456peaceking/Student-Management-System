#include <iostream>
#include <string>
#include "../include/student.h"
#include "../include/file_handler.h"
#include "../include/grade_calculator.h"

extern std::string DATA_DIR;

int main(int argc, char* argv[]) {
    if (argc < 2) { std::cerr << "ERROR:No command given\n"; return 1; }

    // First arg is always the data directory path
    DATA_DIR = argv[1];
    if (argc < 3) { std::cerr << "ERROR:No command given\n"; return 1; }

    std::string cmd = argv[2];

    if (cmd == "add_student") {
        if (argc < 7) { std::cerr << "ERROR:Missing arguments\n"; return 1; }
        Student s;
        s.roll = std::stoi(argv[3]);
        s.name = argv[4];
        s.className = argv[5];
        s.contact = argv[6];
        add_student(s);
        std::cout << "Student Added\n";

    } else if (cmd == "view_students") {
        view_students();

    } else if (cmd == "search_student") {
        if (argc < 4) { std::cerr << "ERROR:Missing roll\n"; return 1; }
        search_student(std::stoi(argv[3]));

    } else if (cmd == "update_student") {
        if (argc < 7) { std::cerr << "ERROR:Missing arguments\n"; return 1; }
        Student s;
        s.roll = std::stoi(argv[3]);
        s.name = argv[4];
        s.className = argv[5];
        s.contact = argv[6];
        update_student(s);

    } else if (cmd == "delete_student") {
        if (argc < 4) { std::cerr << "ERROR:Missing roll\n"; return 1; }
        delete_student(std::stoi(argv[3]));

    } else if (cmd == "add_grades") {
        if (argc < 7) { std::cerr << "ERROR:Missing arguments\n"; return 1; }
        add_grades(std::stoi(argv[3]), std::stoi(argv[4]), std::stoi(argv[5]), std::stoi(argv[6]));

    } else if (cmd == "view_grades") {
        view_grades();

    } else if (cmd == "view_student_grades") {
        if (argc < 4) { std::cerr << "ERROR:Missing roll\n"; return 1; }
        view_student_grades(std::stoi(argv[3]));

    } else if (cmd == "mark_attendance") {
        if (argc < 6) { std::cerr << "ERROR:Missing arguments\n"; return 1; }
        mark_attendance(std::stoi(argv[3]), argv[4], argv[5]);

    } else if (cmd == "view_attendance") {
        view_attendance();

    } else if (cmd == "attendance_percentage") {
        if (argc < 4) { std::cerr << "ERROR:Missing roll\n"; return 1; }
        attendance_percentage(std::stoi(argv[3]));

    } else if (cmd == "generate_report") {
        if (argc < 5) { std::cerr << "ERROR:Missing arguments\n"; return 1; }
        generate_report(std::stoi(argv[3]), argv[4]);

    } else {
        std::cerr << "ERROR:Unknown command\n"; return 1;
    }

    return 0;
}
