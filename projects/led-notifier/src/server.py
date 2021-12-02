# External deps.
from flask import Flask, render_template, request

# Internal deps.
import api

app = Flask( __name__ )

@app.route( '/' )
def index():
    return render_template( 'index.html' )

@app.route( '/api/' )
def api_route():
    api.handler( request )
    return 'Default API response, done.'

@app.route( '/api/logs/' )
def logs_route():
    logs = api.get_logs()
    return str( logs )

# Start the web server.
if __name__ == '__main__':
    app.run( host = '0.0.0.0', port = 80, debug = False )
