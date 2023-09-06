def getSearchResults(words,queries):
    mp = {}
    for s in queries:
        mp[''.join(sorted(s))] = []
    for word in words:
        w1 = word
        w = ''.join(sorted(word))
        if w in mp:
            mp[w].append(w1)
    return [v for v in mp.values()]

words = ["allot", "cat", "peach","dusty","act","cheap"]
queries = ["tac", "study","peahc"]

print(getSearchResults(words,queries))