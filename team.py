class Team:

    def __init__(self, quiz, name):
        self.name = name
        self.players = []
        self.score = 0
        self.text_color = (5, 5, 5)
        self.bg_color = quiz.settings.colors[name]
        self.display_side = quiz.settings.sides[name]

    def add_player(self, player):
        self.players.append(player)
        player.team = self

    def remove_player(self, player):
        self.players.remove(player)

    def update_score(self):
        self.score = sum([player.score for player in self.players])