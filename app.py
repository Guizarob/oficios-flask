from flask import Flask, render_template, request, redirect, url_for, flash 
from models import Oficios
from databases import db
from forms import OficioForm
from flask_migrate import Migrate

from dotenv import load_dotenv
import os

import datetime
import calendar

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

# ---------------------------------------------------------
#           MESES 

MESES = {
    'enero': 1,
    'febrero': 2,
    'marzo': 3,
    'abril': 4,
    'mayo': 5,
    'junio': 6,
    'julio': 7,
    'agosto': 8,
    'septiembre': 9,
    'octubre': 10,
    'noviembre': 11,
    'diciembre': 12
}

#-------------------------------------------------------
    
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

@app.route('/buscar-fecha')
def buscar_fecha():

    query_fecha = request.args.get('fecha')

    if not query_fecha:
        flash('Debes ingresar una fecha')
        return redirect(url_for('inicio'))

    try:
        partes = query_fecha.lower().split()

        if len(partes) != 2:
            raise ValueError

        mes_texto = partes[0]
        anio = int(partes[1])

        mes = MESES.get(mes_texto)

        if not mes:
            raise ValueError

        fecha_inicio = datetime.date(anio, mes, 1)

        ultimo_dia = calendar.monthrange(anio, mes)[1]

        fecha_fin = datetime.date(anio, mes, ultimo_dia)

        oficios = Oficios.query.filter(
            Oficios.fecha.between(fecha_inicio, fecha_fin)
        ).all()

        return render_template(
            'index.html',
            datos=oficios,
            total=len(oficios)
        )

    except:
        flash('Formato inválido. Usa por ejemplo: mayo 2026')
        return redirect(url_for('inicio'))

if __name__ == '__main__':
    app.run(debug=True)