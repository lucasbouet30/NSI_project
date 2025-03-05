import math
import sqlite3

class leveling:
    def __init__(self):
        self.BASE_XP = 100  # l'xp doit toujours être supérieur a 100 pour avoir un résultat positif
        self.SCALING_FACTOR = 1.5  # Facteur pour augmenter la difficulté
        self.TITLES = {
            1: "Apprenti", 
            5: "Maestro", 
            10: "Virtuose", 
            15: "Disciple de Rhapsode", 
            20: "Apôtre de Rhapsode", 
            25: "Incarnation de Rhapsode"}
        
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
        for title, expReq in enumerate(self.TITLES):
            if lvl >= expReq:
                return title
        

    def get_user_info(self, user_id):
        """Récupère les informations de l'utilisateur depuis la base de données."""
        conn = sqlite3.connect('rhapsody.db')
        cursor = conn.cursor()
        
        cursor.execute('SELECT exp, lvl, title FROM users WHERE id = ?', (user_id,))
        user_info = cursor.fetchone()
        
        conn.close()
        
        if user_info:
            exp, lvl, title = user_info
            next_lvl_xp = self.calculate_xp_for_next_lvl(lvl + 1)
            return {
                'exp': exp,
                'lvl': lvl,
                'title': title,
                'next_lvl_xp': next_lvl_xp
            }
        return None

    # Exemple d'utilisation
    if __name__ == "__main__":
        user_id = 1  # ID de l'utilisateur
        current_exp = 15000  # Expérience actuelle de l'utilisateur

        update_user_lvl(user_id, current_exp)
        user_info = get_user_info(user_id)

        if user_info:
            print(f"Niveau actuel : {user_info['lvl']}")
            print(f"Titre : {user_info['title']}")
            print(f"XP : {user_info['exp']} / {user_info['next_lvl_xp']}")
        else:
            print("Utilisateur non trouvé.")
