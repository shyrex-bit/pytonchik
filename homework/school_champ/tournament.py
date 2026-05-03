from participant import Participant
from captain import Captain
from decorators import log_action


class Tournament:
    def __init__(self):
        self._participants = []

    def add_participant(self, participant: Participant):
        self._participants.append(participant)

    def show_participants(self):
        if not self._participants:
            print("Участников пока нет.")
            return

        for i, p in enumerate(self._participants, 1):
            print(f"{i}. {p}")

    def find_participant(self, name: str):
        for p in self._participants:
            if p.name == name:
                return p
        return None

    @log_action
    def add_points_to_participant(self, name: str, points: int):
        participant = self.find_participant(name)

        if not participant:
            print("Участник не найден.")
            return

        participant.add_points(points)

    @log_action
    def remove_points_from_participant(self, name: str, points: int):
        participant = self.find_participant(name)

        if not participant:
            print("Участник не найден.")
            return

        participant.remove_points(points)

    def show_rating(self):
        if not self._participants:
            print("Участников пока нет.")
            return

        sorted_list = sorted(self._participants, key=lambda p: p.score, reverse=True)

        print("Рейтинг турнира:")
        for i, p in enumerate(sorted_list, 1):
            print(f"{i}. {p.name} — {p.score} баллов")

    def get_winner(self):
        if not self._participants:
            print("Победителя пока нет.")
            return

        winner = max(self._participants, key=lambda p: p.score)
        print("Победитель турнира:", winner)

    def show_debug_info(self):
        for p in self._participants:
            print(p.__dict__)

    def __len__(self):
        return len(self._participants)