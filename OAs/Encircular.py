def isRobotBounded(instructions: str) -> str:
    x, y = 0, 0
    dirx, diry = 0, 1

    for c in instructions:
        if c == "G":
            x += dirx
            y += diry

        elif c == "L":
            dirx, diry = -diry, dirx

        elif c == "R":
            dirx, diry = diry, -dirx

    if (x == 0 and y == 0) or (dirx != 0 or diry != 1):
        return "YES"
    else:
        return "NO"


instructions = 'GRGRGRGR'
print(isRobotBounded(instructions))
