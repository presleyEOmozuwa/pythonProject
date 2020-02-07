from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import User, Wish
import datetime
import bcrypt


def index(request):
    return render(request, 'index.html')


def register(request):
    if request.method == 'POST':
        errors = User.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
                return redirect('/')
        else:
            hash = bcrypt.hashpw(
                request.POST['password'].encode(), bcrypt.gensalt())
            user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'],
            email=request.POST['email'], password=hash)
            print(user)

    return redirect('/loginpage')



def login_page(request):
    return render(request, 'login.html')


def login(request):
    if request.method == 'POST':
        try:
            print(request.POST['email'])
            user = User.objects.get(email=request.POST['email'])
        except:
            messages.error(request, "E-mail or password is invalid.")
            return redirect('/')

        if not bcrypt.checkpw(
                request.POST['loginpassword'].encode(), user.password.encode()):
            messages.error(request, "E-mail or password invalid.")
            return redirect("/")
        request.session['id'] = user.id
        request.session['email'] = user.email
        request.session['first_name'] = user.first_name
        request.session['last_name'] = user.last_name
        return redirect('/wishes')
    else:
        return redirect('/')


def wishes(request):
    context = {
        "all_wishes": Wish.objects.all()
    }
    return render(request, 'wishes.html', context)


def wishes_logout(request):
    request.session.clear()
    return redirect('/')


def wishes_remove(request, id):
    wish_to_remove = Wish.objects.get(id=id)
    if request.session['email'] == wish_to_remove.creator.email:
        wish_to_remove.delete()
    return redirect('/wishes')


def wishes_new(request):
    return render(request, 'wishes_new.html')


def wishes_new_logout(request):
    request.session.clear()
    return redirect('/')


def wishes_create(request):
    if request.method == 'POST':
        errors = Wish.objects.self_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
                return redirect('/wishes/new')
        else:
            creator = User.objects.get(email=request.session['email'])
            Wish.objects.create(
                title=request.POST['title'], creator=creator)
            return redirect('/wishes')
            
def wishes_edit_id(request, id):
    context ={
        "wish_to_edit" : Wish.objects.get(id=id)
    }
    return  render(request, 'wishes_edit_id.html', context)


def wishes_update_id(request, id):
        if request.method == 'POST':
            errors = Wish.objects.self_validator(request.POST)
            if len(errors) > 0:
                for key, value in errors.items():
                    messages.error(request, value)
                return redirect(f'/wishes/edit/{id}')
            else:
                wish_to_update = Wish.objects.get(id=id)
                wish_to_update.Title = request.POST['Title']
                wish_to_update.Description = request.POST['Description']
                wish_to_update.UpdatedAt = datetime.datetime.now()
                wish_to_update.save()
        return redirect('/wishes')

def wishes_granted_id(request, id):
    wish_granted = Wish.objects.get(id=id)
    wish_granted.granted = True
    wish_granted.granted_at = datetime.datetime.now()
    wish_granted.save()
    return redirect('/wishes')

def wishes_like_id(request, id):
    users_who_like=User.objects.get(id=request.session['id'])
    like_wish=Wish.objects.get(id=id)
    like_wish.like.add(users_who_like)
    return redirect('/wishes')