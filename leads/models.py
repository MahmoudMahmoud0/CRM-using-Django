from django.db import models
# from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
# Create your models here.

# User = get_user_model() # it is highly recommended to create a custom User model so we can customize it

class UserProfile(models.Model):

    user = models.OneToOneField("User", on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class User(AbstractUser): # you have to tell Django that you have your own custom user model with "AUTH_USER_MODEL = 'leads.User'" in settings.py
    # customize here or pass
    is_organizer = models.BooleanField(default=True)
    is_agent = models.BooleanField(default=False)
    pass

class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) # One to one field: one user can have one agent
    organization = models.ForeignKey(UserProfile, on_delete=models.CASCADE) # or user_profile

    def __str__(self):
        '''
        returns the string representation of the object on the admin dashboard or in the shell
        '''
        return self.user.email
    

class Lead(models.Model):

    # SOURCES_CHOICE = (
    #     ('YouTube', 'YouTube'),
    #     ('Google', 'Google'),
    #     ('Newsletter', 'Newsletter'),
    # )


    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    age = models.IntegerField(default=0)

    # description = models.TextField()
    # date_added = models.DateTimeField(auto_now_add=True)
    # phone_number = models.CharField(max_length=20)
    # email = models.EmailField()

    # phoned = models.BooleanField(default=False)
    # source = models.CharField(choices=SOURCES_CHOICE, max_length=100)

    # profile_picture = models.ImageField(blank=True, null=True) # blank=True means that we are submitting an empty string | null=True means that there is no value in the database | these makes profiel picture field optional
    # special_files = models.FileField(blank=True, null=True)

    agent = models.ForeignKey(Agent, null=True, blank=True, on_delete=models.SET_NULL) # or agent = models.ForeignKey("Agent") 
    '''
    foreign key: every lead has an agent
    note that foreign keys always need to have the on_delete positional argument
    cascade: if the agent is deleted, all of his leads are deleted
    set_null: if the agent is deleted, the value agent in the lead model is set to null after deletion. This only works if we allow null to be true
    set_default: if the agent is deleted, the value agent in lead model is set to default after deletion. This only works if we set a default value
    '''
    organization = models.ForeignKey(UserProfile, on_delete=models.CASCADE) # or user_profile
    category = models.ForeignKey("Category", related_name="leads", null=True, blank=True, on_delete=models.SET_NULL)
    '''
    when you add a related_name, you give category access to all the leads holding that category through the related name through self.get_object().leads
    '''
    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Category(models.Model):
    name = models.CharField(max_length=30) # new, contacted, converted, unconverted
    organization = models.ForeignKey(UserProfile, on_delete=models.CASCADE) # or user_profile

    def __str__(self):
        return self.name


def post_user_created_signal(sender, instance, created, **kwargs):
    if created:
        user_profile = UserProfile.objects.create(user=instance)

post_save.connect(post_user_created_signal, sender=User)
