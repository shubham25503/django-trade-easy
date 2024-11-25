from email import message
import requests
from http.client import HTTPResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponseRedirect
from todo_list.models import T_List , crypto_tbl
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login , logout as logouts


def home(request):
    if request.session.has_key('aut') == 1:
        apidata = requests.get('https://api.coingecko.com/api/v3/coins/markets?vs_currency=inr&order=market_cap_desc&per_page=100&page=1&sparkline=false').json()
        return render(request, 'home.html', {'apidata':apidata})
    else:
        return redirect('authlogin')
def logout(request):
    logouts(request)
    return redirect('home')

def stockmarket(request):
    apidata = requests.get('https://api.coingecko.com/api/v3/coins/markets?vs_currency=inr&order=market_cap_desc&per_page=100&page=1&sparkline=false').json()
    return render(request, 'stockmarket.html', {'apidata':apidata})

def marketnews(request):
    return render(request, 'marketnews.html', {})

def portfolio(request):
    if request.method == "POST":
        qid = request.POST['id']
        invtkn = request.POST['invtkn']
        pandl = request.POST['pandl']
        uiid = request.session['u_id']
        inst = T_List.objects.get(u_id=uiid)
        t_amt = inst.t_amt
        invtkn = float(invtkn)
        pandl = float(pandl)
        inst.t_amt =  t_amt + invtkn + pandl
        print( t_amt + invtkn + pandl)
        print(invtkn)
        print(pandl)
        print(inst.t_amt)
        inst.save()
        request.session['token'] = inst.t_amt
        inst1 = crypto_tbl.objects.get(id=qid)
        inst1.delete()   
        return redirect('home')
    uiid= request.session['u_id']
    aaa = crypto_tbl.objects.filter(u_id=uiid)
    apidata = requests.get('https://api.coingecko.com/api/v3/coins/markets?vs_currency=inr&order=market_cap_desc&per_page=100&page=1&sparkline=false').json()
    return render(request, 'portfolio.html', {'aaa':aaa,'apidata':apidata})

def buycrypto(request):
    return render(request, 'buycrypto.html', {})
def sell_crypto(request):
    return render(request, 'sell_crypto.html', {})


def cryptocurrency(request):
    
    if request.method == "POST":
        if request.POST['submit'] == "buy_crypto":
            uiid= request.session['u_id']
            abc = T_List.objects.get(u_id=uiid)
            qwa = int(request.POST['t_amt'])
            print(abc.t_amt)
            if abc.t_amt >= qwa :
                ins1 = crypto_tbl(b_img=request.POST['b_img'],b_price=request.POST['b_price'],b_amt=request.POST['c_amt'],b_token=request.POST['t_amt'],b_name=request.POST['cname'],u_id=request.session['u_id']);
                ins1.save();
                abc.t_amt = abc.t_amt - qwa
                print(qwa)
                print(abc.t_amt)
                request.session['token'] = abc.t_amt
                abc.save()
                return redirect('home')
            else :
                return redirect('cryptocurrency')
        else:
            c_id = request.POST['id']
            c_img = request.POST['img']
            c_name = request.POST['name']
            c_current_price = request.POST['current_price']
            return render(request, 'buycrypto.html', {'c_id':c_id,'c_img':c_img,'c_name':c_name,'c_current_price':c_current_price})
    apidata = requests.get('https://api.coingecko.com/api/v3/coins/markets?vs_currency=inr&order=market_cap_desc&per_page=100&page=1&sparkline=false').json()
    return render(request, 'cryptocurrency.html', {'apidata':apidata})

def mailinbox(request) :
    return render(request, 'mailinbox.html', {})

def authlogin(request) :

    if request.method == "POST" :
        uname = request.POST['uname']
        pass1 = request.POST['pass']

        user = authenticate(username = uname, password = pass1)
        if user is not None: 
            login(request, user)
            fname = user.first_name
            u_id = user.id
            t_get = T_List.objects.all()
            for trans in t_get:
                if trans.u_id == u_id :
                    request.session['aut'] = 1
                    request.session['u_id'] = u_id
                    request.session['fname'] = user.first_name
                    request.session['email'] = user.email
                    request.session['token'] = trans.t_amt
            #eturn render(request, home, {'fname': fname})
            return redirect('home')

        else :
            messages.error(request,"Incorrect Credentials")
            return redirect('authlogin')

    return render(request, 'authlogin.html', {})

def authregister(request) :
    if request.method == "POST" :
        uname = request.POST['uname']
        pass1 = request.POST['pass']
        email = request.POST['email']
        fname = request.POST['fname']
        lname = request.POST['lname']

        myuser = User.objects.create_user( uname, email , pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        ins = T_List(t_amt=5000,u_id=myuser.id)
        ins.save() 
        messages.success(request, "Registration successful")
        return redirect('authlogin')
    return render(request, 'authregister.html', {})


