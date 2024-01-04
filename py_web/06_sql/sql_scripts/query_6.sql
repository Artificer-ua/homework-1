SELECT classes.clas, students.fullname
FROM students
LEFT JOIN classes ON classes.id = students.class_id
WHERE classes.id  = 2
GROUP BY classes.clas, students.fullname
ORDER BY classes.clas ASC;