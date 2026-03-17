#include <iostream>
#include <sstream>
#include <vector>
#include "student.h"

void add_student(Student s);
void view_students();
void search_student(int roll);

// Helper to join arguments (for names with spaces)
std::string join_args(char* argv[], int start, int end) {
    std::string result = "";
    for(int i = start; i <= end; i++) {
        result += argv[i];
        if(i != end) result += " ";
    }
    return result;
}

int main(int argc, char* argv[]) {

    if(argc < 2){
        std::cout << "No command provided\n";
        return 1;
    }

    std::string command = argv[1];

    if(command == "add_student") {

        if(argc < 6){
            std::cout << "Usage: add_student <roll> <name> <class> <contact>\n";
            return 1;
        }

        Student s;

        s.roll = std::stoi(argv[2]);

        // ✅ FIX: handle names with spaces
        // name = everything between roll and class
        s.name = join_args(argv, 3, argc - 3);

        s.className = argv[argc - 2];
        s.contact = argv[argc - 1];

        add_student(s);
        std::cout << "Student Added\n";
    }

    else if(command == "view_students") {
        view_students();
    }

    else if(command == "search_student") {

        if(argc < 3){
            std::cout << "Usage: search_student <roll>\n";
            return 1;
        }

        int roll = std::stoi(argv[2]);
        search_student(roll);
    }

    else {
        std::cout << "Unknown command\n";
    }

    return 0;
}
