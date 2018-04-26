#!/usr/bin/python
# -*- coding: utf-8 -*-
from app import create_app
# from flask_script import Manager
import os


application = create_app(os.getenv('FLASK_CONFIG') or 'default')
# manager = Manager(application)

if __name__ == '__main__':
    application.run(debug=True)
    # manager.run()
