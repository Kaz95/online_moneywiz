from flask import Flask

app = Flask(__name__)

from online_moneywiz import routes
