from django.dispatch import receiver
from django.db.models.signals import post_save, m2m_changed

from user_profile.models import User
from .models import Notification