from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, DateField, SubmitField
from wtforms.validators import DataRequired, Optional, URL

class OficioForm(FlaskForm):

    numero_oficio = StringField('Número de oficio', validators=[DataRequired()])

    asunto = StringField('Asunto', validators=[DataRequired()])

    remitente = StringField('Remitente', validators=[DataRequired()])

    destinatario = StringField('Destinatario', validators=[DataRequired()])

    acusado = BooleanField('¿Tiene acuse?')

    hipervinculo = TextAreaField(
    'Hipervínculo del documento',
    validators=[DataRequired(), URL()])

    observaciones = TextAreaField('Observaciones', validators=[Optional()])

    antecedentes = TextAreaField('Antecedentes', validators=[Optional()])

    fecha = DateField('Fecha', format='%Y-%m-%d', validators=[Optional()]) ## Actualizar el formato  y dar opciones  a errores del cliente o usuario

    enviar = SubmitField('Guardar oficio')