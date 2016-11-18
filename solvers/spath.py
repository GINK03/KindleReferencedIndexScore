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

"""
2 3
   0x 1x 2x
0y ..#
1y ...
ex) 0x0y
ERROR

10 15
..##.....#.....
..........##...
.##...##..#....
#....#.......#.
.......#.......
.....#.#..#....
.....#.#..#....
.#............#
...#.##....##..
..........#....
"""
n2 = {}
Y, X = map(lambda x:int(x),  raw_input().strip().split(" "))
nodestate = []
for _ in range(Y):
  nodestate.append( map(lambda x:x, raw_input().strip()) )
#print "state ", nodestate
nodenames = []
for y in range(Y):
  for x in range(X):
    if nodestate[y][x] == ".":
      nodenames.append(str(x)+"x" + str(y) + "y")
end_point = nodenames[-1]
#print nodenames
""" build path"""
for n in nodenames:
  x = int(n.split("x").pop(0)) 
  y = int(n.split("x").pop().split('y').pop(0)) 
  next_x = str(x+1) + "x" + str(y) + "y"
  if X > x and next_x in nodenames:
    if n2.get(n) == None:
      n2.update( {n: { next_x:2  } } )
    else:
      n2[n][next_x] = 0 
  
  buttom_y = str(x) + "x" + str(y+1) + "y"
  if Y > y and buttom_y in nodenames:
    if n2.get(n) == None:
      n2.update( {n: {buttom_y: 1} } ) 
    else:
      n2[n][buttom_y] = 1
  if X > x and Y > y and next_x not in nodenames and buttom_y not in nodenames:
    n2[n] = {}
  """
  upper_y = str(x) + "x" + str(y-1) + "y"
  if upper_y in nodenames:
    if n2.get(n) == None:
      n2.update( {n: {upper_y: 1} } ) 
    else:
      n2[n][upper_y] = 1
  """
  if x == X-1 and y == Y-1: 
    n2[n] = {}
#print n2

hyperparam = []
def FindShortestPath(begin, end, shortestPath, h, nestlv = 1):
    if begin == end:
        shortestPath = [end]
        return 0
    currentBestLen = 1e10
    currentBestRoute = []
    cache = ""
    for neigh in h[begin].keys():
        aiResult = []
        cost = FindShortestPath(neigh, end, aiResult, h, nestlv + 1)
        if cost + h[begin][neigh] < currentBestLen:
            currentBestLen = cost + h[begin][neigh]
            currentBestRoute = [begin] + aiResult
            #cache = [ begin, neigh ]
    shortestPath = currentBestRoute
    #print "FindShortestPath from %s to %s has cost %d for %s " \
    #    % (begin, end, currentBestLen, shortestPath), nestlv
    hyperparam.append( (shortestPath, nestlv, currentBestLen )  )
    return currentBestLen

bestRoute = []
FindShortestPath("0x0y", end_point, bestRoute, n2)
hyperparam.reverse()
pos = 0
buff = []
for h in hyperparam:
  if h[2] == 1e10:
    continue
  if pos > h[1]:
    break
  pos = h[1]
  buff.append(h[0][0])
#  print h[0][0], h[1], h[2]
#print ",".join(buff)

"diff iter"
sw = [0, 0]
sw2 = [0, 0]
cnt = 0
for i, b in enumerate(buff):
  h_, t_ = b.split('x')
  ri = int(h_)
  bu = int(t_.split('y').pop(0))
  if i == 0:
    continue
  if i == 1:
    if ri > 0:
      sw = [1, 0]
    if bu > 0:
      sw = [0, 1]
    continue
  
  ri_vector, bu_vector = None, None,
  if sw2[0] == sw[0]:
    ri_vector = "Active"

  if sw2[1] == sw[1]:
    bu_vector = "Active"

  if sw2[0] != ri and ri_vector:
    #print "tern right"
    cnt += 1
  if sw2[1] != bu and bu_vector:
    #print "tern buttom"
    cnt += 1
  #print i, ri_vector, bu_vector, [ri, bu]

  sw2 = sw
  sw = [ri, bu]
 
print cnt
