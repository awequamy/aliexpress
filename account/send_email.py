from cgitb import html
from django.core.mail import send_mail
from product.models import *

def send_confirmation_email(user):
    code=user.activation_code
    full_link=f'http://localhost:8000/api/v1/account/activate/{code}/'
    to_email=user.email
    send_mail('HELLO! ACTIVATE YOUR ACCOUNT!!!',
    f'to activate your account click on the lilnk below:\n{full_link}', 
    'awequamy@gmail.com', 
    [to_email,],
    fail_silently=False)

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

# def send_html_email():
#     from django.template.loader import render_to_string
#     product=Product.objects.all()[0]
#     html_message=render_to_string('f.html',{'name':product.title, 'description':product.description})
#     send_mail(
#         'Subject',
#         'Vam pismo',
#         'example@admin.com',
#         ['awequamy@gmail.com'],
#         html_message=html_message,
#         fail_silently=False
#     )

