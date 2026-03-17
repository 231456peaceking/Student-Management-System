#include <fstream>
#include <iostream>
#include <sstream>
#include "student.h"
void add_student(Student s){
    std::ofstream file("data/students.txt", std::ios::app);

    if(!file){
        std::cerr << "Error opening file\n";
        return;
    }

    file << s.roll << "|" << s.name << "|" << s.className << "|" << s.contact << std::endl;
}
void view_students(){
    std::ifstream file("data/students.txt");
    std::string line;

    while(getline(file,line)){
        std::cout<<line<<std::endl;
    }
}

void search_student(int roll){
    std::ifstream file("data/students.txt");
    std::string line;

    while(getline(file,line)){
        if(line.find(std::to_string(roll))==0){
            std::cout<<line<<std::endl;
            return;
        }
    }

    std::cout<<"Student not found\n";
}
