def backspacec(s1,s2):
    stack_s1 = []
    stack_s2 = []

    for c1,c2 in zip(s1, s2):
        if stack_s1 and c1 == '#':
            stack_s1.pop()
        else:
            stack_s1.append(c1)

        if stack_s2 and c2 == '#':
            stack_s2.pop()
        else:
            stack_s2.append(c2)

    return 1 if stack_s1==stack_s2 else 0

s1 = '#axx#bb#c'
s2 = '#axbd#c#c'

print(backspacec(s1,s2))