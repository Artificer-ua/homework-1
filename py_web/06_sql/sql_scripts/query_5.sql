SELECT teachers.fullname, subjects.subjects
FROM subjects
LEFT JOIN teachers ON teachers.id = subjects.teacher_id
GROUP BY teachers.fullname, subjects.subjects
ORDER BY teachers.fullname ASC;