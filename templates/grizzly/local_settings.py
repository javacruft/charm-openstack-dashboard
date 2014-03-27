import os

from django.utils.translation import ugettext_lazy as _
from openstack_dashboard import exceptions
{% if use_syslog %}
from logging.handlers import SysLogHandler
{% endif %}

DEBUG = {{ debug }}
TEMPLATE_DEBUG = DEBUG

# Set SSL proxy settings:
# For Django 1.4+ pass this header from the proxy after terminating the SSL,
# and don't forget to strip it from the client's request.
# For more information see:
# https://docs.djangoproject.com/en/1.4/ref/settings/#secure-proxy-ssl-header
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTOCOL', 'https')

# If Horizon is being served through SSL, then uncomment the following two
# settings to better secure the cookies from security exploits
#CSRF_COOKIE_SECURE = True
#SESSION_COOKIE_SECURE = True

# Default OpenStack Dashboard configuration.
HORIZON_CONFIG = {
    'dashboards': ('project', 'admin', 'settings',),
    'default_dashboard': 'project',
    'user_home': 'openstack_dashboard.views.get_user_home',
    'ajax_queue_limit': 10,
    'auto_fade_alerts': {
        'delay': 3000,
        'fade_duration': 1500,
        'types': ['alert-success', 'alert-info']
    },
    'help_url': "http://docs.openstack.org",
    'exceptions': {'recoverable': exceptions.RECOVERABLE,
                   'not_found': exceptions.NOT_FOUND,
                   'unauthorized': exceptions.UNAUTHORIZED},
}

# Specify a regular expression to validate user passwords.
# HORIZON_CONFIG["password_validator"] = {
#     "regex": '.*',
#     "help_text": _("Your password does not meet the requirements.")
# }

# Disable simplified floating IP address management for deployments with
# multiple floating IP pools or complex network requirements.
# HORIZON_CONFIG["simple_ip_management"] = False

# Turn off browser autocompletion for the login form if so desired.
# HORIZON_CONFIG["password_autocomplete"] = "off"

LOCAL_PATH = os.path.dirname(os.path.abspath(__file__))

# Set custom secret key:
# You can either set it to a specific value or you can let horizion generate a
# default secret key that is unique on this machine, e.i. regardless of the
# amount of Python WSGI workers (if used behind Apache+mod_wsgi): However, there
# may be situations where you would want to set this explicitly, e.g. when
# multiple dashboard instances are distributed on different machines (usually
# behind a load-balancer). Either you have to make sure that a session gets all
# requests routed to the same dashboard instance or you set the same SECRET_KEY
# for all of them.

SECRET_KEY = "{{ secret }}"

# We recommend you use memcached for development; otherwise after every reload
# of the django development server, you will have to login again. To use
# memcached set CACHES to something like
# CACHES = {
#    'default': {
#        'BACKEND' : 'django.core.cache.backends.memcached.MemcachedCache',
#        'LOCATION' : '127.0.0.1:11211',
#    }
#}

CACHES = {
    'default': {
        'BACKEND' : 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION' : '127.0.0.1:11211'
    }
}

# Send email to the console by default
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# Or send them to /dev/null
#EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'

{% if ubuntu_theme %}
# Enable the Ubuntu theme if it is present.
try:
    from ubuntu_theme import *
except ImportError:
    pass
{% endif %}

# Default Ubuntu apache configuration uses /horizon as the application root.
# Configure auth redirects here accordingly.
LOGIN_URL='{{ webroot }}/auth/login/'
LOGIN_REDIRECT_URL='{{ webroot }}'

# The Ubuntu package includes pre-compressed JS and compiled CSS to allow
# offline compression by default.  To enable online compression, install
# the node-less package and enable the following option.
COMPRESS_OFFLINE = {{ compress_offline }}

# Configure these for your outgoing email host
# EMAIL_HOST = 'smtp.my-company.com'
# EMAIL_PORT = 25
# EMAIL_HOST_USER = 'djangomail'
# EMAIL_HOST_PASSWORD = 'top-secret!'

# For multiple regions uncomment this configuration, and add (endpoint, title).
# AVAILABLE_REGIONS = [
#     ('http://cluster1.example.com:5000/v2.0', 'cluster1'),
#     ('http://cluster2.example.com:5000/v2.0', 'cluster2'),
# ]

