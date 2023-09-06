def min_chairs(simulations):
    ans = []

    for s in simulations:
        chairs = 0
        available_chairs = 0

        for c in s:
            if c == 'C' or c == 'U':
                if available_chairs == 0:
                    chairs += 1
                else:
                    available_chairs -= 1
            else:
                available_chairs += 1

        ans.append(chairs)

    return ans


# Test
simulations = ["CCCRRR", "CC","CCRURC"]
print(min_chairs(simulations))  # Expected output: [1]
