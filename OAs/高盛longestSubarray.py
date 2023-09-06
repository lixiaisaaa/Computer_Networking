def longestSubArray(nums, k):
    left = 0
    max_len = 0
    summ = 0
    for right, n in enumerate(nums):
        summ += n
        while summ > k:
            summ -= nums[left]
            left += 1

        if summ <= k:
            max_len = max(max_len, right - left + 1)

    return max_len

nums = []
k = 3
print(longestSubArray(nums,k))