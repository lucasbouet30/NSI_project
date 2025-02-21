# START packages

# importation des tout les packets (pip install -r requirements.txt)
from flask import *
import flask_login
import json
import dill as pickle
import hashlib
import re
import os
import minechordify as chordify
import minescrapper as scrapper
import minefa2 as fa2
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
    def __init__(self, email, password, discordId=101):
        # constructeur pour indiquer les infos
        self.id = email
        self.password = password
        self.discordId = discordId
        
    def reset_mdp(self, passw):
        self.password = hash_it(passw)
        
    def __str__(self):
        # méthode pour return quelque chose pour le débug
        return f"{self.id} | {self.password}"
        
        
# création d'une fonction permetant de hasher les mots de passes (str -> str)
# plus sécurisé / mots de passes cryptés et non en clair
def hash_it(data):
    # utilisation de hashlib
    a = hashlib.md5(data.encode())
    return a.hexdigest() # return un string


# server purpose only (temp)
users = {'test@gmail.com': User('test@gmail.com', hash_it("testtest123."), 600288096046678036)}
with open('data/users.pkl', 'wb') as file:
    pickle.dump(users, file)

varDB = {'test@gmail.com': {"el1":"coco", "el2":"cucu"}}
with open('data/vars.pkl', 'wb') as file:
    pickle.dump(users, file)
# end



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
users = {'test@gmail.com':User('test@gmail.com',hash_it("testtest123."), 600288096046678036)}
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
    typed_discord_id = request.form["discord-id"]
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
                if typed_discord_id != None and typed_discord_id != 0:
                    users[email] = User(email,hash_it(password), typed_discord_id) # en le chiffrant et oui chef
                    savedata()
                    print(users)
                else:
                    users[email] = User(email,hash_it(password)) # en le chiffrant et oui chef
                    savedata()
                    print(users)
                # on le redirige vers la page de login
                return redirect(url_for("login"))
                
    # bref tous les else
    
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
    LOGIN_ERROR = None

    # Retrieve user based on email (safe handling of potential None value)
    user = users.get(request.form["email"])

    # Extract "remindme" checkbox value (improved handling of empty list)
    remind = request.form.getlist("rememberme")  # Returns an empty list if not checked
    remind = remind[0] if remind else False  # Extract first element (if present) or set to False

    # Validate credentials and handle errors gracefully
    if user is None:
        LOGIN_ERROR = "Invalid email or account not found."
    elif not user.password == hash_it(request.form["password"]):
        LOGIN_ERROR = "Incorrect password."

    if LOGIN_ERROR is not None:
        # Flash error message for display on login page
        flash(LOGIN_ERROR, 'error')  # Specify category for styling (optional)
        return redirect(url_for("login"))  # Redirect back to login page

    # Successful login:
    flash("Bon retour parmis nous !", 'success')  # Flash success message for display
    session['logged_in'] = True
    flask_login.login_user(user, remember=remind)
    return redirect(url_for("profile"))  # Redirect to profile page
    
# END login pages / methods

print('Compte test : \n test@gmail.com \n testtest123.')

@app.post("/2fareset")
def fa2resetp():
    if request.method == 'POST':
        ERROR_CODE = None
        DISPLAY_FORM = None
        if 'send_message' in request.form:
            # fa2.send_2fa()
            # users = {'test@gmail.com': User('test@gmail.com', hash_it("testtest123."), 1123456677654432)}
            email = request.form["email"]
            print(email == "")
            if email != "" and email in users:
                global current_user_2fa
                current_user_2fa = users.get(email)
                user_discord_id = current_user_2fa.discordId
                global code_generated
                print(user_discord_id)
                code_generated = fa2.send_2fa(str(user_discord_id))
                print(code_generated)
                if code_generated == 101:
                    flash("invalid discord id", "errormail")
            else:
                ERROR_CODE = "Invalide email ou email vide"
                flash(ERROR_CODE, 'erroremail')
                print(f"flashed {ERROR_CODE}")
                return redirect(url_for("fa2reset"))
            
        elif 'validate_code' in request.form:
            code_typed = request.form['input_code']
            print(code_typed)
            if code_generated == code_typed:
                DISPLAY_FORM = "ok"
            else:
                DISPLAY_FORM = "Invalid or empty code"
                
            flash(DISPLAY_FORM, "validcode")
            
        elif 'reset_password' in request.form:
            new_password = request.form['mdp']
            current_user_2fa.reset_mdp(new_password)
            return redirect(url_for("login"))
            
            
    return redirect(url_for("fa2reset"))

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
    
@app.route('/2fareset')
def fa2reset():
    return render_template('2fareset.html')
    
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

