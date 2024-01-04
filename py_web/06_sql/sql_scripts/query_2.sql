SELECT students.fullname, subjects.subjects, ROUND(AVG(grades.grade), 2) AS avg_grade
FROM grades
LEFT JOIN students ON students.id = grades.student_id
LEFT JOIN subjects ON subjects.id = grades.subject_id
WHERE subjects.id  = 4
GROUP BY students.fullname, subjects.subjects
ORDER BY avg_grade DESC
LIMIT 1;