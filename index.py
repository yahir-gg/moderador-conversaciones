from flask import Flask, render_template

# objeto apara crear rutas
app = Flask(__name__)

# / es pagina principal
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/contacto')
def contacto():
    return render_template('contacto.html')
 
@app.route('/chat')
def chat():
    return render_template('chat.html')

# ctrl+shift+r para recargar sin cache
if __name__ == '__main__':
    app.run(debug=True)