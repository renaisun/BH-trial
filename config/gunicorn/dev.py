# Django WSGI application path in pattern MODULE_NAME:VARIABLE_NAME
wsgi_app = "financial_data.wsgi:application"
# The granularity of Error log outputs
loglevel = "debug"
# The number of worker processes for handling requests
workers = 2
# The socket to bind
bind = "0.0.0.0:8123"
# Restart workers when code changes (development only!)
reload = True
# Write access and error info to /var/log
accesslog = errorlog = "./logs/dev.log"
# Redirect stdout/stderr to log file
capture_output = False
# PID file so you can easily fetch process ID
pidfile = "./dev.pid"
# Daemonize the Gunicorn process (detach & enter background)
daemon = False