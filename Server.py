#Credit goes to Project Mesa whose code this is based off of: https://github.com/projectmesa/mesa-examples/tree/main/examples/Schelling

import mesa     #imports the mesa module

from Model import Disease   #imports the item "Disease" from Model.py

def get_susceptible_agents(model):  #function to return the count of susceptible agents
    return f"Susceptible: {model.susceptible}"

def get_infected_agents(model): #function to return the count of infected agents
    return f"Infected: {model.infected}"

def get_recovered_agents(model):    #function to return the count of recovered agents
    return f"Recovered: {model.recovered}"

def get_dead_agents(model): #function to return the count of dead agents
    return f"Dead: {model.dead}"

def disease_draw(agent):    #function to return the data needed to visualise the data
    if agent is None:   #returns nothing if there are no agents
        return
    
    portrayal = {"Shape": "circle", "r": 0.5, "Filled": "true", "Layer": 0, "Label": agent.age} #makes each agent a filled circle with radius 0.5

    if agent.type == 0: #runs if the agent is susceptible
        portrayal["Color"] = ["#0000FF", "#9999FF"] #sets the colour to be blue
    elif agent.type == 1:   #runs if the agent is infected
        portrayal["Color"] = ["#FF0000", "#FF9999"] #sets the colour to be red
    elif agent.type == 2:   #runs if the agent is recovered
        portrayal["Color"] = ["#00FF00", "#99FF99"] #sets the colour to be green
    elif agent.type == 3:   #runs if the agent is dead
        portrayal["Color"] = ["#000000", "#999999"] #sets the colour to be gray
    return portrayal

canvas_element = mesa.visualization.CanvasGrid(disease_draw, 100, 100, 1000, 1000)  #creates a canvas with the information from "disease_draw", 20*20 cells and 500*500 pixels
status_chart = mesa.visualization.ChartModule([{"Label": "susceptible", "Color": "Blue"}, {"Label": "infected", "Color": "Red"}, {"Label": "recovered", "Color": "Green"}, {"Label": "dead", "Color":"Black"}]) #sets up a graph to plot the amount of each type of agent over time

model_params = {
    "height": 100,
    "width": 100,
    "density": mesa.visualization.Slider("Agent density", 0.5, 0.1, 1.0, 0.1),  #creates a slider for the population density. Default value 0.8, lowest value 0.1, highest value 1.0, jump of 0.1
    "i_0": mesa.visualization.Slider("Starting infected", 1, 1, 20, 1), #creates a slider for the starting infected. Default value 1, lowest value 1, highest value 20, jump of 1
    "beta": mesa.visualization.Slider("Chance of being infected", 0.4, 0.01, 1.0, 0.01),  #creates a slider for the chance of being infected. Default value 0.4, lowest value 0.01, highest value 1.0, jump of 0.01
    "gamma_0": mesa.visualization.Slider("Chance of recovering at age 10", 0.1, 0.01, 1.0, 0.01),   #creates a slider for the chance of recovering at age 10. Default value 0.1, lowest value 0.01, highest value 1.0, jump of 0.01
    "gamma_1": mesa.visualization.Slider("Chance of recovering at age 80", 0.05, 0.01, 1.0, 0.01),  #creates a slider for the chance of recovering at age 80. Default value 0.05, lowest value 0.01, highest value 1.0, jump of 0.01
    "delta_0": mesa.visualization.Slider("Chance of dying at age 10", 0.01, 0.01, 1.0, 0.01),   #creates a slider for the chance of dying at age 10. Default value 0.01, lowest value 0.01, highest value 1.0, jump of 0.01
    "delta_1": mesa.visualization.Slider("Chance of dying at age 80", 0.05, 0.01, 1.0, 0.01),   #creates a slider for the chance of recovering at age 80. Default value 0.05, lowest value 0.01, highest value 1.0, jump of 0.01
}   #defines the parameters for the simulation

server = mesa.visualization.ModularServer(
    Disease,
    [canvas_element, get_susceptible_agents, get_infected_agents, get_recovered_agents, get_dead_agents, status_chart],
    "Disease",
    model_params,
)   #defines the information to run the simulation and plot the data
