from inspect import getsourcefile
import os.path
import sys

current_path = os.path.abspath(getsourcefile(lambda:0))
current_dir = os.path.dirname(current_path)
parent_dir = current_dir[:current_dir.rfind(os.path.sep)]

sys.path.insert(0, parent_dir)

from v1.api import *

api.add_resource(Authenticate, '/Authenticate')
api.add_resource(logout, '/logout')



if __name__ == '__main__':
    app.run(debug=True)
