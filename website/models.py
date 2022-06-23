from django.db import models
from django.contrib.auth.models import User, auth
from django.forms import ModelForm, DateInput, TimeInput

# Create your models here.


class uprofile(models.Model):
    meta = models.ForeignKey(User, on_delete=models.CASCADE)
    profileimg = models.ImageField(
        upload_to='profileimgs/', default='profileimgs\defaultpimg.jpg')
    phone_no = models.BigIntegerField()
    address = models.TextField(max_length=300)


class uprofileform(ModelForm):
    class Meta:
        model = uprofile
        fields = ['profileimg', 'phone_no', 'address']


booktno = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


class tablebooking(models.Model):
    uname = models.ForeignKey(User, on_delete=models.CASCADE)
    rest_name = models.CharField(max_length=255, blank=True)
    name = models.CharField(max_length=100)
    tableno = models.IntegerField()
    date = models.DateField()
    time = models.TimeField()


class tablebookingform(ModelForm):
    class Meta:
        model = tablebooking
        fields = '__all__'
        exclude = ["uname", 'rest_name']
        widgets = {
            'date': DateInput(format=('%m/%d/%Y'), attrs={'type': 'date'}),
            'time': TimeInput(format='%H:%M', attrs={'type': 'time'})
        }


# class orderfood(models.Model):


# class Reviews(models.Model):
#     username = models.CharField(max_length=255)
#     comment = models.TextField()


# preferrdfood = []


class Orderfood(models.Model):
    uname = models.ForeignKey(User, on_delete=models.CASCADE)
    rest_name = models.CharField(max_length=255, blank=True)
    preffood = models.CharField(max_length=255)
    quantity = models.IntegerField()
    pincode = models.IntegerField()
    city = models.CharField(max_length=255)
    address = models.TextField()


class Orderfoodform(ModelForm):
    class Meta:
        model = Orderfood
        fields = '__all__'
        exclude = ['uname', 'rest_name']


class roombooking(models.Model):
    uname = models.ForeignKey(User, on_delete=models.CASCADE)
    hotel_name = models.CharField(max_length=255, blank=True)
    roomno = models.IntegerField()
    date_in = models.DateField()
    date_out = models.DateField()


class hotelbookingform(ModelForm):
    class Meta:
        model = roombooking
        fields = '__all__'
        exclude = ["uname", 'hotel_name']
        widgets = {
            'date_in': DateInput(format=('%m/%d/%Y'), attrs={'type': 'date'}),
            'date_out': DateInput(format=('%m/%d/%Y'), attrs={'type': 'date'}),

        }
