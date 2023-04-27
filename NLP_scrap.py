# importing required modules
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from itertools import zip_longest
import csv
import time

# prepare driver
options = Options()
user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'    
options.add_argument('user-agent={0}'.format(user_agent))
options.add_argument("--headless")

# load the page
num = 1500
driver = webdriver.Chrome(executable_path=r'C:/Program Files/chromedriver.exe', options=options)
url = f'http://srv1.eulc.edu.eg/eulc_v5/libraries/start.aspx?fn=ApplySearch&SearchId=14544703&frameName=&PageNo=1&PageSize={num}'
driver.get(url)
src = driver.page_source
soup = bs(src, "html.parser")

# Lists to collect the data
years = []
titles_en = []
dewi_nums = []
titles_ar = []
abstracts_en = []
abstracts_ar = []

# missed data
belograpg_nums = []

# The dewis we are searching in
required_dewis = [574, 575, 576, 577, 578, 579, 580, 573, 572, 571, 616, 617, 630, 632]

# First click on button to get all required data
details_btn = driver.find_elements(By.XPATH, '//input[@value="تفاصيل"]')
for btn in details_btn:
    driver.execute_script("arguments[0].click();", btn)
time.sleep(5)
src = driver.page_source
soup = bs(src, "html.parser")
driver.quit()

# Now we collect the data
tables = soup.find_all("table", {"class":"centercontent_text_grey_9pt"})
tables = tables[1000:]
try:
    for table in tables:
        rows = []
        for i, row in enumerate(table.find_all('tr')):
            rows.append([el.text.strip() for el in row.find_all('td')])
        try:    
            dewi = int(float(rows[0][-1][:3]))
        except:
            continue
        year = rows[5][-1].replace('.', '')
        title_en = rows[2][-1].replace('/', '')
        title_ar  = rows[4][-1]
        abs_Ar = rows[9][-1]
        abs_En = rows[10][-1]
        
        if dewi in required_dewis:
            dewi_nums.append(dewi)
            years.append(year.strip())
            titles_en.append(title_en.strip())
            titles_ar.append(title_ar.strip())
            abstracts_ar.append(abs_Ar.strip())
            abstracts_en.append(abs_En.strip())
        #print(year, dewi, title_en)
        #print()
except:
    pass

# put data in a CSV file   
file_list = [dewi_nums, years, titles_en, titles_ar, abstracts_ar, abstracts_en]
exported = zip_longest(*file_list)
with open("C:/Users/Menna/Desktop/NLP_data.csv", "w", newline='', encoding=('utf-8')) as file:
    wr = csv.writer(file)
    wr.writerow(["Dewi Num", "Year", "English Title", "Arabic Title", "Abstract AR", "Abstract EN"])
    wr.writerows(exported)
