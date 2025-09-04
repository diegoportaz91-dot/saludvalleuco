from flask import render_template, request, redirect, url_for, flash, abort, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import or_, and_, func
from app import app, db
from models import Admin, Professional, Analytics, Advertisement, SPECIALTIES
from forms import LoginForm, ProfessionalForm, SearchForm
from datetime import datetime, timedelta

def track_analytics(action_type, target_id=None, target_type=None):
    """Helper function to track user analytics"""
    try:
        analytics = Analytics(
            action_type=action_type,
            target_id=target_id,
            target_type=target_type,
            user_ip=request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr),
            user_agent=request.headers.get('User-Agent'),
            referrer=request.headers.get('Referer')
        )
        db.session.add(analytics)
        db.session.commit()
    except Exception as e:
        print(f"Analytics tracking error: {e}")

@app.route('/')
def index():
    """Homepage with search and quick access categories"""
    form = SearchForm()
    
    # Get quick access categories with counts
    quick_categories = []
    priority_specialties = ['Pediatría', 'Ginecología', 'Odontología', 'Psicología']
    
    for specialty in priority_specialties:
        count = Professional.query.filter_by(specialty=specialty, available=True).count()
        quick_categories.append({
            'name': specialty,
            'count': count,
            'url': url_for('search', specialty=specialty)
        })
    
    # Get some featured professionals (only available ones)
    featured_professionals = Professional.query.filter_by(available=True).limit(6).all()
    
    # Track page view
    track_analytics('page_view', target_type='homepage')
    
    return render_template('index.html', 
                         form=form, 
                         quick_categories=quick_categories,
                         featured_professionals=featured_professionals)

@app.route('/buscar')
def search():
    """Search professionals with filters"""
    form = SearchForm()
    
    # Get search parameters from URL or form
    query = request.args.get('query', '').strip()
    specialty = request.args.get('specialty', '')
    location = request.args.get('location', '')
    available_only = request.args.get('available_only', 'true').lower() == 'true'
    
    # Track search analytics if there are search parameters
    if query or specialty or location:
        track_analytics('search', target_type='search')
    
    # Populate form with current values
    form.query.data = query
    form.specialty.data = specialty
    form.location.data = location
    form.available_only.data = available_only
    
    # Build query
    professionals_query = Professional.query
    
    # Apply filters
    if query:
        professionals_query = professionals_query.filter(
            or_(
                Professional.name.ilike(f'%{query}%'),
                Professional.specialty.ilike(f'%{query}%'),
                Professional.description.ilike(f'%{query}%')
            )
        )
    
    if specialty:
        professionals_query = professionals_query.filter(Professional.specialty == specialty)
    
    if location:
        professionals_query = professionals_query.filter(Professional.location == location)
    
    if available_only:
        professionals_query = professionals_query.filter(Professional.available == True)
    
    # Order by plan (premium first) then by name
    professionals = professionals_query.order_by(
        Professional.plan.desc(),  # premium first
        Professional.name
    ).all()
    
    return render_template('search.html', 
                         form=form, 
                         professionals=professionals,
                         query=query,
                         specialty=specialty,
                         location=location)

@app.route('/profesional/<int:professional_id>')
def professional_detail(professional_id):
    """Individual professional profile page"""
    professional = Professional.query.filter_by(id=professional_id, available=True).first_or_404()
    
    # Track profile view
    track_analytics('profile_view', target_id=professional_id, target_type='professional')
    
    return render_template('professional.html', professional=professional)

