SELECT t.fullname, d.name, ROUND(AVG(g.grade), 0) as av
FROM grades g 
JOIN disciplines d ON d.id = g.discipline_id 
JOIN teachers t ON t.id = d.teacher_id 
WHERE t.id = 1
GROUP BY d.name; 