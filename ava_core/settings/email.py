# Python Imports
import os

# EMAIL SETTINGS

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.mandrillapp.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = os.environ.get('MANDRILL_USERNAME', '')        # Empty for no authentication
EMAIL_HOST_PASSWORD = os.environ.get('MANDRILL_PASSWORD', '')    # Empty for no authentication
EMAIL_USE_SSL = False       # SSL/TLS negotiated immediately (like HTTPS does)
EMAIL_USE_TLS = False       # Use STARTTLS command to enable SSL/TLS


DEFAULT_FROM_EMAIL='robot@dfend.io'