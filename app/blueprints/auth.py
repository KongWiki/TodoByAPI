"""
@time : 2019/7/25上午10:45
@Author: kongwiki
@File: auth.py
@Email: kongwiki@163.com
"""
"""
认证蓝本
生成测试账户
"""
from faker import Faker
from flask import render_template, redirect, url_for, Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user

from app.extensions import db
from app.models import User, Item

auth_bp = Blueprint('auth', __name__)
fake = Faker()


@auth_bp.route("/register")
def register():
    username = fake.user_name()
    # 确保随机生成的用户名不重复
    while User.query.fileter_by(username=username).first() is not None:
        username = fake.user_name()
    password = fake.word()
    user = User(username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    # 添加几个待办条目 作为示例
    item1 = Item(body=("Good good study day day up"), author=user)
    item2 = Item(body=("eate apple"), author=user)
    item3 = Item(body=("clean the bedroom"), author=user)
    item4 = Item(body=_("go to sleep"), author=user, done=True)
    db.session.add_all([item1, item2, item3, item4])
    db.session.commit()

    return jsonify(username=username, password=password, message='Generate success.')
