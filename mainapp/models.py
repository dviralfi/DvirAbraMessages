"""
Models - a model maps to a single database table

This file contains implementation of Model Classes: 

* Message
* MessageUser
"""


from django.db import models
from django.contrib.auth.models import AbstractUser

class Message(models.Model):
    """
    A class to represent a Message.

    Attributes
    ----------
    sender : ForeignKey of MessageUser model
        The message sender MessageUser Object

    receiver : ForeignKey of MessageUser model
        The message receiver MessageUser Object

    message_txt : str
        the message text content
    subject : str (maximum 50 characters)
        The Message subject

    creation_date : DateField (comes from models.Model Fields)

    is_read : Boolean
        True - if the message have been read by the User
        False - not read yet

    Methods
    -------
    __str__(self): (override built-in method)
        returns the Message subject
    """
    
    # 'null=False, blank=False' means that these fields are required both in the user-end(by django), and in the database.
    sender = models.ForeignKey('MessageUser',on_delete=models.CASCADE,related_name='sender',null=False, blank=False) 

    receiver = models.ForeignKey('MessageUser',on_delete=models.CASCADE,related_name='receiver',null=False, blank=False)

    
    message_txt = models.TextField(blank=True,null=True) # This Field can be empty
    subject = models.CharField(max_length=50,blank=True,null=True) # This Field can be empty
    creation_date = models.DateTimeField(auto_now_add=True) # the auto_now_add=True generates the date right when the Object is created
    is_read = models.BooleanField(default=False) # Default is that the message not been read yet


    def __str__(self):
        return self.subject

    class Meta:
        ordering = ['creation_date'] # order the Messages by creation date.

class MessageUser(AbstractUser):
    """
    A class to represent a User.

    The class Inherits the `AbstractUser` Class that Django provides, which gives you all the methods and attributes the Desault `User` Class have, and you can custom it for your own needs.

    in this project case - I added the `messages` as a ManyToMany Field.
    """
    messages = models.ManyToManyField(Message)








        


    
    """
    def get_user_messages(self):
        messages = Message.objects.filter(Q(sender=self.id)|Q(receiver=self.id))
        return messages
    """