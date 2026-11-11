import agentpy as ap

MOVES = [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 1), (-1, 0)] 

class Particle(ap.Agent):
    stuck: bool

    def setup(self):
        self.stuck = False

    def step(self):
        if self.stuck:
            return
        
        move = self.model.random.choice(MOVES)
        p0, p1 = self.model.grid.positions[self]
        new_position = (p0 + move[0], p1 + move[1])
        if new_position in self.model.grid.empty:
            self.model.grid.move_to(self, new_position)

        if self.can_stick():
            self.stuck = True


    def can_stick(self) -> bool:
        neighbors = self.model.grid.neighbors(self, distance=1).to_list()
        return any(neighbor.stuck for neighbor in neighbors)