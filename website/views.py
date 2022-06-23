from website.models import hotelbookingform
from . import sampleds as ds
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate
from django.core.mail import EmailMessage, send_mail, EmailMultiAlternatives
from website.models import uprofileform, uprofile, tablebookingform, Orderfoodform, tablebooking, Orderfood
from django.contrib.auth.decorators import login_required
from . import scrapper as s

# import requests

# Create your views here.


def em():
    send_mail('form django after fixing issue', 'mana isp issue ', 'maremandasreekrishna@gmail.com',
              ['maremandasreekrishna@gmail.com', 'jurendrav@gmail.com'])


def home(request):
    return render(request, 'home.html')


def loginuser(request):
    if request.method == 'POST':
        uname = request.POST['uname']
        passw = request.POST['pass']
        msg = "invalid credentials"
        try:

            user = auth.authenticate(request, username=uname, password=passw)
        except:
            return render(request, 'login.html', {'msg': msg})
        # print(user)

        if user is not None:
            print('authenticated')
            auth.login(request, user)
            return render(request, 'home.html')
    return render(request, 'login.html')


def logoutuser(request):
    auth.logout(request)
    return redirect('/')


def Register(request):
    if request.method == 'POST':
        uname = request.POST['uname']
        password = request.POST['pass']
        conpass = request.POST['conpass']
        email = request.POST['email']
        if password == conpass:
            user = User.objects.create_user(
                username=uname, password=password, email=email)
            user.save()
            # email = EmailMessage('confirmation mail', 'You have successfully registered in zwiggy we look farward to serve you',
            #                      to=[email])
            # email.send()
            send_mail("Confirm Registration in Zwiggy",
                      f'Dear {uname} you are successfully registerd in Zwiggy', 'maremandasreekrishna@gmail.com', [email])
            return HttpResponseRedirect('/')
        else:
            return render(request, 'Registration.html', {'errormsg': 'please fill the fields correctly'})

    else:
        return render(request, 'Registration.html')


@login_required(login_url='/login')
def upload(request):
    if request.method == 'POST':
        form = uprofileform(request.POST, request.FILES,
                            )
        if form.is_valid():
            profile = form.save(commit=False)
            profile.meta = request.user
            profile.save()
            return HttpResponse('success')
    else:
        form = uprofileform()
    return render(request, 'upload.html', {'form': form})


def profile(request):
    # print(request.method, "    ", user.is_authenticated)
    if request.method == 'GET':
        if request.user.is_authenticated:
            form = uprofileform()
            tbookdetails = tablebooking.objects.filter(
                uname=request.user)
            ordfobject = Orderfood.objects.filter(uname=request.user)
            # request.session['tblname'] = tbookdetails.rest_name
            print(ordfobject)
            # print(request.user.u)
            try:
                p = uprofile.objects.get(meta=request.user)
                form = uprofileform(instance=p)

                # print(request.user)
                # print(tbookdetails)
            except:
                return render(request, "user_profile.html", {'form': form, 'tablebookhistory': tbookdetails, 'orderfoodhistory': ordfobject})
            return render(request, "user_profile.html", {'form': form, 'url': p.profileimg.url, 'phone': p.phone_no, 'address': p.address, 'tablebookhistory': tbookdetails, 'orderfoodhistory': ordfobject})
        return HttpResponseRedirect('login')
    else:
        rname = request.POST['rname']
        rtable = request.POST['rtable']
        rtime = request.POST['rtime']
        rdate = request.POST['rdate']
        upbook = tablebooking.objects.get(
            uname=request.user, rest_name=rname, tableno=rtable)
        upbookform = tablebookingform(instance=upbook)
        # a = request.user
        # if a is not None:
        #     form = uprofileform(request.POST, request.FILES)
        #     if form.is_valid():
        #         p = form.save(commit=False)
        #         p.meta = request.user
        #         p.save()
        #         return HttpResponse('successfully updated profile')

        # return render(request, 'restdetails.html', {'updatetableob': upbookform})
        redirect(f'restdetails/<{rname}>')


