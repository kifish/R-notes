import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.patches import Polygon
from mpl_toolkits.basemap import Basemap
from matplotlib.collections import PatchCollection

font = {'family': 'SimHei'}
matplotlib.rc('font', **font)
# fig = plt.figure(figsize=(16, 12))
fig = plt.figure()
ax = fig.add_subplot(111)

basemap = Basemap(llcrnrlon=75, llcrnrlat=10, urcrnrlon=150,
                  urcrnrlat=55, projection='poly', lon_0=116.65, lat_0=40.02,ax = ax)
basemap.readshapefile(shapefile="./bou2_4p", name="china")
mapData = pd.DataFrame(basemap.china_info)
#导入的shp格式地图中很多行政区划信息乱码，需要纠正编码
mapData["NAME"] = mapData["NAME"].map(
    lambda x: x.decode("gbk") if len(x) != 0 else x)

sheet1 = pd.read_excel('各单位地理位置分布.xlsx', sheet_name='Sheet4')
sheet1 = sheet1.replace(['-Inf', 'Inf'], 'null')
sheet1 = sheet1.fillna(0)
total = sum(sheet1['病例量'].tolist())

###构建省份上色填充函数：
def plotProvince(row):
    color = (42/256, 87/256, 141/256, row['病例量']/total)
    # color 相当于一个长度为4的tuple
    # 可以根据colormap来确定color的tuple
    patches = []
    # 一个省有多个多边形组成
    for province_, shape in zip(mapData["NAME"].tolist(), basemap.china):
        if province_ == row['省']:
            patches.append(Polygon(xy=np.array(shape), closed=True))
    ax.add_collection(PatchCollection(patches, facecolor=color,
                                      edgecolor=color, linewidths=1., zorder=2))
sheet1.apply(lambda row: plotProvince(row), axis=1)
plt.axis("off")  # 关闭坐标轴
# plt.savefig("save.png") #保存图表到本地
plt.show()  # 显示图表