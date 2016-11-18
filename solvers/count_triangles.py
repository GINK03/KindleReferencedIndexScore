def findnumberofTriangles(arr):
    n = len(arr)
    arr.sort()
    count = 0
    for i in range(0,n):
        k = i 
        for j in range(i,n):
            while (k < n and arr[i] + arr[j] > arr[k]):
                k += 1
            count += k - j
    return count

ia =  raw_input().strip().upper().split(' ').pop()
max_len = int(ia)

triangle_ents = range(1, max_len+1) 
print findnumberofTriangles(triangle_ents)
