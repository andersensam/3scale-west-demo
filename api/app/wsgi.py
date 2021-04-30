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
 # @version: 2020-04-26
 #
 # General Notes:
 #
 # TODO: Continue adding functionality 
 #
 #

import os
from APIDemo import app as application

if __name__ == '__main__':
	from wsgiref.simple_server import make_server
	httpd = make_server('', 8080, application)
	httpd.serve_forever()
