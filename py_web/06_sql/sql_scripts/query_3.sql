SELECT subjects.subjects, classes.clas, ROUND(AVG(grades.grade), 2) AS avg_grade
FROM grades
LEFT JOIN students ON students.id = grades.student_id
LEFT JOIN subjects ON subjects.id = grades.subject_id
LEFT JOIN classes ON classes.id = students.class_id
WHERE subjects.id  = 2
GROUP BY subjects.subjects, classes.clas
ORDER BY avg_grade DESC;