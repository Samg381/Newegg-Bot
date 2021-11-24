import selenium
from selenium import webdriver
from msedge.selenium_tools import Edge, EdgeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import winsound
import time
import os


#options = webdriver.EdgeOptions()
#options.add_argument('--ignore-certificate-errors')
#path_to_adblocker = r'C:\webdrivers\uBlock\1.32.4_0'
#options.add_argument('load-extension=' + path_to_adblocker)
# options.add_argument('--incognito')
# options.add_argument('--headless')
#options.add_argument(r"user-data-dir=C:\\Users\\Sam\\AppData\\Local\\Microsoft\\Edge\\User Data\\Profile 2")
#options.add_argument("profile-directory=Profile 2")

#driver = webdriver.Edge(options=options)


options = EdgeOptions()
options.use_chromium = True
options.add_argument("--user-data-dir=C:\\webdrivers\\Profiles\\Default")
options.add_argument("--start-maximized")
driver = Edge(options=options)

URLs = [

        #TESTER
        #'https://www.newegg.com/p/38Y-0192-00036',

        # MOBO
        'https://www.newegg.com/asus-rog-maximus-z690-extreme/p/N82E16813119520',

        # RAM
        'https://www.newegg.com/corsair-32gb-288-pin-ddr5-sdram/p/N82E16820236817'
        ]

masterDelay = 40   # Time (seconds) between stock checks. Beware too low a number! 35 SECONDS TOO SMALL- RECOMMEND 40
clickDelay = 0.10  # Delay (seconds) between clicks. Used mostly during auto-checkout
timeoutDelay = 3   # Max wait time for page to load. Exceeding this time forces a restart.

#def checklogin():


def buyitem():
    popup = driver.find_elements(By.ID, 'popup-close')
    if popup:
        print(popup)
        print('Popup detected')
        popup[0].click()
        print('Popup closed')
        time.sleep(clickDelay)

    productBuy.click()
    print('Clicked add to cart')

    time.sleep(clickDelay)

    try:
        insurance = WebDriverWait(driver, timeoutDelay).until(EC.presence_of_element_located((By.XPATH, '//button[text()="No, thanks"]')))
        if insurance:
            insurance.click()
            print('Upsell declined')
    except selenium.common.exceptions.TimeoutException:
        print('No upsell detected')
        pass


    time.sleep(clickDelay)

    try:
        checkout = WebDriverWait(driver, timeoutDelay).until(EC.presence_of_element_located((By.XPATH, "//*[@class='btn btn-undefined btn-primary']")))
        if checkout:
            checkout.click()
            print('Clicked checkout!')
            pass
    except selenium.common.exceptions.TimeoutException:
        print('No checkout detected. Trying view cart.')
        try:
            viewcart = WebDriverWait(driver, timeoutDelay).until(EC.presence_of_element_located((By.XPATH, "//*[@class='btn']")))
            if viewcart:
                viewcart.click()
                print('Clicked view cart')
        finally:
            print('No checkout or cart button detected! Terminating script.')
            exit()

#
#    checkout = WebDriverWait(driver, timeoutDelay).until(EC.presence_of_element_located((By.XPATH, "//*[@class='btn btn-primary btn-wide']")))
#
#    time.sleep(clickDelay)
#
#    if checkout:
#        checkout.click()
#        print('Clicked checkout')
#
#    time.sleep(999999)


def curitem():
    #return str(URLs.index(url) + 1)
    itemname = driver.find_element_by_class_name("product-title")
    return "'" + itemname.text[:25] + "...'"

firstLoop = True

while True:
    for url in URLs:
        if firstLoop:
            firstLoop = False
        else:
            time.sleep(masterDelay)

        driver.get(url)
        productBuy = WebDriverWait(driver, timeoutDelay).until(EC.presence_of_element_located((By.ID, "ProductBuy")))

        if productBuy.text == "ADD TO CART":
            print("Item " + curitem() + " in stock!")
            beepNum = 0
            while beepNum < 4:
                winsound.Beep(370 + beepNum * 200, 80)
                beepNum += 1
                if beepNum == 4:
                    continue
            buyitem()

        elif str(productBuy.text) == ("OUT OF STOCK" or "SOLD OUT"):
            print("Item " + curitem() + " out of stock (" + "Button Disabled" + ")")

        elif str(productBuy.text) == "AUTO NOTIFY":
            print("Item " + curitem() + " out of stock (" + "Auto Notify" + ")")

        elif str(productBuy.text) == "":
            print("Item " + curitem() + " out of stock (" + "Button Hidden" + ")")

            continue
        else:
            print("Script error on item " + curitem() + " Printing 'productBuy' var value below:")
            print(productBuy.text)
            print("'productBuy' does not match known values. Terminating script.")
            driver.quit()

    time.sleep(masterDelay)
    os.system('cls||clear')  # Clear console (platform agnostic)
