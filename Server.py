import mesa

from Model import Disease

def get_susceptible_agents(model):
    return f"Susceptible: {model.susceptible}"

def get_infected_agents(model):
    return f"Infected: {model.infected}"

def get_recovered_agents(model):
    return f"Recovered: {model.recovered}"

def disease_draw(agent):
    if agent is None:
        return
    
    portrayal = {"Shape": "circle", "r": 0.5, "Filled": "true", "Layer": 0}

    if agent.type == 0:
        portrayal["Color"] = ["#0000FF", "#9999FF"]
    elif agent.type == 1:
        portrayal["Color"] = ["#FF0000", "#FF9999"]
    elif agent.type == 2:
        portrayal["Color"] = ["#00FF00", "#99FF99"]
    return portrayal

canvas_element = mesa.visualization.CanvasGrid(disease_draw, 20, 20, 500, 500)
status_chart = mesa.visualization.ChartModule([{"Label": "susceptible", "Color": "Blue"}, {"Label": "infected", "Color": "Red"}, {"Label": "recovered", "Color": "Green"}])

model_params = {
    "height": 20,
    "width": 20,
    "density": mesa.visualization.Slider("Agent density", 0.8, 0.1, 1.0, 0.1),
    "i_0": mesa.visualization.Slider("Starting infected", 1, 1, 20, 1),
    "beta": mesa.visualization.Slider("Chance of being infected", 0.2, 0.05, 2, 0.05),
    "gamma": mesa.visualization.Slider("Chance of recovering", 0.1, 0.05, 2, 0.05),
}

server = mesa.visualization.ModularServer(
    Disease,
    [canvas_element, get_susceptible_agents, get_infected_agents, get_recovered_agents, status_chart],
    "Disease",
    model_params,
)
