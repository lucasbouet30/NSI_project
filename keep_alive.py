# Fichier permettant de simuler une activité régulière sur render
# on peut de ce fait avoir un site toujours actif (host sur render gratuit)

from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
  return "Rhapsopy a le coeur qui bat !"

def run():
  app.run(host='0.0.0.0', port=8080)

def keep_alive():
  t = Thread(target=run)
  t.start()
