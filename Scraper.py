from bs4 import BeautifulSoup as bs  
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd 
import requests as rq

url = 'https://en.wikipedia.org/wiki/List_of_brightest_stars'

service = webdriver.EdgeService(executable_path="C:/Users/jalal/VSCodePrgms/python_files/HW_127/msedgedriver.exe")
browser = webdriver.Edge(service=service)

browser.get(url)

time.sleep(3)

star_data = []
individual_stars_data = []
def scrape_stars_table():
    soup = bs(browser.page_source, "html.parser")
    for table in soup.find_all("table", attrs = {"class", "wikitable sortable sticky-header jquery-tablesorter"}):
        for tbody in table.find_all("tbody"):
            for tr_tag in tbody.find_all("tr"):
                td_tags = tr_tag.find_all("td")
                star_list = []
                for index, td_tag in enumerate(td_tags):
                    if index == 1 or index == 4:
                        star_list.append(td_tag.contents[-1])
                    elif index == 2 or index == 3:
                        if (str(td_tag.contents[0]))[0] != '<':
                            star_list.append(td_tag.contents[0])
                        else:
                            star_list.append(td_tag.contents[0].contents[0])
                    else:
                        star_list.append(td_tag.contents[0])
                if str(td_tags[2].contents[0])[0] != '<':
                    hyperlink = "-"
                    star_list.append(hyperlink)
                else:
                    hyperlink = 'https://en.wikipedia.org/wiki/List_of_brightest_stars' + td_tags[2].find_all("a", href = True)[0]["href"]
                    star_list.append(hyperlink)
                    print(hyperlink)
                star_data.append(star_list)
                print(star_list)
                print(len(star_list))

def scrape_individual_stars(hyperlink):
    try:
        new_page = rq.get(hyperlink)
        new_soup = bs(new_page.content, "html.parser")
        individual_star_list = []
        name = 0
        mass = 0
        radius = 0
        absolute_mag = 0
        apparent_mag = 0
        temperature = 0
        age = 0
        name = new_soup.find("div", attrs = {"class" : "mw-body-content"}).find("table").find("caption").contents[0]
        for tr_tag in new_soup.find("div", attrs = {"class" : "mw-body-content"}).find("table").find("tbody").find_all("tr"):
            if "Mass</a>" in str(tr_tag.contents[0]) and mass == 0:
                if "nowrap" in str(tr_tag.contents[1]):
                    factor1 = tr_tag.contents[1].find("span", attrs = {"class" : "nowrap"}).contents[1]
                    if 'Solar mass' in str(tr_tag.contents[1]):
                        mass = eval(factor1) * 1.989*(10**30)
                    elif '</span>10' in str(tr_tag.contents[1]):
                        exp = int(tr_tag.contents[1].find("span", attrs = {"class" : "nowrap"}).contents[4].contents[0])
                        mass = eval(factor1)*(10**exp)
                else:
                    factor1 = tr_tag.contents[1].contents[0]
                    if 'Solar mass' in str(tr_tag.contents[1]):
                        mass = eval(factor1) * 1.989*(10**30)
                    elif '</span>10' in str(tr_tag.contents[1]):
                        exp = int(tr_tag.contents[1].find("span", attrs = {"class" : "nowrap"}).contents[4].contents[0])
                        mass = eval(factor1)*(10**exp)
                print(mass)
            
            elif "Radius</a>" in str(tr_tag.contents[0]) and radius == 0:
                if "nowrap" in str(tr_tag.contents[1]):
                    factor1 = tr_tag.contents[1].find("span", attrs = {"class" : "nowrap"}).contents[1]
                    if 'Solar radius' in str(tr_tag.contents[1]):
                        radius = eval(factor1) * 696340
                    elif '</span>10' in str(tr_tag.contents[1]):
                        exp = int(tr_tag.contents[1].find("span", attrs = {"class" : "nowrap"}).contents[4].contents[0])
                        radius = eval(factor1)*(10**exp)
                else:
                    factor1 = tr_tag.contents[1].contents[0]
                    if 'Solar radius' in str(tr_tag.contents[1]):
                        radius = eval(factor1) * 696340
                    elif '</span>10' in str(tr_tag.contents[1]):
                        exp = int(tr_tag.contents[1].find("span", attrs = {"class" : "nowrap"}).contents[4].contents[0])
                        radius = eval(factor1)*(10**exp)
                print(radius)

            elif "Temperature</a>" in str(tr_tag.contents[0]) and temperature == 0:
                if "nowrap" in str(tr_tag.contents[1]):
                    temperature = tr_tag.contents[1].find("span", attrs = {"class" : "nowrap"}).contents[1]
                else:
                    temperature = tr_tag.contents[1].contents[0]
                print(temperature)

            elif "Age</a>" in str(tr_tag.contents[0]) and age == 0:
                if "nowrap" in str(tr_tag.contents[1]):
                    factor1 = tr_tag.contents[1].find("span", attrs = {"class" : "nowrap"}).contents[1]
                    if 'Myr' in str(tr_tag.contents[1]):
                        age = eval(factor1) * 1000000
                    elif 'Gyr' in str(tr_tag.contents[1]):                
                        age = eval(factor1) * 1000000000
                else:
                    factor1 = tr_tag.contents[1].contents[0]
                    if 'Myr' in str(tr_tag.contents[1]):
                        age = eval(factor1) * 1000000
                    elif 'Gyr' in str(tr_tag.contents[1]):
                        age = eval(factor1) * 1000000000
                print(age)
            
            elif 'title="Absolute magnitude"' in str(tr_tag.contents[0]) and absolute_mag == 0:
                if "nowrap" in str(tr_tag.contents[1]):
                    absolute_mag = tr_tag.contents[1].find("span", attrs = {"class" : "nowrap"}).contents[1]
                else:
                    absolute_mag = tr_tag.contents[1].contents[0]
                print(absolute_mag)
            
            elif 'title="Apparent magnitude"' in str(tr_tag.contents[0]) and apparent_mag == 0:
                if "nowrap" in str(tr_tag.contents[1]):
                    apparent_mag = tr_tag.contents[1].find("span", attrs = {"class" : "nowrap"}).contents[1]
                else:
                    apparent_mag = tr_tag.contents[1].contents[0]
                print(apparent_mag)
        
        individual_star_list.append(name)
        individual_star_list.append(mass)
        individual_star_list.append(radius)
        individual_star_list.append(absolute_mag)
        individual_star_list.append(apparent_mag)
        individual_star_list.append(temperature)
        individual_star_list.append(age)
        individual_stars_data.append(individual_star_list)
        print(individual_star_list)

    except:
        time.sleep(1)
        scrape_individual_stars


scrape_stars_table()
#scrape_individual_stars("https://en.wikipedia.org/wiki/Aldebaran")

for starlist in star_data:
    if len(starlist) > 6:
        scrape_individual_stars(starlist[6])
    else:
        individual_stars_data.append(['-','-','-','-','-','-'])

headers_for_main_table = ["Rank", "Visual Magnitutde", "Name", "Bayer Designation", "Distance", "Spectral Type", "Hyperlink"]
headers_for_individual_star = ["Name", "Mass", "Radius", "Absolute Magnitude", "Apparent Magnitude", "Temperature", "Age"]

main_list_stars_sheet = pd.DataFrame(star_data, columns = headers_for_main_table)
individual_stars_sheet = pd.DataFrame(individual_stars_data, columns = headers_for_individual_star)

main_list_stars_sheet.to_csv("StarData1.csv", index = True, index_label = "id")
individual_stars_sheet.to_csv("IndividualStarData.csv", index = True, index_label = "id")