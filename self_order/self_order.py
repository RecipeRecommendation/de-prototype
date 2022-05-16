import json
import time
from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from constants import ROOT


def login(driver):
    driver.get('https://www.bigbasket.com/')
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "(//a[normalize-space() = 'Login/Sign Up'])[last()]"))).click()
    username = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'otpEmail')))
    username.send_keys('6354368727')
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "(//button[normalize-space() = 'Continue'])[1]"))).click()

    otp = input("Enter Otp: ")
    print("Entered Otp!")

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@id = 'otp']"))).click()
    time.sleep(2)

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@id = 'otp']"))).send_keys(otp)

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'login')]"))).click()
    return


def search(driver, keyword):
    time.sleep(3)
    search_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'input')))
    search_box.clear()
    search_box.send_keys(keyword)
    search_ = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'button.btn.btn-default.bb-search')))
    search_.click()
    return


def add_item(driver, quantity):
    html_list = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "(//button[normalize-space() = 'Add'])[1]")))
    html_list.click()
    if quantity > 1:
        for i in range(quantity):
            html_list = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "(//button[@class ='btn rt'])[1]")))
            time.sleep(1.5)
            html_list.click()
    return


def go_to_checkout(driver):
    driver.get('https://www.bigbasket.com/basket/?ver=1')
    return


def get_total(driver):
    return WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//span[@id = 'finalTotal']"))).text


def get_shopping_list():
    items = json.load(open(ROOT + "/resources/items.json"))
    shopping_list = []
    quantity_list = []
    for key in items.keys():
        shopping_list.append(items[key]['item'])
        if items[key]['quantity'] == '':
            quantity_list.append(6)
        else:
            quantity_list.append(int(items[key]['quantity']))
    return shopping_list, quantity_list


def submit_order(driver):
    while True:
        try:
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//a[@class = 'uiv2-removerow ']"))).click()
        except:
            print("Error! or Done")
            break


def self_order():
    # options = webdriver.ChromeOptions()
    # options.add_argument("headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    login(driver)
    shopping_list, quantity_list = get_shopping_list()
    shopping_list = [s.rstrip() for s in shopping_list]
    for item, quantity in zip(shopping_list, quantity_list):
        search(driver, item)
        add_item(driver, quantity)
        driver.get('https://www.bigbasket.com/')
    go_to_checkout(driver)
    total_price = {"total": get_total(driver)}
    with open(ROOT + "/resources/total_price.json", "w") as total:
        json.dump(total_price, total, indent=4)
    submit_order(driver)


if __name__ == "__main__":
    self_order()
