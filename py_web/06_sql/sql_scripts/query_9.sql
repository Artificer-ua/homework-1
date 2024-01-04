SELECT subjects.subjects, students.fullname
from grades
LEFT JOIN students ON students.id = grades.student_id
LEFT JOIN subjects ON subjects.id = grades.subject_id
LEFT JOIN classes ON classes.id = students.class_id
WHERE students.id = 8
GROUP BY students.fullname, subjects.subjects
ORDER BY subjects.subjects ASC;