@ login_required(login_url='/login')
def updateprofiledetails(request):
    p = uprofile.objects.get(meta=request.user.id)
    form = uprofileform(instance=p)
    form.save()
    return render(request, 'user_profile.html', {'form': form})


# def restsview(request):
#     return render(request, 'displayrest.html')


def contactus(request):
    return render(request, 'contactus.html')


def aboutus(request):
    return render(request, 'aboutus.html')


def foodcard(request):
    return render(request, 'foodindex.html', {'d': [1, 2, 3, 4, 5, 6]})


@ login_required(login_url='/login')
def updatebooktable(request):

    uptbl = tablebooking.objects.get(uname=request.user, rest_name=request.session['tbldata'].rest_name,
                                     name=request.session['tbldata'].name, tableno=request.session['tbldata'].tableno)
    tbform = tablebookingform(instance=uptbl)
    print(uptbl)
    return render(request, 'restdetails.html', {'tbform': tbform})


def updatefoodorder(request):
    # uorders = orderfood.objects.all()

    return HttpResponse('order history for food')


def orderfood(request):
    res_name = request.session['rest_name']
    forderf = Orderfoodform(request.POST)
    forder = Orderfood(uname=request.user.id, rest_name=res_name, preffood=forderf.data['preffood'], quantity=forderf.data[
        'quantity'], pincode=forderf.data['pincode'], city=forderf.data['city'], address=forderf.data['address'])
    forder.save()
    return HttpResponse("oreder food success")


def sample_charts(request):
    recommendeddata = ds.recommended()
    return render(request, 'chart.html', {'data': recommendeddata})


def foodrecommendations(request):
    imgs = [
        'https://res.cloudinary.com/swiggy/image/upload/fl_lossy,f_auto,q_auto,w_508,h_320,c_fill/nlqtdgbpqmgy16ygbs40',
        'https://images2.minutemediacdn.com/image/upload/c_crop,h_2172,w_3864,x_0,y_202/f_auto,q_auto,w_1100/v1558021472/shape/mentalfloss/80312-istock-957009874.jpg',
        'https://res.cloudinary.com/swiggy/image/upload/fl_lossy,f_auto,q_auto,w_508,h_320,c_fill/jugcspco53mumqfzrdmm',
        'https://www.qsrmagazine.com/sites/default/files/styles/story_page/public/2020-09/KFC%20X%20DoorDash%20PR%20Image%202.png?itok=lYdjw8El',
        'https://res.cloudinary.com/swiggy/image/upload/fl_lossy,f_auto,q_auto,w_508,h_320,c_fill/ipcgcltnatzrvle5ro7f',
        'https://res.cloudinary.com/swiggy/image/upload/fl_lossy,f_auto,q_auto,w_508,h_320,c_fill/pecmimj4eppsh5elkg8z',
        'https://res.cloudinary.com/swiggy/image/upload/fl_lossy,f_auto,q_auto,w_508,h_320,c_fill/qk9r0zabernzrlctvhdw',
        'https://i.insider.com/5ba544539c888d54308b4567?width=1136&format=jpeg',
        'https://res.cloudinary.com/swiggy/image/upload/fl_lossy,f_auto,q_auto,w_508,h_320,c_fill/yoomlurvz3ivvmsvjhqp',
        'https://res.cloudinary.com/swiggy/image/upload/fl_lossy,f_auto,q_auto,w_508,h_320,c_fill/kkxgxdkgplmnts8me0ne'
    ]
    da = ds.recommended()
    d = ds.get_restaurant_names(da)
    zipv = zip(d['names'], d['ratings'], imgs)
    return render(request, 'displayrest.html', {'d': zipv})


