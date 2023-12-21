from flask import Flask,render_template,request
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

@app.route("/",methods=['GET','POST'])
def home():
    pokemon = None
    if request.method == 'POST' :
        name_pokemon = request.form.get('name')
        if name_pokemon:
            data = get_pokemon_data(name_pokemon.lower())
            if data:
                pokemon={
                    'id':data.get('id'),
                    'name' : data.get('name').upper(),
                    'height':data.get('height'),
                    'weight' : data.get('weight'),
                    'order' :data.get('order'),
                    'type' : 'profesor',
                    'photo':data.get('sprites').get('other').get('official-artwork').get('front_default')
                    } 
                print(pokemon)     
    return render_template('pokemon.html',pokemon=pokemon)

@app.route("/detalle/<name>/")
def detalle(name):
    data = get_pokemon_data(name.lower())
    pokemon={
                    'id':data.get('id'),
                    'name' : data.get('name').upper(),
                    'height':data.get('height'),
                    'weight' : data.get('weight'),
                    'order' :data.get('order'),
                    'type' : 'profesor',
                    'hp' : data.get('stats')[0].get('base_stat'),
                    'attack' : data.get('stats')[1].get('base_stat'),
                    'defence' : data.get('stats')[2].get('base_stat'),
                    'speed' : data.get('stats')[5].get('base_stat'),
                    'photo':data.get('sprites').get('other').get('official-artwork').get('front_default')
                    } 

    return render_template('detalle.html',pokemon = pokemon)


#@app.route("/detalle")
#def detalle():
#    return render_template('detalle.html')

@app.route("/insert_pokemon/<pokemon>")
def insert(pokemon):
    new_pokemon= pokemon
    if new_pokemon:
        obj=Pokemon(pokemon)
        db.session.add(obj)
        db.session.commit()    
       
    return 'Pokemon agregado'



@app.route("/selectbyid/<id>")
def selectbyid(id):
    poke = Pokemon.query.filter_by(id=id).first()
    return str (poke.id) + str(poke.name)


if __name__=='__main__':
    app.run(debug=True) 
