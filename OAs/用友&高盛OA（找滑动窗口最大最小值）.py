# 用友版本 相减
# 高盛版本是 multiply
import heapq


def maxMin(nums, operations):
    max_h = []
    min_h = []
    ans = []
    for num, op in zip(nums, operations):
        if op == "push":
            heapq.heappush(max_h, -num)
            heapq.heappush(min_h, num)
        elif op == "pop":
            max_h.pop(max_h.index(-num))
            min_h.pop(min_h.index(num))

        product = -max_h[0] * min_h[0]
        ans.append(product)
    return ans
nums = [1,2,3,1]
operations = ["push","push","push","pop"]
print(maxMin(nums,operations ))




