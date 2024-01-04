SELECT students.fullname, classes.clas, grades.grade, subjects.subjects
FROM grades
LEFT JOIN students ON students.id = grades.student_id
LEFT JOIN subjects ON subjects.id = grades.subject_id
LEFT JOIN classes ON classes.id = students.class_id
WHERE classes.id = 1 AND subjects.id = 6
GROUP BY students.fullname, classes.clas, grades.grade, subjects.subjects
ORDER BY classes.clas ASC;