#ifndef FILE_HANDLER_H
#define FILE_HANDLER_H

#include <string>
#include "student.h"

// Global data directory path set at startup
extern std::string DATA_DIR;

/**
 * @brief Add a student record to students.txt
 * @param s Student struct with all fields populated
 */
void add_student(Student s);

/**
 * @brief Print all student records to stdout
 */
void view_students();

/**
 * @brief Search for a student by exact roll number
 * @param roll Integer roll number to find
 */
void search_student(int roll);

/**
 * @brief Update an existing student record by roll number
 * @param s Student struct with updated fields (roll used as key)
 */
void update_student(Student s);

/**
 * @brief Delete a student record by roll number
 * @param roll Roll number of student to delete
 */
void delete_student(int roll);

/**
 * @brief Add or update grade record for a student
 * @param roll Roll number
 * @param math Math marks
 * @param english English marks
 * @param science Science marks
 */
void add_grades(int roll, int math, int english, int science);

/**
 * @brief Print all grade records to stdout
 */
void view_grades();

/**
 * @brief Print grades for a specific student
 * @param roll Roll number to look up
 */
void view_student_grades(int roll);

/**
 * @brief Mark attendance for a student on a date
 * @param roll Roll number
 * @param date Date string YYYY-MM-DD
 * @param status "Present" or "Absent"
 */
void mark_attendance(int roll, const std::string& date, const std::string& status);

/**
 * @brief Print all attendance records to stdout
 */
void view_attendance();

/**
 * @brief Calculate and print attendance percentage for a student
 * @param roll Roll number
 */
void attendance_percentage(int roll);

/**
 * @brief Generate a full report card for a student
 * @param roll Roll number
 * @param reports_dir Directory to write report file into
 */
void generate_report(int roll, const std::string& reports_dir);

#endif
