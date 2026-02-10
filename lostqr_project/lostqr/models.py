from django.db import models
import uuid
from django.core.validators import RegexValidator
from django.contrib.auth.models import User



class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=100,)
    mail = models.EmailField(max_length=254, blank=True, null=True)
    phone_regex = RegexValidator(
    regex=r'^(\+90|0)?(5\d{9})$', 
    message="Phone number should be in '+905551234567' format. 9-15 digits are allowed."
    )
    phone = models.CharField(
        validators=[phone_regex],
        max_length=20, 
        blank=True)
    social_media = models.CharField(max_length=50, blank=True)
    message = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User ,on_delete=models.CASCADE)
    qr_label = models.CharField(max_length=12, blank=True, null=True)

    def __str__(self):
        return f"Losts Label - {self.username or str(self.id)}"