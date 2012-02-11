#!/usr/bin/env python

from os import environ
from os.path import join, dirname

from google.appengine.dist import use_library
use_library('django', '1.2')

from google.appengine.ext import db
from google.appengine.ext.webapp import template, RequestHandler, WSGIApplication
from google.appengine.ext.webapp.util import run_wsgi_app


DEBUG = environ['SERVER_SOFTWARE'].startswith('Dev')
DIR = dirname(__file__)


def render_template(path):
	path = path.replace('/', ',')
	full_path = join(DIR, 'templates/%s.html' % path)

	html = template.render(full_path, {})

	if not DEBUG:
		html = html.replace('\n', '').replace('\t', '')

	return html


class MainHandler(RequestHandler):
	def get(self, path='index'):
		try:
			html = render_template(path)
		except:
			html = render_template('missing')

		self.response.out.write(html)


if __name__ == '__main__':
	routes = [
		(r'^/$' 								, MainHandler	),
		(r'^/((?:\w|\-)+(?:/(?:\w|\-)+)*)/?$'	, MainHandler	),
	]
	application = WSGIApplication(routes, debug=DEBUG)
	run_wsgi_app(application)
