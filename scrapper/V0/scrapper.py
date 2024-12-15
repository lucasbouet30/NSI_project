import requests
from bs4 import BeautifulSoup

class Scrapper:
    def __init__(self, music):
        self.music = music
        self.link = None
        self.base = "https://www.songsterr.com/"
        self.links = []
        self.difficulties = {}
        self.booted = False
        
    def get_full_link(self):
        temp = self.music
        self.link = self.base + f"?pattern={temp.replace(' ', '%20')}"
                
    def load_link(self):
        self.get_full_link()
        self.req = requests.get(self.link)
        if self.req.status_code == 200:
            soup = BeautifulSoup(self.req.text, 'html.parser')

            # Trouver toutes les balises <a> avec la classe "B0cew"
            elements = soup.find_all('a', class_='B0cew')

            # Récupérer les liens dans un tableau
            self.links = [self.base + elem['href'][1:] for elem in elements if 'href' in elem.attrs]
            self.booted = True
        else:
            print(f"Erreur : impossible d'accéder à la page ({self.req.status_code})")
            
        return self.links
        
    def get_dificulties(self):
        if not self.booted :
            raise Exception("use load_link() to load your url before :( ")
        self.req = requests.get(self.link)
        if self.req.status_code == 200:
            soup = BeautifulSoup(self.req.text, features="lxml")
            elements = soup.find_all('span', class_='B7220c')
            temp = 0
            for element in elements :
                level = element.get("title")
                level = level.split(".",1)
                if level[0] != "Not":
                    self.difficulties[self.links[temp]] = {"level" : level[0], "tier" : level[1].strip()}
                else:
                    self.difficulties[self.links[temp]] = None
                temp += 1

            return self.difficulties

    def iframe(self, **kwargs):
        if not self.booted :
            raise Exception("use load_link() to load your url before :( ")
        if kwargs.get("l",None) != None and kwargs["l"] >= len(self.links):
            raise Exception("link number must be lower than the max links number")
        w = kwargs.get("w", 100)
        h = kwargs.get("h", 100)
        t = kwargs.get("k", self.music)
        class_ = kwargs.get("c", "tab-iframe")
        default = self.links[0] if kwargs.get("l", None) == None else self.links[kwargs["l"]]

        return f"<iframe width='{w}' height='{h}' title='{t}' class='{class_}' src='{default}'></iframe>"


 # tests   
#scrapper = Scrapper("bones imagine dragon")
#links = scrapper.load_link()
#print(links)
#print(scrapper.iframe())
