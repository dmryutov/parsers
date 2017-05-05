<?php
/**
 * @brief   Extract financial indicators from `profbanking.com`
 * @file    get_indecator.php
 * @author  dmryutov (dmryutov@gmail.com)
 * @version 1.0
 * @date    15.04.2016
 * @note    http://www.profbanking.com/info/835-chart-of-accounts-in-banks.html
 */

// Turn on error reporting
set_time_limit(600000);
ini_set('memory_limit', '4096M');
$start_time = MICROTIME(true);
// Connect to DB
$db = mysql_connect('localhost', 'root', '') or die('Database connection error!');
mysql_select_db('banks2', $db);
mysql_query("SET NAMES utf8");

$file = mb_convert_encoding(file_get_contents('downloads/table1.html', true), 'UTF-8', 'CP-1251');
$file = str_replace("> <", '><', preg_replace('/\s+/', ' ', $file));

$dom = new DOMDocument();
$dom->loadHTML('<meta http-equiv="Content-Type" content="text/html; charset=utf-8">'. $file);
$tr = $dom->getElementsByTagName('tr');

foreach ($tr as $row) {
    $td = $row->getElementsByTagName('td');
    if ($td->length != 4 || intval($td[0]->nodeValue) == 0 &&
        intval($td[1]->nodeValue) == 0 || $td[2]->nodeValue == '3') {
        continue;
    }

    if (intval($td[0]->nodeValue) != 0) {
        mysql_query("INSERT INTO indicator (id, name) VALUES ('". $td[0]->nodeValue ."', '".
                    mb_convert_encoding($td[2]->nodeValue, 'CP-1251', 'UTF-8') ."')")
                    or die(mysql_error());
    } else {
        mysql_query("INSERT INTO indicator (id, parent_id, name) VALUES ('".
                    $td[1]->nodeValue ."', '". substr($td[1]->nodeValue, 0, 3) ."', '".
                    mb_convert_encoding($td[2]->nodeValue, 'CP-1251', 'UTF-8') ."')")
                    or die(mysql_error());
    }
}

$file = mb_convert_encoding(file_get_contents('downloads/table2.html', true), 'UTF-8', 'CP-1251');
$file = str_replace("> <", '><', preg_replace('/\s+/', ' ', $file));

$dom = new DOMDocument();
$dom->loadHTML('<meta http-equiv="Content-Type" content="text/html; charset=utf-8">'. $file);
$tr = $dom->getElementsByTagName('tr');

foreach ($tr as $row) {
    $td = $row->getElementsByTagName('td');
    if ($td->length != 2 || intval($td[0]->nodeValue) == 0 || $td[1]->nodeValue == '2') {
        continue;
    }
    if (strlen($td[0]->nodeValue) == 3) {
        mysql_query("INSERT INTO indicator (id, name) VALUES ('". $td[0]->nodeValue ."', '".
                    mb_convert_encoding($td[1]->nodeValue, 'CP-1251', 'UTF-8') ."')")
                    or die(mysql_error());
    } else {
        mysql_query("INSERT INTO indicator (id, parent_id, name) VALUES ('".
                    $td[0]->nodeValue ."', '". substr($td[0]->nodeValue, 0, 3) ."', '".
                    mb_convert_encoding($td[1]->nodeValue, 'CP-1251', 'UTF-8') ."')")
                    or die(mysql_error());
    }
}

$file = mb_convert_encoding(file_get_contents('downloads/table3.html', true), 'UTF-8', 'CP-1251');
$file = str_replace("> <", '><', preg_replace('/\s+/', ' ', $file));

$dom = new DOMDocument();
$dom->loadHTML('<meta http-equiv="Content-Type" content="text/html; charset=utf-8">'. $file);
$tr = $dom->getElementsByTagName('tr');

foreach ($tr as $row) {
    $td = $row->getElementsByTagName('td');
    if ($td->length != 3 || intval($td[0]->nodeValue) == 0 || $td[1]->nodeValue == '2') {
        continue;
    }
    if (strlen($td[0]->nodeValue) == 3) {
        mysql_query("INSERT INTO indicator (id, name) VALUES ('". $td[0]->nodeValue ."', '".
                    mb_convert_encoding($td[1]->nodeValue, 'CP-1251', 'UTF-8') ."')")
                    or die(mysql_error());
    } else {
        mysql_query("INSERT INTO indicator (id, parent_id, name) VALUES ('".
                    $td[0]->nodeValue ."', '". substr($td[0]->nodeValue, 0, 3) ."', '".
                    mb_convert_encoding($td[1]->nodeValue, 'CP-1251', 'UTF-8') ."')")
                    or die(mysql_error());
    }
}
