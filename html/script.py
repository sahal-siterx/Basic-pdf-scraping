from bs4 import BeautifulSoup

with open('index.html') as html:
    soup = BeautifulSoup(html, 'html.parser')

# print(soup.prettify())
# print(soup.get_text())
# print(soup.p)
# print(type(soup.p))
