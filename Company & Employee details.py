"""
                                                    ~~AK Niloy~~
                                                    ~16.11.2021~

This is a python script to scrape linkedin profiles of both companies & their employees.
Suppose u wanna search for a company name vintage. There are several companies named after that. Just paste the search link of 
the linkedin search result. it will find all the companies and scrap their info.


Following information will be extracted or web scraped from each company:

                                    A. Full name of the company
                                    B. Information on the “About” tab of the page
                                    
Following information should be extracted or web scraped from each profile of employee of each
company if publicly available:

                                        A. Profile Name, Company Name, About
                                        B. Experience
                                        C. Education
                                        D. Licenses & certifications
                                        E. Skills & endorsements







"""
from typing import List
import selenium
from selenium import webdriver
from selenium.webdriver.common import keys
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

import requests, time, random
from bs4 import BeautifulSoup
import pandas as pd
import xlsxwriter
import re


def find_duplicates(sequence):
  first_seen = set()
  first_seen_add = first_seen.add  
  duplicates = set(i for i in sequence if i in first_seen or first_seen_add(i) )
  # turn the set into a list (as requested)
  return duplicates 



browser = webdriver.Chrome('C:/Users/niloy/Desktop/scrapper/Linkedin scarpper demo/chromedriver.exe') 
#give the full path of chromedriver.exe file


browser.get('https://www.linkedin.com/login')
file = open('C:/Users/niloy/Desktop/scrapper/Linkedin scarpper demo/config.txt') 
# put your linkedin email and pass in here
lines = file.readlines()
username = lines[0]
password = lines[1]


elementID = browser.find_element_by_id('username')
elementID.send_keys(username)

elementID = browser.find_element_by_id('password')
elementID.send_keys(password)

elementID.submit()




browser.get('https://www.linkedin.com/search/results/companies/?keywords=bondstein&origin=SWITCH_SEARCH_VERTICAL&sid=XX)') 
# paste the search link for data scrap. here comppanies are searched
url = 'https://www.linkedin.com/search/results/companies/?keywords=sigmind&origin=SPELL_CHECK_REPLACE&sid=jRk&spellCorrectionEnabled=false'

time.sleep(10)

src = browser.page_source
soup = BeautifulSoup(src, 'lxml')

company_soup = soup.find_all(class_= 'app-aware-link', href=True)

company_links= []

for link in company_soup:
    company_links.append(link['href'])

True_company_Links = find_duplicates(company_links)
True_company_Links = list(True_company_Links)
print(True_company_Links)

table =[]

for links in True_company_Links:
    browser.get(links+"/about")

    time.sleep(5)

    link_src = browser.page_source
    soup = BeautifulSoup(link_src, 'lxml')
    #clearprint(soup)
    job_soup = soup.find('h1')
    Company_name = job_soup.text.strip()
    about_soup = soup.find('p',{'class': 'break-words white-space-pre-wrap mb5 text-body-small t-black--light'})
    About = about_soup.text.strip()
    info_soup = soup.find_all('dd')
    info = []  
    for name in info_soup:
        res = re.sub('\n\n +', ' ', name.text.strip())
        info.append(res)   
    #print(info)
    
    table_dct = (
        {'Company_name': Company_name,
        'About': About,
        'info': info}
        )
    table.append(table_dct)
    
    browser.back()
    time.sleep(5)
df_company= pd.DataFrame(table)
writer = pd.ExcelWriter('Linkedin scarpper demo/Company_details.xlsx', engine='xlsxwriter')
df_company.to_excel(writer, sheet_name='Sheet3', index=False)
writer.save()

start = time.time()

for links in True_company_Links:
    
    browser.get(links)
    link_src = browser.page_source
    soup = BeautifulSoup(link_src, 'lxml')
    #clearprint(soup)
    job_soup = soup.find('h1')
    Companyy = job_soup.text.strip()

    
    
    browser.get(links+"/people")

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
        time.sleep(5)
        # You can change it as per your needs and internet speed
    
        end = time.time()
  
    # We will scroll for 20 seconds.
        # You can change it as per your needs and internet speed
        if round(end - start) > 40:
            break
    
    start = 0
    link_src = browser.page_source
    pp_soup = BeautifulSoup(link_src, 'lxml')
    #print(pp_soup)
    demo = pp_soup.find('ul', {'class': 'display-flex list-style-none flex-wrap'})
    #print(demo)
    profile_link_soup = demo.find_all('a', {'class' : 'ember-view'},  href = True)
    print(profile_link_soup)
    profile_links= []

    for link in profile_link_soup:
        profile_links.append(link.get('href'))

    profile_links = find_duplicates(profile_links)
    profile_links = list(profile_links)
    print(profile_links)

    time.sleep(5)

    table =[]
    
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
            df_employee= pd.DataFrame(table)

            writer = pd.ExcelWriter('Linkedin scarpper demo/'+ Companyy + '_Employee_info.xlsx', engine='xlsxwriter')

            df_employee.to_excel(writer, sheet_name='Sheet4', index=False)

            writer.save()







browser.quit()