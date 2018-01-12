__author__ = 'some_guy'
import os
import sys
# make python to know what the starting point of this whole thing
# and be able to find stuff within the app.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask_api import app


if __name__ == '__main__':
    app.run(port=3001, debug=True)
