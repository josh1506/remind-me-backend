from django.core.mail import EmailMessage


class Utils:
    @staticmethod
    def send_email(data):
        '''
        send_email(subject, body, to)
        subject - email subject/headline of the email
        body - email body
        to - who will be sending
        '''

        subject = data['subject']
        body = data['body']
        user_email = data['to']

        email = EmailMessage(subject=subject, body=body, to=[user_email])
        email.send()
