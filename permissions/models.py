from django.db import models
from django.contrib.auth.models import User

class ProfileObjects(models.Model):
    profile_object_name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.profile_object_name


class ProfileObjectPermissions(models.Model):
    profile_object = models.ForeignKey(ProfileObjects)
    object_permission = models.CharField(max_length=100)
    permission_order = models.IntegerField()

    def __unicode__(self):
        return self.object_permission


class GrantedPermissions(models.Model):
    object_owner = models.ForeignKey(User, related_name='owner')
    object_permission = models.OneToOneField(ProfileObjectPermissions)
    grantee = models.ForeignKey(User, blank=True, null=True)

    def __unicode__(self):
        return self.object_permission

    @staticmethod
    def get_permissions(owner, grantee, profile_object_name):
        
        profile_objects = ProfileObjects.objects.filter(profile_object_name = profile_object_name)[0]
        profile_object_permissions = ProfileObjectPermissions.objects.filter(
                                       profile_object = profile_objects.id).order_by('permission_order')

        for profile_object_permission in profile_object_permissions:
            permissions = GrantedPermissions.objects.filter(
                            object_owner = owner
                          ).filter(
                            grantee = grantee
                          ).filter(
                            object_permission = profile_object_permission.id
                          )
            if (permissions.count != 0):
                return profile_object_permission.object_permission

        return ValueError
            
