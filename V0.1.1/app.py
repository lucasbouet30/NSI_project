# START packages

# importation des tout les packets (pip install -r requirements.txt)
from flask import *
import flask_login
import json
import pickle
import hashlib
import re
import os
print("Current working directory:", os.getcwd())


# END packages

# ----------

# START flask instance

# creation de l'instance de flask pour y acceder aux méthodes par exemple
app = Flask(__name__)

# END flask instance

# ----------

# START login function

# initialisation du module de login / register de flask
app.secret_key = "rhapsopy"
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

# creation d'une classe pour définir qu'est ce qu'un user (couple email / mot de passe)
class User(flask_login.UserMixin): # type : user
    def __init__(self, email, password):
        # constructeur pour indiquer les infos
        self.id = email
        self.password = password
        
    def __str__(self):
        # méthode pour return quelque chose pour le débug
        return f"{self.id} | {self.password}"
        
        
# création d'une fonction permetant de hasher les mots de passes (str -> str)
# plus sécurisé / mots de passes cryptés et non en clair
def hash_it(data):
    # utilisation de hashlib
    a = hashlib.md5(data.encode())
    return a.hexdigest() # return un string
    
# permet de loads les datas au lancement du serveur flask (utilisateurs)
with open('data/users.pkl', 'rb') as file:
    # utilisation de pickle pour charger le tout dans un fichier .pkl (\data\users.pkl)
    users = pickle.load(file)
with open('data/vars.pkl','rb') as file1:
    # pareil
    varDB = pickle.load(file1) 


# fonction pour sauvegarder les utilisateurs
# e.g : ajouter un utilisateur lors du register et le mettre dans la database
def savedata():
    with open('data/users.pkl', 'wb') as file:
        # utilisation de pickle encore une fois
        pickle.dump(users, file)
# permet de sauvegarder les modifications (les variables)
def savemods():
    with open('data/vars.pkl', 'wb') as file:
        # utilisation de pickle encore une fois
        pickle.dump(varDB, file)
        
# END login function

# ----------

# START tests

# afficher la database
print(users)
print(varDB)
# la modifier avec juste un seul utilisateur pour le test 
varDB = {'test@gmail.com': {"el1":"coco", "el2":"cucu"}}
users = {'test@gmail.com':User('test@gmail.com',hash_it("testtest123."))}
# sauvegarder les données dans le fichier
savemods()
savedata()

# END tests

# ----------

# START login pages / methods

# mise en place du login_manager pour récupérer l'utilisateur en cours
@login_manager.user_loader
def user_loader(id):
    return users.get(id)
    
# la page de register (\templates\register.html)
@app.get("/register")
def register():
    return render_template("register.html")
    
# la page de register côté logique (post)
@app.post("/register")
def registerp():
    # on récupère les entrées utilisateur
    email = request.form["email"]
    password = request.form["password"]
    # on vérifie si l'email est un format valide soit : 
    # une partie alphanumérique avec lettres nombres et "." 
    # un @
    # une autre partie alphanumérique bla bla bla
    # un "."
    # et une partie avec des lettres 
    if re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        # on vérifie si l'email n'existe pas déjà sinon on ne peux pas créer un compte avec deux fois le meme email
        if email not in users:
            # on check si le mot de passe est assez grand (hé ouaip le truc chiant)
            if len(password) > 7:
                # on append l'utilisateur dans la database
                users[email] = User(email,hash_it(password)) # en le chiffrant et oui chef
                savedata()
                print(users)
                # on le redirige vers la page de login
                return redirect(url_for("login"))
                
    # bref tout les else
    
            else:
                flash("password must be greater than 7 characters")
                return redirect(url_for("register"))
        else:
            flash("email already exists")
            return redirect(url_for("register"))
    else :
        flash("invalid email")
        return redirect(url_for("register"))
    
# la page de login (\templates\login.html)
@app.get("/login")
def login():
    # flask render_template method
    return render_template('login.html')
    
# la page de logout (\templates\logout.html)
@app.route("/logout")
@flask_login.login_required
def logout():
    session['logged_in'] = False
    flask_login.logout_user()
    # déconexion de l'utilisateur grâce à cette fonction
    flash("You have been logged out")
    # alerte sur la page
    return render_template("logout.html")
    
# la page de login côté logique et server
@app.post("/login")
def loginp():
    # on récupère l'user correspondant à l'email (si il n'y en a pas, user = None)
    user = users.get(request.form["email"])
    remind = False if [] == request.form.getlist("remindme") else True
    print(f"remind me : {remind}")
    # vérification si, quelque chose est rentré ou, si le mot de passe crypté ne match pas avec celui de crypé dans la database
    if user is None or user.password != hash_it(request.form["password"]):
        # petite alerte pour indiquer que c'est faux
        flash("Incorrect password or email")
        return redirect(url_for("login"))
    # sinon on affiche la page
    flash("Welcome back !")
    session['logged_in'] = True
    # et on login l'user grâce à cette fonction
    print(user)
    flask_login.login_user(user,remember=remind)
    return redirect(url_for("profile"))
    
# END login pages / methods

# ----------

# START rendering webpages

#-
# permet de créer toutes les pages côté serveur
#-

server_on_start = False
@app.route('/')
def home():
    global server_on_start
    # Rendre le template "index.html"
    if server_on_start == False:
        session['logged_in'] = False
        server_on_start = True
    return render_template('index.html')
    
@app.route('/learning')
def learning():
    return render_template('learning.html')
    
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')
    
@app.route('/tools')
def tools():
    return render_template('tools.html')
    
@app.route('/planning')
def planning():
    return render_template('planning.html')
    
@app.route('/support')
def support():
    return render_template('support.html')

@app.route('/403')
def err403():
    return render_template('errors/403.html')

@flask_login.login_required
@app.route('/profile')
def profile():
    try :
        if session['logged_in'] == False:
            return redirect('403')
    except :
        return redirect('403')
    print(session['logged_in'])
    return render_template('profile.html')
    
# END rendering webpages

# ----------

# START flask server starting

# lance le serveur au lancement du fichier python
if __name__ == '__main__':
    app.run(debug=True)
    
# END flask server starting
