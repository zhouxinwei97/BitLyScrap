from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import sys
import time


def num_clicks(position_of_clicks, relevant):
    clicks = ""
    for x in range(position_of_clicks, position_of_clicks + 10):
        if relevant[11].string[position_of_clicks] != ",":
            clicks += relevant[11].string[position_of_clicks]
            position_of_clicks += 1
        else:
            break;

    return clicks


def main():
    clicks_file = open("Click_Sept.txt", "a")
    lines = []
    print("Processing:")
    for line in sys.stdin:
        lines.append(line.strip())

    lines = list(filter(None,lines))

    for counter in range(len(lines)):
        if "bit.ly" in lines[counter]:
            lines[counter] = "https://" + lines[counter] + "+"


    clicksList = []
    for x in range(len(lines)):
        print (lines[x])
        clicks_file.write(lines[x])
        clicks_file.write('\n')

        if "bit.ly" in lines[x]:
            driver = webdriver.Chrome()
            driver.get(lines[x])
            clicks_wrapper = driver.find_elements_by_xpath('//*[@id="main"]/div/div[1]/div[3]/div[1]/div[1]/div/div[1]/span[1]')[0]
            clicks = clicks_wrapper.text
            driver.close()
            clicksList.append(clicks)
            clicks_file.write("  " + clicks)
            clicks_file.write('\n')
            # page = requests.get(lines[x])
            # soup = BeautifulSoup(page.content, "html.parser")
            # relevant = soup.body.contents
            # position_of_clicks = relevant[11].string.find("user_clicks") + 14
            # clicks = num_clicks(position_of_clicks, relevant)

    counter = 0
    num_deals = 0
    for line in lines:
        if "bit.ly" in line:
            print(line, clicksList[counter])
            counter += 1
            num_deals += 1
        else:
            print(line)


    print("total deals scrapped = ", num_deals/2)
    clicks_file.close()


if __name__ == "__main__":
    start = time.time()
    main() # ~1s to scrap 1 link's clicks
    print("Time taken = ", time.time() - start)


