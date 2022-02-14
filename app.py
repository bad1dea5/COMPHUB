#
#
#

from eventlet import listen, wsgi
from COMPHUB.application import create_app

app = create_app()
wsgi.server(listen(('', 8080)), app, debug=True)
