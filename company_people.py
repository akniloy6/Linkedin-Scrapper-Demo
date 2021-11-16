#!/usr/bin/env python
# coding: utf-8

## Ak Niloy



import requests, time, random
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import xlsxwriter
import re




browser = webdriver.Chrome('C:/Users/niloy/Desktop/scrapper/Linkedin scarpper demo/chromedriver.exe') #give the full path of chromedriver.exe file


browser.get('https://www.linkedin.com/login')
file = open('config.txt') # put your linkedin email and pass in here
lines = file.readlines()
username = lines[0]
password = lines[1]


elementID = browser.find_element_by_id('username')
elementID.send_keys(username)

elementID = browser.find_element_by_id('password')
elementID.send_keys(password)

elementID.submit()

def find_duplicates(sequence):
  first_seen = set()
  first_seen_add = first_seen.add  
  duplicates = set(i for i in sequence if i in first_seen or first_seen_add(i) )
  # turn the set into a list (as requested)
  return duplicates 



browser.get('https://www.linkedin.com/company/bondstein/people/') # paste the search link for data scrap. here jobs for robotics engineer was searched


time.sleep(10)


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
soup = BeautifulSoup(src, 'lxml')

job_soup = soup.find('h1')



Company_name = job_soup.text.strip()

#people_soup = soup.find('ul',{'class': 'display-flex list-style-none flex-wrap'})

demo = soup.find('ul', {'class': 'display-flex list-style-none flex-wrap'})
#print(demo)
profile_link_soup = demo.find_all('a', {'class' : 'ember-view'},  href = True)
#print(profile_link_soup)
profile_links= []

for link in profile_link_soup:
    profile_links.append(link.get('href'))

profile_links = find_duplicates(profile_links)
profile_links = list(profile_links)

start_2 = time.time()


print(profile_links)

for x in profile_links:
    
    
    url = 'https://www.linkedin.com'+ x
    #url = pl.encode('ascii', 'ignore').decode('unicode_escape')
    print(url)
    browser.get(url)

    time.sleep(5)

    start_2 = time.time()

    #start_2 = time.time()

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
    
        end_2 = time.time()
    
        # We will scroll for 20 seconds.
        # You can change it as per your needs and internet speed
        if round(end_2 - start_2) > 20:
            break

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

    writer = pd.ExcelWriter('Linkedin scarpper demo/'+ "Bondstein" + '_Employee_info.xlsx', engine='xlsxwriter')

    df.to_excel(writer, sheet_name='Sheet4', index=False)

    writer.save()


browser.quit()




