"""
@time : 2019/7/25上午10:45
@Author: kongwiki
@File: todo.py
@Email: kongwiki@163.com
"""
from flask import render_template, request, Blueprint, jsonify
from flask_login import current_user, login_required

from app.extensions import db
from app.models import Item


todo_bp = Blueprint("todo", __name__)

"""
todo的CRUD
"""


@todo_bp.route("/items/new", methods=['POST'])
@login_required
def new_item():
    data = request.get_json()
    if data is None or data['body'].strip() == '':
        return jsonify(message='非法数据'), 400
    item =  Item(body=data['body'], author=current_user._get_current_object())
    db.session.add(item)
    db.session.commit()
    return jsonify(html=render_template('_item.html', item=item), message='+1')



