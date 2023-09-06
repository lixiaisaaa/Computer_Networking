def numberOfAlerts(precedingMinutes, alertThreshold, numCalls):
    left, right = 0, 0
    summ = 0
    ans = 0
    for right, n in enumerate(numCalls):
        summ += n
        while right - left + 1 > precedingMinutes:
            summ -= numCalls[left]
            left += 1

        if right - left + 1 == precedingMinutes:
            if summ / precedingMinutes > alertThreshold:
                ans += 1
    return ans

if __name__ == "__main__":
    num_calls = [0,11,10,10,7]
    alert_threshold = 10
    preceding_minutes = 3
    print(numberOfAlerts(preceding_minutes, alert_threshold, num_calls))
