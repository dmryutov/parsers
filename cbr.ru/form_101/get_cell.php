<?php
/**
 * @brief   Get cell content script
 * @file    get_cell.php
 * @author  dmryutov (dmryutov@gmail.com)
 * @version 1.0
 * @date    23.04.2016
 */

function get_cell($td, $i, $title)
{
    global $LETTERS, $aSheet, $initOffset, $default_style;
    $j = 1;
    $offS = array();

    if (intval($td[0]->nodeValue) != 0) {
        $query = mysql_query("SELECT CONCAT(i2.name, ' -> ', i1.name) nm FROM indicator i1 ".
                            "LEFT JOIN indicator i2 ON i1.parent_id=i2.id WHERE i1.id = '".
                            $td[0]->nodeValue ."'") or die(mysql_error());
        $res = mysql_fetch_array($query);
        $aSheet->setCellValue($LETTERS[0].$i, $res['nm']);
    }

    foreach ($td as $col) {
        $k = $cs = $rs = $offset = 0;
        $st = $default_style;

        foreach ($initOffset as $key => $value) {
            if ($j+$k >= $key) {
                $k++;
            }
        }
        $k += $j;

        foreach ($col->attributes as $attr) {
            $name = $attr->nodeName;
            $value = $attr->nodeValue;
            
            if ($name == 'class' && strpos($value, 'center') !== false) {
                $st['alignment']['horizontal'] = PHPExcel_STYLE_ALIGNMENT::HORIZONTAL_CENTER;
            }
            if ($name == 'class' && strpos($value, 'right') !== false) {
                $st['alignment']['horizontal'] = PHPExcel_STYLE_ALIGNMENT::HORIZONTAL_RIGHT;
            }
            if ($name == 'class' && strpos($value, 'bold') !== false || $title) {
                $st['font']['bold'] = true;
            }
            if ($name == 'colspan') {
                $cs = $value;
                $offset += $value-1;
            }
            if ($name == 'rowspan') {
                $rs = $value;
            }
        }

        if ($cs > 1 && $rs > 1) {
            for ($t=0; $t < $cs; $t++) {
                $offS[$k+$t] = $rs-1;
            }
            $aSheet->mergeCells($LETTERS[$k].$i .':'. $LETTERS[$k+$cs-1].($i+$rs-1));
        } elseif ($cs > 1) {
            $aSheet->mergeCells($LETTERS[$k].$i .':'. $LETTERS[$k+$cs-1].$i);
        } elseif ($rs > 1) {
            $offS[$k] = $rs-1;
            $aSheet->mergeCells($LETTERS[$k].$i .':'. $LETTERS[$k].($i+$rs-1));
        }

        $aSheet->setCellValue($LETTERS[$k].$i, $col->nodeValue);
        $aSheet->getStyle($LETTERS[$k].$i .':'. $LETTERS[$k].$i)->applyFromArray($st);
        $j += $offset + 1;
    }
    if ($td['length'] > 0) {
        foreach ($initOffset as $key => $value) {
            $initOffset[$key]--;
            if ($value <= 1) {
                unset($initOffset[$key]);
            }
        }
        $initOffset = $initOffset + $offS;
    }

    return $j;
}
