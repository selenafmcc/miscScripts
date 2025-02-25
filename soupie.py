 
#Beautiful soup time!!
from bs4 import BeautifulSoup 
import requests

URL = "https://ccmcc.neocities.org/pages/layout"
reqURL = requests.get(URL)
soup = BeautifulSoup(reqURL.text, "lxml")
# lxml is our parser! There are different types of parsers, and we don't HAVE to use lxml. But we have the lxml parser module installed (thank you pip!) just as an example. lxml is fast, but it depends on the device running it to have C installed. WIndows machine? No problem! other OS? dicy dicy!
#soup = BeautifulSoup(reqURL.text, "html.parser")
# html.parse comes with python. It's a wee bit slower than lxml, and a bit less lenient than other possible parsers, but it comes with python and doesn't need to be installed. Basically, any device that has python will have python's built in html parser.
#soup = BeautifulSoup(reqURL.text,"html5lib")
# html5lib is another parser we need to install. It parses HTML pretty much the same way a browser does, which makes it the slowest of the bunch! But it makes your HTML nice and indented with little effort. 

#As a note, lxml also has an xml parser. It's fast, and is pretty much the only xml parser in the python module game! So let's get comfortable using lxml to parse our webpages.

#print(soup.prettify())
# Since we are using lxml, and we dont have html5lib to parse our html all pretty like, we're going to use this method to indent nested tags for us.

#lets check out some of our soupie abilities.

#elementMatch = soup.title.text
#print(elementMatch)
# we grabbed the title element of the webpage. You know what this is, It's in our header! So easy. Don't you love those dot accessors?

# Let's get a bit more complicated
elementMatch = soup.div.text
#print(elementMatch)
# we have many divs on this page. accessing this way return the FIRST match
elementMatch = soup.find('div', class_='footer').text
#print(elementMatch)
# Using the find method will help us narrow our search! We use "class_" because the word CLASS is already being in something else by python. you don't need it for every attribute you're trying to find, but you do need it for a couple! read the documentation

# Let's try something new. Let's say we want to grab the title, the summary, and the title link for EACH article. Let's do it for one, first.

elArticle = soup.find_all("div", class_="article")
# with find_all, we don't look for the first match. We look for ALL matches. That means elArticle stops being a single object and starts being a LIST of objects
#print(elArticle)
# Prints every matching element one after another

# lets make a loop
for article in elArticle:
    elHead = article.h2.a.text
    elSumm = article.p.text
    elAnchor = article.h2.a['href']
    #print('\n'+elHead+'\n'+elSumm+'\n'+elAnchor+'\n')
# That sure is some Beautiful Soup! Did you notice how we accessed the href attribute from the a tag? You can treat the attributes of a tag by treating said tag like a dictionary of elements. You can grab tag ids, classes, even style attributes this way! Wowza!

#When using this on webpages, you'll have to figure out how the page is formatted. Do repeated elements all share a class? Or is it worse than that? The truth is, human are capable of great evil, and web design is no different!

# Let's grab the current top 10 words from the merriam webster dictionary website.

URL = "https://www.merriam-webster.com/"
reqURL = requests.get(URL)
soup = BeautifulSoup(reqURL.text, "lxml")
#print(soup.prettify())
#Now here's an issue. It's 2025. Websites don't necesarilly load everything at once! Lazy loading is a standard of modern web design efficiency, after all. SO the HTML page we grab this way is INCOMPLETE! It hasn't loaded teh thing we need yet! Wuh-oh!

# Selenium time! Selenium will launch, pilot, and close a browser of our choice! She can interact with web pages the same way a user does, so she can interact with JS elements and circumvent this lazy loading blockade.

from selenium import webdriver
#from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options as FFO
import time

#We import the webdriver, which launches the faux browser, Keys, which lets us use keyboard actions,and  By, to help us find elements. We also have function for waiting in the browser. Time is built-in to Python itself. You can guess how it works :p Since we will be using forefox, we also import some firefox options
ffoptions = FFO()
ffoptions.add_argument("--headless")
browser = webdriver.Firefox(options=ffoptions)
# She comes with other browsers, like chrome at all. But we like Firefox, don't we! Setting the Firefox options to Headless mode means we don't need an entire forefox browser to pop up. That'd kind of defeat the purpose of this scrape!
browser.get(URL)

# Since the website we're using doesn't have anything like an infinite scroll, we only need to give it time to load the element we're waiting for (in this case, the top ten, all div items with the class "word-text"
#time.sleep(5)
# Here, we wait 5 seconds for the site to load. This is dependent on server times, so after 5 seconds, we might not have the whole page loaded! This also wouldn't be efficient for certain tasks, like loading an infinite-scroll page up to certain amount.

wait = WebDriverWait(browser,10)
wait.until(EC.presence_of_element_located((By.CLASS_NAME,'word-text')))
# Here, instead of an arbitrary sleep timer, we are waiting (up to 10 seconds)for the site to successfully load the elements we are looking for: the elements with the "word-text" class. The moment they load, the script continues as folows.

page = browser.page_source
browser.quit()
# So now, we have a slightly-more-loaded version of our website stored in our page variable!

soup = BeautifulSoup(page, 'lxml')
allList = soup.find_all('div', class_="word-text")

print('\n',"The top 10 searched up words on the Merriam-Webster dictionary, as of",time.ctime(), "are as follows: ")
for idx, div in enumerate(allList):
    title = div.text
    print(f"#{idx+1}: {title}")

# Groovy B) We've done something pretty, pretty cool here! Requests is the quickest way to get a static HTML page + all its info, whereas Selenium can handle all of those tricky fancy loading sites. Regardless of which one we use, our girl BeautifulSoup is built to parse all the info we get from an HTML file. The python side of things ain't so difficult, is it?
# One thing to remember as we embark on our scraping journey is the presence of a robots.txt file on just about every website you can think of. Seriously. Go to www.website.com/robots.txt and see its scraping permissions! Don't break any website's rules and you won't get yourself in trouble.
# Next time we do this, we should check a site's robots.txt for our allowed permissions, and we should also remember to use TIMEOUTS to ensure we aren't trapped loading a page. In the case of requests, a TIMEOUT will let us know they couldn't get anything from the webpage because the server didn't send a response in time. In the case of Selenium, using the Wait method like we did means we should double check we did, in fact, get what we wanted, and the site didn't crap out on us.
# But that's for next time :)
