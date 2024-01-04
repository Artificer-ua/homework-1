SELECT students.fullname, ROUND(AVG(grades.grade), 2) AS avg_grade
FROM grades
LEFT JOIN students ON students.id = grades.student_id
GROUP BY students.fullname
ORDER BY avg_grade DESC
LIMIT 5;