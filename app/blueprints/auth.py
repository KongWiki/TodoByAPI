"""
@time : 2019/7/25上午10:45
@Author: kongwiki
@File: auth.py
@Email: kongwiki@163.com
"""
from faker import Faker
from flask import render_template, redirect, url_for, Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from flask_babel import _

from app.extensions import db
from app.models import User, Item

auth_bp = Blueprint('auth', __name__)
fake = Faker()

"""
认证蓝本
生成测试账户
进行用户账号的 注册 登录 登出
"""


# 登录处理
@auth_bp.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('todo.app'))
    if request.method == 'POST':
        data = request.get_json()
        username = data['username']
        password = data['password']

        user = User.query.filter_by(username=username).first()
        if user is not None and user.validate_password(password):
            login_user(user)
            return jsonify(message=_('Login Success'))
        return jsonify(message=_('Invalid username or password')), 400
    return render_template('_login.html')


# 注册
@auth_bp.route("/register")
def register():
    username = fake.user_name()
    # 确保随机生成的用户名不重复
    while User.query.filter_by(username=username).first() is not None:
        username = fake.user_name()
    password = fake.word()
    user = User(username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    # 添加几个待办条目 作为示例
    item1 = Item(body=("Good good study day day up"), author=user)
    item2 = Item(body=("Eate apple"), author=user)
    item3 = Item(body=("Clean the bedroom"), author=user)
    item4 = Item(body=("Go to sleep"), author=user, done=True)
    db.session.add_all([item1, item2, item3, item4])
    db.session.commit()

    return jsonify(username=username, password=password, message=_('Generate success.'))


# 退出登录
@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return jsonify(message=_('Logout Success.'))
