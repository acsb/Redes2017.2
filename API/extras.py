from flask_restful import *

class HelloWorld(Resource):

	def get(self):
		headers = {'Content-Type': 'text/html'}
		return make_response(render_template('./template/index.html'),200,headers)