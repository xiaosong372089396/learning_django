#!/usr/bin/env python
# -*- coding:utf-8 -*-

import smtplib
import email.MIMEMultipart
import email.MIMEText
import email.MIMEBase
import os.path


From = "xiaosong@qq.com"
To = "to"
passwd = "123456"
# file_name = "history.log"
content = "hello 1111"


class smtp_api(object):
    # froms 发件人
    # to    收件人
    # passwd 发件人密码
    # file_name 文件名称
    # Subject 邮件主题
    # content 邮件内容
    def __init__(self, Froms, to, passwd, file_name=None, Subject=None, content=None):
        self.froms = Froms
        self.to = to
        self.passwd = passwd
        self.file_name = file_name
        self.subject = Subject
        self.content = content


    def smtplogin(self):
        server = smtplib.SMTP("smtp.exmail.qq.com")
        server.login(self.froms, self.passwd)  # 仅smtp服务器需要验证时

        # 构造MIMEMultipart对象做为根容器
        main_msg = email.MIMEMultipart.MIMEMultipart()

        # 构造MIMEText对象做为邮件显示内容并附加到根容器
        # text_msg = email.MIMEText.MIMEText("this is a test text to text mime")

        text_msg = email.MIMEText.MIMEText(self.content)
        main_msg.attach(text_msg)

        # 构造MIMEBase对象做为文件附件内容并附加到根容器
        contype = 'application/octet-stream'
        maintype, subtype = contype.split('/', 1)

        # 读入文件内容并格式化,  此处是增加附件功能
        # data = open(file_name, 'rb')
        # file_msg = email.MIMEBase.MIMEBase(maintype, subtype)
        # file_msg.set_payload(data.read())
        # data.close( )
        # email.Encoders.encode_base64(file_msg)

        # 设置附件头
        # basename = os.path.basename(file_name)
        # file_msg.add_header('Content-Disposition', 'attachment', filename=basename)
        # main_msg.attach(file_msg)

        # 设置根容器属性
        main_msg['From'] = self.froms
        main_msg['To'] = self.to
        main_msg['Subject'] = self.subject
        main_msg['Date'] = email.Utils.formatdate()

        # 得到格式化后的完整文本
        fullText = main_msg.as_string()

        # 用smtp发送邮件
        try:
            server.sendmail(self.froms, self.to, fullText)
        finally:
            server.quit()
            return True

#if __name__ == "__main__":
#    a = smtp_api(Froms=From, to=To, passwd=passwd, content=content)  # file_name
#    a.smtplogin()