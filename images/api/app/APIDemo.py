 #  ______    ______   ______       ___   ___   ________   _________  
 # /_____/\  /_____/\ /_____/\     /__/\ /__/\ /_______/\ /________/\ 
 # \:::_ \ \ \::::_\/_\:::_ \ \    \::\ \\  \ \\::: _  \ \\__.::.__\/ 
 #  \:(_) ) )_\:\/___/\\:\ \ \ \    \::\/_\ .\ \\::(_)  \ \  \::\ \   
 #   \: __ `\ \\::___\/_\:\ \ \ \    \:: ___::\ \\:: __  \ \  \::\ \  
 #    \ \ `\ \ \\:\____/\\:\/.:| |    \: \ \\::\ \\:.\ \  \ \  \::\ \ 
 #     \_\/ \_\/ \_____\/ \____/_/     \__\/ \::\/ \__\/\__\/   \__\/ 
 #
 # Project: 3scale Quick Demo
 # @author : Samuel Andersen
 # @version: 2020-04-28
 #
 # General Notes:
 #
 # TODO: Continue adding functionality 
 #
 #

import requests
import json
import io
import os
import uuid
import urllib.parse
from flask import Flask
from flask import render_template
from flask import request
from flask import send_file
from flask import make_response
from flask import session
from flask import redirect
from flask import url_for
from flask import escape
from flask import send_from_directory
from flask_restful import reqparse, abort, Api, Resource
from functools import wraps, update_wrapper
from datetime import datetime, timedelta, tzinfo, timezone
from werkzeug.http import parse_authorization_header

app = Flask(__name__)
api = Api(app)

## Simple Response to the <api>/hello call
class Hello(Resource):

	## Have a header to be used across the different methods
	customHeader = {
		'Access-Control-Allow-Origin': '*',
		'Access-Control-Allow-Methods': 'GET',
		'Access-Control-Allow-Headers': 'Content-Type, Auth-User, Remote-User',
		'Access-Control-Allow-Credentials': 'true',
	}

	## Method to respond to OPTIONS
	def options(self):

		return {'Allow': 'GET'}, 200, self.customHeader

	## Method to handle GET requests
	def get(self):

		if (os.environ['API_VERSION'] == '1'):

			return "Hello from api-1!", 200, self.customHeader

		elif (os.environ['API_VERSION'] == '2'):

			return "Aloha from api-2~", 200, self.customHeader

		return "Thanks for using api-3.", 200, self.customHeader

## Check if a user is sent with the <api>/check_header call
class CheckHeader(Resource):

	## Have a header to be used across the different methods
	customHeader = {
		'Access-Control-Allow-Origin': '*',
		'Access-Control-Allow-Methods': 'GET',
		'Access-Control-Allow-Headers': 'Content-Type, Auth-User, Remote-User, X-Red-Hat-Auth',
		'Access-Control-Allow-Credentials': 'true',
	}

	## Method to respond to OPTIONS
	def options(self):

		return {'Allow': 'GET'}, 200, self.customHeader

	## Method to handle GET requests
	def get(self):

		userRead = request.headers.get('X-Red-Hat-Auth')

		if ((not userRead) or (len(userRead) == 0)):

			return "Unauthorized", 403, self.customHeader

		if (os.environ['API_VERSION'] == '1'):

			return "User on api-1 is %s" % userRead, 200, self.customHeader

		return "Generic response", 200, self.customHeader


## Define the APIs we're exposing in this section
api.add_resource(Hello, '/api/hello')

api.add_resource(CheckHeader, '/api/check_header')

if __name__ == '__main__':

	app.secret_key = b'\x1c\x99\xf6"2\xe9\xcf\xcatk42\xa2\x8e\xc7\xee\xb45\xc1l\xf0It\x08'
	
	app.run(threaded = False)