SELECT teachers.fullname, subjects.subjects, ROUND(AVG(grades.grade), 2)
FROM grades
LEFT JOIN students ON students.id = grades.student_id
LEFT JOIN subjects ON subjects.id = grades.subject_id
LEFT JOIN classes ON classes.id = students.class_id
LEFT JOIN teachers ON teachers.id = subjects.teacher_id
WHERE subjects.teacher_id = 2
GROUP BY subjects.subjects, teachers.fullname
ORDER BY subjects.subjects ASC;