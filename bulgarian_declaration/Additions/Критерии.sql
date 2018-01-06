SELECT
	t_res.*,
	(criterion_1 + criterion_2 + criterion_3 + criterion_4 + criterion_5 +
	 criterion_6 + criterion_7 + criterion_8 + criterion_9) AS criterion_sum
FROM
(SELECT
	p.id, p.name, p.work, p.position, d.id AS declaration_id, d.year,
	(GREATEST(
		CASE WHEN
			NVL((SELECT SUM(summa) FROM nalichnie_ds t WHERE
				declaration_id IN (SELECT id FROM declaration WHERE year <= d.year AND person_id = d.person_id)), 0)  -- 6
			+ NVL((SELECT SUM(summa) FROM bankovskie_depozity t WHERE
				declaration_id IN (SELECT id FROM declaration WHERE year <= d.year AND person_id = d.person_id)), 0)  -- 7
			- NVL((SELECT SUM(stoimost) FROM nedvizhimoe_imuschestvo t WHERE
				declaration_id IN (SELECT id FROM declaration WHERE year <= d.year AND person_id = d.person_id) AND
				type != 2), 0)  -- 1 + 1.1
			< 0
		THEN 1 ELSE 0 END,
		(SELECT LEAST(COUNT(1), 1) FROM nedvizhimoe_imuschestvo t WHERE
			declaration_id IN (SELECT id FROM declaration WHERE year <= d.year AND person_id = d.person_id) AND
			type != 2 AND
			stoimost IS NULL)  -- 1 + 1.1
	)) * 36 AS criterion_1,

	(CASE WHEN
		NVL((SELECT SUM(summa) FROM nalichnie_ds t WHERE
			declaration_id = d.id), 0)  -- 6
		+ NVL((SELECT SUM(summa) FROM bankovskie_depozity t WHERE
			declaration_id = d.id), 0)  -- 7
		+ NVL((SELECT SUM(stoimost) FROM nedvizhimoe_imuschestvo t WHERE
			declaration_id = d.id AND
			type = 2), 0)  -- 2
		+ NVL((SELECT SUM(stoimost) FROM transport t WHERE
			declaration_id = d.id AND
			type = 3), 0)  -- 5
		+ NVL((SELECT NVL(SUM(declarant), 0) + NVL(SUM(suprug), 0) FROM dohody_ne_ot_zp t WHERE
			declaration_id = d.id), 0)  -- 13
		- NVL((SELECT SUM(stoimost) FROM nedvizhimoe_imuschestvo t WHERE
			declaration_id = d.id AND
			type != 2), 0)  -- 1 + 1.1
		- NVL((SELECT SUM(stoimost) FROM transport t WHERE
			declaration_id = d.id AND
			type != 3), 0)  -- 3 + 3.1 + 4
		- NVL((SELECT SUM(summa) FROM debitorskay_zadolzhnost t WHERE
			declaration_id = d.id), 0)  -- 8
		- NVL((SELECT SUM(summa) FROM kreditorskay_zadolzhnost t WHERE
			declaration_id = d.id), 0)  -- 9
		< 0
	THEN 1 ELSE 0 END) * 12 AS criterion_2,

	(SELECT LEAST(COUNT(1), 1) FROM nedvizhimoe_imuschestvo t  -- 1 + 1.1
		RIGHT JOIN nedvizhimoe_imuschestvo t2 ON  -- 2
			t.vid_sobstvennosti = t2.vid_sobstvennosti AND
			t.mesto = t2.mesto AND
			t.administrativnyi_center = t2.administrativnyi_center AND
			t.ploschad = t2.ploschad AND
			t2.type = 2
		WHERE
			t.declaration_id IN (SELECT id FROM declaration WHERE year <= d.year AND person_id = d.person_id) AND
			t.type != 2 AND
			t.id IS NULL) * 15 AS criterion_3,

	(GREATEST(
		CASE WHEN
			NVL((SELECT SUM(summa) FROM nalichnie_ds t WHERE
				declaration_id IN (SELECT id FROM declaration WHERE year <= d.year AND person_id = d.person_id)), 0)  -- 6
			+ NVL((SELECT SUM(summa) FROM bankovskie_depozity t WHERE
				declaration_id IN (SELECT id FROM declaration WHERE year <= d.year AND person_id = d.person_id)), 0)  -- 7
			- NVL((SELECT SUM(stoimost) FROM transport t WHERE
				declaration_id IN (SELECT id FROM declaration WHERE year <= d.year AND person_id = d.person_id) AND
				type != 3), 0)  -- 3 + 3.1 + 4
			< 0
		THEN 1 ELSE 0 END,
		(SELECT LEAST(COUNT(1), 1) FROM transport t WHERE
			declaration_id IN (SELECT id FROM declaration WHERE year <= d.year AND person_id = d.person_id) AND
			type != 2 AND
			stoimost IS NULL)  -- 3 + 3.1 + 4
	)) * 7 AS criterion_4,

	(CASE WHEN
		NVL((SELECT SUM(summa) FROM nalichnie_ds t WHERE
			declaration_id = d.id), 0)  -- 6
		+ NVL((SELECT SUM(stoimost) FROM nedvizhimoe_imuschestvo t WHERE
			declaration_id = d.id AND
			type = 2), 0)  -- 2
		+ NVL((SELECT SUM(stoimost) FROM transport t WHERE
			declaration_id = d.id AND
			type = 3), 0)  -- 5
		+ NVL((SELECT NVL(SUM(declarant), 0) + NVL(SUM(suprug), 0) FROM dohody_ne_ot_zp t WHERE
			declaration_id = d.id), 0)  -- 13
		- NVL((SELECT SUM(summa) FROM bankovskie_depozity t WHERE
			declaration_id = d.id), 0)  -- 7
		< 0
	THEN 1 ELSE 0 END) * 7 AS criterion_5,

	(SELECT LEAST(COUNT(1), 1)
		FROM nalichnie_ds t WHERE
		declaration_id = d.id AND
		(proishozhdenie_ds = '' OR proishozhdenie_ds IS NULL)) * 5 AS criterion_6,  -- 6

	(SELECT LEAST(COUNT(1), 1)
		FROM bankovskie_depozity t WHERE
		declaration_id = d.id AND
		(proishozhdenie_ds = '' OR proishozhdenie_ds IS NULL) AND
		(LOWER(vne_strany) = 'да' OR vne_strany = '1')) * 9 AS criterion_7,  -- 7

	(GREATEST(
		(SELECT LEAST(COUNT(1), 1) FROM akcii t WHERE
			declaration_id = d.id AND
			(summa IS NULL OR emitent = '' OR emitent IS NULL)),  -- 10
		(SELECT LEAST(COUNT(1), 1) FROM doli_v_ooo t WHERE
			declaration_id = d.id AND
			type = 0 AND
			(stoimost IS NULL OR organizacia = '' OR organizacia IS NULL))  -- 11
	)) * 4 AS criterion_8,

	(GREATEST(
		(SELECT LEAST(COUNT(1), 1) FROM debitorskay_zadolzhnost t WHERE
			declaration_id = d.id AND
			(summa IS NULL OR (
				(ot_grazhdanina_bolgarii = '' OR ot_grazhdanina_bolgarii IS NULL) AND
				(ot_inostrannogo_grazdanina = '' OR ot_inostrannogo_grazdanina IS NULL)
			))),  -- 8
		(SELECT LEAST(COUNT(1), 1) FROM kreditorskay_zadolzhnost t WHERE
			declaration_id = d.id AND
			(summa IS NULL OR (
				(naimenovanie_banka = '' OR naimenovanie_banka IS NULL) AND
				(drugoi_kreditor = '' OR drugoi_kreditor IS NULL)
			)))  -- 9
	)) * 5 AS criterion_9
FROM
	declaration d
	LEFT JOIN person p ON p.id = d.person_id) t_res;
