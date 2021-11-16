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
install the following libraries

requests
bs4
BeautifulSoup4
selenium
pandas
xlsxwriter

I've attached the chromium driver but it may not work depending the version of chromium browser installed in your pc. 
If the versions doesnt match, please download the matching version driver from the following link:
https://chromedriver.chromium.org/downloads

dont forget to edit the config file and enter your linkedn and pass before running the code.



