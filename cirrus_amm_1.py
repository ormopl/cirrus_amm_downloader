from bs4 import BeautifulSoup
import requests
import os
import wget
import sys

revision_check = ""

sr22t_amm_html_g6 = "http://servicecenters.cirrusdesign.com/tech_pubs/SR2X/pdf/amm/SR22+/html/ammtoc.html"
sr22t_amm_html_g5 =  "http://servicecenters.cirrusdesign.com/tech_pubs/SR2X/pdf/amm/SR22/html/ammtoc.html"
sr20_amm_g6 = ""
sr20_amm_g5 = ""

sr22t_base_address_g6 = "http://servicecenters.cirrusdesign.com/tech_pubs/SR2X/pdf/amm/SR22+/"
sr22t_base_address_g5 = "http://servicecenters.cirrusdesign.com/tech_pubs/SR2X/pdf/amm/SR22/"
sr20_base_address_g6 = ""
sr20_base_address_g5 = ""

pdf_address_list = []

folder_name = ""

html = requests.get(sr22t_amm_html_g6)

def bar_progress(current, total, width=80):
  progress_message = "Downloading: %d%% [%d / %d] bytes" % (current / total * 100, current, total)
  sys.stdout.write("\r" + progress_message)
  sys.stdout.flush()

def scrapper(file):
    global soup
    global folder_name
    soup = BeautifulSoup(file.content, 'html.parser')
    content_check = soup.find_all('ul')
    content_revision = soup.find_all("p")
    for rev in content_revision:
        for rev_line in rev.find_all("b"):
            print(rev_line.text)
            folder_name = (rev_line.text).replace("/", "-")
    for line in content_check:
        for id in line.find_all("a"):
            pdf_address_list.append(sr22t_base_address_g6 + id["href"][3:])
            #print(base_address + id["href"][3:])
    print(f"{len(pdf_address_list)} files found!")

def makeFolder():
    if os.path.exists(folder_name) == True:
        print(f"{folder_name} folder exists!")
    else:
        os.mkdir(folder_name)

def downloader(link_list):
    enum = 1

    for link in (link_list):
        wget.download(link, bar=bar_progress, out=folder_name)
        print(f" | File {link} downloaded! Total: [{enum}/{len(pdf_address_list)}] [{round(((enum/len(pdf_address_list))*100), 2)} %]" )
        enum+=1
        print("Downloading Finished!")

#main loop

if html.status_code == 200:
    print("Cirrus Technical Documentation Scrapper v0.1")
    print("Page Available, status code: ", html.status_code)
    scrapper(html)
    makeFolder()
    #downloader(pdf_address_list)
else:
    print("Page is not available, finishing. Status code: ",html.status_code)
    os.exit()
