
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import requests

def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    browser = Browser("chrome", **executable_path, headless=False)
    #print("it worked!")
    return browser


# Mars News
def mars_news():
    #try:
        # Browser initiation 
        browser = init_browser()

        # Visit the related url through splinter module
        url = "https://mars.nasa.gov/news"
        browser.visit(url)
        html = browser.html

        # Parse html with bs
        news_soup = BeautifulSoup(html, "html.parser")
        try:
            slide_element = news_soup.select_one("ul.item_list li.slide")
            slide_element.find("div", class_="content_title")

            # Scrape the Latest News Title (Dear Ani, I have changed the name, and the whole structure!!)
            # Use Parent Element to Find First <a> Tag and Save it as news_title
            news_title = slide_element.find("div", class_="content_title").get_text()
            news_paragraph = slide_element.find("div", class_="article_teaser_body").get_text()

        except AttributeError:
            return None, None
        return news_title, news_paragraph


# Featured Image
def featured_image():
    try:
        # Browser initiation 
        browser = init_browser()

        #Visit the url for JPL Featured Space Image
        JPL_Featured_Image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
        browser.visit(JPL_Featured_Image_url)

        # Ask Splinter to Go to Site and Click Button with Class Name full_image
        # <button class="full_image">Full Image</button>
        full_image_button = browser.find_by_id("full_image")
        full_image_button.click()

        # Create HTML object; parse with bs
        html = browser.html
        image_bs4 = BeautifulSoup(html, "html.parser")

        # Retrieve background-image url (The comment out code worked well in Jupiter lab but not here so I changed it.)
        # image = image_bs4.find("img", class_="thumb")["src"]
        # featured_image_url = "https://www.jpl.nasa.gov" + image
        # print(featured_image_url) 
        img = image_bs4.select_one("figure.lede a img")
        try:
            img_url = img.get("src")
        except AttributeError:
            return None

    # Use Base URL to Create Absolute URL
        img_url = f"https://www.jpl.nasa.gov{img_url}"
        return img_url 
    finally:
        browser.quit()  


# Mars Weather

def mars_weather():

    try:
        # Browser initiation 
        browser = init_browser()

        # Visit Mars Weather Twitter through splinter module
        weather_url = "https://twitter.com/marswxreport?lang=en"
        browser.visit(weather_url)   

        # HTML Object 
        html_weather = browser.html

        # Parse HTML with Beautiful Soup
        weather_bs4 = BeautifulSoup(html_weather, "html.parser")
    #    # Retrieve all elements that contain news title in the specified range (Here again I changed the jupiter code)
    #      Look for entries that display weather related words to exclude non weather related tweets 
    #       latest_tweets = weather_bs4.find_all('div', class_ = 'js-tweet-text-container')
    #       for tweet in latest_tweets: 
            #     weather_tweet = tweet.find('p').text
            #     if 'Sol' and 'pressure' in weather_tweet:
            #         print(weather_tweet)
            #         break
            #     else: 
            #         pass
        # Find all elements that contain tweets
        latest_tweets = weather_bs4.find("div", 
                                    attrs={
                                           "class": "tweet", 
                                            "data-name": "Mars Weather"
                                        })
        # Search Within Tweet for <p> Tag Containing Tweet Text                                
        mars_weather_info = latest_tweets.find("p", "tweet-text").get_text()
        return mars_weather_info
    finally:   
        browser.quit()

# Mars Facts
def mars_facts():
    try:
        # Visit Marcs facts url
        #facts_url = "https://space-facts.com/mars/"

        # Use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
        df = pd.read_html("https://space-facts.com/mars/")[1]
    except BaseException:
        return None
        # Assign the columns `["Features", "Value"]`
        df.columns = ["Features", "Value"]

        df.set_index("Features", inplace=True)
    return df.to_html(classes="table table-striped")

# # Mars Hemispheres
def hemisphere():
    browser = init_browser()
    # Visit the USGS Astrogeology Science Center Site
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    # Create an empty list with links for the hemispheres
    hemisphere_image_urls = []

    # Get a List of All the Hemisphere
    links = browser.find_by_css("a.product-item h3")
    for item in range(len(links)):
        hemisphere = {}  
        
        # Find Element on Each Loop to Avoid a Stale Element Exception
        browser.find_by_css("a.product-item h3")[item].click()
        
        # Find Sample Image Anchor Tag & Extract <href>
        sample_element = browser.find_link_by_text("Sample").first
        hemisphere["img_url"] = sample_element["href"]
        
        # Get Hemisphere Title
        hemisphere["title"] = browser.find_by_css("h2.title").text
            
        # Append Hemisphere Object to List
        hemisphere_image_urls.append(hemisphere)
        
        # Navigate Backwards
        browser.back()
    return hemisphere_image_urls

    # Helper Function
def scrape_hemisphere(html_text):
        hemis_soup = BeautifulSoup(html_text, 'html.parser')
        try:
            title_element = hemis_soup.find("h2", class_ ="title").get_text()
            sample_element = hemis_soup.find("a", text="Sample").get("href")
        except AttributeError:
            title_element = None
            sample_element = None 
        hemisphere = {
            "title": title_element,
            "img_url": sample_element
        }
        return hemisphere

    #################################################
    # Main Scarping part

def scrape_all():
        #title_first, paragraph_first = mars_news()
        news_title, news_paragraph = mars_news()
        img_url = featured_image()
        mars_weather_info = mars_weather()
        facts = mars_facts()
        hemisphere_image_urls = hemisphere()


        data = {
            "news_title": news_title,
            "news_paragraph": news_paragraph,
            "featured_image": img_url,
            "weather": mars_weather_info,
            "facts": facts,
            "hemispheres": hemisphere_image_urls
        }
        return data 

if __name__ == "__main__":
    print(scrape_all())  








