import mesa     #imports the "mesa" module. This module is used for Agent Based Modelling

class DiseaseAgent(mesa.Agent): #defines a class called "DiseaseAgent" that inherits from the Agent class from the mesa module

    def __init__(self, pos, model, agent_type): #initialises the class with these variables
        super().__init__(pos, model)    #makes this class inherit from the Agent class
        self.pos = pos  #sets up the position of the agent
        self.type = agent_type  #susceptible = 0, infected = 1, recovered = 2

    def step(self): #defines what happens to each agent at each step
        if self.type == 0:  #this block happens if the agent is currently susceptible
            infected_neighbors = 0  #sets up a counter for the infected neighbors
            for neighbor in self.model.grid.iter_neighbors(self.pos, True): #counts how many neighbors are currently infected
                if neighbor.type == 1:
                    infected_neighbors += 1
                    
            for i in range(infected_neighbors): #for every infected neighbor it will run this block
                if self.random.random() <= self.model.beta: #generates a random number and checks if it is less than "beta" (chance of being infected)
                    self.type = 1   #sets the agent to be infected
                    self.model.susceptible -= 1     #removes 1 from the count of susceptible agents
                    self.model.infected += 1    #adds 1 to the count of infected agents
                    break   #stops running the for loop
                    
        elif self.type == 1:    #this block happens if the agent is currently infected
            if self.random.random() <= self.model.gamma:    #generates a random number and checks if it is less than "gamma" (chance of recovering)
                self.type = 2   #sets the agent to be recovered
                self.model.infected -= 1    #removes 1 from the count of infected agents
                self.model.recovered += 1   #adds 1 to the count of recovered agents

        else:   #this block happens if the agent is currently recovered
            ()  #does nothing

#        self.model.grid.move_to_empty(self)    #randomises the position of all agents in the grid

class Disease(mesa.Model):  #defines a class called "Disease" that inherits from the Model class from the mesa module

    def __init__(self, width=20, height=20, density=0.8, i_0=1, beta=0.2, gamma=0.1):   #initialises the class with these variables (with default values)
        self.width = width  #sets the grid's width 
        self.height = height    #sets the grid's height
        self.density = density  #sets the population density of the grid
        self.i_0 = i_0  #sets the starting count of infected agents
        self.beta = beta    #sets the chance of being infected
        self.gamma = gamma  #sets the chance of recovering

        self.schedule = mesa.time.RandomActivation(self)    #activates every agent in a random order each time step
        self.grid = mesa.space.SingleGrid(width, height, torus=False)   #creates a width*height sized grid (that does not wrap around)

        count = 0   #sets up a counter for how many agents have been placed
        for cell in self.grid.coord_iter(): #for every cell in the grid, it will run this block
            x = cell[1] #sets x equal to the x coordinate of the cell
            y = cell[2] #sets y equal to the y coordinate of the cell
            if self.random.random() < self.density: #generates a random number, runs this block if that number is less than the density
                if count < i_0: #runs this block if the counter is less than the amount of initial infected agents
                    agent_type = 1  #sets the agent to be infected
                    count += 1  #ups the count by 1
                else:   #runs this block if the previous did not run
                    agent_type = 0  #sets the agent to be susceptible

                agent = DiseaseAgent((x,y), self, agent_type)   #sets an agent up with its position and type
                self.grid.place_agent(agent, (x,y)) #places the agent in the grid
                self.schedule.add(agent)    #adds the agent to the scheduler

        self.susceptible = self.schedule.get_agent_count()-i_0    #sets the count of susceptible agents equal to the total count minus the starting infected amount
        self.infected = i_0   #sets the count of infected agents equal to the starting number of infected agents
        self.recovered = 0  #sets the count of recovered agents equal to 0
        self.datacollector = mesa.DataCollector(
            {"susceptible": "susceptible", "infected": "infected", "recovered": "recovered"},
            {"x": lambda a: a.pos[0], "y": lambda a: a.pos[1]},
        )   #gathers the amount of each type of agent along with their position?


        self.running = True #sets the status to be running
        self.datacollector.collect(self)    #collects the data?

    def step(self): #defines what happens at each step
        self.schedule.step()    #moves the scheduler forward one step
        self.datacollector.collect(self)    #collects the data?

        if self.infected == 0:  #if the amount of infected agents is 0, runs this
            self.running = False    #stops the code from running

        
