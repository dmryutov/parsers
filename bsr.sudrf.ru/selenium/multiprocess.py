# -*- coding: utf-8 -*-
"""
@brief:  Extract judicial acts from `bsr.sudrf.ru` (multiprocess version)
@file:   multiprocess.py
@author: dmryutov (dmryutov@gmail.com)
@date:   25.04.2017 -- 26.04.2017
"""
import csv
from multiprocessing import Pool
import os

import selenium.webdriver as webdriver

import settings


def find_name(elements):
    """
    @brief: Find name of law offender in document
    @param elements: Document paragraphs
    @return: Name of law offender
    """
    name = ''
    for j in range(len(elements) - 1):
        try:
            text = elements[j].text + ' ' + elements[j+1].text
            match = settings.NAME_MASK.search(text)
            if match:
                name = match.group(2)
                for ending in settings.BAD_ENDINGS:
                    if name.endswith(ending):
                        name = name[:-1 * len(ending)]
                name = name.strip()
                if name in settings.MONTH_LIST:
                    name = text[:text.index(',')].strip()
                break
        except Exception:  # pylint: disable=broad-except
            name = ''
    return name


def extract_acts(site):
    """
    @brief: Extract acts content to csv file
    @param site: First site in search result
    """
    # Initialize driver connection
    browser = webdriver.Firefox(executable_path=settings.DRIVER_PATH)
    browser.implicitly_wait(settings.TIMEOUT)
    # Load site
    browser.get(site)

    csv_exists = os.path.exists(settings.CSV_PATH)
    with open(settings.CSV_PATH, 'a', encoding='utf8') as output_file:
        csv_writer = csv.writer(output_file, delimiter=';', quoting=csv.QUOTE_ALL)
        if not csv_exists:
            csv_writer.writerow(settings.HEADERS)

        i = 1
        prev_progress = ''
        # Iterate while "Next" button is enabled
        while True:
            try:
                progress = browser.find_element_by_css_selector('.text.result-counter') \
                                  .text.encode()
                if prev_progress == progress:
                    continue

                row = [i]
                elements = browser.find_elements_by_class_name('docValue')
                # Iterate through all fields except last one (34 - 1 = 33)
                for element in elements[:33]:
                    row.append(element.text)

                # You have to switch to the iframe like so
                frame = browser.find_element_by_class_name('field-iframe')
                browser.switch_to_frame(frame)

                elements = browser.find_elements_by_tag_name('p')
                row.append(find_name(elements))
                # Switch back to the "default content" (that is, out of the iframes)
                browser.switch_to_default_content()

                csv_writer.writerow(row)
                prev_progress = progress
                print(i)
                i += 1

                button = browser.find_element_by_css_selector('.card-paginator .to-right-red')
                if 'yui-button-disabled' in button.get_attribute('class'):
                    break
                button.find_element_by_tag_name('button').click()
            except Exception:  # pylint: disable=broad-except
                browser.refresh()

    browser.close()
    browser.quit()


def main():
    """
    @brief: Main function
    """
    pool = Pool(processes=len(settings.FIRST_ACT))
    pool.map(extract_acts, settings.FIRST_ACT)
    pool.close()
    pool.join()


if __name__ == '__main__':
    main()
