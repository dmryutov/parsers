/**
 * @brief   Useful SQL queries 
 * @file    queries.sql
 * @author  dmryutov (dmryutov@gmail.com)
 * @version 1.0
 * @date    25.04.2015
 */

/* ПОЛУЧЕНИЕ ДЕКЛАРАЦИЙ */
SELECT count(*) FROM declaration_all d
LEFT JOIN authority a ON a.name=d.organization
WHERE
	d.type = 'Антикоррупционная декларация' AND
	(
		d.organization IN ('Государственный Совет Республики Коми', 'Глава республики Коми', 'Избирательная комиссия Республики Коми', 'Правительство республики Коми')
		OR d.organization IN ('СУ СК РФ Республика Коми', 'МВД Республика Коми', 'Прокуратура Республики Коми', 'УФССП Республика Коми', 'ГУ МЧС Республика Коми', 'ГУФСИН Республика Коми', 'УФСКН Республика Коми')
		OR d.organization IN ('УФМС России по Республике Коми', 'Росприроднадзор Республика Коми', 'Россельхознадзор Республика Коми', 'УГАДН Республика Коми', 'ТО Росздравнадзора Республика Коми', 'Управление Роспотребнадзора Республика Коми', 'ТО Росстата Республика Коми', 'Росреестр Республика Коми', 'УФНС Республика Коми', 'УФК Республика Коми', 'Управление ФАС Республика Коми', 'Управление Роскомнадзора Республика Коми', 'ГИТ Республика Коми', 'Республика Коми (ликвидировано 10.02.2016)', 'ТУ Росимущества Республика Коми')
	);

/*SELECT *
FROM declaration a
WHERE (
	SELECT COUNT(*) 
	FROM declaration b
	WHERE
		b.pdl_id = a.pdl_id AND
		b.year >= a.year AND
		b.type = 'Антикоррупционная декларация'
) <= 3*/


/* ОБЪЕДИНЕНИЕ ТАБЛИЦ */
INSERT INTO declaration22 (old_id, pdl_id, year, position, organization, link)
SELECT id, pdl_id, year, position, organization, link FROM declaration d
WHERE
	d.type = 'Антикоррупционная декларация' AND
	d.organization IN ('Государственный Совет Республики Коми', 'Глава республики Коми', 'Избирательная комиссия Республики Коми', 'Правительство республики Коми');

INSERT INTO transport22 (old_id, owner, type, car)
SELECT declaration_id, owner, type, car FROM transport t WHERE t.declaration_id IN
(
	SELECT DISTINCT id FROM declaration d
	WHERE
	d.type = 'Антикоррупционная декларация' AND
	d.organization IN ('Государственный Совет Республики Коми', 'Глава республики Коми', 'Избирательная комиссия Республики Коми', 'Правительство республики Коми')
);

INSERT INTO real_estate22 (old_id, owner, type, region, square, note)
SELECT declaration_id, owner, type, region, square, note FROM real_estate r WHERE r.declaration_id IN
(
	SELECT DISTINCT id FROM declaration d
	WHERE
	d.type = 'Антикоррупционная декларация' AND
	d.organization IN ('Государственный Совет Республики Коми', 'Глава республики Коми', 'Избирательная комиссия Республики Коми', 'Правительство республики Коми')
);

INSERT INTO income22 (old_id, owner, amount, note)
SELECT declaration_id, owner, amount, note FROM income i WHERE i.declaration_id IN
(
	SELECT DISTINCT id FROM declaration d
	WHERE
	d.type = 'Антикоррупционная декларация' AND
	d.organization IN ('Государственный Совет Республики Коми', 'Глава республики Коми', 'Избирательная комиссия Республики Коми', 'Правительство республики Коми')
);

UPDATE transport22 t
LEFT JOIN declaration22 d ON d.old_id=t.old_id
SET t.declaration_id=d.id
WHERE t.old_id IS NOT NULL;

UPDATE real_estate22 r
LEFT JOIN declaration22 d ON d.old_id=r.old_id
SET r.declaration_id=d.id
WHERE r.old_id IS NOT NULL;

UPDATE income22 i
LEFT JOIN declaration22 d ON d.old_id=i.old_id
SET i.declaration_id=d.id
WHERE i.old_id IS NOT NULL;

UPDATE declaration22 d
LEFT JOIN (
	SELECT p1.id as o_id, p2.id as n_id FROM pdl p1
	INNER JOIN pdl22 p2 ON p1.last_name=p2.last_name AND p1.name=p2.name AND p1.second_name=p2.second_name
	WHERE p1.id IN (
		SELECT pdl_id FROM declaration22
		WHERE old_id IS NOT NULL
	)
) t ON d.pdl_id=t.o_id
SET d.pdl_id=t.n_id, d.old_id=NULL
WHERE d.old_id IS NOT NULL AND t.o_id IS NOT NULL;

INSERT INTO pdl22 (old_id, last_name, name, second_name)
SELECT id, last_name, name, second_name FROM pdl p
WHERE p.id IN (
	SELECT DISTINCT pdl_id FROM declaration22
	WHERE old_id IS NOT NULL
)

UPDATE declaration22 d
LEFT JOIN pdl22 p ON d.pdl_id=p.old_id
SET d.pdl_id=p.id, d.old_id=NULL
WHERE d.old_id IS NOT NULL;


/* ИТОГОВАЯ ТАБЛИЦА */
SELECT
	last_name, name, second_name, year,
	(SELECT ROUND(SUM(amount), 2) FROM income i WHERE i.declaration_id=d.id AND i.owner = '') as "income",
	(SELECT ROUND(SUM(square), 2) FROM real_estate r WHERE r.declaration_id=d.id AND r.owner = '' AND (r.type NOT LIKE 'Земельный%' AND r.type NOT LIKE 'Земли%')) as "square(house)",
	(SELECT ROUND(SUM(square), 2) FROM real_estate r WHERE r.declaration_id=d.id AND r.owner = '' AND (r.type LIKE 'Земельный%' OR r.type LIKE 'Земли%')) as "square(land)",
	(SELECT COUNT(1) FROM transport t WHERE t.declaration_id=d.id AND t.owner = '') as "transport",
	
	(SELECT ROUND(SUM(amount), 2) FROM income i WHERE i.declaration_id=d.id AND i.owner != '') as "family_income",
	(SELECT ROUND(SUM(square), 2) FROM real_estate r WHERE r.declaration_id=d.id AND r.owner != '' AND (r.type NOT LIKE 'Земельный%' AND r.type NOT LIKE 'Земли%')) as "family_square(house)",
	(SELECT ROUND(SUM(square), 2) FROM real_estate r WHERE r.declaration_id=d.id AND r.owner != '' AND (r.type LIKE 'Земельный%' OR r.type LIKE 'Земли%')) as "family_square(land)",
	(SELECT COUNT(1) FROM transport t WHERE t.declaration_id=d.id AND t.owner != '') as "family_transport",
	position
FROM declaration d
LEFT JOIN pdl p ON p.id=d.pdl_id
ORDER BY 1, 2, 3, 4 DESC;