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


# 首页 展示数据
@todo_bp.route('/app')
@login_required
def app():
    # 数据库中所有的任务
    all_count = Item.query.with_parent(current_user).count()
    # 计划完成任务
    active_count = Item.query.with_parent(current_user).filter_by(done=False).count()
    # 已经完成任务
    completed_count = Item.query.with_parent(current_user).filter_by(done=True).count()
    return render_template('_app.html', items=current_user.items,
                           all_count=all_count, active_count=active_count, completed_count=completed_count)


# 增
@todo_bp.route("/items/new", methods=['POST'])
@login_required
def new_item():
    data = request.get_json()
    if data is None or data['body'].strip() == '':
        return jsonify(message='非法数据'), 400
    item = Item(body=data['body'], author=current_user._get_current_object())
    db.session.add(item)
    db.session.commit()
    return jsonify(html=render_template('_item.html', item=item), message='+1')


# 改
@todo_bp.route("/item/<int:item_id>/edit", methods=["PUT"])
@login_required
def edit_item(item_id):
    item = Item.query.get_or_404(item_id)
    if current_user != item.author:
        return jsonify(message='Permission denied. '), 403

    data = request.get_json()
    if data is None or data['body'].strip() == '':
        return jsonify(message='Invalid item body. '), 400
    item.body = data['body']
    db.session.commit()
    return jsonify(message='Item updated')


# 局部更新
@todo_bp.route('/item/<int:item_id>/toggle', methods=["PATCH"])
@login_required
def toggle_item(item_id):
    item = Item.query.get_or_404(item_id)
    if current_user != item.author:
        return jsonify(message="Permission denied."), 403
    item.done = not item.done
    db.session.commit()
    return jsonify(message='Item toggled.')


# 删
@todo_bp.route('/item/<int:item_id>/delete', methods=['DELETE'])
@login_required
def delete_item(item_id):
    item = Item.query.get_or_404(item_id)
    if current_user != item.author:
        return jsonify(message="Permission denied. "), 403

    db.session.delete(item)
    db.session.commit()
    return jsonify(message="Item delated.")


# 删除表
@todo_bp.route("/item/clear", methods=['DELETE'])
@login_required
def clear_items():
    items = Item.query.with_parent(current_user).filter_by(done=True).all()
    for item in items:
        db.session.delete(item)
    db.session.commit()
    return jsonify(message="All clear!")
