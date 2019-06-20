#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
import time
import hashlib
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib


# 项目 scheme 名称（一般就是我们的工程名称）
project_scheme = "xxxx"
# 指定项目下 build 编译目录（存放在工程根目录 build 文件里）
build_path = "./build"
# 指定项目下 archive 编译目录
archive_path = build_path + "/archive/temp.xcarchive"
# 打包后ipa存储目录（存放在工程目录 build 里的 ipa 文件里）
targer_ipa_path = build_path + "/ipa"

# 配置蒲公英KEY
API_KEY = "xxxxxxxxxxxxxxxxxxxx"
# 配置蒲公英更新描述信息
PGYER_DESC = "xxxxxxxxxxxxxxxxxxxx"

# 邮件信息
from_addr = "xxxx@163.com"
password = "xxxxxxxx"
smtp_server = "smtp.163.com"
to_addr = 'xxxx@xx.com'


# 清理项目 build目录
def clean_project_build():
    print "cleaning..."

    os.system("rm -r %s" % (build_path))

    print "\n** CLEAN ARCHIVE FILE SUCCEED **\n"

# build
def build_project():
    print "archiving..."

    os.system('xcodebuild archive -scheme %s -archivePath %s -configuration Release' % (project_scheme,archive_path))

# 打包ipa
def build_ipa():
    print "exporting..."

    global ipa_filename
    ipa_filename = time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))
    os.system ('xcodebuild -exportArchive -archivePath %s -exportPath %s/%s -exportOptionsPlist exportIpaOption.plist'%(archive_path,targer_ipa_path,ipa_filename))

#上传配置蒲
def upload_Pgyer():
    print "uploading..."

    ipa_path = ("%s/%s/%s.ipa" % (targer_ipa_path,ipa_filename,project_scheme))
    print "ipaPath:"+ipa_path
    ipa_path = os.path.expanduser(ipa_path)
    upload_com = "curl -F 'file=@%s' -F '_api_key=%s' -F 'buildUpdateDescription=%s' https://www.pgyer.com/apiv2/app/upload" % (ipa_path,API_KEY,PGYER_DESC)
    os.system(upload_com)
    print "\n** UPLOAD TO PGYER SUCCEED **\n"

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))
    
# 发邮件
def send_mail():
    print "sending..."
    
    msg = MIMEText('iOS测试项目已经打包完毕，请前往 https://www.pgyer.com/xxxxx 下载测试！', 'plain', 'utf-8')
    msg['From'] = _format_addr('自动打包系统 <%s>' % from_addr)
    msg['To'] = _format_addr('测试人员 <%s>' % to_addr)
    msg['Subject'] = Header('iOS客户端打包程序', 'utf-8').encode()
    server = smtplib.SMTP(smtp_server)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(from_addr, password)
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()
    print "\n** SEND EMAIL SUCCEED **\n"

def main():
    # 清理build目录
    clean_project_build()
    # 编译项目
    build_project()
    # 打包ipa
    build_ipa()
    # 上传蒲公英
    upload_Pgyer()
    # 发邮件
    send_mail()

# 执行
main()
