from config import settings
from util.send_mail import SendMail
import json,time,sys
from base.count import Count

class MailReport:

    def send_result_mail(self,report_file=None):
        c = Count()
        count_tuple = c.count()
        count = str(int(count_tuple[0]) + int(count_tuple[1]))
        content = settings.EMAIL_CONTENT.format(count,count_tuple[0],count_tuple[1],report_file,
                                                settings.DB_TYPE,settings.DB_HOST,settings.DB_USER,settings.DB_PASSWD,
                                                settings.DB_NAME,settings.TABLE_NAME)
        s = SendMail()
        sub = settings.EMAIL_SUB.format(time.strftime("%Y-%m-%d %H:%M:%S"))
        s.send_mail(settings.EMAIL_RECEIVER, sub, content)

if __name__ == "__main__":
    m = MailReport()
    m.send_result_mail(sys.argv[1])
