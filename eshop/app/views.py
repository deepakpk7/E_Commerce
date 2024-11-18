from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import *
# Create your views here.

def e_shop_login(req):
    if 'shop' in req.session:
        return redirect(shop_home)
    if req.method=='POST':
        uname=req.POST['uname']
        password=req.POST['password']
        data=authenticate(username=uname,password=password)
        if data:
            login(req,data)
            req.session['shop']=uname  #Create Session
            return redirect(shop_home)
        else:
            messages.warning(req, "Invalid Username or Password")
            return redirect(e_shop_login)
    else:
        return render(req,'login.html')
    

def register(req):
    return render(req,'register.html')


def shop_home(req):
    if 'shop' in req.session:
        data=Product.objects.all()
        return render(req,'shop/home.html',{'products':data})
    else:
        return redirect(e_shop_login)
    
def add_product(req):
    if 'shop' in req.session:
        if req.method=='POST':
            pid=req.POST['pid']
            name=req.POST['name']
            dis=req.POST['dis']
            price=req.POST['price']
            off_price=req.POST['offer_price']
            stock=req.POST['stock']
            file=req.FILES['img']
            data=Product.objects.create(pid=pid,name=name,
                                        dis=dis,price=price,
                                        offer_price=off_price,
                                        stock=stock,img=file)
            data.save()
            return redirect(shop_home)
        else:
            return render(req,'shop/add_product.html')
    else:
        return redirect(e_shop_login)
    
def e_shop_logout(req):
    logout(req)
    req.session.flush() #Delete session
    return redirect(e_shop_login)

def edit_product(req,pid):
    if req.method=='POST':
        p_id=req.POST['pid']
        name=req.POST['name']
        dis=req.POST['dis']
        price=req.POST['price']
        off_price=req.POST['offer_price']
        stock=req.POST['stock']
        file=req.FILES.get('img')
        if file:
            Product.objects.filter(pk=pid).update(pid=p_id,name=name,
                                        dis=dis,price=price,
                                        offer_price=off_price,
                                        stock=stock)
            data=Product.objects.get(pk=pid)
            data.img=file
            data.save()
        else:
            Product.objects.filter(pk=pid).update(pid=p_id,name=name,
                                        dis=dis,price=price,
                                        offer_price=off_price,
                                        stock=stock)
        return redirect(shop_home)
    else:
        data=Product.objects.get(pk=pid)
        return render(req,'shop/edit.html',{'data':data})