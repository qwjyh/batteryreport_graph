from cProfile import label
import re
from bs4 import BeautifulSoup
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
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

# dataframeに変換
df = pd.DataFrame(
  {"DATE" : pd.to_datetime(dates),
   mat_T[1][0] : charge,
   mat_T[2][0] : design}
)
print(df.dtypes)

print(df)
print()
print(df.dtypes)
print(df["DATE"][0], type(df["DATE"][0]))

fig, ax = plt.subplots() # create a figure containing a single axes
ax.plot(df.iloc[:, 0], df.iloc[:, 1], label = df.columns[1])
ax.plot(df.iloc[:, 0], df.iloc[:, 2], label = df.columns[2])
ax.set_xlabel("date[Y/M/D]")
ax.set_ylabel("capacity / mWh")
ax.set_title("Battery capacity history")
ax.legend()
plt.show()
