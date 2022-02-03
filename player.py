class Player:

    def __init__(self, name):
        self.name = name
        self.team = None
        self.score = 0

    def score_points(self, points):
        self.score += points
        self.team.update_score()
