from telethon.sync import TelegramClient
import sys
import csv
from selenium import webdriver
import time


def bit_ly_clicks(bit_ly_list):
    new_bit_ly_list = []
    # process all links for headless chrome to process
    for links in bit_ly_list:
        bit_ly_link = links.split(" ")
        for all_links in bit_ly_link:
            if 'bit.ly' in all_links:
                if "(" in all_links:
                    start_position = all_links.find("(")
                    end_position = all_links.find(")")
                    all_links = all_links[start_position + 1: end_position]
                if 'http://' not in all_links:  # creating bitly+ links to check on clicks
                    new_bit_ly_list.append("https://" + all_links + "+")
                else:
                    new_bit_ly_list.append(all_links + "+")

    if len(new_bit_ly_list) == 0:
        return 0
    # setup headless chrome for improved efficiency
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    driver = webdriver.Chrome(options=options)

    clicksList = []  # a post may have >1 bitly link, need the consolidated number and not individual bitly clicks
    for links in new_bit_ly_list:
        driver.get(links)
        print(links)
        try:
            clicks_wrapper = driver.find_element_by_css_selector(
                '.info-wrapper--clicks-text')  # position of bitly clicks
            clicks = clicks_wrapper.text
            if "," in clicks:
                clicks = clicks.replace(",", "")  # bitly formating will return value >1000 as 1,000
            clicksList.append(clicks)
        except:
            clicksList.append(0)
            continue
    total_clicks = 0
    driver.close()
    for clicks in clicksList:
        total_clicks += int(clicks)

    return total_clicks


def main():
    # usage: python3 telethonscrap chatname, month to scrap
    # e.g. scraping for oct and nov. python3 telethonscrap sgfooddeals "10 11"
    name = 'a'
    api_id = 'a' 
    api_hash = 'a'
    chat = sys.argv[1]
    month = sys.argv[2].split(" ")
    print(month)
    print(chat)

    telegram_group_lists = {'sgfooddeals': 'https://t.me/sgfooddeals/',
                            'sgweekend': 'https://t.me/sgweekend/',
                            'sgparenthings': 'https://t.me/sgparenthings/',
                            'budgetbabes': 'https://t.me/budgetbabes/',
                            'sgstudentpromos': 'https://t.me/sgstudentpromos/',
                            'sgtravelpromos': 'https://t.me/sgtravelpromos/',
                            'sgfitnesshealth': 'https://t.me/sgfitnesshealth/'
                            }
    post_link_template = telegram_group_lists[chat]

    with TelegramClient(name, api_id, api_hash) as client:
        output_file_name = chat + '.csv'
        with open(output_file_name, "w+") as csv_file:
            new_writer = csv.writer(csv_file)
            new_writer.writerow(['TITLE', 'DATE', 'VIEWS', 'CLICKS', 'CTR', 'POST LINK'])
            for message in client.iter_messages(chat):
                if message.text == None:
                    continue
                date = message.date.strftime("%m/%d/%Y")
                month_of_post = date.split("/")[0]
                day = date.split("/")[1]
                if month_of_post not in month:
                    print(month_of_post in month)
                    break
                splitted_message = message.text.split('\n')
                id = message.id
                post_link = post_link_template + str(id)
                views = message.views
                title = splitted_message[0]
                bit_ly = []
                for sub_message in splitted_message:
                    if 'bit.ly' in sub_message:
                        bit_ly.append(sub_message)
                clicks = bit_ly_clicks(bit_ly)
                clicks_per_views = (int(clicks) / int(views)) * 100
                clicks_per_views = f'{clicks_per_views:.2f}'
                clicks_per_views = clicks_per_views + "%"
                if "*" in title:
                    title = title.replace("*",
                                          "")  # remove * as the title may be bold, which will be reflected as **text**
                written_date = day + " " + get_month(month_of_post)
                new_writer.writerow([title, written_date, place_value(views), place_value(clicks), clicks_per_views, post_link])


def get_month(month):
    months_in_a_year = {'1': "January", '2': "February", '3': "March", '4': "April", '5': "May", '6': "June",
                        '7': "July", '8': "August", '9': "September", '10': "October", '11': 'November',
                        '12': "December"}
    return months_in_a_year[month]


# takes in a value and add a , between every 1000
def place_value(number):
    return ("{:,}".format(number))


if __name__ == '__main__':
    start = time.time()
    main()
    print("Time taken = ", time.time() - start)
