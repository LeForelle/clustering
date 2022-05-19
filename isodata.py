from matplotlib.image import imread
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import centers

field = Image.open('kmeans.tif') #считываю файл
plt.figure(figsize=(12, 6))
plt.imshow(field)

fix_width = 1000 #сжатие изображения
width_percent = (fix_width / float(field.size[0]))
height = int((float(field.size[1])*float(width_percent)))

field_res = field.resize((fix_width, height))
field_res.save('kmeanssq.tif') #сохранение сжатого изображения
field = imread('kmeanssq.tif')
y = field.reshape(-1, 4) #создаю массив содержащий 4 канала
x = np.array(y, dtype=np.float16)
n_clusters = 7 #needed number of clusters
n_centers = 10
Qn = len(x)//10 #параметр, с которым сравнивается количество выборочных образов, вошедших в кластер
Qs = 0.1 #параметр, характеризующий среднеквадратичное отклонение
Qc = 0.25 #параметр, характеризующий компактность
L = 2 #максимальное количество пар центров кластеров, которые можно объединить
I = 5 #permitted number of iterations

center = centers.choise_of_centers(x, len(x), n_centers)
iter = 1

while iter <= I:
    center_sets = [[] for i in range(n_centers)]
    summ = [[0]*4 for i in range(n_centers)]
    count = [0]*n_centers
    average_dist = [0]*n_centers
    for i in range(len(x)):
        c = 1000
        for j in range(n_centers):
            dist = centers.distance_calculation(x[i], center[j])
            if c > dist:
                min_distance = j
                c = dist
        center_sets[min_distance].append(i)
        summ[min_distance][0] += x[i][0]
        summ[min_distance][1] += x[i][1]
        summ[min_distance][2] += x[i][2]
        summ[min_distance][3] += x[i][3]
        average_dist[min_distance] += c
        count[min_distance] += 1
    removing_centers = []
    for i in range(n_centers):
        if count[i] < Qn:
            removing_centers.append(i)
    n_centers -= len(removing_centers)
    b=0
    for i in removing_centers:
        center_sets.pop(i - b)
        summ.pop(i-b)
        count.pop(i-b)
        center.pop(i-b)
        average_dist.pop(i-b)
        b+=1
    average_dist_all = 0
    for i in range(n_centers):
        average_dist_all += average_dist[i]
        average_dist[i] /= count[i]
    average_dist_all /= sum(count)
    for i in range(n_centers):
        center[i][0] = summ[i][0]/count[i]
        center[i][1] = summ[i][1]/count[i]
        center[i][2] = summ[i][2]/count[i]
        center[i][3] = summ[i][3]/count[i]
    if iter == I:
        Qc = 0
        center, n_centers, center_sets = centers.merge(center, n_centers, Qc, L, count, center_sets)
    elif n_centers<=n_clusters/2:
        center, n_centers = centers.razbienie(x, center_sets, center, Qs, n_clusters, average_dist, average_dist_all, Qn)
    elif iter%2==0 or n_centers>=2*n_clusters:
        center, n_centers, center_sets = centers.merge(center, n_centers, Qc, L, count, center_sets)
    else:
        center, n_centers = centers.razbienie(x, center_sets, center, Qs, n_clusters, average_dist, average_dist_all, Qn)
    iter += 1
    print(iter)

print(x)
print(center)
for centr in range(len(center_sets)):
    for i in center_sets[centr]:
        for g in range(4):
            x[i][g] = center[centr][g]

x = x.reshape(field.shape)

plt.figure(figsize=(12, 6))
plt.imshow((x * 255).astype(np.uint8))
plt.show()