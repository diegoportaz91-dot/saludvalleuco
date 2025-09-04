# Overview

Salud Valle de Uco is a healthcare professional directory application built for the Valle de Uco region in Argentina (San Carlos, Tunuyán, and Tupungato). The web application allows users to search and find healthcare professionals while providing administrators with tools to manage professional listings. The system supports both basic (free) and premium (paid) professional profiles with enhanced features for premium users.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Web Framework Architecture
- **Flask-based web application** using Python as the primary backend language
- **Flask-SQLAlchemy** for ORM and database abstraction layer
- **Flask-Login** for authentication and session management
- **Flask-WTF** with WTForms for form handling and validation
- **Jinja2** templating engine for server-side rendering

## Frontend Architecture
- **Server-side rendered HTML** with Bootstrap 5 for responsive UI components
- **Font Awesome** for iconography and visual elements
- **Custom CSS** with CSS variables for theme consistency
- **JavaScript** for progressive enhancement (tooltips, smooth scrolling, form interactions)
- **Mobile-responsive design** optimized for various device sizes

## Database Design
- **SQLAlchemy ORM** with declarative base model
- **Two-tier user system**: Admin users for management, Professional records for directory listings
- **Flexible schema** supporting both basic and premium professional profiles
- **Connection pooling** with pre-ping health checks for database reliability

## Authentication & Authorization
- **Flask-Login** session-based authentication for admin users
- **Werkzeug password hashing** for secure credential storage
- **Role-based access control** with admin-only management features
- **Session management** with configurable secret keys

## Business Logic Architecture
- **Two-tier professional plans**: Basic (free) and Premium (paid) with feature differentiation
- **Location-based organization** covering three municipalities
- **Specialty-based categorization** for healthcare services
- **Search and filtering system** with multiple criteria support
- **Availability status tracking** for professional listings

## Data Model Structure
- **Professional model** with conditional premium features (photos, maps, extended details)
- **Admin model** for system management
- **Predefined constants** for specialties and locations to ensure data consistency
- **Timestamp tracking** for creation and modification auditing

# External Dependencies

## Core Framework Dependencies
- **Flask** - Web application framework
- **Flask-SQLAlchemy** - Database ORM and abstraction
- **Flask-Login** - User authentication and session management
- **Flask-WTF** - Form handling and CSRF protection
- **WTForms** - Form validation and rendering
- **Werkzeug** - WSGI utilities and security functions

## Frontend Dependencies
- **Bootstrap 5.3.0** (CDN) - CSS framework for responsive design
- **Font Awesome 6.4.0** (CDN) - Icon library for UI elements
- **Custom CSS/JS** - Application-specific styling and functionality

## Database Support
- **SQLite** - Default development database (fallback configuration)
- **PostgreSQL-ready** - Production database configuration via DATABASE_URL environment variable
- **SQLAlchemy engine options** - Connection pooling and health check configurations

## Deployment Dependencies
- **ProxyFix middleware** - Support for reverse proxy deployments
- **Environment variable configuration** - Secure configuration management for database URLs and session secrets
- **WSGI-compatible** - Ready for deployment on various hosting platforms

## Optional Integration Points
- **Photo hosting services** - URL-based image storage for premium professional photos
- **Mapping services** - Coordinate storage for location-based features (premium plans)
- **WhatsApp integration** - Contact method for enhanced professional profiles