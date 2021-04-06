from django.shortcuts import render, redirect
from home.models import *
from django.contrib.auth.models import auth
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate, logout
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import datetime
import razorpay
from django.core.mail import EmailMessage


def index(request):
    items = Course.objects.all()
    return render(request, 'index.html', {'items': items})


def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        parentname = request.POST['parentname']
        email = request.POST['email']
        mobile = request.POST['mobile']
        watsappmobile = request.POST['watsapp_mobile']
        password = request.POST['password']
        confirmpassword = request.POST['confirmpassword']
        childclass = request.POST['childclass']
        if password != confirmpassword:
            messages.info(request, 'must have Passwords same')
            return redirect('/register')
        elif Account.objects.filter(phonenumber=mobile).exists():
            messages.info(request, 'Phone number is already taken')
            return redirect('/register')
        else:
            user = Account.objects.create_user(
                username=username, password=password, phonenumber=mobile,
                email=email, classname=childclass, parentname=parentname, whatsappnumber=watsappmobile)
            if user:
                email = EmailMessage(
                    'New User', 'ynew user is register name '+user.username+' mobilenumber is '+user.phonenumber, to=['smhassain02@gmail.com'])
                email.send()
            auth.login(request, user)
            return redirect('/')
    else:
        return render(request, 'register.html')


def Login(request):
    if request.method == 'POST':
        Phone = request.POST['Phone']
        password = request.POST['password']
        print("mahi", Phone, password)
        user = authenticate(phonenumber=Phone, password=password)
        if user:
            auth_login(request, user)
            return redirect("/")
        else:
            messages.info(request, 'Email or Password Is Incorrect')
            return redirect('/login')
    else:
        return render(request, 'login.html')


def Logout_view(request):
    logout(request)
    return redirect('/')


def Purchase_course(request):
    if request.method == "POST":
        courseid = request.POST['courseid']
        R = Course.objects.filter(id=courseid)
        userid = request.user.id
        if Purchase.objects.filter(coursesId=courseid, userid=userid, status=True).exists():
            return redirect('/')
        else:
            Purchase.objects.filter(
                coursesId=courseid, userid=userid, status=False).delete()
            date = datetime.today()
            amount = (R[0].price)*100
            amount = (amount*.18)+amount
            client = razorpay.Client(
                auth=("rzp_test_EL0CgmCc3DbVfk", "Zdvcs8kQHHGWucUbrJ6n7EM1"))
            payment = client.order.create(
                {'amount': amount, 'currency': 'INR', 'payment_capture': '1'})
            order_status = payment['status']
            if order_status == 'created':
                amount = amount//100
                order = Purchase(paymentDate=date, ammount=amount,
                                 transactionid=payment['id'])
                instance = order
                instance.userid_id = userid
                instance.coursesId_id = courseid
                instance.save()
                customer = Account.objects.filter(id=userid)
                amo = {
                    'payment': payment,
                    'course': R[0],
                    'course1': R[0].price,
                    'customer': customer[0]
                }
                return render(request, "checkout.html", amo)
            else:
                return render(request, "faild.html")


@csrf_exempt
def Success(request):
    if request.method == "POST":
        client = razorpay.Client(
            auth=("rzp_test_EL0CgmCc3DbVfk", "Zdvcs8kQHHGWucUbrJ6n7EM1"))
        response = request.POST
        params_dict = {
            'razorpay_payment_id': response['razorpay_payment_id'],
            'razorpay_order_id': response['razorpay_order_id'],
            'razorpay_signature': response['razorpay_signature']
        }
        status = client.utility.verify_payment_signature(params_dict)
        if status == None:
            item = Purchase.objects.filter(
                transactionid=params_dict['razorpay_order_id'])
            Purchase.objects.filter(
                transactionid=params_dict['razorpay_order_id']).update(status=True)
            messages.info(request, 'successfully bought this course')
            return redirect('/')
        else:
            messages.info(request, 'Failed to buy')
            return redirect('/')