@app.route('/login', methods=['GET', 'POST'])
def admin_login():
    """Admin login page"""
    if current_user.is_authenticated:
        return redirect(url_for('admin_dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(username=form.username.data).first()
        if admin and check_password_hash(admin.password_hash, form.password.data):
            login_user(admin)
            next_page = request.args.get('next')
            flash('Sesión iniciada correctamente', 'success')
            return redirect(next_page) if next_page else redirect(url_for('admin_dashboard'))
        else:
            flash('Usuario o contraseña incorrectos', 'error')
    
    return render_template('admin/login.html', form=form)

@app.route('/admin/logout')
@login_required
def admin_logout():
    """Admin logout"""
    logout_user()
    flash('Sesión cerrada correctamente', 'info')
    return redirect(url_for('index'))

@app.route('/admin')
@login_required
def admin_dashboard():
    """Admin dashboard with professional management"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '').strip()
    
    # Build query
    query = Professional.query
    if search:
        query = query.filter(
            or_(
                Professional.name.ilike(f'%{search}%'),
                Professional.specialty.ilike(f'%{search}%'),
                Professional.location.ilike(f'%{search}%')
            )
        )
    
    professionals = query.order_by(Professional.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    
    # Statistics
    stats = {
        'total': Professional.query.count(),
        'basic': Professional.query.filter_by(plan='basic').count(),
        'premium': Professional.query.filter_by(plan='premium').count(),
        'available': Professional.query.filter_by(available=True).count()
    }
    
    return render_template('admin/dashboard.html', 
                         professionals=professionals, 
                         stats=stats,
                         search=search)

@app.route('/admin/profesional/nuevo', methods=['GET', 'POST'])
@login_required
def admin_add_professional():
    """Add new professional"""
    form = ProfessionalForm()
    
    if form.validate_on_submit():
        professional = Professional(
            name=form.name.data,
            specialty=form.specialty.data,
            location=form.location.data,
            phone=form.phone.data,
            plan=form.plan.data,
            available=form.available.data,
            photo_url=form.photo_url.data or None,
            address=form.address.data or None,
            schedule=form.schedule.data or None,
            whatsapp=form.whatsapp.data or None,
            contact_type=form.contact_type.data,
            insurance_coverage=form.insurance_coverage.data or None,
            description=form.description.data or None,
            latitude=form.latitude.data,
            longitude=form.longitude.data
        )
        
        db.session.add(professional)
        db.session.commit()
        flash(f'Profesional {professional.name} agregado correctamente', 'success')
        return redirect(url_for('admin_dashboard'))
    
    return render_template('admin/professional_form.html', form=form, title='Agregar Profesional')

@app.route('/admin/profesional/<int:professional_id>/editar', methods=['GET', 'POST'])
@login_required
def admin_edit_professional(professional_id):
    """Edit existing professional"""
    professional = Professional.query.get_or_404(professional_id)
    form = ProfessionalForm(obj=professional)
    
    if form.validate_on_submit():
        form.populate_obj(professional)
        professional.updated_at = db.func.now()
        db.session.commit()
        flash(f'Profesional {professional.name} actualizado correctamente', 'success')
        return redirect(url_for('admin_dashboard'))
    
    return render_template('admin/professional_form.html', 
                         form=form, 
                         title='Editar Profesional',
                         professional=professional)

@app.route('/admin/profesional/<int:professional_id>/eliminar', methods=['POST'])
@login_required
def admin_delete_professional(professional_id):
    """Delete professional"""
    professional = Professional.query.get_or_404(professional_id)
    name = professional.name
    db.session.delete(professional)
    db.session.commit()
    flash(f'Profesional {name} eliminado correctamente', 'success')
    return redirect(url_for('admin_dashboard'))

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.route('/admin/analytics')
@login_required
def admin_analytics():
    """Analytics dashboard for admin"""
    try:
        # Get date range (last 30 days by default)
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=30)
        
        # Basic stats
        total_page_views = Analytics.query.filter(
            Analytics.action_type == 'page_view',
            Analytics.created_at >= start_date
        ).count()
        
        total_profile_views = Analytics.query.filter(
            Analytics.action_type == 'profile_view',
            Analytics.created_at >= start_date
        ).count()
        
        total_searches = Analytics.query.filter(
            Analytics.action_type == 'search',
            Analytics.created_at >= start_date
        ).count()
        
        # Most viewed professionals
        popular_professionals = db.session.query(
            Professional.name,
            Professional.specialty,
            func.count(Analytics.id).label('views')
        ).join(
            Analytics, Professional.id == Analytics.target_id
        ).filter(
            Analytics.action_type == 'profile_view',
            Analytics.created_at >= start_date
        ).group_by(
            Professional.id, Professional.name, Professional.specialty
        ).order_by(
            func.count(Analytics.id).desc()
        ).limit(10).all()
        
        # Daily views for chart
        daily_views = db.session.query(
            func.date(Analytics.created_at).label('date'),
            func.count(Analytics.id).label('views')
        ).filter(
            Analytics.created_at >= start_date,
            Analytics.action_type.in_(['page_view', 'profile_view'])
        ).group_by(
            func.date(Analytics.created_at)
        ).order_by(
            func.date(Analytics.created_at)
        ).all()
        
        return render_template('admin/analytics.html',
                             total_page_views=total_page_views,
                             total_profile_views=total_profile_views,
                             total_searches=total_searches,
                             popular_professionals=popular_professionals,
                             daily_views=daily_views,
                             start_date=start_date,
                             end_date=end_date)
    except Exception as e:
        app.logger.error(f"Error in analytics: {e}")
        flash('Error al cargar las estadísticas. Por favor, intente nuevamente.', 'error')
        return render_template('admin/analytics.html',
                             total_page_views=0,
                             total_profile_views=0,
                             total_searches=0,
                             popular_professionals=[],
                             daily_views=[],
                             start_date=datetime.utcnow() - timedelta(days=30),
                             end_date=datetime.utcnow())

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

@app.route('/test-static')
def test_static():
    """Test route to verify static files are being served"""
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Test Static Files</title>
    </head>
    <body>
        <h1>Test de Archivos Estáticos</h1>
        <p>Si puedes ver este mensaje, Flask está funcionando.</p>
        <p>Ahora vamos a probar los archivos estáticos:</p>
        <ul>
            <li><a href="/static/css/style.css">CSS</a></li>
            <li><a href="/static/js/main.js">JavaScript</a></li>
        </ul>
        <script src="/static/js/main.js"></script>
        <p>Revisa la consola del navegador para ver si hay errores.</p>
    </body>
    </html>
    '''
