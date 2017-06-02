import requests

from bs4 import BeautifulSoup

lines = [1, 2, 3, 4, 6, 7, 9, 10, 11, 13, 14, 15, 17, 18, 20, 22, 23, 24, 25, 26, 27, 28, 31, 33, 35, 44]
line_to_last_stops = {}

for i in lines:
    res = requests.get('http://www.ztm.waw.pl/rozklad_nowy.php?c=182&l=1&q=' + str(i))
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, "html.parser")
    kis = soup.find_all("th", class_="ki")
    line_to_last_stops[i] = (kis[0].strong.text, kis[1].strong.text)