def restaurant_details(request, restid):
    if request.method == 'GET':
        details = ds.get_restaurant_details(restid)
        tbook = tablebookingform()
        foorder = Orderfoodform()
        request.session['rest_name'] = details[3]

        return render(request, 'restdetails.html', {'data': details, 'tbook': tbook, 'foorder': foorder})
    else:
        print("Book" in request.POST)
        try:
            if request.method == 'POST' and 'Book' == request.POST['booktable']:
                res_name = request.session['rest_name']
                tdook = tablebookingform(request.POST)
                tbform = tablebooking(uname=request.user, rest_name=res_name,
                                      name=tdook.data['name'], tableno=tdook.data['tableno'], date=tdook.data['date'], time=tdook.data['time'])
                tbform.save()
                send_mail('Table booking confirmation from zwiggt',
                          f' \nDear {request.user.username} you table booking in {res_name} with table no:{request.POST["tableno"]} on {request.POST["date"]} at {request.POST["time"] } has been confirmed', 'maremandasreekrishna@gmail.com', [request.user.email, ])
                return render(request, 'messpage.html', {'msgdata': "your table is successfully booked"})
            else:
                res_name = request.session['rest_name']
                forderf = Orderfoodform(request.POST)
                forder = Orderfood(uname=request.user.id, rest_name=res_name, preffood=forderf.data['preffood'], quantity=forderf.data[
                    'quantity'], pincode=forderf.data['pincode'], city=forderf.data['city'], address=forderf.data['address'])
                forder.save()
                return HttpResponse('success ordering food')
        except:
            pass
        try:
            print("orderfood" in request.POST)
            res_name = request.session['rest_name']
            # forderf = Orderfoodform(request.POST)

            forder = Orderfood(uname=request.user, rest_name=res_name, preffood=request.POST['preffood'], quantity=request.POST[
                               'quantity'], pincode=request.POST['pincode'], city=request.POST['city'], address=request.POST['address'])
            print(res_name)
            forder.save()
            send_mail('Order Description in Zwiggy',
                      f'Dear {request.user.username} your order has been confirmed\n Here are details from {res_name} restaurant {request.POST["preffood"]},{request.POST["address"]}', 'maremandasreekrishna@gmail.com', [request.user.email])
            return HttpResponse('success ordering food')
        except:
            return HttpResponseRedirect('/login')


def findrestaurant(request):
    simg = [
        'https://res.cloudinary.com/swiggy/image/upload/fl_lossy,f_auto,q_auto,w_508,h_320,c_fill/nlqtdgbpqmgy16ygbs40',
        'https://images2.minutemediacdn.com/image/upload/c_crop,h_2172,w_3864,x_0,y_202/f_auto,q_auto,w_1100/v1558021472/shape/mentalfloss/80312-istock-957009874.jpg',
        'https://res.cloudinary.com/swiggy/image/upload/fl_lossy,f_auto,q_auto,w_508,h_320,c_fill/jugcspco53mumqfzrdmm',
        'https://www.qsrmagazine.com/sites/default/files/styles/story_page/public/2020-09/KFC%20X%20DoorDash%20PR%20Image%202.png?itok=lYdjw8El',

    ]
    rest_name = request.POST['restname']
    results = ds.searchrestaurant(rest_name)
    zipres = zip(results, simg)
    return render(request, 'displayrest.html', {'results': zipres})


# def decidebookororder(request):
#     print(request)


def tableupdatehandler(request, restid):
    if request.method == 'GET':
        details = ds.get_restaurant_details(restid)
        uptbl = tablebooking.objects.get(uname=request.user, rest_name=request.GET['rname'],
                                         name=request.GET['rbname'], tableno=request.GET['rtable'])
        request.session['rname'] = request.GET['rname']
        request.session['name'] = request.GET['rbname']
        request.session['tableno'] = request.GET['rtable']
        tbook = tablebookingform(instance=uptbl)

        # print(tbook.rest_name)
        foorder = Orderfoodform()
        request.session['rest_name'] = details[3]
        return render(request, 'restdetails.html', {'data': details, 'tbook': tbook, 'foorder': foorder, 'rest_name': restid})
    else:
        uptb = tablebookingform(request.POST)
        uptbob = tablebooking.objects.get(uname=request.user, rest_name=request.session['rname'],
                                          name=request.session['name'], tableno=request.session['tableno'])
        # uptbob.update(name=uptb.data['name'], tableno=uptb.data['tableno'],
        #               date=uptb.data['date'], time=uptb.data['time'])
        uptbob.name = request.POST['name']
        uptbob.tableno = request.POST['tableno']
        uptbob.date = request.POST['date']
        uptbob.time = request.POST['time']
        uptbob.save()
        send_mail('table booking updation confirmation',
                  f'updated details are : \n{request.POST["name"]} {request.POST["date"]} {request.POST["time"]}', 'maremandasreekrishna@gmail.com', [request.user.email])
        return render(request, 'messpage.html', {'msgdata': "Your table booking updated successfully "})


