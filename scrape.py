from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd
import requests
info={}

 def scrape_headline(): 
    news_url = "https://mars.nasa.gov/news/"

    response=requests.get(news_url)
    soup = BeautifulSoup(response.text, "lxml")

    results=soup.find_all("div", class_="slide")

    headline=results[0].find("div",class_="content_title")
    headline_text=headline.find("a").text
    headline_text=headline_text.strip()

    preview=results[0].find("div", class_="rollover_description_inner").text
    preview=preview.strip()

    info.update({"headline":headline_text,"preview":preview})

 def scrape_featured_image():   
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=True)

    jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(jpl_url)
    browser.click_link_by_partial_text("FULL IMAGE")
    browser.click_link_by_partial_text("more info")

    url_string="https://www.jpl.nasa.gov/"
    html=browser.html
    soup=BeautifulSoup(html, "html.parser")
    image=soup.find("figure", class_="lede")
    image=image.find("a")["href"]
    featured_image_url=url_string+image

    info.update({"featured_image":featured_image_url})


    browser.quit()

def scrape_table():
    facts_url="https://space-facts.com/mars/"
    mars_table=pd.read_html(facts_url)[0]
    mars_table_html=mars_table.to_html()

    info.update({"Mars Info Table":mars_table_html})


def scrape_images():
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=True)

    usgs_url="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(usgs_url)
    url_string="https://astrogeology.usgs.gov/"
    html=browser.html
    soup=BeautifulSoup(html,"html.parser")

    image_links=[]
    for result in soup.find_all("div",class_="item"):
        link=result.find("a", class_="itemLink product-item")["href"]
        link=url_string+link
        browser.visit(link)
        html=browser.html
        soup=BeautifulSoup(html,"html.parser")
        image=soup.find("img", class_="wide-image")["src"]
        image_source=url_string+image
        title=soup.find("h2",class_="title").text
        image_links.append({"title":title,"link":image_source})

    info.update({"images":image_links})

    browser.quit()

def scrape():
    scrape_headline()
    scrape_featured_image()
    scrape_table
    scrape_images()
    return info


