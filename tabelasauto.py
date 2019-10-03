import shutil
from datetime import datetime, date
from time import sleep
import re
import subprocess
import requests
import filecmp
from requests.auth import HTTPBasicAuth
import urllib

import pyautogui
from tkinter import messagebox

from secrets import PASSWORD, CLI_PASSWORD, LOJASENHA

from mergetab import parse, genhtml

print("Run python db_auto.py")
exit(1)

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

    pyautogui.click(136, 49)
    sleep(5)

    pyautogui.typewrite(DEST + timestamp + ".html\n")
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

    pyautogui.click(136, 49)
    sleep(5)

    pyautogui.typewrite(DEST + "uni" + timestamp + ".html\n")
    sleep(2)

    pyautogui.click(1273, 2)
    # sleep(1)
    # pyautogui.click(799, 12)

    # copy ttf files
    shutil.copy("c:/Users/Heitor/Desktop/code/mergetabelas/anoto.ttf", "c:/Users/Heitor/Desktop/tabelas_site/anoto.ttf")
    shutil.copy("c:/Users/Heitor/Desktop/code/mergetabelas/anoto.ttf", "c:/Users/Heitor/Desktop/tabelas_site/anotobold.ttf")

    # merge htmls
    cods = parse(DEST + timestamp + ".html", DEST + "uni" + timestamp + ".html")
    return genhtml(cods)
    

def post_tabelas(fname):
    session = requests.Session()
    session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'})

    def req_dl(url, local):
        r = session.get(url)
        with open(local, "wb") as myfile:
            myfile.write(r.content)
            
    try:
        session.post("https://pontualimportbrinde1.websiteseguro.com/site-admin/crud/tabela_upload_exec.php", auth=HTTPBasicAuth("pontual", PASSWORD), files={
            'arquivo_htm': open(DEST + fname + ".html", 'rb'),
            'arquivo_pdf': open(DEST + fname + ".pdf", 'rb')})
        
        dtitle, dmsg = "OK", "Upload feito com sucesso"
    except Exception as e:
        print("Algo deu errado no upload das tabelas.")
        print(e)
        messagebox.showinfo("Erro", "Erro na tentativa de upload")
        exit(1)

    messagebox.showinfo(dtitle, dmsg)
    
    sleep(1)
    
    # Download latest files
    print("Trying to download files...")

    try:
        baixar_r = session.post("http://pontualimportbrindes.com.br/tabela_baixar.php", data={ "senha": CLI_PASSWORD })
        
        baixar_body = str(baixar_r.content)
    except:
        messagebox.showinfo("Erro", "Nao foi possivel baixar tabelas novas")
        exit(1)
        
    file_pat = r'estoque_[0-9a-f]{8}'

    tabela_s = re.search(file_pat, baixar_body)
    tabela_name = tabela_s.group(0)

    req_dl("http://pontualimportbrindes.com.br/tabelas_htm/" + tabela_name + ".html", DL_DEST + tabela_name + ".html")
    req_dl("http://pontualimportbrindes.com.br/tabelas/" + tabela_name + ".pdf", DL_DEST + tabela_name + ".pdf")

    

    # compare files

    files_ok = (filecmp.cmp(DEST + fname + ".html", DL_DEST + tabela_name + ".html") and
                filecmp.cmp(DEST + fname + ".pdf", DL_DEST + tabela_name + ".pdf"))

    if files_ok:
        dtitle, dmsg = "OK", "Arquivos verificados com sucesso"
    else:
        dtitle, dmsg = "Erro", "Erro: Tabelas baixadas são diferentes daquelas feitas no upload"
        
    messagebox.showinfo(dtitle, dmsg)

    
fname = download_tabelas()
sleep(1)
post_tabelas(fname)

input("Fim. Pressione Enter para fechar.")
