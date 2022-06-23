from django.shortcuts import render
from .forms import bookingtableform
# Create your views here.


def booktable(request):

    form = bookingtableform()
    return render(request, 'bookingform.html', {'form': form})
