class Participant:
    def __init__(self, name: str, school_class: str):
        self.name = name
        self.school_class = school_class
        self._score = 0

    @property
    def score(self):
        return self._score

    @property
    def status(self):
        if self._score == 0:
            return "нет баллов"
        elif self._score >= 50:
            return "лидер"
        return "участник"

    def add_points(self, points: int):
        if points <= 0:
            return

        self._score += points

    def remove_points(self, points: int):
        if points <= 0:
            return

        self._score -= points

        if self._score < 0:
            self._score = 0

    def get_role(self):
        return "Участник"

    def __str__(self):
        return f"{self.name}, {self.school_class} класс — {self.score} баллов, роль: {self.get_role()}"

    def __repr__(self):
        return f"Participant(name='{self.name}', school_class='{self.school_class}', score={self.score})"