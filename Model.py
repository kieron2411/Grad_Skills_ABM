import mesa
import random

class DiseaseAgent(mesa.Agent):

    def __init__(self, pos, model, agent_type):
        super().__init__(pos, model)
        self.pos = pos
        self.type = agent_type  #susceptible = 0, infected = 1, recovered = 2

    def step(self):
        if self.type == 0:
            for neighbor in self.model.grid.iter_neighbors(self.pos, True):
                if neighbor.type == 1:
                    if self.random.random() <= self.model.beta:
                        self.type = 1
                        self.model.susceptible -= 1
                        self.model.infected += 1
                        break
                    

        elif self.type == 1:
            if self.random.random() <= self.model.gamma:
                self.type = 2
                self.model.infected -= 1
                self.model.recovered += 1

        else:
            ()

#        self.model.grid.move_to_empty(self)

class Disease(mesa.Model):

    def __init__(self, width=20, height=20, density=0.8, i_0=1, beta=0.2, gamma=0.1):
        self.width = width
        self.height = height
        self.density = density
        self.i_0 = i_0
        self.beta = beta
        self.gamma = gamma

        self.schedule = mesa.time.RandomActivation(self)
        self.grid = mesa.space.SingleGrid(width, height, torus=False)


        count = 0
        for cell in self.grid.coord_iter():
            x = cell[1]
            y = cell[2]
            if self.random.random() < self.density:
                if count < i_0:
                    agent_type = 1
                    count += 1
                else:
                    agent_type = 0

                agent = DiseaseAgent((x,y), self, agent_type)
                self.grid.place_agent(agent, (x,y))
                self.schedule.add(agent)

        self.susceptible = self.schedule.get_agent_count()-1
        self.infected = 1
        self.recovered = 0
        self.datacollector = mesa.DataCollector(
            {"susceptible": "susceptible", "infected": "infected", "recovered": "recovered"},
            {"x": lambda a: a.pos[0], "y": lambda a: a.pos[1]},
        )


        self.running = True
        self.datacollector.collect(self)

    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)

        if self.infected == 0:
            self.running = False

        
