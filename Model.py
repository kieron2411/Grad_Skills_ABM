#Credit goes to Project Mesa whose code this is based off of: https://github.com/projectmesa/mesa-examples/tree/main/examples/Schelling

import mesa     #imports the "mesa" module. This module is used for Agent Based Modelling
import random

class DiseaseAgent(mesa.Agent): #defines a class called "DiseaseAgent" that inherits from the Agent class from the mesa module

    def __init__(self, pos, model, agent_type, age): #initialises the class with these variables
        super().__init__(pos, model)    #makes this class inherit from the Agent class
        self.pos = pos  #sets up the position of the agent
        self.type = agent_type  #susceptible = 0, infected = 1, recovered = 2, dead = 3
        self.age = age

    def move(self): #defines how the agents move
        if self.type == 3:  #checks if the agent is dead
            pass    #does nothing
        else:
            x, y = self.pos #sets "x" and "y" equal to the x and y coordinates of the agent
            new_position = (x+random.randint(-1,1), y+random.randint(-1,1)) #sets the new coordinates equal to the current ones +- 1
            try:    #trys running the following line
                self.model.grid.move_agent(self, new_position)  #moves the agent to the new position
            except: #runs this if the previous line results in an error (will happen if there is already an agent in the new location
                self.model.grid.move_agent(self, (x,y)) #keeps the agent in its current position

    def step(self): #defines what happens to each agent at each step
        if self.type == 0:  #this block happens if the agent is currently susceptible
            infected_neighbors = 0  #sets up a counter for the infected neighbors
            for neighbor in self.model.grid.iter_neighbors(self.pos, False): #counts how many neighbors are currently infected
                if neighbor.type == 1:
                    infected_neighbors += 1
                    
            for i in range(infected_neighbors): #for every infected neighbor it will run this block
                if self.random.random() <= self.model.beta: #generates a random number and checks if it is less than "beta" (chance of being infected)
                    self.type = 4   #sets the agent to be a temporary type which will be changed to infected
                    self.model.susceptible -= 1     #removes 1 from the count of susceptible agents
                    self.model.infected += 1    #adds 1 to the count of infected agents
                    break   #stops running the for loop
                    
        elif self.type == 1:    #this block happens if the agent is currently infected
            recover_chance = (((self.model.gamma_1-self.model.gamma_0)/70)*(self.age-10))+self.model.gamma_0     #equation of a straight line passing through recovery rate for age 10 and 80
            death_chance = (((self.model.delta_1-self.model.delta_0)/70)*(self.age-10))+self.model.delta_0   #equation of a straight line passing through death rate for age 10 and 80
            if self.random.random() <= recover_chance:    #generates a random number and checks if it is less than "recover_chance"
                self.type = 5   #sets the agent to be a temporary type which will be changed to recovered
                self.model.infected -= 1    #removes 1 from the count of infected agents
                self.model.recovered += 1   #adds 1 to the count of recovered agents
            elif self.random.random() <= death_chance:  #generates a random number and checks if it is less than "death_chance"
                self.type = 3   #sets the agetn to be dead
                self.model.infected -= 1    #removes 1 from the count of infected agents
                self.model.dead += 1    #adds 1 to the count of dead agents

        else:   #this block happens if the agent is currently recovered
            ()  #does nothing

    def advance(self):  #defines what happens to each agent at each step once the step is complete
        if self.type == 4:  #this block happens if the agent is currently of the temporary infected type
            self.type = 1   #converts the agent to be infected
        elif self.type == 5:    #this block happens if the agent is currently of the temporary recovered type
            self.type = 2   #converts the agent to be recovered
        self.move() #moves the agents

class Disease(mesa.Model):  #defines a class called "Disease" that inherits from the Model class from the mesa module

    def __init__(self, width=50, height=50, density=0.5, i_0=1, beta=0.2, gamma_0=0.2, gamma_1=0.1, delta_0=0.01, delta_1=0.05):   #initialises the class with these variables (with default values)
        self.width = width  #sets the grid's width 
        self.height = height    #sets the grid's height
        self.density = density  #sets the population density of the grid
        self.i_0 = i_0  #sets the starting count of infected agents
        self.beta = beta    #sets the chance of being infected
        self.gamma_0 = gamma_0  #sets the chance of recovering at age 10
        self.gamma_1 = gamma_1  #sets the chance of recovering at age 80
        self.delta_0 = delta_0  #sets the chance of dying at age 10
        self.delta_1 = delta_1  #sets the chance of dying at age 80

        self.schedule = mesa.time.SimultaneousActivation(self)    #activates every agent at once each time step
        self.grid = mesa.space.SingleGrid(width, height, torus=False)   #creates a width*height sized grid (that does not wrap around)

        xi_0 = random.sample(range(0, height), i_0) #generates a random list of i_0 amount of x coordinates
        yi_0 = random.sample(range(0, width), i_0)  #generates a random list of i_0 amount of y coordinates
        starting_infected = []  #creates an empty list
        for i in range(i_0):    #runs this block i_0 times
            starting_infected.append((xi_0[i], yi_0[i]))    #appends each of the x and y coordinates to the list

        for cell in starting_infected:  #for every randomly generated cell from above, it will run this block
            agent_type = 1  #sets the agent to be infected
            age = random.randint(10,80)
            agent = DiseaseAgent(cell, self, agent_type, age)    #sets an agent up with its position and type
            self.grid.place_agent(agent, cell)  #places the agent in the grid
            self.schedule.add(agent)    #adds the agent to the scheduler

        for cell in self.grid.coord_iter(): #for every cell in the grid, it will run this block
            x = cell[1] #sets x equal to the x coordinate of the cell
            y = cell[2] #sets y equal to the y coordinate of the cell
            if (x,y) in starting_infected:  #checks if the cell is one of the generated infected 
                pass    #does nothing if so
            elif self.random.random() < self.density: #generates a random number, runs this block if that number is less than the density. Only checks if the previous fails
                agent_type = 0  #sets the agent to be susceptible
                age = random.randint(10,80)
                agent = DiseaseAgent((x,y), self, agent_type, age)   #sets an agent up with its position, type and age
                self.grid.place_agent(agent, (x,y)) #places the agent in the grid
                self.schedule.add(agent)    #adds the agent to the scheduler            

        self.susceptible = self.schedule.get_agent_count()-i_0    #sets the count of susceptible agents equal to the total count minus the starting number of infected
        self.infected = i_0   #sets the count of infected agents equal to the starting number of infected agents
        self.recovered = 0  #sets the count of recovered agents equal to 0
        self.dead = 0
        self.datacollector = mesa.DataCollector(
            {"susceptible": "susceptible", "infected": "infected", "recovered": "recovered", "dead": "dead"},
            {"x": lambda a: a.pos[0], "y": lambda a: a.pos[1]},
        )   #gathers the amount of each type of agent along with their position?


        self.running = True #sets the status to be running
        self.datacollector.collect(self)    #collects the data?

    def step(self): #defines what happens at each step
        self.schedule.step()    #moves the scheduler forward one step
        self.datacollector.collect(self)    #collects the data?

        if self.infected == 0:  #if the amount of infected agents is 0, runs this
            self.running = False    #stops the code from running
