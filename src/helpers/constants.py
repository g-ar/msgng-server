import os
import sys

BASE_DIR = os.path.realpath(sys.argv[0]).split('/src')[0]
HOST = ""
PORT = 6666
DATABASE = {"path": os.path.join(BASE_DIR, "msg.db")}
