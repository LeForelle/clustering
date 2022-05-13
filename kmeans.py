from matplotlib.image import imread
import matplotlib.pyplot as plt
import numpy as np
import centers
from sklearn.cluster import KMeans

field = imread('kmeans.tif')
plt.figure(figsize=(12, 6))
plt.imshow(field)

field = field/255.0
x = field.reshape(-1, 4)

iter = 0
n_clusters = 3
min_distance = [0]*len(x)
prev_iter = []
center = centers.choise_of_centers(x, len(x), n_clusters)

while iter < 100:
    summ = [0]*n_clusters
    for i in range(n_clusters):
        summ[i] = [0]*4
    count = [0]*4
    for i in range(len(x)):
        c = 100
        for j in range(n_clusters):
            if c > centers.distance_calculation(x[i], center[j]):
                min_distance[i] = j
                c = centers.distance_calculation(x[i], center[j])
        summ[min_distance[i]][0] += x[i][0]
        summ[min_distance[i]][1] += x[i][1]
        summ[min_distance[i]][2] += x[i][2]
        summ[min_distance[i]][3] += x[i][3]
        count[min_distance[i]] += 1
    for i in range(n_clusters):
        center[i][0] = summ[i][0]/count[i]
        center[i][1] = summ[i][1]/count[i]
        center[i][2] = summ[i][2]/count[i]
        center[i][3] = summ[i][3]/count[i]
    if iter > 0 and prev_iter == min_distance:
        break
    prev_iter = list(min_distance)
    min_distance = [0]*len(x)
    iter += 1
    print(iter)

print(x)
print(center)
for i in range(len(x)):
    x[i] = center[prev_iter[i]]

x = x.reshape(field.shape)

plt.figure(figsize=(12, 6))
plt.imshow((x * 255).astype(np.uint8))
plt.show()


        