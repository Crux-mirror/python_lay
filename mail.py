
#coding=utf-8
from email.mime.text import MIMEText
import smtplib
from email.header import Header
from email import encoders
from email.utils import parseaddr,formataddr
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase


def _format_addr(s):
    name,addr = parseaddr(s)
    return formataddr((Header(name,'utf-8').encode(),\
addr.encode('utf-8') if isinstance(addr,unicode) else addr))


#邮件对象
msg = MIMEMultipart()

#邮件正文
msg.attach(MIMEText('send with file...','plain','utf-8'))

#添加附件MIMEBase
with open(r'C:\Users\30\Desktop\emoji.jpg','rb') as f:
    #设置附件的MIME和文件名
    mime = MIMEBase('image','jpeg',filename='emoji.jpg')
    print 'aa'
    #加上必要头部信息
    mime.add_header('Content-Disposition', 'attachment', filename='emoji.jpg')
    mime.add_header('Content-ID', '<0>')
    mime.add_header('X-Attachment-Id', '0')
    #读取附件内容
    mime.set_payload(f.read())

    #BAse64编码
    encoders.encode_base64(mime)
    #添加到MIMEMutipart中
    msg.attach(mime)

#email 地址和口令
from_addr = '18883855535@163.com'
passwprd = raw_input('passwprd:')

#stmp服务器地址
smtp_server = 'smtp.163.com'
#收件人地址
to_addr = '1041298470@qq.com'

msg['From'] = _format_addr(u'python爱好者<%s>' %from_addr)
msg['To'] = _format_addr(u'管理员<%s>' %to_addr)
msg['Subject'] = Header(u'来自smtp的测试...','utf-8').encode()

server = smtplib.SMTP(smtp_server,25)#默认端口25
#server.connect(smtp_server)
server.set_debuglevel(1)
server.login(from_addr,passwprd)
for i in range(1,4):
    server.sendmail(from_addr,[to_addr],msg.as_string())
server.quit()