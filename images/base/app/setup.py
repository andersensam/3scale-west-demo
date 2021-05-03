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

from setuptools import setup

requirements = list()
with open('/tmp/app/requirements.txt') as f:
	requirements = f.read().splitlines()

setup(name='3scale Demo',
      version='1.0',
      description='Base image for 3scale API demo',
      author='Samuel Andersen',
      author_email='samander@redhat.com',
      url='https://3scale.apps.lab.andersentech.net',
      install_requires=requirements,
     )
