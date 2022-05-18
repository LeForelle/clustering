from matplotlib.image import imread
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import centers

field = Image.open('kmeans.tif') #считываю файл
plt.figure(figsize=(12, 6))
plt.imshow(field)

fix_width = 4000 #сжатие изображения
width_percent = (fix_width / float(field.size[0]))
height = int((float(field.size[1])*float(width_percent)))

field_res = field.resize((fix_width, height))
field_res.save('kmeanssq.tif') #сохранение сжатого изображения
field = imread('kmeanssq.tif')
print(field.shape)
field = field/255.0
y = field.reshape(-1, 4) #создаю массив содержащий 4 канала
x = np.array(y, dtype=np.float16)

iter = 0
n_clusters = 3
min_distance = [n_clusters]*len(x) #массив с информацией к какому кластеру принадлежит пиксель
prev_iter = [] #массив предыдущей итерации для выхода из цикла
center = centers.choise_of_centers(x, len(x), n_clusters)#функция изначального определения центроидов
black = np.zeros((1, 4))

while iter < 100:
    summ = [0]*n_clusters
    for i in range(n_clusters):
        summ[i] = [0]*4
    count = [0]*4
    for i in range(len(x)):
        if x[i].all() == 0:
            continue
        c = 100
        for j in range(n_clusters): #определение до какого из центроидов наименьшее расстояние
            if c > centers.distance_calculation(x[i], center[j]):
                min_distance[i] = j
                c = centers.distance_calculation(x[i], center[j])
        summ[min_distance[i]][0] += x[i][0]
        summ[min_distance[i]][1] += x[i][1]
        summ[min_distance[i]][2] += x[i][2]
        summ[min_distance[i]][3] += x[i][3]
        count[min_distance[i]] += 1
    for i in range(n_clusters): #пересчитываю координаты центроидов
        center[i][0] = summ[i][0]/count[i]
        center[i][1] = summ[i][1]/count[i]
        center[i][2] = summ[i][2]/count[i]
        center[i][3] = summ[i][3]/count[i]
    if iter > 0 and prev_iter == min_distance: #сраниваю с предыдущей итерацией
        break
    prev_iter = list(min_distance)
    min_distance = [0]*len(x)
    iter += 1
    print(iter)

print(x)
print(center)
for i in range(len(x)):
    if x[i].all() == 0:
            continue
    x[i] = center[prev_iter[i]] #присваиваю один цвет кластеру

x = x.reshape(field.shape) 

plt.figure(figsize=(12, 6))
plt.imshow((x * 255).astype(np.uint8)) #преобразование обратно в изображение
plt.show()


        