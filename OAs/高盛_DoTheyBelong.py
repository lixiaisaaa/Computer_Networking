# Do they belong

def pointsBelong(x1, y1, x2, y2, x3, y3, xp, yp, xq, yq) -> int:
    ab = calc_distance(x1, y1, x2, y2)
    bc = calc_distance(x2, y2, x3, y3)
    ac = calc_distance(x1, y1, x3, y3)
    if ab + bc <= ac or ab + ac <= bc or ab + bc <= ac:
        return 0

    area = calc_Area(x1, y1, x2, y2, x3, y3)
    p1 = calc_Area(xp, yp, x2, y2, x3, y3)
    p2 = calc_Area(x1, y1, xp, yp, x3, y3)
    p3 = calc_Area(x1, y1, x2, y2, xp, yp)
    q1 = calc_Area(xq, yq, x2, y2, x3, y3)
    q2 = calc_Area(x1, y1, xq, yq, x3, y3)
    q3 = calc_Area(x1, y1, x2, y2, xq, yq)

    q_flag, p_flag = False, False
    if q1 + q2 + q3 == area:
        q_flag = True
    if p1 + p2 + p3 == area:
        p_flag = True

    if not q_flag and p_flag:
        return 1
    elif q_flag and not p_flag:
        return 2
    elif q_flag and p_flag:
        return 3
    elif not q_flag and not p_flag:
        return 4


def calc_distance(x1, x2, y1, y2):
    return ((y2 - y1) ** 2 + (x2 - x1) ** 2) ** 0.5


def calc_Area(x1, y1, x2, y2, x3, y3) -> float:

    return abs(x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)) / 2

print(pointsBelong(0, 0, 1, 0, 0, 1, 0.5, 0.5, 1.5, 1.5))  # Expected: 3 (Both points inside)
print(pointsBelong(0, 0, 1, 0, 0, 1, 0.5, 0.5, 0.2, 0.2))      # Expected: 1 (Only P inside)
print(pointsBelong(0, 0, 1, 0, 0, 1, -1, -1, 0.5, 0.5))   # Expected: 2 (Only Q inside)
print(pointsBelong(0, 0, 1, 0, 0, 1, -1, -1, 2, 2))       # Expected: 4 (Both points outside)
print(pointsBelong(0, 0, 0, 0, 0, 0, 0, 0, 0, 0))         # Expected: 0 (Cannot form a triangle)
print(pointsBelong(2, 2, 7, 2, 5, 4, 4, 3, 7, 4))