import math

class leveling:
    def __init__(self):
        self.BASE_XP = 100
        self.SCALING_FACTOR = 1.5
        self.TITLES = {
            1: ["Apprenti", "static/assets/images/RankIcons/1_rank_icon.svg"],
            5: ["Maestro", "static/assets/images/RankIcons/2_rank_icon.svg"],
            10: ["Virtuose", "static/assets/images/RankIcons/3_rank_icon.svg"],
            15: ["Disciple de Rhapsode", "static/assets/images/RankIcons/4_rank_icon.svg"],
            20: ["Apôtre de Rhapsode", "static/assets/images/RankIcons/5_rank_icon.svg"],
            25: ["Incarnation de Rhapsode", "static/assets/images/RankIcons/6_rank_icon.svg"],
            "trop": ["Rhapsode", "static/assets/images/RankIcons/6_rank_icon.svg"]
        }
    def find_username(self, email):
        """Extrait le nom d'utilisateur d'une adresse e-mail."""
        parts = email.split('@')
        # Retourner la partie avant le '@'
        return parts[0]


    def calculate_lvl(self, exp):
        """Calcule le niveau basé sur l'expérience."""
        return int(math.log(exp / self.BASE_XP, self.SCALING_FACTOR) + 1)

    def calculate_xp_for_next_lvl(self, exp):
        """Calcule l'XP nécessaire pour le prochain niveau."""
        lvl = self.calculate_lvl(exp)
        return int(self.BASE_XP * (self.SCALING_FACTOR ** (lvl - 1)))

    def get_title(self, exp):
        """Retourne le titre correspondant au niveau."""
        lvl = self.calculate_lvl(exp)

        reste = lvl % 5
        if lvl <= 1:
            return self.TITLES[1][0]
        elif reste == 0:
            return self.TITLES[lvl][0]
        elif lvl > 25:
            return self.TITLES['trop'][0]
        else:
            print(lvl - reste)
            return self.TITLES[lvl - reste][0]
    
    def get_badge(self, exp):
        """Retourne le chemin vers le svg du badge correspondant au niveau."""
        lvl = self.calculate_lvl(exp)

        reste = lvl % 5
        if lvl <= 1:
            return self.TITLES[1][1]
        elif reste == 0:
            return self.TITLES[lvl][1]
        elif lvl > 25:
            return self.TITLES['trop'][1]
        else:
            print(lvl - reste)
            return self.TITLES[lvl - reste][1]
