# Web-scraping
# In this individual project, I built a web application that scrapes various websites for data related to the Mission to Mars and displays the information in a single HTML page. 
## Outlines:  
### Step 1 - Scraping

* I Completed initial scraping using Jupyter Notebook, BeautifulSoup, Pandas, and Requests/Splinter.

*  Splinter is used to navigate the site and find the image url for the current Featured Mars Image and assign the url string to a variable called `featured_image_url`.



* Pandas is used to scrape the table containing facts about the planet including Diameter, Mass, etc.

* Pandas is also used to convert the data to a HTML table string.

* Python dictionary is used to store the data using the keys `img_url` and `title`.

* Append the dictionary with the image url string and the hemisphere title to a list. This list will contain one dictionary for each hemisphere.


### Step 2 - MongoDB and Flask Application

MongoDB with Flask templating is used to creating a new HTML page that displays all of the information that was scraped from the URLs above.

* I Started by converting my Jupyter notebook into a Python script called `scrape_mars.py` with a function called `scrape` that will
execute all of my scraping code from above and return one Python dictionary containing all of the scraped data.

* Creating a route called `/scrape` that will import my `scrape_mars.py` script and call my `scrape` function.

* The return value is stored in Mongo as a Python dictionary.

* Creating a root route `/` that will query my Mongo database and pass the mars data into an HTML template to display the data.

* Creating a template HTML file called `index.html` that will take the mars data dictionary and display all of the data in the appropriate HTML elements.
