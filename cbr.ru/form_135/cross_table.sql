/**
 * @brief   Create pivot table
 * @file    cross_table.sql
 * @author  dmryutov (dmryutov@gmail.com)
 * @version 1.0
 * @date    27.04.2016
 */

SET group_concat_max_len = 1048576;
SET @sql = NULL;
SELECT
  GROUP_CONCAT(DISTINCT
    CONCAT(
      'MAX(IF(indicator = ''',
      indicator,
      ''', total, NULL)) AS "',
      (CASE WHEN ISNULL(i.name) THEN indicator ELSE CONCAT(indicator, ' (', i.name, ')') END),
    '"'
    ) ORDER BY indicator
  ) INTO @sql
FROM banks_2008_03 b LEFT JOIN indicator2 i on b.indicator=i.id;
SET @sql = CONCAT('SELECT bl.name name, date, ', @sql,
			' FROM banks_2008_03 b LEFT JOIN bank bl ON b.bank_id=bl.number GROUP BY bl.name');

PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;