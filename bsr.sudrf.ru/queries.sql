/**
 * @brief   Useful SQL queries 
 * @file    queries.sql
 * @author  dmryutov (dmryutov@gmail.com)
 * @version 1.0
 * @date    09.05.2017
 */

/* GET MAX LENGTH IN EACH COLUMN */
DELIMITER //

SET SESSION group_concat_max_len = 8192;

SET @table = "act2";
SELECT CONCAT('SELECT MAX(LENGTH(`', group_concat(COLUMN_NAME SEPARATOR '`)), MAX(LENGTH(`'), '`)) FROM ', @table, ';') 
INTO @expr
FROM  INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA = (select database()) 
AND   TABLE_NAME = @table;

SELECT @expr;

PREPARE sql FROM @expr;
EXECUTE sql;
DEALLOCATE PREPARE sql;

//