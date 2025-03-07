from django.db import models
from django.db.models.base import Model
from django.db.models import Q
from django.contrib.auth.backends import ModelBackend, UserModel

class Owner(models.Model):
    name = models.CharField(blank = False, max_length=120,null=False)
    email = models.EmailField(blank = False, null=False)
    rollNo = models.CharField(max_length=9, blank = False, null=False)
    phoneNo = models.CharField(max_length=13)
    rating = models.FloatField(blank = True, default=0.0)
    profilePicture = models.ImageField(blank = True, null = True)
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=120, blank = False, null=False)
    company = models.CharField(max_length=120, blank = True)
    price = models.IntegerField(blank = False, null=False)
    description = models.TextField(blank=True, null=True)
    quantity = models.IntegerField(blank = False, null=False)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, related_name="products")
    dateCreated = models.DateTimeField(auto_now_add=True)
    lastModified = models.DateTimeField(auto_now=True)
    sold = models.BooleanField(default = False)
    def __str__(self):
        return self.name

    @property
    def get_images(self):
        images = self.image_set.all()
        return images


class Image(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name="Images")
    images = models.ImageField(blank=True, null=True, upload_to=f'images')
    def __str__(self):
        return self.images.name

    @property
    def ImageURL(self):
        try:
            url = self.image.url
            if url=='':
                url='images/default.jpeg'
        except:
            url = ''
        return url


class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try: #to allow authentication through phone number or any other field, modify the below statement
            user = UserModel.objects.get(Q(username__iexact=username) | Q(email__iexact=username))
        except UserModel.DoesNotExist:
            UserModel().set_password(password)
        except UserModel.MultipleObjectsReturned:
            return UserModel.objects.filter(email=username).order_by('id').first()
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user

    def get_user(self, user_id):
        try:
            user = UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None

        return user if self.user_can_authenticate(user) else None


