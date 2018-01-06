<?php
/**
 * @brief   Export financial indicators to excel table
 * @file    export_result.php
 * @author  dmryutov (dmryutov@gmail.com)
 * @version 1.0
 * @date    28.04.2016 -- 22.05.2016
 */

require_once '../PHPExcel/PHPExcel.php';
require_once 'bank_list.php';
require_once 'get_cell.php';

// Turn on error reporting
ini_set('display_errors', 'On');
error_reporting(E_ALL);
// PHP settings
set_time_limit(600000);
ini_set('memory_limit', '4096M');
$start_time = MICROTIME(true);
// Connect to DB
$db = mysql_connect('localhost', 'root', '') or die('Database connection error!');
mysql_select_db('banks2', $db);
mysql_query("SET NAMES utf8");

global $LETTERS, $aSheet, $initOffset, $default_style;
$DOM = new DOMDocument();
$LETTERS = array(
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
    'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'AG', 'AH',
    'AI', 'AJ', 'AK', 'AL', 'AM', 'AN', 'AO', 'AP', 'AQ', 'AR', 'AS', 'AT', 'AU', 'AV', 'AW',
    'AX', 'AY', 'AZ', 'BA', 'BB', 'BC', 'BD', 'BE', 'BF', 'BG', 'BH', 'BI', 'BJ', 'BK', 'BL',
    'BM', 'BN', 'BO', 'BP', 'BQ', 'BR', 'BS', 'BT', 'BU', 'BV', 'BW', 'BX', 'BY', 'BZ', 'CA',
    'CB', 'CC', 'CD', 'CE', 'CF', 'CG', 'CH', 'CI', 'CJ', 'CK', 'CL', 'CM', 'CN', 'CO', 'CP',
    'CQ', 'CR', 'CS', 'CT', 'CU', 'CV', 'CW', 'CX', 'CY', 'CZ', 'DA', 'DB', 'DC', 'DD', 'DE',
    'DF', 'DG', 'DH', 'DI', 'DJ', 'DK', 'DL', 'DM', 'DN', 'DO', 'DP', 'DQ', 'DR', 'DS', 'DT',
    'DU', 'DV', 'DW', 'DX', 'DY', 'DZ'
);
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

$border['borders']['allborders']['style'] = PHPExcel_Style_Border::BORDER_THIN;
$default_style = array('alignment' => array(
    'vertical' => PHPExcel_STYLE_ALIGNMENT::VERTICAL_CENTER
));


for ($f = 1; $f <= 3500; $f++) {
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
    $body = substr(
        $file,
        strpos($file, '<body_div>') + 10,
        strpos($file, '</body_div>') - strpos($file, '<body_div>') - 10
    );
    
    // Number
    $number = substr(
        $head,
        strpos($head, 'номер</td><td>') + 19,
        strrpos($head, '</tr>', -1) - strpos($head, 'номер</td>') - 24
    );

    // Date
    $date = substr(
        $head,
        strpos($head, '<h1>') + 4,
        strpos($head, '</h1>') - strpos($head, '<h1>') - 4
    );
    $date = substr(
        $head,
        strpos($head, 'sp;1 ') + 5,
        strpos($head, ' г.') - strpos($head, '&nbsp;') - 5
    );
    $date = explode(' ', $date);
    foreach ($MONTH_LIST[1] as $key => $value) {
        if ($date[0] == $value) {
            $m = $MONTH_LIST[0][$key];
            break;
        }
    }
    $y = $date[1];

    // Excel settings
    $pExcel = new PHPExcel();
    // Active sheet
    $pExcel->setActiveSheetIndex(0);
    $aSheet = $pExcel->getActiveSheet();
    // Sheet title
    $aSheet->setTitle($m .'_'. $y);
    // Font settings
    $pExcel->getDefaultStyle()->getFont()->setName('Arial');
    $pExcel->getDefaultStyle()->getFont()->setSize(11);
    // Column width
    $aSheet->getColumnDimension('A')->setWidth(40);

    // Table parsing
    $DOM->loadHTML('<meta http-equiv="Content-Type" content="text/html; charset=utf-8">'. $body);
    $tr = $DOM->getElementsByTagName('tr');
    
    $i = $j = 1;
    $initOffset = array();
    foreach ($tr as $row) {
        get_cell($row->getElementsByTagName('th'), $i, true);
        $j = get_cell($row->getElementsByTagName('td'), $i, false);
        $i++;
    }

    // Set styles
    $aSheet->getStyle('A1:'. $LETTERS[$j-1].($i-1))->applyFromArray($border);
    $aSheet->getStyle('A1:'. $LETTERS[$j-1].($i-1))->getAlignment()->setWrapText(true);

    // Save to file
    $dir = 'Excel/'. $BANK_LIST[$number] .'/'. $y;
    if (!is_dir($dir)) {
        mkdir($dir, 0755, true);
    }

    $fname = $dir .'/'. $m .'_'. $y .'.xlsx';
    if (file_exists($fname)) {
        unlink($fname);
    }
    $objWriter = PHPExcel_IOFactory::createWriter($pExcel, 'Excel2007');
    $objWriter->save($fname);

    unset($aSheet);
    unset($pExcel);
}

echo "<br><br>Total time - ". round((MICROTIME(true) - $start_time), 3) ." seconds.";
