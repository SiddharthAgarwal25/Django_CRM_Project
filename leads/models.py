from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
# Create your models here.


class User(AbstractUser):
    is_organiser = models.BooleanField(default=True)
    is_agent = models.BooleanField(default=False)



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
    

class Lead(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    age = models.IntegerField(default=0)
    # This means if an agents get deleted the lead assigned to them will not get deleted.
    agent = models.ForeignKey("Agent",null=True, blank=True ,on_delete=models.SET_NULL)
    organisation = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    category = models.ForeignKey("Category",null=True,related_name="leads" , blank=True, on_delete=models.SET_NULL)
    description = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    phone_number = models.CharField(max_length=10)
    email = models.EmailField()



    def __str__(self):
        return f"First name :  {self.first_name},  last_name: {self.last_name}, age: {self.age} , agent_assigned : {self.agent}."

class Agent(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    organisation = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.email 
        
class Category(models.Model):
    name =  models.CharField(max_length=30) # New, Contacted, Converted, Unconverted
    organisation = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    def __str__(self):
        return self.name

def post_user_created_signal(sender, instance, created, **kwargs):
    print(instance)
    if created:
        UserProfile.objects.create(user=instance)




post_save.connect(post_user_created_signal, sender=User)