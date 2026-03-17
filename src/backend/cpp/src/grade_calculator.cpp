#include "../include/grade_calculator.h"

/**
 * @brief Map percentage to letter grade
 * @param percent Percentage value (0-100)
 * @return Letter grade character
 */
char calculate_grade(float percent) {
    if (percent >= 90) return 'A';
    if (percent >= 80) return 'B';
    if (percent >= 70) return 'C';
    if (percent >= 60) return 'D';
    return 'F';
}

/**
 * @brief Calculate percentage from three subject marks out of 300 total
 * @param math Math marks
 * @param english English marks
 * @param science Science marks
 * @return Percentage as float
 */
float calculate_percentage(int math, int english, int science) {
    float total = math + english + science;
    return (total / 300.0f) * 100.0f;
}
