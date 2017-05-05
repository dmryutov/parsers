<?php
/**
 * @brief   Generate parsing links
 * @file    generate_links.php
 * @author  dmryutov (dmryutov@gmail.com)
 * @version 1.0
 * @date    26.04.2016
 */

$FILE_NAME = 'links.txt'

if (file_exists($FILE_NAME)) {
    unlink($FILE_NAME);
}
$file = file('files/number.txt');
$i = 1;
foreach ($file as $value) {
    $value = str_replace("\\r\\n", '', preg_replace('/\s+/', '', $value));
    for ($y = 2003; $y <= 2016; $y++) {
        for ($m = 1; $m <= 12; $m++) {
            if ($m < 10) {
                $m2 = '0'. $m;
            } else {
                $m2 = $m;
            }
            file_put_contents('links.txt',
                'http://www.cbr.ru/credit/fo135.asp?regn='. $value .
                '&when='.$y .$m2 .'01'. "\r\n",
                FILE_APPEND);
        }
    }

    echo $i .'/'. count($file) .'<br>';
    $i++;
}
