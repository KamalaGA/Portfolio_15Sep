import random

class Agent:

    def __init__(self, environment, agents, y, x):
        if (x == None):
            self.x = random.randint(0,100)
        else:
            self.x = x
        if (y == None):
            self.y = random.randint(0,100)
        else:
            self.y = y
        self.environment = environment
        self.store = 0
        self.agents = agents
        

    def distance_between(self, agents_row_a):
        return (((agents_row_a.x - self.x)**2) +
        ((agents_row_a.y - self.y)**2))**0.5

    def set_x(self, new_x_value):
        self.x = new_x_value

    def set_y(self, new_y_value):
        self.y = new_y_value

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def move(self):
       if random.random() < 0.5:
           self.set_x((self.get_x() - 1) % 100)
       else:
           self.set_x((self.get_x() + 1) % 100)
       if random.random() < 0.5:
           self.set_y((self.get_y() - 1) % 100)
       else:
           self.set_y((self.get_y() + 1) % 100)
           
    def eat(self):
        if self.environment[self.y][self.x] > 10:
            self.environment[self.y][self.x] -= 10
            self.store += 10
        else:
            self.store += self.environment[self.y][self.x]

    def share_with_neighbours(self, neighbourhood):
        for agent in self.agents:
            distance = self.distance_between(agent)
            if distance <= neighbourhood:
                store_sum = self.store + agent.store
                average = store_sum / 2
                self.store = average
                agent.store = average
                
