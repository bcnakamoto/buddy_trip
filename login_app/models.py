from django.db import models
import re
import bcrypt

email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User_Manager(models.Manager):
    def validate(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors['first_name'] = 'First Name must be at least 2 characters'

        if len(postData['last_name']) < 2:
            errors['last_name'] = 'Last Name must be at least 2 characters'

        if not email_regex.match(postData['email']):
            errors['email'] = 'Invalid Email Address'
        
        check_email = self.filter(email=postData['email'])
        if check_email:
            errors['email'] = "Email already in use"

        if len(postData['password']) < 8:
            errors['password'] = 'Password must be at least 8 characters'
        
        if postData['password'] != postData['pw_confirmation']:
            errors['password'] = 'Passwords do not match'
        return errors

    def authenticate(self, email, password):
        users = self.filter(email=email)
        if not users:
            return False

        user = users[0]
        return bcrypt.checkpw(password.encode(), user.password.encode())

    def register(self, postData):
        pw = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt()).decode()
        return self.create(
            first_name = postData['first_name'],
            last_name = postData['last_name'],
            email = postData['email'],
            password = pw
        )

class User(models.Model):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = User_Manager()

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)

class Trip_Manager(models.Manager):
    def validate(self, postData):
        errors = {}
        if len(postData['dest']) < 1:
            errors['dest'] = 'Destination must be at least 2 characters'

        if len(postData['plan']) < 1:
            errors['plan'] = 'Please describe your trip plans'

        if postData['end_date'] <= postData['start_date']:
            errors['end_date'] = 'Return date must be later than departure date'
        return errors

class Trip(models.Model):
    dest = models.CharField(max_length=255)
    start_date = models.DateField(auto_now=False)
    end_date = models.DateField(auto_now=False)
    plan = models.CharField(max_length=255)
    owner = models.ForeignKey('User', on_delete=models.CASCADE, related_name='trips')
    joiner = models.ManyToManyField('User', default=None, related_name='joiner')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = Trip_Manager()
