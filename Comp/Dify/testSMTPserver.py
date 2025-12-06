from aiosmtpd.controller import Controller

class Handler:
    async def handle_DATA(self, server, session, envelope):
        print("=== メール受信 ===")
        print("From:", envelope.mail_from)
        print("To:", envelope.rcpt_tos)
        print("Body:\n", envelope.content.decode("utf-8"))
        print("=================")
        return "250 OK"

controller = Controller(Handler(), hostname="0.0.0.0", port=1025)
controller.start()

print("SMTPサーバ起動中… Ctrl+C で停止")
import time
while True:
    time.sleep(1)
