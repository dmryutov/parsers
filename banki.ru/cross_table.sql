/**
 * @brief   Create pivot table
 * @file    cross_table.sql
 * @author  dmryutov (dmryutov@gmail.com)
 * @version 1.0
 * @date    22.10.2015 -- 22.10.2015
 */

SET group_concat_max_len = 1048576;
SET @sql = NULL;
SELECT
  GROUP_CONCAT(DISTINCT
    CONCAT(
      'MAX(IF(indicator = ''',
      indicator,
      ''', total, NULL)) AS "',
      (CASE WHEN ISNULL(i.parent_id) THEN i.name ELSE CONCAT(i2.name, ' -> ', i.name) END),
    '"'
    ) ORDER BY (CASE WHEN ISNULL(i.parent_id) THEN i.name ELSE CONCAT(i2.name, ' -> ', i.name) END)
  ) INTO @sql
FROM banks_2008_03;
SET @sql = CONCAT('SELECT name, license, region, date, ', @sql, ' FROM banks_2008_03 GROUP BY name');

PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;