from django.db import models
from django.contrib.auth.models import User

class ObjectPermissions(models.Model):
    object_type = models.CharField(max_length=100)
    permission_name = models.CharField(max_length=100)
    permission_order = models.IntegerField()

    def __unicode__(self):
        return self.object_type + self.permision_name


class GrantedPermissions(models.Model):
    object_owner = models.ForeignKey(User, related_name='owner')
    object_id    = models.CharField(max_length=50)
    object_permission = models.OneToOneField(ObjectPermissions)
    grantee = models.ForeignKey(User, blank=True, null=True)

    def __unicode__(self):
        return self.object_permission

    @staticmethod
    def get_permissions(owner, grantee, object_type, object_id):
        
        objects_info = ObjectPermissions.objects.filter(
                           object_type = object_type
                           ).order_by(
                           'permission_order'
                           )

        for object_info in objects_info:
            permissions = GrantedPermissions.objects.filter(
                            object_owner = owner
                          ).filter(
                            grantee = grantee
                          ).filter(
                            object_permission = object_info.id
                          ).filter(
                            object_id = object_id
                          )

            if (permissions.count() == 1):
                return object_info.permission_name
            else:
                return ValueError
            
