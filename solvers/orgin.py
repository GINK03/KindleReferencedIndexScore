neighbours = {
    "A": {"B": 3, "C": 4},
    "B": {"D": 2},
    "C": {"D": 1, "E": 1, "F": 6},
    "D": {"H": 1},
    "E": {"H": 7},
    "F": {"G": 1},
    "G": {},
    "H": {"G": 3}
}


def FindShortestPath(begin, end, shortestPath):
    print "From %s to %s" % (begin, end)
    if begin == end:
        shortestPath = [end]                           # (1)
        return 0
    currentBestLen = 1e10
    currentBestRoute = []
    for neigh in neighbours[begin].keys():
        aiResult = []
        cost = FindShortestPath(neigh, end, aiResult)
        if cost + neighbours[begin][neigh] < currentBestLen:
            currentBestLen = cost + neighbours[begin][neigh]
            currentBestRoute = [begin] + aiResult
    shortestPath = currentBestRoute                    # (2)
    print "FindShortestPath from %s to %s has cost %d for %s " \
        % (begin, end, currentBestLen, shortestPath)
    return currentBestLen

bestRoute = []
FindShortestPath("A", "G", bestRoute)
print "Best path is", bestRoute
