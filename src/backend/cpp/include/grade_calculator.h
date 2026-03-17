#ifndef GRADE_CALCULATOR_H
#define GRADE_CALCULATOR_H

/**
 * @brief Calculate letter grade from percentage
 * @param percent Float percentage value
 * @return Single char grade: A/B/C/D/F
 */
char calculate_grade(float percent);

/**
 * @brief Calculate percentage from three subject marks
 * @param math Math marks (0-100)
 * @param english English marks (0-100)
 * @param science Science marks (0-100)
 * @return Percentage as float
 */
float calculate_percentage(int math, int english, int science);

#endif
