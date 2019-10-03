from datetime import datetime, date
from time import sleep
import re
import subprocess
from selenium import webdriver

import pyautogui
from tkinter import messagebox

from secrets import PASSWORD, CLI_PASSWORD, LOJASENHA

#print("manually update")
#exit(0)

year = str(date.today().year)
timestamp = datetime.strftime(datetime.now(), "tab__%Y_%m_%d__%H_%M_%S")
DEST = 'C:\\Users\\Heitor\\Desktop\\tabelas_site\\'
DL_DEST = 'C:\\Users\\Heitor\\Desktop\\tabelas_site\\download\\'

def download_tabelas():
    print("Begin saving tabelas")

    # Close all virtual lojas
    subprocess.run(r'C:\Users\Heitor\Desktop\code\tabelas-autoupload\winactivateloja.exe')
    sleep(2)
    pyautogui.click(799, 12)

    sleep(4)
    subprocess.run(r'C:\Users\Heitor\Desktop\code\tabelas-autoupload\winactivateloja.exe')
    sleep(2)
    pyautogui.click(799, 12)
    sleep(4)
    
    # Pontual
    subprocess.Popen(r'\\amazonia\Work\estoque\Pontual.exe')
    sleep(6)
    pyautogui.click(403, 347)
    pyautogui.typewrite(LOJASENHA + "\n")

    sleep(3)

    pyautogui.PAUSE = 0.25
    pyautogui.FAILSAFE = True

    pyautogui.moveTo(106, 30, duration=0.1)

    pyautogui.click()
    pyautogui.moveTo(130, 160, duration=0.25)
    pyautogui.moveTo(311, 151, duration=0.25)
    pyautogui.moveTo(327, 238, duration=0.1)
    pyautogui.click()
    sleep(1)
    pyautogui.click(716, 360)


    sleep(14)

    pyautogui.click(90, 49)
    sleep(5)

    pyautogui.typewrite(DEST + timestamp + ".xls\n")
    sleep(2)

    pyautogui.click(1273, 2)
    # sleep(1)
    # pyautogui.click(799, 12)

    sleep(3)

    # Uniao
    subprocess.Popen(r'\\amazonia\Work\UNIAO\pontual2008.exe')
    sleep(6)
    pyautogui.click(403, 347)
    pyautogui.typewrite(LOJASENHA + "\n")

    sleep(3)

    pyautogui.PAUSE = 0.25
    pyautogui.FAILSAFE = True

    pyautogui.moveTo(106, 30, duration=0.1)

    pyautogui.click()
    pyautogui.moveTo(130, 160, duration=0.25)
    pyautogui.moveTo(311, 151, duration=0.25)
    pyautogui.moveTo(327, 238, duration=0.1)
    pyautogui.click()
    sleep(1)
    pyautogui.click(716, 360)


    sleep(14)

    pyautogui.click(90, 49)
    sleep(5)

    pyautogui.typewrite(DEST + "uni" + timestamp + ".xls\n")
    sleep(2)

    pyautogui.click(1273, 2)

    return [DEST + timestamp + ".xls", DEST + "uni" + timestamp + ".xls"]
    

def post_tabelas(filenames):
    f1, f2 = filenames
    
    # selenium
    profile = webdriver.FirefoxProfile()
    profile.set_preference('network.http.phishy-userpass-length', 255)

    browser = webdriver.Firefox(firefox_profile=profile)
    browser.get("https://pontual:" + PASSWORD + "@pontualimportbrinde1.websiteseguro.com/site-admin/crud/tabela_upload.php")
    browser.find_element_by_id("fileInput1").send_keys(f1)
    browser.find_element_by_id("fileInput2").send_keys(f2)
    browser.find_element_by_id("continue").click()
    
    # messagebox.showinfo(dtitle, dmsg)

    
fnames = download_tabelas()
sleep(1)
post_tabelas(fnames)
