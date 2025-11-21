from bs4 import BeautifulSoup
import requests
url="https://web.archive.org/web/20200518073855/https://www.empireonline.com/movies/features/best-movies-2"
response=requests.get(url=url)
response.raise_for_status()
page = response.text

soup = BeautifulSoup(page, "html.parser")
titles = [item.string for item in soup.find_all(name="h3", class_="title")]
titles.reverse()
with open("movies.txt", "w") as f:
    for movie in titles:
        try:
            f.write(f"{movie}\n")
        except UnicodeEncodeError:
            f.write(f"{movie.encode('utf-8')}\n")


# Task 2
# soup = BeautifulSoup(yc_webpage, "html.parser")
# titles = soup.select(selector=".titleline a")[0::2]
# titles_texts=[]
# titles_links=[]
# titles_upvotes=[int(item.string.split()[0]) for item in soup.find_all(name="span", class_="score")]
# for title in titles:
#     titles_texts.append(title.string)
#     titles_links.append(title.get("href"))
# print(titles_texts)
# print(titles_links)
# print(titles_upvotes)
#
# index_of_max = (titles_upvotes.index(max(titles_upvotes)))
# print(index_of_max)
# print(f"{titles_texts[index_of_max]} - {titles_links[index_of_max]}")

# Task 1
#import lxml
# with open("website.html") as f:
#     contents = f.read()
#
# soup = BeautifulSoup(contents, "html.parser")
#
# # print(soup.a.string)
# all_anchor_tags = soup.find_all(name="a")
# # print(all_anchor_tags)
# for tag in all_anchor_tags:
#     # print(tag.getText())
#     # print(tag.get("href"))
#     pass
#
# heading = soup.find(name="h3", class_="heading")
# # print(heading)
# name=soup.select_one(selector="#name")
# # print(name)
# print(soup.select(".heading"))
