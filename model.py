import random
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.animation import FuncAnimation
import requests
import bs4
import matplotlib.pyplot as plt
import agentframework
import csv

import tkinter
plt.ioff() # This prevents matplotlib from plotting a figure in spyder

num_of_agents = 10 # Total number of agents
num_of_iterations = 100  # Total number of iterations
neighbourhood = 20  # shortest distance before agents share the environment
environment = []
agents = []

agent_x =[]
agent_y = []

# Web scrapping
r = requests.get('http://www.geog.leeds.ac.uk/courses/computing/practicals/python/agent-framework/part9/data.html')  # This grabs the website in the quatation marks
content = r.text #This grabs all the contents of the website between quotation marks
soup = bs4.BeautifulSoup(content, 'html.parser')
td_ys = soup.find_all(attrs={"class" : "y"})  # This grasps all html elements with classes y
td_xs = soup.find_all(attrs={"class" : "x"})  # This grasps all html elements with classes x

# Oppening the csv file in the same folder
with open("in.txt") as raster_file: # Open csv file within the same folder
    raster_rows = csv.reader(raster_file, delimiter=",") #reading all the content in the csv file
    
    # This loop gets all the rows in the csv
    for raster_row in raster_rows: 
        # This loop gets all the content within a row
        rowlist = []
        for raster_value in raster_row:
            rowlist.append(float(raster_value)) # Adding csv value to rowlist list
        environment.append(rowlist)
    raster_file.close()
        
# Make the agents.
for i in range(num_of_agents):
    y = int(td_ys[i].text)
    x = int(td_xs[i].text)
    agents.append(agentframework.Agent(environment, agents, y, x)) # Initializing all the 10 agents
        
fig = plt.figure(figsize=(6,6))  # Creating a matplotlib figure
ax = plt.axes(xlim=(0,99),ylim=(0,99))  # creating axes to where graphs and images can be displayed

for i in range(num_of_agents):
    agent_x.append(agents[i].x)
    agent_y.append(agents[i].y)
    
scat = ax.scatter(agent_x,agent_y)  # creating a scatter plot to show agents

for j in range(num_of_iterations):
    for i in range(num_of_agents):
        random.shuffle(agents)
        agents[i].move()  # calling move method
        agents[i].eat()  # calling eat method
        agents[i].share_with_neighbours(neighbourhood)  # callling share with neighbours menthod


# The function bellow creates an animation of agents
def update(j): 
    global scat, agents
    random.shuffle(agents)
    scat.remove()  # This destroys the previous scatter plot
    agent_x.clear()
    agent_y.clear()
    
    # The loop creates new coordinates for the agest so that the agents can change location
    for i in range(num_of_agents):
        random.shuffle(agents)
        agents[i].move()
        
        agent_x.append(agents[i].x)  # Creating new x coordinates for the new scatter plots
        agent_y.append(agents[i].y)  # Creating new y coordinates for the new scatter plots
    scat = ax.scatter(agent_x,agent_y) # This creates new scatter plots

ax.imshow(environment)  # This displays the environment in the axis ax
        
# Graphical user interface
root = tkinter.Tk()  # initializing the tkinter GUI
root.wm_title("Model")
canvas = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(fig, master=root)
canvas._tkcanvas.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

anim = FuncAnimation(fig, update, frames=[x for x in range(num_of_iterations)], interval=500)  # initializing scatterplot animation

tkinter.mainloop()
