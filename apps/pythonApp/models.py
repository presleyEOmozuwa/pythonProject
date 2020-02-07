
from django.db import models
import re



class UserManager(models.Manager):
    def basic_validator(self, postdata):
        errors = {}
        if len(postdata['first_name']) < 2:
            errors['first_name'] = "First Name must be at least 2 characters"

        if len(postdata['last_name']) < 2:
            errors['last_name'] = "Last Name must be at least 2 characters"

        if len(postdata['password']) < 8:
            errors['password'] = "Password must be at least 8 characters"

        if len(postdata['confirm_password']) < 8:
            errors['password'] = "Password must be at least 8 characters"

        if not re.match(r"[^@]+@[^@]+\.[^@]+", postdata['email']):
            errors['email'] = 'E-mail address is not in a valid format.'

        try:
            User.objects.get(email=postdata['Email'])
            errors['email'] = 'E-mail address already in use.'
        except:
            pass

        if not postdata['password'] == postdata['confirm_password']:
            errors['password_match'] = 'Submitted passwords do not match.'
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = UserManager()


class WishManager(models.Manager):
    def self_validator(self, postdata):
        errors = {}
        if len(postdata['title']) < 3:
            errors['title'] = "Title field must be at least 3 characters"

        if len(postdata['description']) < 3:
            errors['description'] = "Description must be at least 3 characters" 
        return errors      


class Wish(models.Model):
    title = models.CharField(max_length=45)
    description = models.CharField(max_length=45)
    granted = models.BooleanField(default=False)
    granted_at = models.DateTimeField(blank=True, null=True)
    creator = models.ForeignKey(User, related_name="user_wishes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    like = models.ManyToManyField(User, related_name ="liked_wish")
    objects = WishManager() 
