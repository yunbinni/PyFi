from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import numpy as np; np.random.seed(42)
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# 데이터 불러오기
hibe = pd.read_csv('HYBE.csv')

# 띄울 사진들 불러오기
jpg_name_np = np.array(['20201216.png', '20210113.png', '20210122.png','20210218.png','20210615.png']).astype('<U12')
cmap = plt.cm.RdYlGn

# 사진 띄울 경로 지정하기
data = pd.DataFrame(hibe)
xx1 = data[data['Date'] == '2020-12-16'].index[0]
xx1
xx2 = data[data['Date'] == '2021-01-13'].index[0]
xx2
xx3 = data[data['Date'] == '2021-01-22'].index[0]
xx3
xx4 = data[data['Date'] == '2021-02-18'].index[0]
xx4
xx5 = data[data['Date'] == '2021-06-15'].index[0]
xx5
yy1 = hibe.iloc[xx1, 4]
yy1
yy2 = hibe.iloc[xx2, 4]
yy2
yy3 = hibe.iloc[xx3, 4]
yy3
yy4 = hibe.iloc[xx4, 4]
yy4
yy5 = hibe.iloc[xx5, 4]
yy5
# 경로 지정후 인덱스값 리스트로 저장
x = [xx1,xx2,xx3,xx4,xx5]
y = [yy1,yy2,yy3,yy4,yy5]

# 그래프 그리기
fig = plt.figure()
plt.plot(hibe.Date, hibe.Close)
ax = fig.add_subplot(111)
line, = ax.plot(x, y, ls="", marker="o")
image_path = np.asarray(jpg_name_np)

# 이미지 상자 만들기
image = plt.imread(image_path[0])
im = OffsetImage(image, zoom=0.5)
xybox=(50., 50.)
ab = AnnotationBbox(im, (0,0), xybox=xybox, xycoords='data',
        boxcoords="offset points",  pad=0.3,  arrowprops=dict(arrowstyle="->"))
# 축에 추가후 보이지 않게 만들기
ax.add_artist(ab)
ab.set_visible(False)

# 호버 이벤트
def hover(event):
    # 마우스가 산점도 위에 있는 경우
    if line.contains(event)[0]:
        # 이벤트에서 배열내의 인덱스를 찾기
        ind, = line.contains(event)[1]["ind"]
        # figure 사이즈 구하기
        w,h = fig.get_size_inches()*fig.dpi
        ws = (event.x > w/2.)*-1 + (event.x <= w/2.)
        hs = (event.y > h/2.)*-1 + (event.y <= h/2.)
        # 그림에서 이벤트가 발생하면
        # 마우스를 기준으로 이미지 위치를 변경
        ab.xybox = (xybox[0]*ws, xybox[1]*hs)
        # 이미지를 보이게 하기
        ab.set_visible(True)
        # 호버링된 스프레이 포인트에 배치
        ab.xy =(x[ind], y[ind])
        # 해당 지점에 해당 이미지를 설정
        im.set_data(plt.imread(image_path[ind]))
    else:
        #마우스가 해당 위치에 없는 경우 안보이기
        ab.set_visible(False)
    fig.canvas.draw_idle()

# 마우스 움직임에 대한 콜백 추가
fig.canvas.mpl_connect('motion_notify_event', hover)

fig = plt.gcf()
fig.set_size_inches(10.5, 9.5)

plt.show()