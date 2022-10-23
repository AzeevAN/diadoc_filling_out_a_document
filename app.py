from time import sleep
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import json
import os


name_file_settings = 'data_settings.json'


def main(data_dict_json):
    driver = webdriver.Chrome()
    driver.get("https://auth.kontur.ru/")
    sleep(5)
    elem = driver.find_element(by=By.CLASS_NAME, value='Tabs__star_2V_I')
    # elem = driver.find_element(by=By.NAME, value='login')
    elem.click()
    sleep(2)
    elems = driver.find_elements(by=By.CLASS_NAME, value='react-ui-123wljp')
    el_c = 1
    for elem in elems:
        if el_c == 3: break
        elem.send_keys(login if el_c == 1 else password)
        el_c += 1
    sleep(2)

    driver.find_element(By.TAG_NAME, 'button').click()
    sleep(10)
    driver.get('https://diadoc.kontur.ru/')
    sleep(5)
    number = 0;
    while number == 0:
        input()
    # elem_new_doc = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div[3]/div[1]/div/div[1]/a/span[2]')
    # elem_new_doc.click()
    # sleep(3)

    elem_upd = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div[4]/div/div[2]/div[1]/div[2]/div[2]/span[4]/button/div/span')
    elem_upd.click()
    sleep(3)
    driver.switch_to.window(driver.window_handles[1])

    if not os.path.isfile(name_file_settings):
        start_position_button_add = int(select_position_browser('Insert start position button add new row: ', driver))
        start_position_first_row = int(select_position_browser('Insert start position first row: ', driver))

        elem_new_row = go_to_button_add(driver, start_position_button_add)
        for i in range(1, len(data_dict_json)):
            elem_new_row.click()

        start_position_last_row = int(select_position_browser('Insert start position last row: ', driver))
        cont_pix = (start_position_last_row - start_position_first_row) / len(data_dict_json)
        cont_pix = round((start_position_last_row - start_position_first_row - cont_pix) / len(data_dict_json))
        data_json = {
            'start_position_button_add': start_position_button_add,
            'start_position_first_row': start_position_first_row,
            'cont_pix': cont_pix
        }
        with open(name_file_settings, 'w', encoding='utf-8') as f:
            json.dump(data_json, f)
    else:
        with open(name_file_settings, encoding='utf-8') as f:
            data_json = json.load(f)
        elem_new_row = go_to_button_add(driver, data_json.get('start_position_button_add'))
        for i in range(1, len(data_dict_json)):
            elem_new_row.click()

    elems_row = driver.find_elements(By.CLASS_NAME, '_2iI1P')
    i = data_json.get('start_position_first_row', 0)
    cont_pix = data_json.get('cont_pix', 0)
    iter = 0
    for elem_r in elems_row:
        driver.execute_script(f"window.scrollTo(0, {i})")
        i += cont_pix
        hov = ActionChains(driver).move_to_element(elem_r)

        hov.perform()
        try:
            name_elem = elem_r.find_element(By.CLASS_NAME, '_2a_nl')
            name_elem.find_element(By.CLASS_NAME, 'react-ui-123wljp').send_keys(f'{data_dict_json[iter].get("name")}')
            name_detail = elem_r.find_element(By.CLASS_NAME, "_1el2i")
            detail = name_detail.find_elements(By.CLASS_NAME, "_3QWUo")
            name_ed = detail[0].find_element(By.CLASS_NAME, 'react-ui-g661dn')
            name_ed.click()
            name_ed.find_element(By.TAG_NAME, "input").send_keys('шт')

            detail[1].find_element(By.TAG_NAME, "input").send_keys(data_dict_json[iter].get('count'))
            detail[2].find_element(By.TAG_NAME, "input").send_keys(data_dict_json[iter].get('price'))

            name_barcode = elem_r.find_element(By.CLASS_NAME, "pthlf")
            t_bar = name_barcode.find_elements(By.CLASS_NAME, "_2t_I2")
            t_bar[0].find_element(By.TAG_NAME, "input").send_keys("шк")
            t_bar[1].find_element(By.TAG_NAME, "input").send_keys(f"{data_dict_json[iter].get('barcode')}")

        except Exception as error:
            print(error)
        iter += 1
    while True:
        chois = input('Exit - 0: ')
        if chois == '0':
            break
    driver.close()


def go_to_button_add(driver: webdriver, position: int) -> webdriver:
    driver.execute_script(f"window.scrollTo(0, {position})")
    elem_new_row = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div/span/div[2]/div[1]/div[8]/div/div/div[1]/div[2]/div/div/div[1]/div/div/div[1]/div/div/div[2]/div/span[2]')
    return elem_new_row


def select_position_browser(text_message: str, driver: webdriver) -> str:
    return_number = 0
    while True:
        position = input(f'{text_message}')
        driver.execute_script(f"window.scrollTo(0, {position})")
        if position == '0': break
        return_number = position
    return return_number


if __name__ == '__main__':
    try:
        with open('load_data.json', encoding='utf-8') as file:
            data_dict_json = json.load(file)
        if data_dict_json is not None:
            main(data_dict_json)
    except Exception as error:
        print(error)
