# 负数部分还没写
# 大体思路：
# - and -  = 去负号，做减法 最后加上 “-”
# - and +  = 做加法
# cornor case 如果有一个数为0， 直接返回另一个数
x = input()
y = input()


def stringSub(x, y):
    is_neg = False

    # 用大的数字减小的数字，如果交换了记录为负数
    if len(x) < len(y):
        y, x = x, y
        is_neg = True

    elif len(x) == len(y) and x < y:
        y, x = x, y
        is_neg = True

    i, j = len(x) - 1, len(y) - 1
    carry, diff = 0, 0
    ans = ""
    while i >= 0 or j >= 0:
        if i >= 0:
            a = int(x[i])
        else:
            a = 0

        if j >= 0:
            b = int(y[j])
        else:
            b = 0

        diff = a - b - carry

        if diff < 0:
            carry = 1
            diff += 10
        else:
            carry = 0

        ans += str(diff)
        i -= 1
        j -= 1

    ans = ans[::-1]
    ans = ans.lstrip("0")

    if not ans:
        ans = "0"
    if is_neg:
        ans = '-' + ans

    return ans


def addStrings(num1: str, num2: str) -> str:
    p1, p2 = len(num1) - 1, len(num2) - 1
    carry = 0
    ans = ""
    while p1 >= 0 or p2 >= 0 or carry:
        if p1 >= 0:
            n1 = int(num1[p1])
        else:
            n1 = 0
        if p2 >= 0:
            n2 = int(num2[p2])
        else:
            n2 = 0

        summ = n1 + n2 + carry
        carry = summ // 10
        gewei = summ % 10
        ans += str(gewei)
        p1 -= 1
        p2 -= 1

    while p1 >= 0:
        ans += num1[p1]
        p1 -= 1

    while p2 >= 0:
        ans += num2[p2]
        p2 -= 1

    return ans[::-1]


if x[0] == '-' and y[0] != '-':
    print("-"+ addStrings(x[1:], y))
elif x[0] != '-' and y[0] == '-':
    print(addStrings(x, y[1:]))
elif x[0] == '-' and y[0] == '-':
    print("-"+stringSub(x[1:], y[1:]))
else:
    print(stringSub(x, y))
