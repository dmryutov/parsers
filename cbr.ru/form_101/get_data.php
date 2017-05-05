<?php
/**
 * @brief   Extract financial indicators from 101 form from `cbr.ru`
 * @file    get_data.php
 * @author  dmryutov (dmryutov@gmail.com)
 * @version 1.0
 * @date    22.04.2016 -- 23.05.2016
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
$BAD_CHARS = array('<sub>', '</sub>', ' ', chr(194).chr(160));

for ($f = 1; $f <= 25000; $f++) {
    echo $f .'<br>';
    if (!file_exists('downloads/article_'. $f .'.txt')) {
        continue;
    }

    $file = mb_convert_encoding(file_get_contents('downloads/article_'. $f .'.txt', true),
                                'UTF-8', 'CP-1251');
    $file = str_replace("> <", '><', preg_replace('/\s+/', ' ', $file));
    
    // Explode document parts
    $head = substr($file, strpos($file, '<header_div>') + 12,
                   strpos($file, '</header_div>') - strpos($file, '<header_div>') - 12);
    $body = substr($file, strpos($file, '<body_div>') + 10,
                   strpos($file, '</body_div>') - strpos($file, '<body_div>') - 10);
    
    // Number
    $number = substr($head, strpos($head, 'номер</td><td>') + 19,
                     strrpos($head, '</tr>', -1) - strpos($head, 'номер</td>') - 24);

    // Date
    $date = substr($head, strpos($head, '<h1>') + 4,
                   strpos($head, '</h1>') - strpos($head, '<h1>') - 4);
    $date = substr($head, strpos($head, 'sp;1 ') + 5,
                   strpos($head, ' г.') - strpos($head, '&nbsp;') - 5);
    $date = explode(' ', $date);
    foreach ($month_list[1] as $key => $value) {
        if ($date[0] == $value) {
            $m = ($key <= 8) ? '0'.($key+1) : $key+1;
            break;
        }
    }
    $y = $date[1];

    // Parse table
    $DOM->loadHTML('<meta http-equiv="Content-Type" content="text/html; charset=utf-8">'. $body);
    $tr = $DOM->getElementsByTagName('tr');
    
    $i = $j = 0;
    foreach ($tr as $row) {
        $td = $row->getElementsByTagName('td');
        if ($td[0]->nodeValue == 'Итого по активу (баланс)') {
            if ($i == 0) {
                mysql_query("INSERT INTO banks_".$y."_$m (bank_id, total, date, indicator) ".
                            "VALUES ('$number', '".
                            str_replace($BAD_CHARS, '', $td[3]->nodeValue) .
                            "', '$y-$m-01', 'ИАБВо')");
                mysql_query("INSERT INTO banks_".$y."_$m (bank_id, total, date, indicator) ".
                            "VALUES ('$number', '".
                            str_replace($BAD_CHARS, '', $td[6]->nodeValue) .
                            "', '$y-$m-01', 'ИАБОд')");
                mysql_query("INSERT INTO banks_".$y."_$m (bank_id, total, date, indicator) ".
                            "VALUES ('$number', '".
                            str_replace($BAD_CHARS, '', $td[9]->nodeValue) .
                            "', '$y-$m-01', 'ИАБОк')");
                mysql_query("INSERT INTO banks_".$y."_$m (bank_id, total, date, indicator) ".
                            "VALUES ('$number', '".
                            str_replace($BAD_CHARS, '', $td[12]->nodeValue) .
                            "', '$y-$m-01', 'ИАБИо')");
            } elseif ($i == 1) {
                mysql_query("INSERT INTO banks_".$y."_$m (bank_id, total, date, indicator) ".
                            "VALUES ('$number', '".
                            str_replace($BAD_CHARS, '', $td[3]->nodeValue) .
                            "', '$y-$m-01', 'ИАВВо')");
                mysql_query("INSERT INTO banks_".$y."_$m (bank_id, total, date, indicator) ".
                            "VALUES ('$number', '".
                            str_replace($BAD_CHARS, '', $td[6]->nodeValue) .
                            "', '$y-$m-01', 'ИАВОд')");
                mysql_query("INSERT INTO banks_".$y."_$m (bank_id, total, date, indicator) ".
                            "VALUES ('$number', '".
                            str_replace($BAD_CHARS, '', $td[9]->nodeValue) .
                            "', '$y-$m-01', 'ИАВОк')");
                mysql_query("INSERT INTO banks_".$y."_$m (bank_id, total, date, indicator) ".
                            "VALUES ('$number', '".
                            str_replace($BAD_CHARS, '', $td[12]->nodeValue) .
                            "', '$y-$m-01', 'ИАВИо')");
            }
            $i++;
        }
        if ($td[0]->nodeValue == 'Итого по пассиву (баланс)') {
            if ($j == 0) {
                mysql_query("INSERT INTO banks_".$y."_$m (bank_id, total, date, indicator) ".
                            "VALUES ('$number', '".
                            str_replace($BAD_CHARS, '', $td[3]->nodeValue) .
                            "', '$y-$m-01', 'ИПБВо')");
                mysql_query("INSERT INTO banks_".$y."_$m (bank_id, total, date, indicator) ".
                            "VALUES ('$number', '".
                            str_replace($BAD_CHARS, '', $td[6]->nodeValue) .
                            "', '$y-$m-01', 'ИПБОд')");
                mysql_query("INSERT INTO banks_".$y."_$m (bank_id, total, date, indicator) ".
                            "VALUES ('$number', '".
                            str_replace($BAD_CHARS, '', $td[9]->nodeValue) .
                            "', '$y-$m-01', 'ИПБОк')");
                mysql_query("INSERT INTO banks_".$y."_$m (bank_id, total, date, indicator) ".
                            "VALUES ('$number', '".
                            str_replace($BAD_CHARS, '', $td[12]->nodeValue) .
                            "', '$y-$m-01', 'ИПБИо')");
            } elseif ($j == 1) {
                mysql_query("INSERT INTO banks_".$y."_$m (bank_id, total, date, indicator) ".
                            "VALUES ('$number', '".
                            str_replace($BAD_CHARS, '', $td[3]->nodeValue) .
                            "', '$y-$m-01', 'ИПВВо')");
                mysql_query("INSERT INTO banks_".$y."_$m (bank_id, total, date, indicator) ".
                            "VALUES ('$number', '".
                            str_replace($BAD_CHARS, '', $td[6]->nodeValue) .
                            "', '$y-$m-01', 'ИПВОд')");
                mysql_query("INSERT INTO banks_".$y."_$m (bank_id, total, date, indicator) ".
                            "VALUES ('$number', '".
                            str_replace($BAD_CHARS, '', $td[9]->nodeValue) .
                            "', '$y-$m-01', 'ИПВОк')");
                mysql_query("INSERT INTO banks_".$y."_$m (bank_id, total, date, indicator) ".
                            "VALUES ('$number', '".
                            str_replace($BAD_CHARS, '', $td[12]->nodeValue) .
                            "', '$y-$m-01', 'ИПВИо')");
            }
            $j++;
        }
        if ($i == 2 && $j == 2) {
            break;
        }
    }
}

echo "<br><br>Total time - ". round((MICROTIME(true) - $start_time), 3) ." seconds.";
