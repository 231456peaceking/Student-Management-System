#include <iostream>

char calculate_grade(float percent){

    if(percent>=90) return 'A';
    if(percent>=80) return 'B';
    if(percent>=70) return 'C';
    if(percent>=60) return 'D';
    return 'F';
}

float calculate_percentage(int m,int e,int s){

    float total=m+e+s;
    return (total/300)*100;
}