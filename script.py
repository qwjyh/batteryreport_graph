import re
from bs4 import BeautifulSoup
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd


# soup作成
soup = BeautifulSoup(open('battery-report.html', encoding="utf-8"), "lxml")

# battery capacity historyの検索、table要素の取得
table = soup.find("h2", text=re.compile("Battery capacity history")).next_sibling.next_sibling.next_sibling.next_sibling

# 保存先のリスト
mat = []

# td(dateTime), td(mw(capacity)), td(mw(design))
trs = table.find_all('tr')
for tr in trs:
  r = [] # ここに行を保存
  for td in tr.find_all('td'):
    r.append(td.get_text(strip = True))
  mat.append(r)

# リストの転置
mat_T = [list(x) for x in zip(*mat)]
# print(mat_T)

# トリム
dates = []
for i in range(1, len(mat_T[0])):
  dates.append(re.search('\d+-\d+-\d+', mat_T[0][i]).group())
charge = []
for i in range(1, len(mat_T[1])):
  charge.append(int("".join(re.findall('\d', mat_T[1][i]))))
design = []
for i in range(1, len(mat_T[2])):
  design.append(int("".join(re.findall('\d', mat_T[2][i]))))
print(design)

# dataframeに変換
df = pd.DataFrame(
  {mat_T[0][0] : dates,
   mat_T[1][0] : charge,
   mat_T[2][0] : design}
)

print(df)

plt.plot(df.iloc[:, 0], df.iloc[:, 1])
plt.show()