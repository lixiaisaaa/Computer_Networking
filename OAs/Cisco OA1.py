#Leetcode 5
from typing import List


def longestPalindrome(self, s: str) -> str:
    def expend(left, right):
        while left >= 0 and right < len(s) and s[left] == s[right]:
            left -= 1
            right += 1
        return s[left + 1:right]

    ans = ''
    for i in range(len(s)):
        # odd length
        substr_odd = expend(i, i)
        # even length
        substr_even = expend(i, i + 1)

        ans = substr_odd if len(substr_odd) > len(ans) else ans
        ans = substr_even if len(substr_even) > len(ans) else ans

    return ans

#Leetcode 1380
def luckyNumbers(self, matrix: List[List[int]]) -> List[int]:
    minv = {min(row) for row in matrix}
    maxv = {max(col) for col in zip(*matrix)}

    return list(minv & maxv)
# ans = []
# for i, row in enumerate(matrix):
#     for j, x in enumerate(row):
#         if x == minRow[i] == maxCol[j]:
#             ans.append(x)
# return ans


