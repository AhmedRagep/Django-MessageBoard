from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib import messages
from django.core.mail import EmailMessage
import threading
from .models import *
from .forms import *
from .tasks import *
# Create your views here.

@login_required
def messageboard(request):
  messageboard = get_object_or_404(MessageBoard,id=1)
  form = MessageCreateForm()
  if request.POST:
    if request.user in messageboard.subscribers.all():
      form = MessageCreateForm(request.POST)
      if form.is_valid():
        message = form.save(commit=False)
        message.author = request.user
        message.messageboard = messageboard
        message.save()
        send_email(message)
    else:
      messages.warning(request,'You need to be subscribed!!')
    return redirect('messageboard')

  return render(request,'index.html',{
    'messageboard':messageboard,
    'form':form
  })


@login_required
def subscribe(request):
  messageboard = get_object_or_404(MessageBoard, id=1)
  if request.user not in messageboard.subscribers.all():
    messageboard.subscribers.add(request.user)
  else:
    messageboard.subscribers.remove(request.user)
  return redirect('messageboard')




def send_email(message):
  messageboard = message.messageboard 
  subscribers = messageboard.subscribers.all()

  for subscriber in subscribers: 
    subject = f'New Message from {message.author.profile.name}'
    body = f'{message.author.profile.name}: {message.body}\n\nRegards from\nMy Message Board'
    
    # ارسال الرسالة باستخدام celery
    send_email_task.delay(subject, body, subscriber.email)


    # بديل ل سيلري ولاكن للمهام البسيطه
#     email_thread = threading.Thread(target=send_email_thread,args=(subject, body, subscriber))
#     email_thread.start()

# def send_email_thread(subject,body,subscriber):
#     email = EmailMessage(subject, body, to=[subscriber.email])
#     email.send()




def staff_user(user):
  return user.is_staff

@user_passes_test(staff_user)
def newsletter(request):
  return render(request,'newsletter.html')