# -*- coding: utf-8 -*-
from celery.decorators import task, periodic_task

@task
def send_mail(user, subject, message, default_from):
    user.email_user(subject, message, default_from)
