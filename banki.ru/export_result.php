<?php
/**
 * @brief   Export financial indicators to excel table
 * @file    export_result.php
 * @author  dmryutov (dmryutov@gmail.com)
 * @version 1.0
 * @date    20.10.2015 -- 22.10.2015
 */

require_once 'PHPExcel/PHPExcel.php';

// Turn on error reporting
ini_set('display_errors', 'On');
error_reporting(E_ALL);
// PHP settings
set_time_limit(60000);
ini_set('memory_limit', '2048M');
$start_time = MICROTIME(true);
// Connect to DB
$db = mysql_connect('localhost', 'root', 'root') or die('Database connection error!');
mysql_select_db('banks', $db);
mysql_query("SET NAMES utf8");

// Header style
$HEADER_STYLE = array(
    'font'=>array(
        'bold' => true,
        'size' => 12,
    ),
    'fill' => array(
        'type' => PHPExcel_STYLE_FILL::FILL_SOLID,
        'color'=>array(
            'rgb' => 'bdd7ee'
        )
    ),
);
// Table style
$TABLE_STYLE = array(
    'borders'=>array(
        'allborders'=>array(
            'style'=>PHPExcel_Style_Border::BORDER_THIN,
        )
    ),
    'alignment' => array(
        'horizontal' => PHPExcel_STYLE_ALIGNMENT::HORIZONTAL_CENTER,
        'vertical' => PHPExcel_STYLE_ALIGNMENT::VERTICAL_CENTER,
    ),
);

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
$MONTH = array(
    'Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль',
    'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'
);
$y = 2015;

for ($m = 1; $m <= 9; $m++) {
    $m2 = ($m < 10) ? '0'. $m : $m;
    $m1 = $MONTH[$m-1];

    // Excel settings
    $pExcel = new PHPExcel();
    // Active sheet
    $pExcel->setActiveSheetIndex(0);
    $aSheet = $pExcel->getActiveSheet();
    // Page orientation and size
    $aSheet->getPageSetup()
           ->setOrientation(PHPExcel_Worksheet_PageSetup::ORIENTATION_PORTRAIT);
    $aSheet->getPageSetup()
           ->SetPaperSize(PHPExcel_Worksheet_PageSetup::PAPERSIZE_A4);
    // Page margins
    $aSheet->getPageMargins()->setTop(1);
    $aSheet->getPageMargins()->setRight(0.75);
    $aSheet->getPageMargins()->setLeft(1.78);
    $aSheet->getPageMargins()->setBottom(1);
    // Sheet title
    $aSheet->setTitle($m1 .'_'. $y);
    // Header and footer
    $aSheet->getHeaderFooter()
           ->setOddHeader('&'. $m1 .'_'. $y);
    $aSheet->getHeaderFooter()
           ->setOddFooter('&L&B'.$aSheet->getTitle().'&RСтраница &P из &N');
    // Font settings
    $pExcel->getDefaultStyle()->getFont()->setName('Calibri');
    $pExcel->getDefaultStyle()->getFont()->setSize(11);

    // Column width
    foreach ($LETTERS as $value) {
        $aSheet->getColumnDimension($value)->setWidth(17);
    }
    $aSheet->getColumnDimension('A')->setWidth(35);
    $aSheet->getColumnDimension('B')->setWidth(10);
    $aSheet->getColumnDimension('C')->setWidth(21);
    $aSheet->getColumnDimension('D')->setWidth(13);

    // DB query
    mysql_query("SET group_concat_max_len = 1048576;") or die(mysql_error());
    mysql_query("SET @sql = NULL;") or die(mysql_error());
    mysql_query("SELECT
        GROUP_CONCAT(DISTINCT
            CONCAT(
                'MAX(IF(indicator = ''',
                indicator,
                ''', total, NULL)) AS \"',
                (CASE WHEN ISNULL(i.parent_id) THEN i.name ELSE CONCAT(i2.name, ' -> ', i.name) END),
                '\"'
            ) ORDER BY (CASE WHEN ISNULL(i.parent_id) THEN i.name ELSE CONCAT(i2.name, ' -> ', i.name) END)
        ) INTO @sql
        FROM banks_".$y."_".$m2." b LEFT JOIN indicator i on b.indicator=i.id
        LEFT JOIN indicator i2 ON i.parent_id=i2.id;");
    mysql_query("SET @sql = CONCAT('SELECT name \"Название\", license \"Лицензия\", ".
                "region \"Регион\", \'$m1 $y\' AS \"Дата\", ', @sql, ' FROM banks_".
                $y."_".$m2." GROUP BY name');") or die(mysql_error());
    mysql_query("PREPARE stmt FROM @sql;") or die(mysql_error());
    $query = mysql_query("EXECUTE stmt;") or die(mysql_error());
    mysql_query("DEALLOCATE PREPARE stmt;") or die(mysql_error());

    $i = 1;
    $j = 0;
    while ($res = mysql_fetch_array($query)) {
        if ($i == 1) {
            foreach ($res as $key => $value) {
                if (!is_int($key)) {
                    $aSheet->setCellValue($LETTERS[$j].'1', $key);
                    $j++;
                }
            }
            $i++;
        }
        $j = 0;
        foreach ($res as $key => $value) {
            if (!is_int($key)) {
                $aSheet->setCellValue($LETTERS[$j].$i, $value);
                $j++;
            }
        }
        $i++;
    }

    // Set styles
    $aSheet->getStyle('A1:'. $LETTERS[($j-1)].'1')->getAlignment()->setWrapText(true);
    $aSheet->getStyle('A1:'. $LETTERS[($j-1)].'1')->applyFromArray($HEADER_STYLE);
    $aSheet->getStyle('A1:'. $LETTERS[($j-1)]. ($i-1))->applyFromArray($TABLE_STYLE);

    // Save to file
    $fname = 'Excel/'. $y .'/'. $m1 .'_'. $y .'.xlsx';
    if (file_exists($fname)) {
        unlink($fname);
    }
    if (!is_dir('Excel/'. $y)) {
        mkdir('Excel/'. $y, 0777);
    }
    $objWriter = PHPExcel_IOFactory::createWriter($pExcel, 'Excel2007');
    $objWriter->save($fname);
    //$objWriter->save(mb_convert_encoding($fname, 'CP-1251', 'UTF-8'));

    echo $fname;
    unset($aSheet);
    unset($pExcel);
    echo "\nTotal time - ". (MICROTIME(true) - $start_time) ." seconds.\n\n";
}
