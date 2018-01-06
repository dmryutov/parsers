<?php
/**
 * @brief   Extract financial indicators from 135 form from `cbr.ru`
 * @file    get_data.php
 * @author  dmryutov (dmryutov@gmail.com)
 * @version 1.0
 * @date    23.04.2016 -- 26.04.2016
 */

// Turn on error reporting
set_time_limit(600000);
ini_set('memory_limit', '4096M');
$start_time = MICROTIME(true);
// Connect to DB
$db = mysql_connect('localhost', 'root', '') or die('Database connection error!');
mysql_select_db('banks2', $db);
mysql_query("SET NAMES utf8");

$DOM = new DOMDocument();
$MONTH_LIST = array(
    array(
        'Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август',
        'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'
    ),
    array(
        'января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августа',
        'сентября', 'октября', 'ноября', 'декабря'
    )
);

for ($f = 1; $f <= 46000; $f++) {
    echo $f .'<br>';
    if (!file_exists('downloads/article_'. $f .'.txt')) {
        continue;
    }

    $file = mb_convert_encoding(
        file_get_contents('downloads/article_'. $f .'.txt', true),
        'UTF-8',
        'CP-1251'
    );
    $file = str_replace("> <", '><', preg_replace('/\s+/', ' ', $file));
    
    // Explode document parts
    $head = substr(
        $file,
        strpos($file, '<header_div>') + 12,
        strpos($file, '</header_div>') - strpos($file, '<header_div>') - 12
    );
    $part2 = substr(
        $file,
        strpos($file, '<part2_div>') + 11,
        strpos($file, '</part2_div>') - strpos($file, '<part2_div>') - 11
    );
    $part3 = substr(
        $file,
        strpos($file, '<part3_div>') + 11,
        strpos($file, '</part3_div>') - strpos($file, '<part3_div>') - 11
    );
    
    // Number
    $number = substr($head, strpos($head, '(порядковый номер)</td><td>') + 42);
    $number = substr($number, 0, strpos($number, '</td>'));

    // Date
    $date = substr(
        str_replace('&nbsp;', ' ', $head),
        strpos($head, '<h1>') + 5,
        strpos($head, '</h1>') -
        strpos($head, '<h1>') - 4
    );
    $date = substr($date, strpos($date, ' 1 ') + 3, strpos($date, ' г.') -
                   strpos($date, ' 1 ') - 3);
    $date = explode(' ', $date);
    foreach ($MONTH_LIST[1] as $key => $value) {
        if ($date[0] == $value) {
            $m = ($key <= 8) ? '0'.($key+1) : $key+1;
            break;
        }
    }
    $y = $date[1];

    // Section 2
    mysql_query("CREATE TABLE IF NOT EXISTS `banks_".$y."_$m` (bank_id integer, ".
                "total varchar(50), `date` date, indicator varchar(20))") or die(mysql_error());

    $part2 = substr(
        $part2,
        strpos($part2, '<li>') + 4,
        strrpos($part2, '</li>') - strpos($part2, '<li>') - 4
    );
    $part2 = explode('</li><li>', $part2);
    foreach ($part2 as $value) {
        $value = str_replace(array('<sub>', '</sub>', ' ', chr(194).chr(160)), '', $value);
        $value = explode('=', $value);
        if (empty($value[1]) || strlen($value[0]) > 20) {
            continue;
        }
        mysql_query("INSERT INTO banks_".$y."_$m (bank_id, total, date, indicator) VALUES ".
                    "('$number', '". substr($value[1], 0, strpos($value[1], ',')) ."', ".
                    "'$y-$m-01', '$value[0]')");
    }

    // Section 3
    $DOM->loadHTML('<meta http-equiv="Content-Type" content="text/html; charset=utf-8">'. $part3);
    $tr = $DOM->getElementsByTagName('tr');

    foreach ($tr as $row) {
        $td = $row->getElementsByTagName('td');
        if (empty($td[1]->nodeValue) || strlen($td[0]->nodeValue) > 10) {
            continue;
        }
        mysql_query("INSERT INTO banks_".$y."_$m (bank_id, total, date, indicator) VALUES ".
            "('$number', '". $td[1]->nodeValue ."', '$y-$m-01', '". $td[0]->nodeValue ."')")
            or die(mysql_error());
    }
}

echo "<br><br>Total time - ". round((MICROTIME(true) - $start_time), 3) ." seconds.";
