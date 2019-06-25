from django.db import models
from datetime import datetime
import re
import bcrypt

current = str(datetime.now())

class TripsManager(models.Manager):
    def tripsValidator(self, form):
        destination = form['destination']
        start_date = form['start_date']
        end_date = form['end_date']
        plan = form['plan']

        errors = {}

        if not destination:
            errors['destination'] = "Please enter a destination"
        if not start_date:
            errors['start_date'] =  "Please enter a start date"
        elif start_date <= current:
            errors['start_date'] = "Please enter a date in the future"
        if not end_date:
            errors['end_date'] = "Please enter an end date"
        elif str(end_date) < str(start_date):
            errors['end_date'] = "Please enter a date after your start date"
        if not plan:
            errors['plan'] = "Please enter a description"

        return errors

class UserManager(models.Manager):
    def regValidator(self, form):
        myname = form['name']
        username = form['username']
        password = form['password']
        confirm_pw = form['confirm_pw']

        errors={}

        if not myname:
            errors['myname'] = "Name can not be blank"
        elif len(myname) < 3:
            errors['myname'] = "Name must be atleast 3 characters"

        if not username:
            errors['username'] = "Username can not be blank"
        elif len(username) < 3:
            errors['username'] = "Username must be atleast 3 characters"

        if not password:
            errors['reg_password'] = "Password can not be blank"
        elif len(password) < 8:
            errors['reg_password'] = "Password must be 8 characters"
        if not confirm_pw:
            errors['confirm_pw'] = "Please confirm password"
        elif password != confirm_pw:
            errors['confirm_pw'] = "Passwords do not match"

        return errors

    def loginValidator(self, form):
        username = form['login_username']
        password = form['login_password']

        errors ={}

        if not username:
            errors['login_username'] = "Please enter email to log in."
        elif not User.objects.filter(username=username):
            errors['login_username'] = "Username not found. Please register."
        else:
            if not password:
                errors['login_password'] = "Password required"
                return errors, False
            else:
                user = User.objects.get(username=username)
                if not bcrypt.checkpw(password.encode(), user.password.encode()):
                    errors['login_password'] = "Incorrect password. Please try again."

                return errors, user

        return errors, False




class User(models.Model):
    name = models.CharField(max_length=45)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Trips(models.Model):
    destination = models.CharField(max_length=255)
    start_date = models.CharField(max_length=255)
    end_date = models.CharField(max_length=255)
    plan = models.CharField(max_length=255)
    planned_by = models.ForeignKey(User, related_name = 'trips_planned', on_delete=models.CASCADE)
    joined_by = models.ManyToManyField(User, related_name = 'joined')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TripsManager()
