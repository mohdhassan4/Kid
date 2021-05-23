from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone


class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, phonenumber, password, whatsappnumber, parentname, classname):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            phonenumber=phonenumber,
            whatsappnumber=whatsappnumber,
            parentname=parentname,
            classname=classname
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, phonenumber, password, whatsappnumber, parentname, classname):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            phonenumber=phonenumber,
            username=username,
            whatsappnumber=whatsappnumber,
            parentname=parentname,
            classname=classname
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    email = models.EmailField(verbose_name="email", max_length=55)
    password = models.CharField(max_length=256)
    username = models.CharField(max_length=50)
    phonenumber = models.CharField(max_length=55, unique=True)
    whatsappnumber = models.CharField(max_length=55, default='')
    parentname = models.CharField(max_length=50, default='')
    classname = models.CharField(max_length=50, default='')
    date_joined = models.DateTimeField(
        verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    USERNAME_FIELD = 'phonenumber'
    REQUIRED_FIELDS = ['username', 'email',
                       'whatsappnumber', 'parentname', 'classname']

    objects = MyAccountManager()

    def __str__(self):
        return self.email

        # For checking permissions. to keep it simple all admin have ALL permissons
    def has_perm(self, perm, obj=None):
        return self.is_admin

        # Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label):
        return True


class Course(models.Model):
    courseName = models.CharField(max_length=100)
    price = models.IntegerField()
    tag = models.CharField(max_length=120)
    date_enrolled = models.DateField(default = timezone.now)
    zoom_link = models.TextField()


class Purchase(models.Model):
    userid = models.ForeignKey(Account, on_delete=models.CASCADE)
    coursesId = models.ForeignKey(Course, on_delete=models.CASCADE)
    paymentDate = models.DateField()
    ammount = models.IntegerField()
    transactionid = models.CharField(max_length=50)
    status = models.BooleanField(default=False)
