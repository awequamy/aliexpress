from django.core.mail import send_mail

def send_confirmation_email(user, code):
    code=code
    # code=user.activation_code
    full_link=f'http://localhost:8000/api/v1/account/activate/{code}/'
    to_email=user
    send_mail('Hi, activate your account!',
    f'Click on the link to activate your account: {full_link}',
    'awequamy@gmail.com',
    [to_email],
    fail_silently=False
    )

def send_reset_password(user):
    code=user.activation_code
    to_email=user.email
    send_mail(
        'Subject',
        f'Your code for resetting the password:{code}',
        'from@example.com',
        [to_email],
        fail_silently=False
    )


def send_notification(user,id):
    code=user.activation_code
    to_email=user.email
    send_mail(
        'Уведомление о создании заказа!!!',
        f'Вы создали заказ номер:{id}',
        'from@example.com',
        [to_email],
        fail_silently=False
    )