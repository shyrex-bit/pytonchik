from participant import Participant


class Captain(Participant):
    
    def __init__(self, name: str, school_class: str, team_name: str):
        super().__init__(name, school_class)
        self.team_name = team_name

    def add_points(self, points: int):
        if points <= 0:
            return

        self._score += points + 2

    def get_role(self):
        return f"Капитан команды {self.team_name}"

    def __str__(self):
        return f"{self.name}, {self.school_class} класс — {self.score} баллов, роль: {self.get_role()}"