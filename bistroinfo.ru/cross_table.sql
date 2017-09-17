/**
 * @brief   Create pivot table
 * @file    cross_table.sql
 * @author  dmryutov (dmryutov@gmail.com)
 * @version 1.0
 * @date    07.06.2017 -- 07.06.2017
 */

SELECT
	CONCAT(
		'SELECT ',
		GROUP_CONCAT(DISTINCT
			CONCAT(
				'MAX(CASE WHEN i.key = ''',
				i.key,
				''' THEN i.value END) AS ',
				'"', i.key, '"'
			)
		),
		' FROM input i GROUP BY i.id ORDER BY i.id;'
	)
FROM input i;


SELECT
	MAX(CASE WHEN i.key = 'BIN' THEN i.value END) AS "BIN",
	MAX(CASE WHEN i.key = 'Платежная система' THEN i.value END) AS "Платежная система",
	MAX(CASE WHEN i.key = 'Страна' THEN i.value END) AS "Страна",
	MAX(CASE WHEN i.key = 'Выдана' THEN i.value END) AS "Выдана",
	MAX(CASE WHEN i.key = 'Тип карты' THEN i.value END) AS "Тип карты",
	MAX(CASE WHEN i.key = 'Категория карты' THEN i.value END) AS "Категория карты"
FROM input i
GROUP BY i.id
ORDER BY i.id;