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
num = 5
driver = webdriver.Chrome(executable_path=r'C:/Program Files/chromedriver.exe', options=options)
url = f'http://srv1.eulc.edu.eg/eulc_v5/libraries/start.aspx?fn=ApplySearch&SearchId=14544703&frameName=&PageNo=1&PageSize={num}'
driver.get(url)
src = driver.page_source
#driver.quit()
soup = bs(src, "html.parser")

years = []
titles_en = []
dewi_nums = []

titles_ar = []
abstracts_en = []
abstracts_ar = []
belograpg_nums = []
required_dewis = [574, 575, 576, 577, 578, 579, 580, 573, 572, 571, 616, 617, 630, 632]

count = 0

tables = soup.find_all("table", {"class":"defaultTableStyle"})
details_btn = driver.find_elements(By.XPATH, '//input[@value="تفاصيل"]')
for btn in details_btn:
    driver.execute_script("arguments[0].click();", btn)
    time.sleep(5)
    driver.get(url)
    src = driver.page_source
    #driver.quit()
    soup = bs(src, "html.parser")
    
    rows = []
    table = soup.find("table", {"class":"centercontent_text_grey_9pt"})
    for row in table.find_all('tr'):
        rows.append([el.text.strip() for el in row.find_all('td')])
    dewi = int(float(rows[0][-1]))
    year = rows[5][-1]
    title_en = rows[2][-1]
    title_ar  = rows[4][-1]
    abs_Ar = rows[9][-1]
    abs_En = rows[10][-1]
    
    #if dewi in required_dewis:
    dewi_nums.append(dewi)
    years.append(year.replace('.', '').strip())
    titles_en.append(title_en.replace('/', '').strip())
    titles_ar.append(title_ar.strip())
    abstracts_ar.append(abs_Ar.strip())
    abstracts_en.append(abs_En.strip())
    print(count)
driver.quit()
file_list = [dewi_nums, years, titles_en, titles_ar, abstracts_ar, abstracts_en]
print(file_list)
exported = zip_longest(*file_list)
with open("C:/Users/Menna/Desktop/Omar Task/NLP_data.csv", "w", newline='', encoding=('UTF-8')) as file:
    wr = csv.writer(file)
    wr.writerow(["Dewi Num", "Year", "English Title", "Arabic Title", "Abstract AR", "Abstract EN"])
    wr.writerows(exported)
print(exported)