from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils import timezone

password_regex = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d).{8,}$'
password_validator = RegexValidator(
    regex=password_regex,
    message = 'Password must contain at least 8 characters, one uppercase letter, one lowercase letter, and one number',
)

# Create your models here.

class CustomUser(AbstractUser):
    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    mobile = models.CharField(max_length=15, null=True, blank=True)
    password = models.CharField(max_length=100, null=True, blank=True, validators=[password_validator])
    address = models.TextField(null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    cart = models.ManyToManyField('Product', related_name='cart', blank=True)

    def __str__(self):
        return self.name or self.username
    
class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.ImageField(upload_to='products/')
    description = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    
    