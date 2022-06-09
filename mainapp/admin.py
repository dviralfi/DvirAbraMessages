"""
Admin site models registration file
"""


from django.contrib import admin
from mainapp.models import *


admin.site.register(Message)
admin.site.register(MessageUser)
