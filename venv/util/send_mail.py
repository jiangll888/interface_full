import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header

class SendMail:
    #global send_user = ""
    def send_mail(self,user_list,sub,content,filename=None):
        sender = "sasa <853876175@qq.com>"
        message = MIMEText(content,_subtype="plain",_charset="utf-8")
        # message = MIMEMultipart()
        message['From'] = Header(sender)
        message['To'] = Header(":".join(user_list))
        message['Subject'] = Header(sub)
        #
        # message.attach(MIMEText(content,_subtype="plain",_charset="utf-8"))

        # att1 = MIMEText(open(filename,"rb").read(),"base64","utf-8")
        # att1["Content-Type"] = 'application/octet-stream'
        # att1["Content-Disposition"] = 'attachment; filename="test.html"'
        # message.attach(att1)

        server = smtplib.SMTP()
        server.connect("smtp.qq.com")
        server.login("853876175@qq.com","oqylmankyowdbdgh")
        server.sendmail(sender,user_list,message.as_string())
        server.close()

if __name__ == "__main__":
    s = SendMail()
    s.send_mail(["jiangliulin@163.com"],"testtest","hahahha")