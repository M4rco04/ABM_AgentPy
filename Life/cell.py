import agentpy as ap

class Cell(ap.Agent):

    def setup(self):
        prob_alive = self.p.initial_density
        self.state = int(self.model.random.random() < prob_alive)

    def calculate_next_state(self):
        neighbors = self.model.grid.neighbors(self)
        alive_neighbors = sum(n.state for n in neighbors)
        
        if self.state == 1 and alive_neighbors in (2, 3):
            self.next_state = 1
        elif self.state == 0 and alive_neighbors == 3:
            self.next_state = 1
        else:
            self.next_state = 0

    def apply_next_state(self):
        self.state = self.next_state