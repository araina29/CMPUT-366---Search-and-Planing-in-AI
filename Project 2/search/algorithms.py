import heapq 

class State:
    """
    Class to represent a state on grid-based pathfinding problems. The class contains a static variable:
    map_width containing the width of the map. Although this variable is a property of the map and not of 
    the state, the property is used to compute the hash value of the state, which is used in the CLOSED list. 

    Each state has the values of x, y, g, and cost. The cost is used as the criterion for sorting the nodes
    in the OPEN list for A*, Bi-A*, and Middle_Meet. For A* and Bi-A* the cost should be the f-value of the node, while
    for Middle_Meet the cost should be the p-value of the node. 
    """
    map_width = 0
    
    def __init__(self, x, y):
        """
        Constructor - requires the values of x and y of the state. All the other variables are
        initialized with the value of 0.
        """
        self._x = x
        self._y = y
        self._g = 0
        self._cost = 0
        
    def __repr__(self):
        """
        This method is invoked when we call a print instruction with a state. It will print [x, y],
        where x and y are the coordinates of the state on the map. 
        """
        state_str = "[" + str(self._x) + ", " + str(self._y) + "]"
        return state_str
    
    def __lt__(self, other):
        """
        Less-than operator; used to sort the nodes in the OPEN list
        """
        return self._cost < other._cost
    
    def state_hash(self):
        """
        Given a state (x, y), this method returns the value of x * map_width + y. This is a perfect 
        hash function for the problem (i.e., no two states will have the same hash value). This function
        is used to implement the CLOSED list of the algorithms. 
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

    def get_cost(self):
        """
        Returns the g-value of the state
        """
        return self._cost
        
    def set_cost(self, cost):
        """
        Sets the g-value of the state
        """
        self._cost = cost

# for plotting purposes
a_num = 1
bi_num = 1
m_num = 1
#Creating an code to implement the A* Algorithm -- A* is an algorithm that sorts the nodes in the heap (OPEN) by their respective f values
def A_star(start_state, goal_state, graph):
    #Defining The initial states in A* algorithm
    global a_num
    list_heap = [start_state]
    heapq.heapify(list_heap)

    Dict_hash = {}
    Dict_hash[start_state.state_hash()] = start_state

    expand_a_algo = 0

    while not len(list_heap) == 0:
        n = heapq.heappop(list_heap)
        if n == goal_state:
            return n.get_g(), expand_a_algo
        bacha = graph.successors(n)
        expand_a_algo += 1
        for i in bacha:
            X_change = abs(i.get_x()-goal_state.get_x())
            Y_change = abs(i.get_y()-goal_state.get_y())

            #Using the fourmulae for the hueristic given in the class notes..
            func_heuristic = 1.5*min(X_change, Y_change)+abs(X_change-Y_change)
            i.set_cost(i.get_g() + func_heuristic)
            hash_i = i.state_hash()
            if hash_i not in Dict_hash.keys():
                # adding i in list_heap and Dict_hash
                heapq.heappush(list_heap, i)
                Dict_hash[hash_i] = i
            if hash_i in Dict_hash.keys() and i < Dict_hash[hash_i]:
                #Updating -- Dict_hash and list_heap with the given new g_value 
                Dict_hash[hash_i].set_g(i.get_g())
                #In this condition we dont update the parent  --- PATH isnt neccessary
                #Heapifying -- list_heap
                Dict_hash[hash_i].set_cost(i.get_g() + func_heuristic)
                heapq.heapify(list_heap)
            if i.state_hash() not in Dict_hash.keys():
                # adding i in list_heap and Dict_hash
                heapq.heappush(list_heap, i)
                Dict_hash[i.state_hash()] = i
            elif i.state_hash() in Dict_hash.keys() and i < Dict_hash[i.state_hash()]:
                #Updating -- Dict_hash and list_heap with the given new g_value 
                Dict_hash[i.state_hash()].set_g(i.get_g())
                #In this condition we dont update the parent  --- PATH isnt neccessary
                #Heapifying -- list_heap
                Dict_hash[hash_i].set_cost(i.get_g() + func_heuristic)
                heapq.heapify(list_heap)
    #Plotting the map
    #graph.plot_map(Dict_hash, start_state, goal_state, 'solution-maps/A_star/' + str(a_num))
    #a_num += 1
    return -1, expand_a_algo


#Creating an code to implement the Bi-A* Algorithm -- in which we bassically run the A* from both the directions.
#Bi-A* encounters a solution path once a state is visited in both searches.
def bi_A_stars(start_state,goal_state,graph):
    #Defining The initial states in the bi_A_stars algorithm
    global bi_num
    list_openf = [start_state]
    list_openb = [goal_state]
    dict_closedf = {}
    dict_closedb = {}
    dict_closedf[start_state.state_hash()] = start_state
    dict_closedb[goal_state.state_hash()] = goal_state
    cost = 99999999999
    expand_bi_a_star = 0

    while len(list_openf)!=0 and len(list_openb)!=0:
        if cost<=list_openf[0].get_cost() or cost<=list_openb[0].get_cost():
            return cost, expand_bi_a_star
        #Doing forward expansion
        if list_openf[0] < list_openb[0]:
            n = heapq.heappop(list_openf)
            expand_bi_a_star +=1
            bacha = graph.successors(n)
            for i in bacha:
                X_change = abs(i.get_x()-goal_state.get_x())
                Y_change = abs(i.get_y()-goal_state.get_y())
                func_heuristic = 1.5*min(X_change, Y_change)+abs(X_change-Y_change)
                i.set_cost(i.get_g() + func_heuristic)
                hash_i = i.state_hash()
                if hash_i in dict_closedb:
                    cost = min(cost, dict_closedb[i.state_hash()].get_cost() + i.get_cost())
                if hash_i in dict_closedf and i < dict_closedf[hash_i]:
                    # updating closed_hash and open_heap with new g value
                    dict_closedf[hash_i].set_g(i.get_g())
                    #In this condition we dont update the parent  --- PATH isnt neccessary
                    # heapify open_heap
                    dict_closedf[hash_i].set_cost(i.get_g() + func_heuristic)
                    heapq.heapify(list_openf)
                if hash_i not in dict_closedf:
                    # adding i in open_heap and closed_hash
                    heapq.heappush(list_openf, i)
                    dict_closedf[hash_i] = i
        #doing backward expansion
        else:
            n = heapq.heappop(list_openb)
            expand_bi_a_star +=1
            bacha = graph.successors(n)
            for i in bacha:
                X_change = abs(i.get_x()-start_state.get_x())
                Y_change = abs(i.get_y()-start_state.get_y())
                func_heuristic = 1.5*min(X_change, Y_change)+abs(X_change-Y_change)
                i.set_cost(i.get_g() + func_heuristic)
                hash_i = i.state_hash()
                if hash_i in dict_closedf:
                    cost = min(cost, dict_closedf[i.state_hash()].get_cost() + i.get_cost())
                if hash_i in dict_closedb and i < dict_closedb[hash_i]:
                    # updating closed_hash and open_heap with new g value
                    dict_closedb[hash_i].set_g(i.get_g())
                    #In this condition we dont update the parent  --- PATH isnt neccessary
                    # heapify open_heap
                    dict_closedb[hash_i].set_cost(i.get_g() + func_heuristic)
                    heapq.heapify(list_openb)
                if hash_i not in dict_closedb:
                    # adding i in open_heap and closed_hash
                    heapq.heappush(list_openb, i)
                    dict_closedb[hash_i] = i
    #plotting the map 
    #graph.plot_map(dict_closedb, start_state, goal_state, 'solution-maps/bi_A_stars/' + str(bi_num))
    #bi_num += 1
    return -1,expand_bi_a_star



#Defining a P_Value -- p(n) = max(f(n), 2 × g(n))
def P_value(self,goal_state):
    f_val = self.get_g() + func_heuristic(self,goal_state)
    return max(f_val,2*self.get_g())

#Making a heuristsics function so we can easily traverse through the meet in the middle code easily
def func_heuristic(self,goal_state):
    X_change = abs(self.get_x()-goal_state.get_x())
    Y_change = abs(self.get_y()-goal_state.get_y())
    return 1.5*min(X_change, Y_change)+abs(X_change-Y_change)



#Creating an code to implement the MM Algorithm -- The bidirectional search algorithm that uses the p-function is known as Meet in the Middle (MM 
def Middle_Meet(start_state,goal_state,graph):
    #Defining The initial states in the meet in the middle algorithm 
    global m_num
    list_openf = [start_state]
    list_openb = [goal_state]
    dict_closedf = {}
    dict_closedb = {}
    dict_closedf[start_state.state_hash()] = start_state
    dict_closedb[goal_state.state_hash()] = goal_state
    cost = 99999999999
    expanded_Middle_Meet = 0

    while len(list_openf)!=0 and len(list_openb)!=0:
        if  cost <= max(
            (list_openf[0].get_g() + list_openb[0].get_g()), 
            (func_heuristic(list_openf[0],goal_state)),
            (func_heuristic(list_openb[0],start_state)),
            (min(list_openf[0].get_cost(), list_openb[0].get_cost()))):
            return cost/2.0, expanded_Middle_Meet
        #Doing forward implementation
        if list_openf[0] < list_openb[0]:
            n = heapq.heappop(list_openf)
            expanded_Middle_Meet +=1
            bacha = graph.successors(n)
            for i in bacha:
                #implementing the heuristic function
                i.set_cost(P_value(i,goal_state))
                hash_i = i.state_hash()
                if hash_i in dict_closedb:
                    cost = min(cost, dict_closedb[i.state_hash()].get_cost() + i.get_cost())
                if hash_i in dict_closedf and i < dict_closedf[hash_i]:
                    # updating closed_hash and open_heap with new g value
                    dict_closedf[hash_i].set_g(i.get_g())
                    #In this condition we dont update the parent  --- PATH isnt neccessary
                    # heapify open_heap
                    dict_closedf[hash_i].set_cost(i.get_cost())
                    heapq.heapify(list_openf)
                if hash_i not in dict_closedf:
                    # adding i in open_heap and closed_hash
                    heapq.heappush(list_openf, i)
                    dict_closedf[hash_i] = i
        #Doing backward implementation
        else:
            n = heapq.heappop(list_openb)
            expanded_Middle_Meet +=1
            bacha = graph.successors(n)
            for i in bacha:
                #implementing the heuristic function 
                i.set_cost(P_value(i,start_state))
                hash_i = i.state_hash()
                if hash_i in dict_closedf:
                    cost = min(cost, dict_closedf[i.state_hash()].get_cost() + i.get_cost())
                if hash_i in dict_closedb and i < dict_closedb[hash_i]:
                    # updating closed_hash and open_heap with new g value
                    dict_closedb[hash_i].set_g(i.get_g())
                    #In this condition we dont update the parent  --- PATH isnt neccessary
                    # heapify open_heap
                    dict_closedb[hash_i].set_cost(i.get_cost())
                    heapq.heapify(list_openb)
                if hash_i not in dict_closedb:
                    # adding i in open_heap and closed_hash
                    heapq.heappush(list_openb, i)
                    dict_closedb[hash_i] = i
    #Plotting the map
    #graph.plot_map(dict_closedb, start_state, goal_state, 'solution-maps/Middle_Meet/' + str(bi_num))
    #bi_num += 1
    return -1,expanded_Middle_Meet

