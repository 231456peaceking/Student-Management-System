#include <iostream>
#include "student.h"

void add_student(Student s);
void view_students();
void search_student(int roll);

int main(int argc,char* argv[]){

    std::string command=argv[1];

    if(command=="add_student"){

        Student s;
        s.roll=std::stoi(argv[2]);
        s.name=argv[3];
        s.className=argv[4];
        s.contact=argv[5];

        add_student(s);
        std::cout<<"Student Added\n";
    }

    else if(command=="view_students"){
        view_students();
    }

    else if(command=="search_student"){
        int roll=std::stoi(argv[2]);
        search_student(roll);
    }

    return 0;
}