OPENSTACK_HOST = "127.0.0.1"
OPENSTACK_KEYSTONE_URL = "{{ service_protocol }}://{{ service_host }}:{{ service_port }}/v2.0"
OPENSTACK_KEYSTONE_DEFAULT_ROLE = "{{ default_role }}"

# Disable SSL certificate checks (useful for self-signed certificates):
# OPENSTACK_SSL_NO_VERIFY = True

# The OPENSTACK_KEYSTONE_BACKEND settings can be used to identify the
# capabilities of the auth backend for Keystone.
# If Keystone has been configured to use LDAP as the auth backend then set
# can_edit_user to False and name to 'ldap'.
#
# TODO(tres): Remove these once Keystone has an API to identify auth backend.
OPENSTACK_KEYSTONE_BACKEND = {
    'name': 'native',
    'can_edit_user': True,
    'can_edit_project': True
}

OPENSTACK_HYPERVISOR_FEATURES = {
    'can_set_mount_point': True,

    # NOTE: as of Grizzly this is not yet supported in Nova so enabling this
    # setting will not do anything useful
    'can_encrypt_volumes': False
}

# The OPENSTACK_QUANTUM_NETWORK settings can be used to enable optional
# services provided by quantum.  Currently only the load balancer service
# is available.
OPENSTACK_QUANTUM_NETWORK = {
    'enable_lb': False
}

# OPENSTACK_ENDPOINT_TYPE specifies the endpoint type to use for the endpoints
# in the Keystone service catalog. Use this setting when Horizon is running
# external to the OpenStack environment. The default is 'internalURL'.
#OPENSTACK_ENDPOINT_TYPE = "publicURL"

# The number of objects (Swift containers/objects or images) to display
# on a single page before providing a paging element (a "more" link)
# to paginate results.
API_RESULT_LIMIT = 1000
API_RESULT_PAGE_SIZE = 20

# The timezone of the server. This should correspond with the timezone
# of your entire OpenStack installation, and hopefully be in UTC.
TIME_ZONE = "UTC"

LOGGING = {
    'version': 1,
    # When set to True this will disable all logging except
    # for loggers specified in this configuration dictionary. Note that
    # if nothing is specified here and disable_existing_loggers is True,
    # django.db.backends will still log unless it is disabled explicitly.
    'disable_existing_loggers': False,
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'django.utils.log.NullHandler',
        },
	{% if use_syslog %}
        'syslog': {
            'level': 'INFO',
            'class': 'logging.handlers.SysLogHandler',
        },
	{% endif %}
        'console': {
            # Set the level to "DEBUG" for verbose output logging.
            'level': 'INFO',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        # Logging from django.db.backends is VERY verbose, send to null
        # by default.
        'django.db.backends': {
            'handlers': ['null'],
            'propagate': False,
        },
        'requests': {
            'handlers': ['null'],
            'propagate': False,
        },
        'horizon': {
            {% if use_syslog %}
            'handlers': ['syslog'],
            {% else %}
            'handlers': ['console'],
            {% endif %}
            'propagate': False,
        },
        'openstack_dashboard': {
            {% if use_syslog %}
            'handlers': ['syslog'],
            {% else %}
            'handlers': ['console'],
            {% endif %}
            'propagate': False,
        },
        'openstack_auth': {
            {% if use_syslog %}
            'handlers': ['syslog'],
            {% else %}
            'handlers': ['console'],
            {% endif %}
            'propagate': False,
        },
        'novaclient': {
            {% if use_syslog %}
            'handlers': ['syslog'],
            {% else %}
            'handlers': ['console'],
            {% endif %}
            'propagate': False,
        },
        'keystoneclient': {
            {% if use_syslog %}
            'handlers': ['syslog'],
            {% else %}
            'handlers': ['console'],
            {% endif %}
            'propagate': False,
        },
        'glanceclient': {
            {% if use_syslog %}
            'handlers': ['syslog'],
            {% else %}
            'handlers': ['console'],
            {% endif %}
            'propagate': False,
        },
        'nose.plugins.manager': {
            {% if use_syslog %}
            'handlers': ['syslog'],
            {% else %}
            'handlers': ['console'],
            {% endif %}
            'propagate': False,
        }
    }
}
