"""
@time : 2019/7/25上午10:45
@Author: kongwiki
@File: home.py
@Email: kongwiki@163.com
"""
from flask import Blueprint, render_template

home_bp = Blueprint('home', __name__)


@home_bp.route("/index")
def index():
    return render_template("index.html")


@home_bp.route("/intro")
def intro():
    return render_template('_intro.html')
