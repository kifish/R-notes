import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.patches import Polygon
from mpl_toolkits.basemap import Basemap
from matplotlib.collections import PatchCollection
import matplotlib.patches as mpatches

font = {'family': 'SimHei'}
matplotlib.rc('font', **font)
fig = plt.figure()
ax = fig.add_subplot(111)
basemap = Basemap(llcrnrlon=75, llcrnrlat=10, urcrnrlon=150,
                  urcrnrlat=55, projection='poly', lon_0=116.65, lat_0=40.02, ax=ax)
basemap.readshapefile(shapefile="./bou2_4p", name="china")
basemap.readshapefile(shapefile="./gadm36_TWN_2", name="taiwan")
mapData = pd.DataFrame(basemap.china_info)
mapData["NAME"] = mapData["NAME"].map(
    lambda x: x.decode("gbk") if len(x) != 0 else x)
sheet = pd.read_excel('各单位地理位置分布.xlsx', sheet_name='Sheet4')
sheet = sheet.replace(['-Inf', 'Inf'], 'null')
sheet = sheet.fillna(0)


def fix(name):
    name = name[:2]
    if name == '黑龍':
        name = '黑龙'
    return name
statenames = list(map(fix, mapData["NAME"].tolist()))

colors = {}
location_colors = {
    '华东': 'brown',
    '华北': 'r',
    '华南': 'g',
    '华中': 'lightyellow',
    '东北': 'cyan',
    '西北': 'orchid',
    '西南': 'lightpink'
}

for _, row in sheet.iterrows():
    k1 = '省'
    k2 = '地区'
    colors[row[k1][:2]] = location_colors[row[k2]]

def plotProvince(row):
    province = row['省'][:2]
    color = colors[province]
    patches = []
    for province_, shape in zip(statenames, basemap.china):
        if province_ == province:
            patches.append(Polygon(xy=np.array(shape), closed=True))
    ax.add_collection(PatchCollection(patches, facecolor=color,
                                      edgecolor=color, linewidths=1., zorder=2))

sheet.apply(lambda row: plotProvince(row), axis=1)

patchs = []
for location, color in location_colors.items():
    patch = mpatches.Patch(color=color, label=location)
    patchs.append(patch)
plt.legend(handles=patchs)

plt.axis("off")  # 关闭坐标轴
plt.show()  # 显示图表