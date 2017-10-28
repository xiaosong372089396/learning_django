# -*- coding:utf-8 -*-

from flask import Flask
from flask import jsonify
from flask import abort
from flask import request
import MySQLdb as mysql
from flask import session
from flask.ext.httpauth import HTTPBasicAuth
import time
import commands
from mobile import message_mobile
from xemail.smtp_api import smtp_api


auth = HTTPBasicAuth()

import conf


app = Flask(__name__)

app.secret_key = 'xiaosong'


tasks1 = [
    {
        'id': 2,
        'code': 4000,
        'message': "验证错误!",
        'codeDesc': "Error",
    },
]


tasks2 = [
    {
        'id': 1,
        'code': 0,
        'message': "验证成功",
        'codeDesc': "Success",
    }
]



def ShowData(username, password):
    conn = mysql.connect(host=conf.DB_HOST, \
                         port=conf.DB_PORT, \
                         user=conf.DB_USER, \
                         passwd=conf.DB_PASS, \
                         db=conf.DB_DATABASE, \
                         charset=conf.DB_CHARSET)
    cur = conn.cursor()
    sql = "select * from auth_user where username='%s' and password='%s'" % (username, password)
    count = cur.execute(sql)
    cur.close()
    conn.close()
    return count != 0


@app.route('/mobile_message/api/v1.0/tasks', methods=['POST'])
def get_data():
    if request.method == 'POST':
        username = request.json.get('username')
        password = request.json.get('password')
        if username is None or password is None:
            abort(400)
        if ShowData(username, password):
            localtime = time.strftime("%b %d %Y %H:%M:%S", time.localtime())
            session['user'] = {'username': username}
            mobile_phone = request.json.get('mobile')
            content = request.json.get('content')
            if message_mobile.Message(mobile_phone, content):
                body = commands.getoutput("echo 'INFO' [ %s ], [ %s ], [ %s ].. >> mobile_message_history.log" % (localtime, mobile_phone, content))
                return jsonify({'tasks': tasks2})
            commands.getoutput("echo 'Error' [ %s ], [ %s ] .. >> mobile_message_error.log" % (localtime, mobile_phone,))
        else:
            return jsonify({'tasks': tasks1})
    else:
        abort(404)

@app.route('/sms_message/api/v1.1/tasks1', methods=['POST'])
def get_smtp():
    if request.method == 'POST':
        username = request.json.get('username')
        password = request.json.get('password')
        if username is None or password is None:
            abort(400)
        if ShowData(username, password):
            localtime = time.strftime("%b %d %Y %H:%M:%S", time.localtime())
            session['user'] = {'username': username}
            froms = request.json.get('from')    # 发件人
            to = request.json.get('to')          # 收件人
            passwd = request.json.get('passwd')  # 发件人邮箱密码
            subject = request.json.get('subject')  # 邮件主题
            content = request.json.get('content')  # 邮件内容
            result = smtp_api(Froms=froms, to=to, passwd=passwd, Subject=subject, content=content)
            if result:
                result.smtplogin()
                body = commands.getoutput("echo 'INFO' [ %s ], [%s, %s, %s, %s], [ %s ]" % (localtime, froms, to, passwd, subject, content))
                return jsonify({'tasks': tasks2})
            commands.getoutput("echo 'Error' [ %s ], [%s, %s, %s, %s], [ %s ]" % (localtime, froms, to, passwd, subject, content))
        else:
            return jsonify({'tasks': tasks1})
    else:
        abort(404)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

##
# Flask-HTTPAuth
# curl -i -X POST -H "Content-Type:application/json" -d '{"username": "xiaosong", "password":"123.com"}' http://127.0.0.1:5000/mobile_message/api/v1.0/tasks
# http://www.cnblogs.com/vovlie/p/4178077.html
# http://www.cnblogs.com/vovlie/p/4182814.html

# https://www.qcloud.com/document/api/228/3947
# http://www.pythondoc.com/flask-restful/third.html

# grant all privleges on messages.* to song@'localhost' identified by 'Ixianlai2016';

# curl -i -X POST -H Content-Type:application/json -d '{"username": "xiaosong", "password":"123.com", "mobile":"15701585464", "content": "hello 1"}' http://127.0.0.1:5000/mobile_message/api/v1.0/tasks