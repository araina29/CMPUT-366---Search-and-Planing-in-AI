import heapq 
class State:
    """
    Class to represent a state on grid-based pathfinding problems. The class contains one static variable:
    map_width containing the width of the map. Although this is a property of the map and not of the state, 
    the width is used to compute the hash value of the state, which is used in the closed_hash list. 

    Each state has the values of x, y, g.  
    """
    map_width = 0
    map_height = 0
    
    def __init__(self, x, y):
        """
        Constructor - requires the values of x and y of the state. All the other variables are
        initialized with the value of 0.
        """
        self._x = x
        self._y = y
        self._g = 0
        
    def __repr__(self):
        """
        This method is invoked when we call a print instruction with a state. It will print [x, y],
        where x and y are the coordinates of the state on the map. 
        """
        state_str = "[" + str(self._x) + ", " + str(self._y) + "]"
        return state_str
    
    def __lt__(self, other):
        """
        Less-than operator; used to sort the nodes in the open_heap list
        """
        return self._g < other._g
    
    def state_hash(self):
        """
        Given a state (x, y), this method returns the value of x * map_width + y. This is a perfect 
        hash function for the problem (i.e., no two states will have the same hash value). This function
        is used to implement the closed_hash list of the algorithms. 
        """
        return self._y * State.map_width + self._x
    
    def __eq__(self, other):
        """
        Method that is invoked if we use the operator == for states. It returns True if self and other
        represent the same state; it returns False otherwise. 
        """
        return self._x == other._x and self._y == other._y

    def get_x(self):
        """
        Returns the x coordinate of the state
        """
        return self._x
    
    def get_y(self):
        """
        Returns the y coordinate of the state
        """
        return self._y
    
    def get_g(self):
        """
        Returns the g-value of the state
        """
        return self._g
        
    def set_g(self, cost):
        """
        Sets the g-value of the state
        """
        self._g = cost
# for plotting purposes
d_num = 1
b_num = 1

def dijkstra(s_initial, s_goal, graph):
    global d_num
    open_heap = [s_initial]
    heapq.heapify(open_heap)

    closed_hash = {}
    closed_hash[s_initial.state_hash()] = s_initial

    expanded_diskstra = 0

    while not len(open_heap) == 0:
        n = heapq.heappop(open_heap)
        if n == s_goal:
            # uncomment the following 2 lines for generating maps in folder plots
            # graph.plot_map(closed_hash, s_initial, s_goal, 'solution-maps/dijkstra/' + str(d_num))
            # d_num += 1
            return n.get_g(), expanded_diskstra
        children = graph.successors(n)
        expanded_diskstra += 1
        for child in children:
            if child.state_hash() not in closed_hash.keys():
                # adding child in open_heap and closed_hash
                heapq.heappush(open_heap, child)
                closed_hash[child.state_hash()] = child
            elif child.state_hash() in closed_hash.keys() and child < closed_hash[child.state_hash()]:
                # updating closed_hash and open_heap with new g value
                closed_hash[child.state_hash()].set_g(child.get_g())
                # not updating parent because path isn't necessary
                # heapify open_heap
                heapq.heapify(open_heap)
    # graph.plot_map(closed_hash, s_initial, s_goal, 'solution-maps/dijkstra/' + str(d_num))
    # d_num += 1
    return -1, expanded_diskstra
def bi_bs(s_initial, s_goal, graph):
    global b_num
    openA = [s_initial]
    openB = [s_goal]
    heapq.heapify(openA)
    heapq.heapify(openB)

    closedA = {}
    closedB = {}
    closedA[s_initial.state_hash()] = s_initial
    closedB[s_goal.state_hash()] = s_goal

    cost = 999999999
    expanded_astar = 0

    while len(openA) != 0 and len(openB) != 0:
        if cost < openA[0].get_g() + openB[0].get_g():
            return cost, expanded_astar
        if  openA[0] < openB[0]:
            n = heapq.heappop(openA)
            expanded_astar += 1
            children = graph.successors(n)
            for child in children:
                if child.state_hash() in closedB:
                    cost = min(cost, closedB[child.state_hash()].get_g() + child.get_g())
                if child.state_hash() in closedA and child < closedA[child.state_hash()]:
                    closedA[child.state_hash()].set_g(child.get_g())
                    # parent updation not necessary
                    heapq.heapify(openA)
                if child.state_hash() not in closedA:
                    heapq.heappush(openA,child)
                    closedA[child.state_hash()] = child
        else:
            n = heapq.heappop(openB)
            expanded_astar += 1
            children = graph.successors(n)
            for child in children:
                if child.state_hash() in closedA:
                    cost = min(cost, closedA[child.state_hash()].get_g() + child.get_g())
                if child.state_hash() in closedB and child < closedB[child.state_hash()]:
                    closedB[child.state_hash()].set_g(child.get_g())
                    # parent updation not necessary
                    heapq.heapify(openB)
                if child.state_hash() not in closedB:
                    heapq.heappush(openB, child)
                    closedB[child.state_hash()] = child
    # graph.plot_map(closedB, s_initial, s_goal, 'solution-maps/bibs/' + str(b_num))
    # b_num += 1
    return -1, expanded_astar
