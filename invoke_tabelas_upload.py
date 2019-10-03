from selenium import webdriver
from time import sleep
from secrets import PASSWORD

profile = webdriver.FirefoxProfile()
profile.set_preference('network.http.phishy-userpass-length', 255)

browser = webdriver.Firefox(firefox_profile=profile)
browser.get("https://pontual:" + PASSWORD + "@pontualimportbrinde1.websiteseguro.com/site-admin/crud/tabela_upload.php")


