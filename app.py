from flask import Flask,render_template
import requests

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column  


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///pokedex.sqlite"

db = SQLAlchemy(app)

class Pokemon(db.Model):
    id :Mapped[int] = mapped_column(db.Integer,primary_key=True,autoincrement=True)
    name: Mapped[str] = mapped_column(db.String,nullable=False)


with app.app_context():
    db.create_all()






def get_pokemon_data(pokemon):
    
    url=f'https://pokeapi.co/api/v2/pokemon/{pokemon}'
    r = requests.get(url).json()
    return r

@app.route("/")
def home():
    return render_template('pokemon.html')

@app.route("/detalle")
def detalle():
    return render_template('detalle.html')

@app.route("/insert")
def insert():
    new_pokemon= 'Pikachu'
    
    if new_pokemon:
        obj=Pokemon(name=new_pokemon)
        db.session.add(obj)
        db.session.commit()    
       
    return 'Pokemon agregado'


@app.route("/select")
def insert():
    Lista_pokemon = Pokemon.query.all()
    for p in Lista_pokemon:
        print(p.name)
    return 'alo'    


@app.route("/select/<name>")
def selectbyname(name):
    poke = Pokemon.query.filter_by(name=name).first()
    return str (poke.id)


if __name__=='__main__':
    app.run(debug=True)
