import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import json


def get_puzzle():
    print("Getting the puzzle...")
    d = datetime.date.today().strftime(r"%Y/%m/%d")
    url = r"https://www.nytimes.com/crosswords/game/mini/" + d
    driver = webdriver.Chrome(r'C:\Users\shkha\Downloads\chromedriver_win32\chromedriver.exe')
    driver.implicitly_wait(30)
    print("Opening the website...")
    driver.get(url)
    
    json_file = {}
    
    reveal_puzzle(driver)
    extract_data(driver, json_file)
    
    print("Closing the browser...")
    driver.quit()
    
def reveal_puzzle(driver):
    try:
        driver.find_element_by_xpath('//*[@id="root"]/div/div/div[4]/div/main/div[2]/div/div[2]/div[2]/article/div[2]').click()
    except NoSuchElementException:
        pass
    
    print("Revealing the puzzle...")
    driver.find_element_by_xpath('//*[@id="root"]/div/div/div[4]/div/main/div[2]/div/div/ul/div[1]/li[2]/button').click()
    driver.find_element_by_xpath('//*[@id="root"]/div/div/div[4]/div/main/div[2]/div/div/ul/div[1]/li[2]/ul/li[3]/a').click()
    driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div[2]/article/div[2]/button[2]').click()
    driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div[2]/span').click()


def extract_data(driver, json_file):        
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    # Extracting clues
    print("Extracting clues...")
    clue_hint_container = soup.findAll(class_="Clue-text--3lZl7")
    clue_key_container = soup.findAll(class_="Clue-label--2IdMY")
    clues = {'across':[], 'down':[]}
    temp = []
    for i in range(len(clue_hint_container)):
        clue = {'key':int(clue_key_container[i].text), 'hint':clue_hint_container[i].text}
        temp.append(clue)
    clues['across'] = temp[:5]
    clues['down'] = temp[5:]
    
    json_file['clues'] = clues
    
    # Extracting cells
    print("Extracting cells...")
    cell_container = soup.find('g', attrs={'data-group':'cells'}).findAll('g')
    cells = []
    for item in cell_container:
        texts = item.findAll('text')
        if len(texts) == 1:
            letter = texts[0].text
        elif len(texts) == 2:
            letter = texts[1].text
        cell = {'id':int(item.find('rect')['id'][8:]), 'key': None if len(texts) <= 1 else (int(texts[0].text)), 'letter': None if len(texts) == 0 else letter}
        cells.append(cell)
        
    json_file['cells'] = cells
    
    path = r"C:\Users\shkha\OneDrive\Desktop\Courses\Spring 18-19\CS 461\Project\Final\code\Data"
    file_name = path + "\\" + datetime.date.today().strftime("%Y-%m-%d") + ".json"
    
    print("Storing the data as a json file...")
    with open(file_name, 'w') as outfile:
        json.dump(json_file, outfile)
        

        
