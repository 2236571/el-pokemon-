from flask import Flask,render_template
import requests
from dotenv import load_dotenv,dotenv_values

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column  


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///pokedex.sqlite"

db = SQLAlchemy(app)

class Pokemon(db.Model):
    id :Mapped[int] = mapped_column(db.Integer,primary_key=True,autoincrement=True)
    name: Mapped[str] = mapped_column(db.String,nullable=False)
    height : Mapped[float] = mapped_column(db.Float,nullable=False)
    weight : Mapped[float] = mapped_column(db.Float,nullable=False)
    order : Mapped[int] = mapped_column(db.Integer,nullable=False)
    type : Mapped[str] = mapped_column(db.String,nullable=False)


with app.app_context():
    db.create_all()



def get_pokemon_data(pokemon):
    
    url=f'https://pokeapi.co/api/v2/pokemon/{pokemon}'
    r = requests.get(url).json()
    return r

@app.route("/")
def home():
    data = get_pokemon_data('lucario')
    pokemon={
        'id':data.get('id'),
        'name' : data.get('name').upper(),
        'height':data.get('height'),
        'weight' : data.get('weight'),
        'order' :data.get('order'),
        'type' : 'profesor',
        'photo':data.get('sprites').get('other').get('official-artwork').get('front_default')
        }        
    return render_template('pokemon.html',pokemon=pokemon)

@app.route("/detalle")
def detalle():
    return render_template('detalle.html')

@app.route("/insert")
def insert():
    new_pokemon= 'ditto'
    
    if new_pokemon:
        obj=Pokemon(name=new_pokemon,height=1.75,weight=100,order=100,type='Normal')
        db.session.add(obj)
        db.session.commit()    
       
    return 'Pokemon agregado'



@app.route("/selectbyid/<id>")
def selectbyid(id):
    poke = Pokemon.query.filter_by(id=id).first()
    return str (poke.id) + str(poke.name)


if __name__=='__main__':
    app.run(debug=True) 
