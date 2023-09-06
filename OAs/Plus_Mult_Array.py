def plusMult(A):
    R_odd, R_even = A[0], A[1]
    for i in range(2,len(A)):
        a = A[i]
        if i % 2 == 0:
            if i % 4 != 0:
                R_even *= a
            else:
                R_even += a
        else:
            if i % 4 != 1:
                R_odd *= a
            else:
                R_odd += a
    print(R_odd, R_even)
    R_even, R_odd = R_even%2, R_odd%2
    print(R_odd,R_even)
    if R_even < R_odd:
        return "ODD"
    elif R_even > R_odd:
        return "Even"
    else:
        return "N"
8 + 48 + 10
66
3 + 35 + 9
1*3 + 5*7 + 9
A = [1,2,3,4,5,6,7,8,9,10]
print(plusMult(A))