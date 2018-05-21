#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
from app import create_app

application = create_app(os.getenv('FLASK_CONFIG') or 'default')

if __name__ == '__main__':
    application.run(debug=True, host="0.0.0.0", port=5000)
