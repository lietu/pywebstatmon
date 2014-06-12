import json
import os
from flask import Flask, send_from_directory
from flask.views import View
from jinja2 import FileSystemLoader, Environment

app = None


class MainView(View):
    """The view for the main (only) page"""

    def __init__(self):
        """Initialize our Jinja2 template"""
        jinja = Environment(loader=FileSystemLoader('web/templates/'))
        self.template = jinja.get_template("index.jinja2")

    def _render_view(self):
        """Simply render our view"""

        return self.template.render({})

    def dispatch_request(self):
        """Called when the URL rule is hit and request is routed to the view"""

        return self._render_view()


class DataView(View):
    """Provides the data updates to the main page"""

    @staticmethod
    def _render_view(results):
        """Return given data in a format the frontend understands"""

        data = []
        for url in results:
            data.append({
                "url": url,
                "last_result": results[url]
            })

        return json.dumps(data)

    def dispatch_request(self):
        """Called when the URL rule is hit and request is routed to the view"""

        results = app.get_results()
        return self._render_view(results)


def start(application):
    """Start the web frontend"""

    # Make sure our views can access the main application
    global app
    app = application

    static_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        '../static/'
    )

    config = app.get_config()

    frontend = Flask(__name__, static_folder=static_path)

    # Make sure we crash if there's some bug in the frontend code, this is so
    # we'll find the bugs
    frontend.config['PROPAGATE_EXCEPTIONS'] = True

    frontend.add_url_rule('/', view_func=MainView.as_view('index'))
    frontend.add_url_rule('/data.json', view_func=DataView.as_view('data'))

    # Set up the route for static files
    @frontend.route('/static/<path:filename>')
    def send_static(filename):
        return send_from_directory(static_path, filename)

    frontend.run(host='0.0.0.0', port=config.http_port)

    return frontend
