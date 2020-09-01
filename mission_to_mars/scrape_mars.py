from splinter import Browser
from bs4 import BeautifulSoup
import time
import pandas as pd

def scrape():
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    title, p = scrape_news(browser)
    return {
        "news_title": title,
        "news_paragraph": p,
        "featured_image": scrape_feat_img(browser),
        "html_table": scrape_mars_facts(),
        "hemisphere_images": scrape_hemisphers(browser)
    }

def scrape_news(browser):
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    time.sleep(3)
    news = soup.find_all('div', class_ ='content_title')
    news_title = news[1].find('a', target = "_self").text

    news_p = soup.find('div', class_='article_teaser_body').text
    return news_title, news_p

def scrape_feat_img(browser):
    next_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(next_url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    start = soup.find('li', class_='slide')
    fancy = start.find('a', class_='fancybox')
    fancy_link = fancy['data-fancybox-href']

    featured_image_url = f'https://www.jpl.nasa.gov{fancy_link}'

    return featured_image_url

def scrape_mars_facts():
    third_url = 'https://space-facts.com/mars/'
    tables = pd.read_html(third_url)
   
    html_table = tables[0]
    html_table.columns = ["Mars Facts", ""]
    html_table.set_index('Mars Facts', inplace=True)
    html_table = html_table.to_html()
   

    return html_table

def scrape_hemisphers(browser):
    fourth_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(fourth_url)
    astro_url = 'https://astrogeology.usgs.gov'
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    #cerberus
    cerberus_u = soup.find_all('a', class_='itemLink product-item')
    cerberus_ur = cerberus_u[1]['href']
    shia_ur = cerberus_u[2]['href']
    syrtis_ur = cerberus_u[4]['href']
    valles_ur = cerberus_u[6]['href']
    titles = soup.find_all('h3')
    c_title= titles[0].text
    sh_title = titles[1].text
    sy_title = titles[2].text
    v_title = titles[3].text

    browser.visit(f'https://astrogeology.usgs.gov/{cerberus_ur}')
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    cerberus_url = astro_url+soup.find('img', class_='wide-image')['src']
    #shia
    browser.visit(f'https://astrogeology.usgs.gov/{shia_ur}')
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    shia_url = astro_url+soup.find('img', class_='wide-image')['src']
    #syrtis
    browser.visit(f'https://astrogeology.usgs.gov/{syrtis_ur}')
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    syrtis_url = astro_url+soup.find('img', class_='wide-image')['src']
    #valles
    browser.visit(f'https://astrogeology.usgs.gov/{valles_ur}')
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    valles_url = astro_url+soup.find('img', class_='wide-image')['src']


    hemisphere_image_urls = [
    {"title": v_title, "img_url": valles_url},
    {"title": c_title, "img_url": cerberus_url},
    {"title": sh_title, "img_url": shia_url},
    {"title": sy_title, "img_url": syrtis_url}]
    browser.quit()
    return hemisphere_image_urls



