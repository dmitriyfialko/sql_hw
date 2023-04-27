SELECT gr.name, s.fullname, g.grade 
FROM grades g 
JOIN students s ON s.id = g.student_id 
JOIN groups gr ON gr.id = s.group_id 
JOIN disciplines d ON d.id = g.discipline_id 
WHERE gr.id = 2 AND d.id = 3
ORDER BY s.fullname;