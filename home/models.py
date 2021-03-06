from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm, TextInput, Textarea

# Create your models here.
from django.utils.safestring import mark_safe


class Setting(models.Model):
    STATUS = (
        ('True', 'Evet'),
        ('False', 'Hayır'),

    )
    title = models.CharField(max_length=150)
    keywords = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    company = models.CharField(max_length=50)
    adress = models.CharField(blank=True,max_length=100)
    phone = models.CharField(blank=True,max_length=15)
    fax = models.CharField(blank=True,max_length=15)
    email = models.CharField(blank=True,max_length=50)
    smtpserver = models.CharField(blank=True, max_length=20)
    smtpemail = models.CharField(blank=True, max_length=20)
    smtppassword = models.CharField(blank=True, max_length=10)
    smtpport = models.CharField(blank=True,max_length=5)
    icon = models.ImageField(blank=True, upload_to='images/')
    facebook = models.CharField(blank=True, max_length=50)
    instagram = models.CharField(blank=True, max_length=50)
    twitter = models.CharField(blank=True, max_length=50)
    aboutus = RichTextUploadingField(blank=True)
    contact = RichTextUploadingField(blank=True)
    references = RichTextUploadingField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class ContactFormMessage(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Read', 'Read'),
        ('Closed', 'Closed'),
    )

    name = models.CharField(max_length=20, blank=True)
    email = models.CharField(max_length=50, blank=True)
    subject = models.CharField(max_length=50, blank=True)
    message = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=10, choices=STATUS, default='New')
    ip = models.CharField(max_length=20, blank=True)
    note = models.CharField(max_length=100,blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name

class ContactForm(ModelForm): #otomatik form oluşturma için
    class Meta:
        model = ContactFormMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control mb-30', 'placeholder': 'Name & Surname'}),
            'subject': TextInput(attrs={'class': 'form-control mb-30', 'placeholder': 'Subject'}),
            'email': TextInput(attrs={'class': 'form-control mb-30', 'placeholder': 'Email Address'}),
            'message': Textarea(attrs={'class': 'form-control mb-30', 'placeholder': 'Your Message', 'rows': '5'}),
        }

class UserProfile(models.Model): #userın ekstra bilgilere ihtiyacımız olabilir
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=150, blank=True)
    city = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=20, blank=True)
    image = models.ImageField(blank=True, upload_to='images/users/')

    def __str__(self):
        return self.user.username

    def user_name(self):
        return  self.user.first_name  + ' ' + self.user.last_name + '   [' +self.user.username + ']'


    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
    image_tag.short_description = 'Image'

class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone', 'address', 'city', 'country', 'image']



class FAQ(models.Model):
    STATUS = (
        ('True', 'Evet'),
        ('False', 'Hayır'),

    )
    ordernumber=models.IntegerField()
    question = models.CharField(max_length=150)
    answer = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question






















