// Main JavaScript for Salud Valle de Uco

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Auto-dismiss alerts after 5 seconds
    var alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        if (!alert.classList.contains('alert-permanent')) {
            setTimeout(function() {
                var alertInstance = new bootstrap.Alert(alert);
                if (alertInstance) {
                    alertInstance.close();
                }
            }, 5000);
        }
    });

    // Smooth scrolling for anchor links
    var anchorLinks = document.querySelectorAll('a[href^="#"]');
    anchorLinks.forEach(function(link) {
        link.addEventListener('click', function(e) {
            var href = this.getAttribute('href');
            if (href && href !== '#') {
                var target = document.querySelector(href);
                if (target) {
                    e.preventDefault();
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            }
        });
    });

    // Back to top button
    createBackToTopButton();

    // Phone number formatting
    formatPhoneNumbers();

    // Search form enhancements
    enhanceSearchForm();

    // Professional form enhancements
    enhanceProfessionalForm();

    // Add loading states to forms
    addLoadingStates();
});

// Create back to top button
function createBackToTopButton() {
    var backToTopButton = document.createElement('button');
    backToTopButton.innerHTML = '<i class="fas fa-arrow-up"></i>';
    backToTopButton.className = 'btn btn-primary btn-floating';
    backToTopButton.style.cssText = `
        position: fixed;
        bottom: 20px;
        right: 20px;
        border-radius: 50%;
        width: 50px;
        height: 50px;
        display: none;
        z-index: 1000;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    `;
    
    backToTopButton.addEventListener('click', function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });

    document.body.appendChild(backToTopButton);

    // Show/hide button based on scroll position
    window.addEventListener('scroll', function() {
        if (window.pageYOffset > 300) {
            backToTopButton.style.display = 'block';
        } else {
            backToTopButton.style.display = 'none';
        }
    });
}

// Format phone numbers for better display
function formatPhoneNumbers() {
    var phoneLinks = document.querySelectorAll('a[href^="tel:"]');
    phoneLinks.forEach(function(link) {
        var phone = link.textContent.trim();
        // Simple formatting for Argentine phone numbers
        if (phone.match(/^\+?54/)) {
            // Already formatted
            return;
        }
        
        // Add basic formatting if needed
        if (phone.match(/^\d{10,}$/)) {
            var formatted = phone.replace(/(\d{3})(\d{3})(\d{4})/, '$1-$2-$3');
            link.textContent = formatted;
        }
    });
}

// Enhance search form functionality
function enhanceSearchForm() {
    var searchForm = document.querySelector('form[action*="search"]');
    if (!searchForm) return;

    var queryInput = searchForm.querySelector('input[name="query"]');
    var specialtySelect = searchForm.querySelector('select[name="specialty"]');
    var locationSelect = searchForm.querySelector('select[name="location"]');

    // Auto-submit on filter change
    if (specialtySelect) {
        specialtySelect.addEventListener('change', function() {
            if (this.value) {
                searchForm.submit();
            }
        });
    }

    if (locationSelect) {
        locationSelect.addEventListener('change', function() {
            if (this.value) {
                searchForm.submit();
            }
        });
    }

    // Add search suggestions (simple implementation)
    if (queryInput) {
        var suggestions = [
            'Pediatría', 'Ginecología', 'Odontología', 'Psicología',
            'Medicina General', 'Cardiología', 'Dermatología'
        ];

        queryInput.addEventListener('input', function() {
            var value = this.value.toLowerCase();
            var existingDatalist = document.getElementById('searchSuggestions');
            
            if (existingDatalist) {
                existingDatalist.remove();
            }

            if (value.length > 2) {
                var datalist = document.createElement('datalist');
                datalist.id = 'searchSuggestions';
                
                suggestions.forEach(function(suggestion) {
                    if (suggestion.toLowerCase().includes(value)) {
                        var option = document.createElement('option');
                        option.value = suggestion;
                        datalist.appendChild(option);
                    }
                });

                if (datalist.children.length > 0) {
                    document.body.appendChild(datalist);
                    queryInput.setAttribute('list', 'searchSuggestions');
                }
            }
        });
    }
}

