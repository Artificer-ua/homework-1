SELECT teachers.fullname, subjects.subjects, students.fullname
FROM grades
LEFT JOIN students ON students.id = grades.student_id
LEFT JOIN subjects ON subjects.id = grades.subject_id
LEFT JOIN classes ON classes.id = students.class_id
LEFT JOIN teachers ON teachers.id = subjects.teacher_id
WHERE students.id = 8 AND teachers.id = 2
GROUP BY students.fullname, subjects.subjects, teachers.fullname
ORDER BY subjects.subjects ASC;