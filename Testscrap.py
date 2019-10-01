from bs4 import BeautifulSoup
import requests



links = ["https://www.capitaland.com/sg/malls/tampinesmall/en/deals.html"]

page = requests.get(links[0])
soup = BeautifulSoup(page.content, "html.parser")
soup_main = soup.find("main")
#print(soup_main.find("div"))

# mydivs = soup.find_all("ul", {"class": "listing-container"})
#
# for div in soup.main.findAll("div", {"class": "listing-section"}):
#     for divs in div:
#         print(divs)
#
# for ultag in soup.find_all('ul', {'class': 'listing-container'}):
#     print(ultag)

#for item in enumerate(soup.body):
   # print(item)

destination = soup.find('article', {'class': 'l-content-column'}).findAll("div")

print(soup.find('ul', {'class' : 'listing-items'}))


how_to_get_data = "https://stackoverflow.com/questions/57468420/cant-scrape-nested-tags-using-beautifulsoup"

#page loads dynamically i think