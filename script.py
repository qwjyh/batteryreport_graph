import re
from bs4 import BeautifulSoup

# soup作成
soup = BeautifulSoup(open('battery-report.html', encoding="utf-8"), "lxml")

# battery capacity historyの検索、table要素の取得
table = soup.find("h2", text=re.compile("Battery capacity history")).next_sibling.next_sibling.next_sibling.next_sibling

# 保存先のリスト
mat = []

# thead
# r = [] # 保存先のrow
# thead = table.find('thead')
# # print(thead)
# tds = thead.tr.find_all('td')
# for td in tds:
#   r.append(td.get_text(strip = True))
# mat.append(r) # matにtheadを追加

# td(dateTime), td(mw(capacity)), td(mw(design))
trs = table.find_all('tr')
for tr in trs:
  r = [] # ここに行を保存
  for td in tr.find_all('td'):
    r.append(td.get_text(strip = True))
  mat.append(r)

# リストの転置
mat_T = [list(x) for x in zip(*mat)]
print(mat_T)
