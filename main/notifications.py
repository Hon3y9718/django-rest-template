from django.core.mail import EmailMessage
import requests
import json

class NotificationService(): 
    APPID = "c536abcd-6020-4377-a331-9eac2a7a04f2"
    RESTAPIKEY = "Yjg5YWVhNGMtODU3Yy00NzQxLTlkN2YtYzE4MTBiZmRjMGJl"

    PUSH_BASE_URL = "https://onesignal.com/api/v1/notifications"

    def sendEmail(self, toMail, subject, body):
        try:
            email = EmailMessage(subject=subject, body=body, from_email="info@mindmeadow.in", to=[toMail])
            email.send()
            print("email sent")
            return True
        except:
            print("email Not sent")
            return False

    def sendPush(self, data, title, subtitle, playerIds):
            header = {
                "Content-Type": "application/json; charset:utf-8",
                "Authorization": f"Basic {self.RESTAPIKEY}"
            }

            body = {
                "app_id": f"{self.APPID}",
                "include_player_ids": playerIds,
                "contents": {"en": f"{subtitle}"},
                "headings": {"en": f"{title}"}
            }     

            try:
                res = requests.post(self.PUSH_BASE_URL, headers=header, data=json.dumps(body))

                print(res.content)
                if(res.status_code == 200):
                    print("Push Sent")
                    return True
                
                else:
                    print("Push Not Sent")
                    return False
            except:
                print("Push Not Sent ")