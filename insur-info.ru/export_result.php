<?php
/**
 * @brief   Export insurance companies to excel table
 * @file    export_result.php
 * @author  dmryutov (dmryutov@gmail.com)
 * @version 1.0
 * @date    03.05.2016
 ; @note    http://www.insur-info.ru/licence/?page=1&order=date
 */

require_once 'PHPExcel/PHPExcel.php';

// PHP settings
set_time_limit(600000);
ini_set('memory_limit', '4096M');
$start_time = MICROTIME(true);

$FILE_NAME = 'output.xlsx';
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

// Table style
$border['borders']['allborders']['style'] = PHPExcel_Style_Border::BORDER_THIN;
$default_style = array('alignment' => array(
    'vertical' => PHPExcel_STYLE_ALIGNMENT::VERTICAL_CENTER
));
$dom = new DOMDocument();

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
// Column name and width
$aSheet->setCellValue('A1', '№');
$aSheet->mergeCells('A1:A2');
$aSheet->setCellValue('B1', 'Рег.№');
$aSheet->mergeCells('B1:B2');
$aSheet->setCellValue('C1', 'Название страховой организации');
$aSheet->mergeCells('C1:C2');
$aSheet->getColumnDimension('C')->setWidth(33);
$aSheet->setCellValue('D1', 'Город');
$aSheet->mergeCells('D1:D2');
$aSheet->getColumnDimension('D')->setWidth(16);
$aSheet->setCellValue('E1', 'Текущий статус лицензии');
$aSheet->mergeCells('E1:E2');
$aSheet->getColumnDimension('E')->setWidth(17);
$aSheet->setCellValue('F1', 'История изменения статусов');
$aSheet->mergeCells('F1:J1');
$aSheet->setCellValue('F2', 'Номер приказа');
$aSheet->getColumnDimension('F')->setWidth(15);
$aSheet->setCellValue('G2', 'Дата подписания приказа');
$aSheet->getColumnDimension('G')->setWidth(13);
$aSheet->setCellValue('H2', 'Дата вступления в силу');
$aSheet->getColumnDimension('H')->setWidth(13);
$aSheet->setCellValue('I2', 'Статус по приказу');
$aSheet->getColumnDimension('I')->setWidth(16);
$aSheet->setCellValue('J2', 'Примечание');
$aSheet->getColumnDimension('J')->setWidth(35);


$i = 3;
$l = 0;
for ($f = 1; $f <= 70; $f++) {
    $file = mb_convert_encoding(
        file_get_contents('files/article_'. $f .'.txt', true),
        'UTF-8',
        'CP-1251'
    );
    $file = str_replace("> <", '><', preg_replace('/\s+/', ' ', $file));

    // Load HTML as DOM
    $dom->loadHTML('<meta http-equiv="Content-Type" content="text/html; charset=utf-8">'. $file);
    $tr = $dom->getElementsByTagName('tr');
    
    $j = 0;
    foreach ($tr as $row) {
        $j++;
        $td = $row->getElementsByTagName('td');
        if (($j < 3) || empty($td[1]->nodeValue)) {
            continue;
        }
        $k = 0;
        foreach ($td as $cell) {
            if ($k > 9) {
                break;
            }
            $value = $cell->nodeValue;
            if (empty($value) && $k == 0) {
                $k = 5;
                continue;
            }
            $aSheet->setCellValue($LETTERS[$k].$i, $value);
            $k++;
        }
        if (!empty($td[0]->nodeValue)) {
            if ($l>0) {
                $aSheet->mergeCells('A'.($i-$l).':A'.($i-1));
                $aSheet->mergeCells('B'.($i-$l).':B'.($i-1));
                $aSheet->mergeCells('C'.($i-$l).':C'.($i-1));
                $aSheet->mergeCells('D'.($i-$l).':D'.($i-1));
                $aSheet->mergeCells('E'.($i-$l).':E'.($i-1));
            }
            $l = 0;
            continue;
        } else {
            $l++;
        }
        $i++;
    }
}

// Set styles
$aSheet->getStyle('A1:'. 'J'.($i-1))->applyFromArray($border);
$aSheet->getStyle('A1:'. 'J'.($i-1))->getAlignment()->setWrapText(true);

// Save to file
if (file_exists($FILE_NAME)) {
    unlink($FILE_NAME);
}
$objWriter = PHPExcel_IOFactory::createWriter($pExcel, 'Excel2007');
$objWriter->save($FILE_NAME);

unset($aSheet);
unset($pExcel);
echo "<br><br>Total time - ". round((MICROTIME(true) - $start_time), 3) ." seconds.";