// Enhance professional form
function enhanceProfessionalForm() {
    var professionalForm = document.querySelector('form[action*="profesional"]');
    if (!professionalForm) return;

    var planSelect = professionalForm.querySelector('select[name="plan"]');
    var premiumFields = document.getElementById('premiumFields');

    if (planSelect && premiumFields) {
        function togglePremiumFields() {
            var isPremium = planSelect.value === 'premium';
            var premiumInputs = premiumFields.querySelectorAll('input, textarea, select');
            
            premiumFields.style.opacity = isPremium ? '1' : '0.6';
            
            premiumInputs.forEach(function(input) {
                if (input !== planSelect) {
                    input.disabled = !isPremium;
                    if (!isPremium) {
                        input.style.backgroundColor = '#f8f9fa';
                        input.style.cursor = 'not-allowed';
                    } else {
                        input.style.backgroundColor = '';
                        input.style.cursor = '';
                    }
                }
            });
        }

        planSelect.addEventListener('change', togglePremiumFields);
        togglePremiumFields(); // Initialize
    }

    // Photo URL preview
    var photoUrlInput = professionalForm.querySelector('input[name="photo_url"]');
    if (photoUrlInput) {
        photoUrlInput.addEventListener('input', function() {
            var url = this.value;
            var existingPreview = document.getElementById('photoPreview');
            
            if (existingPreview) {
                existingPreview.remove();
            }
            
            if (url && url.startsWith('http')) {
                var preview = document.createElement('div');
                preview.id = 'photoPreview';
                preview.className = 'mt-2';
                preview.innerHTML = `
                    <small class="text-muted">Vista previa:</small><br>
                    <img src="${url}" alt="Vista previa" class="rounded" style="max-width: 100px; max-height: 100px; object-fit: cover;">
                `;
                this.parentNode.appendChild(preview);
                
                // Handle image load error
                preview.querySelector('img').addEventListener('error', function() {
                    preview.innerHTML = '<small class="text-danger">Error al cargar la imagen</small>';
                });
            }
        });
    }

    // Coordinate helper
    var latInput = professionalForm.querySelector('input[name="latitude"]');
    var lngInput = professionalForm.querySelector('input[name="longitude"]');
    
    if (latInput && lngInput) {
        var coordinateHelper = document.createElement('div');
        coordinateHelper.className = 'mt-2';
        coordinateHelper.innerHTML = `
            <small class="text-muted">
                <i class="fas fa-info-circle me-1"></i>
                Puedes obtener las coordenadas desde 
                <a href="https://www.google.com/maps" target="_blank" class="text-decoration-none">Google Maps</a>
                haciendo clic derecho en la ubicación.
            </small>
        `;
        lngInput.parentNode.appendChild(coordinateHelper);
    }
}

// Add loading states to forms
function addLoadingStates() {
    var forms = document.querySelectorAll('form');
    
    forms.forEach(function(form) {
        form.addEventListener('submit', function() {
            var submitButton = form.querySelector('button[type="submit"], input[type="submit"]');
            if (submitButton) {
                var originalText = submitButton.textContent || submitButton.value;
                var loadingText = 'Cargando...';
                
                submitButton.disabled = true;
                
                if (submitButton.tagName === 'BUTTON') {
                    submitButton.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>' + loadingText;
                } else {
                    submitButton.value = loadingText;
                }
                
                // Re-enable after 10 seconds as fallback
                setTimeout(function() {
                    submitButton.disabled = false;
                    if (submitButton.tagName === 'BUTTON') {
                        submitButton.textContent = originalText;
                    } else {
                        submitButton.value = originalText;
                    }
                }, 10000);
            }
        });
    });
}

// Utility functions
function showNotification(message, type = 'info') {
    var alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 1055;
        min-width: 300px;
    `;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(alertDiv);
    
    // Auto-dismiss after 5 seconds
    setTimeout(function() {
        var alert = new bootstrap.Alert(alertDiv);
        alert.close();
    }, 5000);
}

function copyToClipboard(text) {
    if (navigator.clipboard) {
        navigator.clipboard.writeText(text).then(function() {
            showNotification('Copiado al portapapeles', 'success');
        });
    } else {
        // Fallback for older browsers
        var textArea = document.createElement('textarea');
        textArea.value = text;
        document.body.appendChild(textArea);
        textArea.select();
        document.execCommand('copy');
        document.body.removeChild(textArea);
        showNotification('Copiado al portapapeles', 'success');
    }
}

// Add click to copy functionality for phone numbers
document.addEventListener('click', function(e) {
    if (e.target.matches('a[href^="tel:"]') && e.ctrlKey) {
        e.preventDefault();
        var phone = e.target.textContent.trim();
        copyToClipboard(phone);
    }
});

// Keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + K to focus search
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        var searchInput = document.querySelector('input[name="query"]');
        if (searchInput) {
            searchInput.focus();
            searchInput.select();
        }
    }
    
    // Escape to clear search
    if (e.key === 'Escape') {
        var searchInput = document.querySelector('input[name="query"]:focus');
        if (searchInput) {
            searchInput.value = '';
            searchInput.blur();
        }
    }
});

// Add fade-in animation to cards
function addFadeInAnimation() {
    var cards = document.querySelectorAll('.card');
    
    var observer = new IntersectionObserver(function(entries) {
        entries.forEach(function(entry) {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1
    });
    
    cards.forEach(function(card) {
        observer.observe(card);
    });
}

// Initialize animations when page loads
window.addEventListener('load', function() {
    addFadeInAnimation();
});
