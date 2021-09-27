from bs4 import BeautifulSoup
import requests
import os
import wget
import sys
from PyPDF2 import PdfFileMerger


revision_check = ""

sr22t_amm_html_g6 = "http://servicecenters.cirrusdesign.com/tech_pubs/SR2X/pdf/amm/SR22+/html/ammtoc.html"
sr22t_amm_html_g5 = "http://servicecenters.cirrusdesign.com/tech_pubs/SR2X/pdf/amm/SR22/html/ammtoc.html"
sr20_amm_g6 = ""
sr20_amm_g5 = ""

sr22t_base_address_g6 = "http://servicecenters.cirrusdesign.com/tech_pubs/SR2X/pdf/amm/SR22+/"
sr22t_base_address_g5 = "http://servicecenters.cirrusdesign.com/tech_pubs/SR2X/pdf/amm/SR22/"
sr20_base_address_g6 = ""
sr20_base_address_g5 = ""

pdf_address_list = []

html = requests.get(sr22t_amm_html_g6)


def bar_progress(current, total, width=80):
  progress_message = "Downloading: %d%% [%d / %d] bytes" % (current / total * 100, current, total)
  sys.stdout.write("\r" + progress_message)
  sys.stdout.flush()

def scrapper(file):
    global rev_line
    global soup
    soup = BeautifulSoup(file.content, 'html.parser')
    content_check = soup.find_all('ul')
    content_revision = soup.find_all("p")
    for rev in content_revision:
        for rev_line in rev.find_all("b"):
            rev_line = rev_line.text
            print(f"Current revision: {rev_line}")
    for line in content_check:
        for id in line.find_all("a"):
            pdf_address_list.append(sr22t_base_address_g6 + id["href"][3:])
            #print(base_address + id["href"][3:])
    #print(content_check)
    print(f"{len(pdf_address_list)} files found!")


def path_creator(path):
    global path_global
    path = path.replace("/", "-")
    path_global = path
    if os.path.exists(path) is True:
        print(f"Folder {path} exists!")
    else:
        os.mkdir(path)
        print(f"Folder {path} created!")


def downloader(link_list, merger_path):
    enum = 1
    for file in os.listdir(merger_path):
        if os.path.exists(f"{path_global}/{file}") == True:
            os.remove(f"{path_global}/{file}")
            print(f"File {file} duplicated, removing")
        else:
            print(file, path_global)
            for link in link_list:
                wget.download(link, bar=bar_progress, out=path_global)
                print(f" | File {link} downloaded! Total: [{enum}/{len(pdf_address_list)}] [{round(((enum / len(pdf_address_list)) * 100), 2)} %]")
                enum += 1
    print("Downloading Finished!")

def merger(merger_path):
    merger_PDF = PdfFileMerger()



#main loop
if html.status_code == 200:
    print("Cirrus Technical Documentation Scrapper v0.1")
    print("Page Available, status code: ", html.status_code)
    scrapper(html)
    path_creator(rev_line)
    downloader(pdf_address_list, path_global)
    merger(path_global)
else:
    print("Page is not available, finishing. Status code: ", html.status_code)
    os.exit()
