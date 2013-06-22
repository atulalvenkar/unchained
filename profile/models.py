from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
import time
import md5

class UserProfile(models.Model):
    owner             = models.OneToOneField(User)
    owner_hash        = models.CharField(max_length=32)
    first_name        = models.CharField(max_length=100)
    middle_name       = models.CharField(max_length=50, null=True)
    last_name         = models.CharField(max_length=100)
    name_prefix       = models.CharField(max_length=30, null=True)
    date_of_birth     = models.DateField()
    sex               = models.CharField(max_length=1)
    primary_phone     = models.CharField(max_length=20, null=True)
    secondary_phone   = models.CharField(max_length=20, null=True)
    personal_website  = models.CharField(max_length=50, null=True)
    home_address      = models.CharField(max_length=200, null=True)
    last_updated      = models.DateTimeField(default=datetime.now)

    def __unicode__(self):
        return self.first_name + ' ' + self.last_name

    def save(self, **kwargs):
        hash_string = str(int(time.time())) + self.first_name
        self.owner_hash = md5.new(hash_string).hexdigest()
        super(UserProfile, self).save(**kwargs)

class EducationProfile(models.Model):
    owner = models.ForeignKey(User)
    school_name = models.CharField(max_length=100)
    college_name = models.CharField(max_length=100)
    # To be enabled when education model is created
    #EducationLevel = model.ForeignKey(Education)

    def __unicode__(self):
        return self.school_name + ' ' + self.college_name
