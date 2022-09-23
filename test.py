import  time
def bubbleSort(arr):
    n = len(arr)
    print("下面打印的是n的长度%s "%n)
    # 遍历所有数组元素
    for i in range(n):
        print("下面打印的是i的长度%s " % i)


        # Last i elements are already in place
        for j in range(0, n  -i- 1):

            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]


arr = [64, 34, 25, 12, 22, 11, 90,9,2,3,4,1,0,10]

bubbleSort(arr)

print("排序后的数组:")
for i in range(len(arr)):
    print("%d" % arr[i]),
