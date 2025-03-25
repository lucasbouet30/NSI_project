# START packages

# importation des tout les packets (pip install -r requirements.txt)
import sqlite3
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
import leveling
from werkzeug.utils import secure_filename


import uuid
from werkzeug.utils import secure_filename
print("Current working directory:", os.getcwd())

RESET = True


user_level = leveling.leveling()
        
# création d'une fonction permetant de hasher les mots de passes (str -> str)
# plus sécurisé / mots de passes cryptés et non en clair
def hash_it(data):
    # utilisation de hashlib
    a = hashlib.md5(data.encode())
    return a.hexdigest() # return un string

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# def request_db(sql_request : str):
#     '''Permet d'éviter les copy pasta'''
#     con = get_db_connection() #ouvrir la base de donnée
#     cur = con.cursor()       #faire un curseur, une sorte de lien
#                             #executer la requète sql
#     cur.execute(sql_request, (session["current_user"],)) 
#     data = cur.fetchone() #récupérer le résultat de la requète
#     con.close()          #fermer la base de donnée
#     return data
    
# END packages

# ----------

# START flask instance

# creation de l'instance de flask pour y acceder aux méthodes par exemple
app = Flask(__name__)

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'static/assets/images/upload/pfps')
app.config['UPLOAD_FOLDER_PFPS'] = UPLOAD_FOLDER
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'static/assets/images/upload/banners')
app.config['UPLOAD_FOLDER_BANNERS'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# END flask instance

# ----------

# START login function

# initialisation du module de login / register de flask
app.secret_key = "rhapsopy"
login_manager = flask_login.LoginManager()
login_manager.init_app(app)
DB_PATH = "data/bob.db"
def get_db_connection():
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    return con

"""
def Sql_cmd(param):
    try:
        res = cur.execute(param)
        return res.fetchall()
    except Exception as e:
        raise e
def SQL(param):
    ans = Sql_cmd(param)
    con.commit()
    return ans
"""

# creation d'une classe pour définir qu'est ce qu'un user 
class User(flask_login.UserMixin):
    def __init__(self, email, password, discordId=101, pfp_path=None, banner_path=None):
        self.id = email
        self.password = password
        self.discordId = discordId
        self.pfp_path = pfp_path or 'assets/images/upload/pfps/empty-pfp.svg'
        self.banner_path = banner_path or 'assets/images/upload/banners/empty-banner.svg'

    def reset_mdp(self, new_password):
        hashed_password = hash_it(new_password)
        con = get_db_connection()
        cur = con.cursor()
        cur.execute("UPDATE Users SET Password = ? WHERE Email = ?", (hashed_password, self.id))
        con.commit()
        con.close()

        

if RESET == True:
    # server purpose only (temp)
    con = get_db_connection()
    cur = con.cursor()
    print(cur.execute('DELETE FROM Users WHERE EXISTS (SELECT 1 FROM Users);'))
    password_t = hash_it("testtest123.")
    print(cur.execute(f'INSERT INTO Users(Id, Email, Password, Pp, Banner, Xp, DiscordId) VALUES (1, "test@gmail.com", "{password_t}", "assets/images/upload/pfps/empty-pfp.svg", "assets/images/upload/banners/empty-banner.svg", 100, 600288096046678036)'))
    con.commit()
    con.close()
    # end


# START login pages / methods

# mise en place du login_manager pour récupérer l'utilisateur en cours
@login_manager.user_loader
def user_loader(email):
    con = get_db_connection()
    cur = con.cursor()
    cur.execute("SELECT Email, Password, DiscordId FROM Users WHERE Email = ?", (email,))
    user_data = cur.fetchone()
    con.close()
    return User(*user_data) if user_data else None
    
# la page de register (\templates\register.html)
@app.get("/register")
def register():
    return render_template("register.html")
    
# la page de register côté logique (post)
@app.post("/register")
def registerp():
    email = request.form["email"]
    password = request.form["password"]
    discord_id = request.form.get("discord-id", 0)
    
    if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        flash("Invalid email format")
        return redirect(url_for("register"))
    
    con = get_db_connection()
    cur = con.cursor()
    cur.execute("SELECT 1 FROM Users WHERE Email = ?", (email,))
    if cur.fetchone():
        flash("Email already exists")
        con.close()
        return redirect(url_for("register"))
    
    if len(password) < 8:
        flash("Password must be at least 8 characters long")
        con.close()
        return redirect(url_for("register"))
    
    cur.execute('SELECT MAX(Id) FROM Users')
    current_id = cur.fetchone()
    next_id = current_id[0] + 1
    hashed_password = hash_it(password)
    if discord_id:
        cur.execute("INSERT INTO Users (Id, Email, Password, DiscordId) VALUES (?, ?, ?, ?)", (next_id, email, hashed_password, discord_id))
    else:
        cur.execute("INSERT INTO Users (Id, Email, Password, DiscordId) VALUES (?, ?, ?, ?)", (next_id, email, hashed_password, 101))
    con.commit()
    con.close()
    flash("Registration successful!")
    return redirect(url_for("login"))
    
# la page de login (\templates\login.html)
@app.get("/login")
def login():
    # flask render_template method
    return render_template('login.html')
    
print('Compte test : \n test@gmail.com \n testtest123.') #pour avoir le compte test sur le terminal coté dev

# la page de login côté logique et server
@app.post("/login")
def loginp():
    email = request.form["email"]
    password = request.form["password"]
    remind = request.form.get("rememberme", False)
    
    con = get_db_connection()
    cur = con.cursor()
    cur.execute("SELECT Email, Password, DiscordId FROM Users WHERE Email = ?", (email,))
    user_data = cur.fetchone()
    con.close()
    
    if not user_data or user_data[1] != hash_it(password):
        flash("Invalid email or password")
        return redirect(url_for("login"))
    
    user = User(*user_data)
    session["current_user"] = email
    session["logged_in"] = True
    flask_login.login_user(user, remember=remind)
    flash("Bon retour parmis nous!")
    return redirect(url_for("profile"))
    
# END login pages / methods

@app.route("/logout")
@flask_login.login_required
def logout():
    try :
        if session['logged_in'] == False:
            return redirect('403')
    except :
        return redirect('403')
    session["logged_in"] = False
    flask_login.logout_user()
    flash("You have been logged out")
    return redirect(url_for("login"))

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
    
@app.errorhandler(403)
def forbidden_error(error):
    return render_template('errors/403.html')
    
@app.errorhandler(401)
def forbidden_error(error):
    return render_template('errors/403.html')
    
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

@app.route('/404')
def err404():
    return render_template('errors/404.html')

@app.route('/500')
def err500():
    return render_template('errors/5.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' in request.files:
        file = request.files['file']
        filename = secure_filename(file.filename)
        uuidimage = hash_it(filename)
        filename = uuidimage + ".jpeg"
        custom_variable = request.form.get('typevar')
        
        con = get_db_connection()
        cur = con.cursor()
        
        if 'pfp' == custom_variable:
            folderchoosen = app.config['UPLOAD_FOLDER_PFPS']
            cur.execute("UPDATE Users SET Pp = ? WHERE Email = ?;", (f'/assets/images/upload/pfps/{filename}', session["current_user"]))
            con.commit()
        elif 'banner' == custom_variable:
            cur.execute("UPDATE Users SET Banner = ? WHERE Email = ?;", (f'/assets/images/upload/banners/{filename}', session["current_user"]))
            con.commit()
            folderchoosen = app.config['UPLOAD_FOLDER_BANNERS']
        file.save(os.path.join(folderchoosen, filename))
        
        
        
    return redirect('profile')

@flask_login.login_required
@app.route('/profile')
def profile():
    try :
        if session['logged_in'] == False:
            return redirect('403')
    except :
        return redirect('403')
    
    con = get_db_connection()
    cur = con.cursor()
    cur.execute('SELECT Xp, Pp, Banner, Email FROM Users WHERE Email=?', (session["current_user"],)) 
    user_data = cur.fetchone()
    con.close()

    exp = user_data[0]
    lvl = user_level.calculate_lvl(exp)
    email = user_data[3]
    user_title= user_level.get_title(exp) 
    user_badge= user_level.get_badge(exp)
    username = user_level.find_username(email)

    pfp_path = user_data[1] # récuperer le chemin pfp
    banner_path = user_data[2] # récuperer le chemin bannière

    user_pfp= url_for('static', filename=pfp_path)
    user_banner= url_for('static', filename=banner_path)

    print(session['logged_in'])
    return render_template('profile.html', 
                           lvl = lvl, 
                           user_title=user_title, 
                           user_badge=user_badge, 
                           username=username,
                           user_pfp=user_pfp,
                           user_banner=user_banner)

# END rendering webpages

# ----------

# START flask server starting

# lance le serveur au lancement du fichier python
if __name__ == '__main__':
    app.run(debug=True)
    
# END flask server starting

