<?php
/**
 * @brief   Extract financial indicators from files downloaded from `banki.ru`
 * @file    get_data.php
 * @author  dmryutov (dmryutov@gmail.com)
 * @version 1.0
 * @date    20.10.2015 -- 22.10.2015
 */

// Turn on error reporting
ini_set('display_errors', 'On');
error_reporting(E_ALL);
// Connect to DB
$db = mysql_connect('localhost', 'root', '') or die('Database connection error!');
mysql_select_db('banks', $db);
mysql_query("SET NAMES utf8");

// Iterate through files
for ($i = 1; $i <= 1; $i++) {
    echo $i.'<br>';
    // Read file
    $file = mysql_real_escape_string(file_get_contents('downloads/article_'. $i .'.txt', true));
    $file = str_replace("\\r\\n", '', preg_replace('/\s+/', ' ', $file));

    // Date
    $dt = substr($file, strpos($file, '<div_date>') + 13, strpos($file, '</div_date>') -
          strpos($file, '<div_date>') - 13);
    $dt = explode('</option>', $dt);

    foreach ($dt as $value) {
        if (strpos($value, 'selected') != 0) {
            $dt = substr($value, strpos($value, 'value=\"') + 8, 10);
            break;
        }
    }
    $dt1 = substr(str_replace('-', '_', $dt), 0, -3);

    // Indicator
    $param = substr(
        $file,
        strpos($file, '<div_pokazat>') + 13,
        strpos($file, '</div_pokazat>') - strpos($file, '<div_pokazat>') - 13
    );

    // Bank name
    $name = substr(
        $file,
        strpos($file, '<div_name>') + 10,
        strpos($file, '</div_name>') - strpos($file, '<div_name>') - 10
    );
    if (empty($name)) {
        continue;
    }
    
    $name = str_replace(
        array('&mdash;', '&laquo;', '&raquo;'),
        array('-', '«', '»'),
        $name
    );
    $name = explode('|||', $name);
    unset($name1);
    foreach ($name as $value) {
        if (strpos($value, 'BANK_ID=&')) {
            $name1[0][] = 'БЕЗ НАЗВАНИЯ';
            $name1[1][] = '-';
            $name1[2][] = '-';
        } else {
            $name1[0][] = mb_convert_encoding(
                substr(
                    $value,
                    strpos($value, '>') + 1,
                    strpos($value, '</a>') - strpos($value, '>') - 2
                ),
                'UTF-8',
                'CP-1251'
            );
            $t = mb_convert_encoding(
                substr($value, strpos($value, 'color-gray-burn')),
                'UTF-8',
                'CP-1251'
            );
            $name1[1][] = substr($t, strpos($t, '№') + 4, strpos($t, ',') - strpos($t, '№') - 4);
            $name1[2][] = substr($t, strpos($t, ',') + 2, strlen($t) - strpos($t, ',') - 9);
        }
    }

    // Raiting
    $pos = substr(
        $file,
        strpos($file, '<div_pos>') + 9,
        strpos($file, '</div_pos>') - strpos($file, '<div_pos>') - 9
    );
    $pos = explode('|||', $pos);
    unset($pos1);
    foreach ($pos as $value) {
        if (strpos($value, '<') == 0) {
            $pos1[] = $value;
        } else {
            $pos1[] = substr($value, 0, strpos($value, '<'));
        }
    }

    // Sum
    $sum = substr(
        $file,
        strpos($file, '<div_sum>') + 9,
        strpos($file, '</div_sum>') - strpos($file, '<div_sum>') - 9
    );
    $sum = str_replace('&minus;', '-', $sum);
    $sum = explode('|||', $sum);
    unset($sum1);
    foreach ($sum as $key => $value) {
        if (!($key & 1)) {
            if (strpos($value, 'span') != 0) {
                $sum1[] = '-';
            } else {
                $sum1[] = str_replace(' ', '', $value);
            }
        }
    }

    // Insert into DB
    mysql_query("CREATE TABLE IF NOT EXISTS `banks_". $dt1 .
                "` (name varchar(255), license varchar(255), region varchar(255), ".
                "total varchar(255), position varchar(255), `date` date, ".
                "indicator varchar(255))") or die(mysql_error());
    foreach ($name1[0] as $key => $value) {
        if (!empty($value)) {
            $query1 = "(name, license, region, total, position, date, indicator) VALUES ";
            $query1 .= "('". $name1[0][$key] ."', '". $name1[1][$key] ."', '". $name1[2][$key] .
                       "', '". $sum1[$key] ."', '". $pos1[$key] ."', '{$dt}', '". $param ."')";
            mysql_query("INSERT INTO `banks_". $dt1. "` $query1") or die(mysql_error());
        }
    }
}
