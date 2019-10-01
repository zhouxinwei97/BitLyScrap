from bs4 import BeautifulSoup
from bs4.element import Tag


def find_title_links(soup, titles_list, bit_ly_links):
    new_file = open('Sept.txt', "w+")
    titles = soup.findAll("div", {"class":"text"})
    i = 1
    for num_titles in range(1,len(titles)):
        content = titles[num_titles].contents #list
        titles_list.append(content[1].get_text())
        print(content[1].get_text())
        new_file.write(content[1].get_text())
        new_file.write('\n')
        print()
        num = 1
        for links in content:
            if isinstance(links, Tag):
                bitly_link = links.get("href")
                if bitly_link is not None and "bit" in bitly_link:
                    if "http" in bitly_link:
                        bitly_link = bitly_link.replace("http://", "")

                    bit_ly_links.append(bitly_link)
                    new_file.write(bitly_link)
                    new_file.write('\n')
                    print(bitly_link)
                    print()
    new_file.close()

def main():
    html_file = open("messages.html")
    soup = BeautifulSoup(html_file, 'html.parser')
    bit_ly_links = []
    titles_list = []
    find_title_links(soup, titles_list, bit_ly_links)
    print("Done")
    html_file.close()


if __name__ == '__main__':
    main()