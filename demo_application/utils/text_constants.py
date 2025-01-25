# constants.py
class Texts:
    def __init__(self, language="en"):
        self.language = language
        self.texts = {
            "en": {
                "page_title": "Belot Card Game Tracker",
                "title": "Belot Card Game Tracker",
                "team_scores": "Team Scores",
                "stats_actions": "Stats Actions",
                "team_a": "Team A",
                "team_b": "Team B",
                "cards_team_a": "Cards for Team A",
                "cards_team_b": "Cards for Team B",
                "points": "points",
                "take_snapshot": "Take Snapshot",
                "capturing_cards": "Capturing cards... Please wait.",
                "cards_detected": "Cards detected successfully!",
                "no_cards_detected": "No valid cards detected. Please try again.",
                "flip_cards": "Flip cards",
                "scoring_options": "Scoring Options",
                "game_mode": "Select Game Mode",
                "bonus_points_team_a": "Bonus Points (Team A)",
                "bonus_points_team_b": "Bonus Points (Team B)",
                "team_a_last_10": "Team A won last 10?",
                "update_scores": "Update Scores",
                "scores_updated": "Scores updated successfully!",
                "revert_last_round": "Revert last round",
                "start_new_game": "Start new game",
                "new_game_started": "New game started successfully!",
                "game_modes": ["All Trumps", "No Trumps", "Spades", "Hearts", "Diamonds", "Clubs"],
            },
            "bg": {
                "page_title": "Счетоводител за Игра на Белот",
                "title": "Счетоводител за Игра на Белот",
                "team_scores": "Резултат",
                "stats_actions": "Извличане на ръце",
                "team_a": "Отбор А",
                "team_b": "Отбор Б",
                "cards_team_a": "Карти от ръце на Отбор А",
                "cards_team_b": "Карти от ръце на Отбор Б",
                "points": "точки",
                "take_snapshot": "Извличане на карти",
                "capturing_cards": "Извличане на карти... Моля изчакайте.",
                "cards_detected": "Картите са открити успешно!",
                "no_cards_detected": "Не са открити валидни карти. Моля опитайте отново.",
                "flip_cards": "Размени картите",
                "scoring_options": "Опции за раздаването",
                "game_mode": "Избор на Режим на игра",
                "bonus_points_team_a": "Анонси (Отбор А)",
                "bonus_points_team_b": "Анонси (Отбор Б)",
                "team_a_last_10": "Отбор А спечели последно 10?",
                "update_scores": "Добавяне на резултата",
                "scores_updated": "Резултатите са обновени успешно!",
                "revert_last_round": "Отмени резултат",
                "start_new_game": "Започване на нова игра",
                "new_game_started": "Нова игра започната успешно!",
                "game_modes": ["Всички Коз", "Без Коз", "Пика", "Купа", "Каро", "Спатия"],
            },
        }

    def get(self, key):
        return self.texts[self.language].get(key, key)

    def get_modes(self):
        return self.texts[self.language]["game_modes"]
