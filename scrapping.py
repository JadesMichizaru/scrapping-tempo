from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import pandas as pd
import time

opsi = webdriver.ChromeOptions()
opsi.add_argument('--headless')
servis = Service('chromedriver.exe')
driver = webdriver.Chrome(service=servis, options=opsi)

tempo_link = "https://www.tempo.co/tag/flashdisk"

driver.get(tempo_link)
driver.set_window_size(1920, 1080)

rentang = 500
for i in range(1, 8): 
    akhir = rentang * i
    perintah = "window.scrollTo(0, " + str(akhir) + ");"
    driver.execute_script(perintah)
    print("loading ke-"+str(i))
    time.sleep(1)

time.sleep(5)

driver.save_screenshot("home.png")
content = driver.page_source
driver.quit()

data = BeautifulSoup(content, 'html.parser')
# print(data.encode("utf-8"))

list_nama, list_gambar, list_link = [], [], []

i = 1
base_url = "https://www.tempo.co"
for area in data.find_all('div', class_="flex flex-col divide-y divide-neutral-500"):
    print('proses ke- '+str(i))
    nama = area.find('p', class_="text-neutral-1200 text-base line-clamp-4").get_text()
    gambar = area.find('img', class_="shrink-0 object-cover w-[80px] h-[80px]")['src']
    link = base_url + area.find('a')['href']
    list_nama.append(nama)
    list_gambar.append(gambar)
    list_link.append(link)
    i+=1
    print("====================================")
    
    df = pd.DataFrame({
        'Nama': list_nama,
        'Gambar': list_gambar,
        'Link': list_link
    })
    
df.to_csv("tempo.csv", index=False, encoding="utf-8-sig")
