from flask import Flask, Blueprint, render_template, redirect, url_for, request, jsonify
from flask_selfdoc import Autodoc

app = Flask(__name__)

auto = Autodoc(app)



doc = Blueprint('doc', __name__)
