"""

~~AK Niloy~~
~16.11.2021~


Scrap Profile details~~~
                                        A. Profile Name, Company Name, About
                                        B. Experience
                                        C. Education
                                        D. Licenses & certifications
                                        E. Skills & endorsements




"""

import requests, time, random
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import xlsxwriter
import re




browser = webdriver.Chrome('C:/Users/niloy/Desktop/scrapper/Linkedin scarpper demo/chromedriver.exe') #give the full path of chromedriver.exe file


browser.get('https://www.linkedin.com/login')
file = open('C:/Users/niloy/Desktop/scrapper/Linkedin scarpper demo/config.txt') # put your linkedin email and pass in here
lines = file.readlines()
username = lines[0]
password = lines[1]


elementID = browser.find_element_by_id('username')
elementID.send_keys(username)

elementID = browser.find_element_by_id('password')
elementID.send_keys(password)

elementID.submit()




browser.get('https://www.linkedin.com//in/nahar-nazmun/') 
# paste the link of the profile u wanna scrape

start = time.time()
  
# will be used in the while loop
initialScroll = 0
finalScroll = 1000
  
while True:
    browser.execute_script(f"window.scrollTo({initialScroll},{finalScroll})")
    # this command scrolls the window starting from
    # the pixel value stored in the initialScroll 
    # variable to the pixel value stored at the
    # finalScroll variable
    initialScroll = finalScroll
    finalScroll += 1000
  
    # we will stop the script for 3 seconds so that 
    # the data can load
    time.sleep(3)
    # You can change it as per your needs and internet speed
  
    end = time.time()
  
    # We will scroll for 20 seconds.
    # You can change it as per your needs and internet speed
    if round(end - start) > 20:
        break


src = browser.page_source

# Now using beautiful soup
src = browser.page_source

# Now using beautiful soup
soup = BeautifulSoup(src, 'lxml')

name_soup = soup.find('h1')
Profile_name = name_soup.text.strip()

job_soup = soup.find('div',{'class':'text-body-medium break-words'})
if job_soup != None:
    job_name = job_soup.text.strip()
else:
    job_name = 'None'



location_soup = soup.find('span',{'class':'text-body-small inline t-black--light break-words'})
if location_soup != None:
    location = location_soup.text.strip()
else:
    location = 'None'




about_soup = soup.find('div', {'class':'inline-show-more-text inline-show-more-text--is-collapsed mt4 t-14'}) 

if about_soup != None:
    about = about_soup.text.strip()
else:
    about = 'None'

Designation = []
companyname = []
all_skill = []

All_education = []


experience_soup = soup.find('section',{'id': 'experience-section'})


certificate_soup = soup.find('section',{'id': 'certifications-section'})

education_soup = soup.find('section',{'id': 'education-section'})

jobname_soup = experience_soup.find_all('h3', {'class': 't-16 t-black t-bold'}) 

educations = education_soup.find_all('h3', {'class': 'pv-entity__school-name t-16 t-black t-bold'})

companyname_soup = experience_soup.find_all('p', {'class': 'pv-entity__secondary-title t-14 t-black t-normal'}) 

skill_soup = soup.find('section', {'class': 'pv-profile-section pv-skill-categories-section artdeco-card mt4 p5 ember-view'}) 
                                    
if skill_soup != None:
    skills = skill_soup.find_all('span', {'class': 'pv-skill-category-entity__name-text t-16 t-black t-bold'})
if skills != None:
    for profile in skills:
        all_skill.append(profile.get_text().strip())





#print(certificate_soup)

all_certificates = []

#print(certificate_soup)
if certificate_soup != None:
    certificates = certificate_soup.find_all('h3')

for profile in certificates:
    all_certificates.append(profile.get_text().strip())
else:
    certificates = 'None'







for profile in jobname_soup:
    Designation.append(profile.get_text().strip())

for profile in companyname_soup:
    companyname.append(profile.get_text().strip())

for profile in educations:
    All_education.append(profile.get_text().strip())





table =[]
table_dct = (
{'Profile_Name': Profile_name,
'Current_Job': job_name,
'Location': location,
'About': about,
'Experiences': Designation,
'Cpmpanies_Workd': companyname,
'Educational_background': All_education,
'Skills': all_skill,
'Certificates': all_certificates}
)
table.append(table_dct)
df= pd.DataFrame(table)

writer = pd.ExcelWriter('Person_info.xlsx', engine='xlsxwriter')

df.to_excel(writer, sheet_name='Sheet4', index=False)

writer.save()

browser.quit()