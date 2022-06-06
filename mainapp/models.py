
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q


class Message(models.Model):
    
    sender = models.ForeignKey(User,on_delete=models.CASCADE,related_name='sender',null=False, blank=False,verbose_name=User.get_username) 

    receiver = models.ForeignKey(User,on_delete=models.CASCADE,related_name='receiver',null=False, blank=False,verbose_name=User.get_username)

    # 'null=False, blank=False' means that these fields are required both in the user-end(by django), and in the database.
    message_txt = models.TextField()
    subject = models.CharField(max_length=50)
    creation_date = models.DateTimeField(auto_now_add=True) 
    is_read = models.BooleanField(default=False)


    def __str__(self):
        return self.subject

    class Meta:
        ordering = ['creation_date'] # order the Messages by creation date.

class User(User):
    messages = models.ManyToManyField(Message)


    def __repr__(self):
        return self.username








        


    
    """
    def get_user_messages(self):
        messages = Message.objects.filter(Q(sender=self.id)|Q(receiver=self.id))
        return messages
    """