# def savetableupdatehandle(request):
#     uptb = tablebookingform(request.POST)
#     uptbob = tablebooking.objects.get(uname=request.user, rest_name=request.session['rname'],
#                                       name=request.session['name'], tableno=request.session['tableno'])
#     uptbob.update(name=uptb.data['name'], tableno=uptb.data['tableno'],
#                   date=uptb.data['date'], time=uptb.data['time'])
#     return HttpResponse("successfully updated")


def canceltablebooking(request):
    tablebooking.objects.filter(name=request.POST['rbname'],

                                uname=request.user,

                                ).delete()
    send_mail('Regarding table booking cancellation',
              f'your  booking with details : {request.POST["rdate"]}\n{request.POST["rtime"]}\n{request.POST["rname"]} is cacelled', 'maremandasreekrishna@gmail.com', [request.user.email])
    return render(request, 'messpage.html', {'msgdata': "your table booking cancelled successfully"})


def cancelorderfood(request):
    Orderfood.objects.filter(
        uname=request.user,

        preffood=request.POST['preffood']
    ).delete()
    return render(request, 'messpage.html', {'msgdata': "you food order cancelled"})


def gethotels(request):
    nameofhotel = [
        'TAJ LAKE PALACE',
        'THE OBEROI UDAIVILAS',
        'THE LEELA PALACE UDAIPUR',
        'TAJ ARAVALI RESORT & SPA',
        'RAMBAGH PALACE',
        'OBEROI RAJVILAS',
        'JW MARRIOTT JAIPUR RESORT & SPA',
        'THE ST. REGIS MUMBAI'
    ]

    ratingofhotel = [
        '4.9',
        '4.6',
        '4.7',
        '4.5',
        '4.6',
        '4.2',
        '4.8',
        '4.6'
    ]
    imgs = [
        'https://www.theasiacollective.com/wp-content/uploads/2020/03/Best-Hotels-India.jpg',
        'https://www.theasiacollective.com/wp-content/uploads/2020/03/Taj-Lake-Palace-1.jpg',
        'https://www.theasiacollective.com/wp-content/uploads/2020/03/The-Oberoi-Udaivilas-1.jpg',
        'https://www.theasiacollective.com/wp-content/uploads/2020/03/The-Leela-Palace-1.jpg',
        'https://www.theasiacollective.com/wp-content/uploads/2020/03/Taj-Aravali-Resort-Spa.jpg',
        'https://www.theasiacollective.com/wp-content/uploads/2020/03/Rambagh-Palace-1.jpg',
        'https://www.theasiacollective.com/wp-content/uploads/2020/03/The-Oberoi-Rajvilas-Jaipur-1.jpg',
        'https://www.theasiacollective.com/wp-content/uploads/2020/03/The-Taj-Mahal-Palace-1.jpg'

    ]
    if request.method == 'GET':
        content = zip(nameofhotel, ratingofhotel, imgs)

        return render(request, 'displayhotel.html', {'d': content})
    else:
        if request.POST['search'] in nameofhotel:
            ind = nameofhotel.index(request.POST['search'])
            print(ind)
            content = zip(nameofhotel[1], ratingofhotel[1], imgs[1])
            return render(request, 'displayhotel.html', {'d': content})
        pass


def roombook(request):
    rform = hotelbookingform()
    return render(request, 'roombook.html', {'rform': rform})
