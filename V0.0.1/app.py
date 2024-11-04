from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    # Rendre le template "index.html"
    return render_template('index.html')
    
@app.route('/learning')
def learning():
    return render_template('learning.html')
    
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')
    
@app.route('/outils')
def outils():
    return render_template('outils.html')
    
@app.route('/planning')
def planning():
    return render_template('planning.html')
    
@app.route('/support')
def support():
    return render_template('support.html')

if __name__ == '__main__':
    app.run(debug=True)
