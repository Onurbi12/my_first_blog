from __future__ import unicode_literals

from django.apps import AppConfig

# from bs4 import BeautifulSoup


class BlogConfig(AppConfig):
    name = "blog"


# with open("./blog/templates/blog/test.html") as html_test:
#     soup = BeautifulSoup(html_test, "html.parser")

# print(soup)
# for element in soup.findAll("a"):
#     print(element)
#     print(element.coords)
