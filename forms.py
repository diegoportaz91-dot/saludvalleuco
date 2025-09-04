from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, BooleanField, FloatField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Optional, NumberRange
from models import SPECIALTIES, LOCATIONS

class LoginForm(FlaskForm):
    """Admin login form"""
    username = StringField('Usuario', validators=[DataRequired(), Length(min=4, max=64)])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Iniciar Sesión')

class ProfessionalForm(FlaskForm):
    """Form for adding/editing professionals"""
    name = StringField('Nombre Completo', validators=[DataRequired(), Length(max=100)])
    specialty = SelectField('Especialidad', choices=[(s, s) for s in SPECIALTIES], validators=[DataRequired()])
    location = SelectField('Localidad', choices=[(l, l) for l in LOCATIONS], validators=[DataRequired()])
    phone = StringField('Teléfono', validators=[DataRequired(), Length(max=20)])
    plan = SelectField('Plan', choices=[('basic', 'Básico (Gratis)'), ('premium', 'Premium (Pago)')], default='basic')
    available = BooleanField('Disponible', default=True)
    
    # Premium fields
    photo_url = StringField('URL de Foto', validators=[Optional(), Length(max=200)])
    address = TextAreaField('Dirección', validators=[Optional()])
    schedule = TextAreaField('Horarios de Atención', validators=[Optional()])
    whatsapp = StringField('WhatsApp', validators=[Optional(), Length(max=20)])
    contact_type = SelectField('Tipo de Contacto', 
                              choices=[('phone', 'Solo teléfono'), 
                                     ('whatsapp', 'Solo WhatsApp'), 
                                     ('both', 'Teléfono y WhatsApp')],
                              default='phone')
    insurance_coverage = TextAreaField('Obras Sociales', validators=[Optional()])
    description = TextAreaField('Descripción', validators=[Optional()])
    latitude = FloatField('Latitud', validators=[Optional(), NumberRange(min=-90, max=90)])
    longitude = FloatField('Longitud', validators=[Optional(), NumberRange(min=-180, max=180)])
    
    submit = SubmitField('Guardar')

class SearchForm(FlaskForm):
    """Search form for professionals"""
    query = StringField('Buscar profesional o especialidad')
    specialty = SelectField('Especialidad', choices=[('', 'Todas')] + [(s, s) for s in SPECIALTIES])
    location = SelectField('Localidad', choices=[('', 'Todas')] + [(l, l) for l in LOCATIONS])
    available_only = BooleanField('Solo disponibles', default=True)
    submit = SubmitField('Buscar')
