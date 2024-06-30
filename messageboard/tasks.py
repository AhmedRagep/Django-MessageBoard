from celery import shared_task
from django.core.mail import EmailMessage
from .models import *
from datetime import datetime
from django.template.loader import render_to_string



@shared_task(name='email_notification')
def send_email_task(subject,body,emailaddress):
    email = EmailMessage(subject, body, to=[emailaddress])
    email.send()
    return emailaddress



@shared_task(name='monthly_newsletter')
def send_newsletter():
    # عنوان الرسالة
    subject = "You Monthly Newsletter"
    # جلب المشتركين فقط
    subscribers = MessageBoard.objects.get(id=1).subscribers.filter(
       profile__newsletter_subscribe=True,
    )
    # تكرار علي المشتركين
    for subscriber in subscribers:
      # تحويل ملف العرض مع اسم المشترك
      body = render_to_string('newsletter.html',{'name':subscriber.profile.name})
      # طريقة ارسال البينات
      email = EmailMessage(subject,body,to=[subscriber.email])
      # تعريف المحتوي علي انه عرض
      email.content_subtype = 'html'
      # ارسال
      email.send()
    # جلب الشهر
    current_month = datetime.now().strftime('%B')
    # جلب عدد المشتركين
    subscriber_count = subscribers.count()
    # ارجاع هذا في ترمينال
    return f'{current_month} Newsletter to {subscriber_count} subs'