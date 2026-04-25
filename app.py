from flask import Flask, render_template, request, redirect, url_for
from models import Oficios
from databases import db
from forms import OficioForm
from flask_migrate import Migrate

from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

USER_DB = os.getenv('DB_USER')
USER_PASSWORD = os.getenv('DB_PASSWORD')
SERVER_DB = os.getenv('DB_HOST')
NAME_DB = os.getenv('DB_NAME')
FULL_URL_DB=  f'postgresql://{USER_DB}:{USER_PASSWORD}@{SERVER_DB}/{NAME_DB}'

app.config['SQLALCHEMY_DATABASE_URI'] = FULL_URL_DB
db.init_app(app)

#Migrar el modulo
migrate = Migrate(app, db)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    
@app.route('/')
def inicio():
    query = request.args.get('q')

    if query:
        oficios = Oficios.query.filter(
            Oficios.numero_oficio.ilike(f"%{query}%")
        ).order_by(Oficios.id).all()
    else:
        oficios = Oficios.query.order_by(Oficios.id).all()

    total_oficios = len(oficios)

    return render_template('index.html', datos=oficios, total=total_oficios)

# @app.route('/oficio/<int:id>')
# def ver_oficio(id):
#     oficio  = Oficios.query.get(id)
#     return render_template('oficio.html', dato = oficio)

@app.route('/oficio/<string:numero>')
def ver_oficio(numero):
    oficios = Oficios.query.filter_by(numero_oficio=numero).all()
    return render_template('oficio.html', datos=oficios)


@app.route('/insertar-oficio', methods = ['GET', 'POST'])
def insertar_oficio():
    oficio = Oficios()
    oficioForm = OficioForm(obj= oficio)

    if request.method == 'POST':
        if oficioForm.validate_on_submit():
            oficioForm.populate_obj(oficio)
            db.session.add(oficio)
            db.session.commit()
            return redirect(url_for('inicio'))

    return render_template('insertar-oficio.html', formulario = oficioForm)

@app.route('/editar-oficio/<int:id>', methods = ['GET', 'POST'])
def editar_oficio(id):
    oficio = Oficios.query.get_or_404(id)
    oficioForm = OficioForm(obj= oficio)
    if request.method == 'POST':
        if oficioForm.validate_on_submit():
            oficioForm.populate_obj(oficio)
            #app.logger.debug(f'Oficio a actualizar: {oficio}')
            db.session.commit()
            return redirect(url_for('inicio'))
    return render_template('editar-oficio.html', formulario = oficioForm)

@app.route('/eliminar-oficio/<int:id>', methods=['POST'])
def eliminar_oficio(id):
    oficio = Oficios.query.get_or_404(id)
    db.session.delete(oficio)
    db.session.commit()
    return redirect(url_for('inicio'))

@app.route('/buscar-oficio')
def buscar_oficio():
    query = request.args.get('q')
    if query:
        oficios = Oficios.query.filter(
            Oficios.numero_oficio.ilike(f"%{query}%")
        ).all()
    else:
        oficios = Oficios.query.all()

    return render_template('index.html', datos = oficios, total = len(oficios))

if __name__ == '__main__':
    app.run(debug=True)