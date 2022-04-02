# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Alumni(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    collegeid = models.ForeignKey('College', models.DO_NOTHING, db_column='CollegeID')  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=100)  # Field name made lowercase.
    email = models.CharField(db_column='Email', unique=True, max_length=100)  # Field name made lowercase.
    phone = models.CharField(db_column='Phone', max_length=10)  # Field name made lowercase.
    passout_year = models.IntegerField(db_column='Passout_year')  # Field name made lowercase.
    experience = models.CharField(db_column='Experience', max_length=200)  # Field name made lowercase.
    current_job = models.CharField(db_column='Current_job', max_length=200)  # Field name made lowercase.
    verification_status = models.IntegerField(db_column='Verification_status')  # Field name made lowercase.
    registration_status = models.IntegerField(db_column='Registration_status')  # Field name made lowercase.
    password = models.CharField(db_column='Password', max_length=100)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'alumni'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class College(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=100)  # Field name made lowercase.
    type = models.CharField(db_column='Type', max_length=100)  # Field name made lowercase.
    city = models.CharField(db_column='City', max_length=50)  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=100)  # Field name made lowercase.
    password = models.CharField(db_column='Password', max_length=100)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'college'


class Directorate(models.Model):
    id = models.CharField(db_column='ID', primary_key=True, max_length=225)  # Field name made lowercase.
    password = models.CharField(db_column='Password', max_length=225)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'directorate'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Email(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=50)  # Field name made lowercase.
    date = models.DateField(db_column='Date')  # Field name made lowercase.
    subject = models.CharField(db_column='Subject', max_length=150)  # Field name made lowercase.
    content = models.TextField(db_column='Content')  # Field name made lowercase.
    cdid = models.IntegerField(db_column='cdID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'email'


class Events(models.Model):
    eventfile = models.TextField(blank=True, null=True)
    cdid = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'events'


class Passingyear(models.Model):
    year = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'passingyear'
