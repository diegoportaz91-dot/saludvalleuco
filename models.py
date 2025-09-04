from app import db
from flask_login import UserMixin
from datetime import datetime
from sqlalchemy import func

class Admin(UserMixin, db.Model):
    """Admin user model for managing the directory"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Admin {self.username}>'

class Professional(db.Model):
    """Healthcare professional model"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    specialty = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(50), nullable=False)  # San Carlos, Tunuyán, Tupungato
    phone = db.Column(db.String(20), nullable=False)
    
    # Premium plan fields
    plan = db.Column(db.String(20), default='basic')  # 'basic' or 'premium'
    photo_url = db.Column(db.String(200))  # URL to photo
    address = db.Column(db.Text)
    schedule = db.Column(db.Text)  # JSON string or text with schedule
    whatsapp = db.Column(db.String(20))
    contact_type = db.Column(db.String(50), default='phone')  # 'phone', 'whatsapp', 'both'
    insurance_coverage = db.Column(db.Text)  # Obras sociales
    description = db.Column(db.Text)
    
    # Map coordinates for premium plans
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    
    # Availability status
    available = db.Column(db.Boolean, default=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Professional {self.name} - {self.specialty}>'

    @property
    def is_premium(self):
        return self.plan == 'premium'

    def get_whatsapp_link(self):
        """Generate WhatsApp link for contact with predefined message"""
        if self.whatsapp:
            # Remove any non-numeric characters and format
            phone = ''.join(filter(str.isdigit, self.whatsapp))
            if phone.startswith('0'):
                phone = '54' + phone[1:]  # Argentina country code
            elif not phone.startswith('54'):
                phone = '54' + phone
            
            # Predefined message
            message = f"Hola Dr./Dra. {self.name.split()[-1]}, encontré su perfil en el Directorio de Salud Valle de Uco y quisiera más información sobre su atención."
            import urllib.parse
            encoded_message = urllib.parse.quote(message)
            return f"https://wa.me/{phone}?text={encoded_message}"
        return None

# Specialty constants for easy reference
SPECIALTIES = [
    'Pediatría',
    'Ginecología',
    'Odontología',
    'Psicología',
    'Medicina General',
    'Cardiología',
    'Dermatología',
    'Traumatología',
    'Neurología',
    'Oftalmología',
    'Otorrinolaringología',
    'Urología',
    'Endocrinología',
    'Gastroenterología',
    'Neumología',
    'Reumatología',
    'Psiquiatría',
    'Kinesiología',
    'Nutrición'
]

LOCATIONS = [
    'San Carlos',
    'Tunuyán',
    'Tupungato'
]

class Analytics(db.Model):
    """Model to track user interactions and statistics"""
    id = db.Column(db.Integer, primary_key=True)
    action_type = db.Column(db.String(50), nullable=False)  # 'page_view', 'profile_click', 'search', 'contact_click'
    target_id = db.Column(db.Integer)  # Professional ID for profile-related actions
    target_type = db.Column(db.String(50))  # 'professional', 'page', 'search'
    user_ip = db.Column(db.String(45))  # IPv4/IPv6 address
    user_agent = db.Column(db.Text)  # Browser info
    referrer = db.Column(db.String(500))  # Where user came from
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Analytics {self.action_type} - {self.created_at}>'

class Advertisement(db.Model):
    """Model for managing advertisement spaces"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text)  # HTML content or image URL
    position = db.Column(db.String(50), nullable=False)  # 'header', 'sidebar', 'footer', 'between_results'
    is_active = db.Column(db.Boolean, default=True)
    link_url = db.Column(db.String(500))  # Optional link
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Advertisement {self.title} - {self.position}>'
