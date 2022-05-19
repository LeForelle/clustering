import random
from math import sqrt

def choise_of_centers(pixcels, amount, n_clusters):
    centers = []
    while n_clusters > 0:
        p = random.randint(0, amount-1)
        p_center = [i for i in pixcels[p]]
        i = 0
        while i < len(centers):
            if centers[i] == p_center:
                p_center = [i for i in pixcels[(p+random.randint(1, amount-1)) % amount]]
                i = 0
            else: i += 1
        centers.append(p_center)
        n_clusters -= 1
    return centers

def distance_calculation(pixcel, center):
    return sqrt((pixcel[0]-center[0])**2 + (pixcel[1] - center[1])**2 + (pixcel[2] - center[2])**2 + (pixcel[3] - center[3])**2)

def merge(center, n_centers, Qc, L, count, center_sets):
    merging_clusters = []
    for i in range(n_centers):
        for j in range(i+1,n_centers):
            d = distance_calculation(center[i],center[j])
            if d<Qc:
                merging_clusters.append([d,i,j])
    merging_clusters = sorted(merging_clusters,key=lambda x: x[0])
    print(merging_clusters)
    merged = []
    for i in range(min(L, len(merging_clusters))):
        if merging_clusters[i][1] not in merged and merging_clusters[i][2] not in merged:
            merged.append(merging_clusters[i][1])
            merged.append(merging_clusters[i][2])
            center.append([0]*4)
            for j in range(4):  
                center[-1][j] = (count[merging_clusters[i][1]]*center[merging_clusters[i][1]][j] + count[merging_clusters[i][2]]*center[merging_clusters[i][2]][j])/(count[merging_clusters[i][1]]+count[merging_clusters[i][2]])
            center_sets.append(center_sets[center[merging_clusters[i][1]]] + center_sets[center[merging_clusters[i][2]]])
    b = 0
    merged.sort()
    for i in merged:
        center_sets.pop(i-b)
        center.pop(i - b)
        b += 1
    assert len(center) == len(center_sets)
    return center, len(center), center_sets

def razbienie(x, center_sets, center, Qs, n_clusters, average_dist, average_dist_all, Qn):
    deviation = [[0]*4 for i in range(len(center))]
    for i in range(len(center)):
        for g in center_sets[i]:
            for component in range(4):
                deviation[i][component] += (center[i][component]-x[g][component])**2
        for component in range(4):
            deviation[i][component] = sqrt(deviation[i][component]/len(center_sets[i]))
    for i in range(len(center)):
        if max(deviation[i])>Qs and (len(center)<n_clusters/2 or (average_dist[i]>average_dist_all and len(center_sets[i]) > 2*(Qn+1))):
            comp_of_max = deviation[i].index(max(deviation[i]))
            change = 0.5 * max(deviation[i])
            new_center = [center[i][g] for g in range(4)]
            new_center[comp_of_max] += change
            center.append(new_center)
            center[i][comp_of_max] -= change
    return center, len(center)
