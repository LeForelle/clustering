import random

def choise_of_centers(pixcels, amount, n_clusters):
    centers = []
    while n_clusters > 0:
        p = random.randint(0, amount)
        p_center = pixcels[p]
        i = 0
        while i < len(centers):
            if centers[i] is p_center:
                p_center = pixcels[(p+random.randint(1, amount-1)) % amount]
                i = 0
            else: i += 1
        centers.append(p_center)
        n_clusters -= 1
    return centers

def distance_calculation(pixcel, center):
    return abs(pixcel[0]-center[0]) + abs(pixcel[1] - center[1]) + abs(pixcel[2] - center[2]) + abs(pixcel[3] - center[3])

