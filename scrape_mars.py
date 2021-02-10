from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
import time


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape_info():
    browser = init_browser()
    #First Article
    # Visit Nasa
    url = 'https://mars.nasa.gov/news'
    browser.visit(url)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    #First Article
    title = soup.find_all('div', class_="content_title")[1].text
    text = soup.find_all('div', class_="article_teaser_body")[0].text

    #Image
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)


    html = browser.html
    soup = bs(html, 'html.parser')

    image = soup.find('a', class_="showimg fancybox-thumbs")
    featured_image_url='https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/'+image['href']

    #table
    url = 'https://space-facts.com/mars/'
    facts = pd.read_html(url)[2]
    named_facts = facts.rename(columns={0: 'Name', 1: 'Fact'})
    named_facts = named_facts.set_index('Name')
    html_facts = named_facts.to_html()
    
    #hemispheres
    url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')
    download = soup.find('div', class_="downloads")
    cerb_image = download.find('a')['href']

    url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')
    download = soup.find('div', class_="downloads")
    schiap_image = download.find('a')['href']

    url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')
    download = soup.find('div', class_="downloads")
    syrt_image = download.find('a')['href']

    url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')
    download = soup.find('div', class_="downloads")
    valles_image = download.find('a')['href']

    hemisphere_image_urls = [
    {"title": "Valles Marineris Hemisphere", "img_url": valles_image},
    {"title": "Cerberus Hemisphere", "img_url": cerb_image},
    {"title": "Schiaparelli Hemisphere", "img_url": schiap_image},
    {"title": "Syrtis Major Hemisphere", "img_url": syrt_image},
    ]

    cerb=hemisphere_image_urls[0]['img_url']

    mars_data = {
        "title": title,
        "text": text,
        "featured_image_url": featured_image_url,
        "table": html_facts,
        "cerb": hemisphere_image_urls[0]['img_url'],
        "schiap": hemisphere_image_urls[1]['img_url'],
        "syrt": hemisphere_image_urls[2]['img_url'],
        "valles": hemisphere_image_urls[3]['img_url']
    }    

    # Quite the browser after scraping
    browser.quit()

    # Return results
    return mars_data