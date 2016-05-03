from django.shortcuts import render, get_object_or_404, render_to_response
from django.http import HttpResponse
from django.template import RequestContext, loader
from .models import User
from django.views.decorators.csrf import csrf_exempt
from django.views import generic
import hashlib, uuid


class ViewUser(generic.ListView):
    model = User
    template_name = 'secu/view_users.html'

# Create your views here.
@csrf_exempt
def index(request):
    context = {}
    if 'users' in request.session:
        context['users'] = request.session['users']
        template = loader.get_template('secu/index.html')
        Us = User.objects.get(username=request.session['users'])
        if request.method == 'POST':
            Us.profile = request.POST['new_profile']
            Us.save()
            return render(request, 'secu/profile_success.html')
        context['users'] = request.session['users']
        template = loader.get_template('secu/index.html')
        Us = User.objects.get(username=request.session['users'])
        context['profile'] = Us.profile
        context['bitbars'] = Us.bitbars
        return HttpResponse(template.render(context, request))
    return render(request, 'secu/index.html')

@csrf_exempt
def register(request):
    if request.method == 'POST':
        user = request.POST['username'] if 'username' in request.POST else ''
        passw = request.POST['password'] if 'password' in request.POST else ''
        error_message = ''
        if user == '':
            error_message = 'Username field needs a value.'
        elif passw == '':
            error_message = 'Password field needs a value.'
        if User.objects.filter(username=user).count() == 1:
            error_message = 'User name already exists.'
        if error_message:
            return render_to_response('secu/register_form.html', {'error_message':error_message}, RequestContext(request))

        template = loader.get_template('secu/register_success.html')
        context = {
            'users': user,
        }

        #Create the user in the database
        # Password needs to be encoded before hashing
        salt = uuid.uuid4().hex
        pwd = passw + salt
        pwd = pwd.encode('utf-8')
        hashed = hashlib.sha1(pwd).hexdigest()

        q = User(username=user, hashed_password=hashed, salt=salt, profile='I like money')
        q.save()
        #create user session
        request.session['users'] = user

        return HttpResponse(template.render(context, request))

    else:
        return render(request, 'secu/register_form.html')

@csrf_exempt
def login(request):
    if request.method == 'POST':
        user = request.POST['username'] if 'username' in request.POST else ''
        passw = request.POST['password'] if 'password' in request.POST else ''
        error_message = ''
        if user == '':
            error_message = 'Username field needs a value.'
        elif passw == '':
            error_message = 'Password field needs a value.'
        us = User.objects.filter(username=user)
        if User.objects.filter(username=user).count() == 0:
            error_message = 'User does not exists.'
        else:
            pwd = passw + us[0].salt
            pwd = pwd.encode('utf-8')
            hashed = hashlib.sha1(pwd).hexdigest()
            if hashed == us[0].hashed_password:
                request.session['users'] = user
                template = loader.get_template('secu/login_success.html')
                context = {
                    'users': user,
                }
                print (user)
                print (context['users'])
                return HttpResponse(template.render(context, request))

            else:
                error_message = 'Wrong user or password'
        if error_message:
            return render_to_response('secu/login.html', {'error_message':error_message}, RequestContext(request))

    else:
        return render(request, 'secu/login.html')

def logout(request):
    try:
        del request.session['users']
    except KeyError:
        pass
    return render(request, 'secu/index.html')

@csrf_exempt
def profile(request):
    context = {}
    if 'users' in request.session:
        other_user = ''
        if 'username' in request.GET:
            other_user = request.GET['username'] if 'username' in request.GET else ''
            print (User.objects.filter(username=other_user).count())
            if User.objects.filter(username=other_user).count() == 0:
                error_message = 'User does not exists.'
                return render_to_response('secu/profile.html', {'error_message':error_message}, RequestContext(request))
        context['users'] = other_user if other_user else request.session['users']
        template = loader.get_template('secu/profile.html')
        Us = User.objects.get(username=context['users'])
        context['profile'] = Us.profile
        context['bitbars'] = Us.bitbars
        print (Us.bitbars)
        context['logged_in_user'] = request.session['users']
        return HttpResponse(template.render(context, request))
    return render(request, 'secu/must_login.html')

@csrf_exempt
def close(request):
    context = {}
    if 'users' in request.session:
        if request.method == 'POST':
            Us = User.objects.get(username=request.session['users'])
            Us.delete()
            del request.session['users']
            return render(request, 'secu/delete_user_success.html')
        context['users'] = request.session['users']
        template = loader.get_template('secu/delete_user.html')
        return HttpResponse(template.render(context, request))

    return render(request, 'secu/must_login.html')

@csrf_exempt
def transfer(request):
    context = {}
    if 'users' in request.session:
        other_user = ''
        if request.method == 'POST':
            other_user = request.POST['destination_username'] if 'destination_username' in request.POST else ''
            error_message = ''
            if User.objects.filter(username=other_user).count() == 0:
                error_message = 'User does not exists.'
            else:
                Us = User.objects.get(username=request.session['users'])
                quantity = int(request.POST['quantity'])
                if Us.bitbars < quantity:
                    error_message = 'Not enough bitbars'
            if error_message:
                return render_to_response('secu/transfer_form.html', {'error_message':error_message}, RequestContext(request))
            else:
                Other_Us = User.objects.get(username=other_user)
                Other_Us.bitbars = Other_Us.bitbars + quantity
                Other_Us.save()
                Us.quantity = Us.bitbars - quantity
                Us.save()
                context['other_us'] = Other_Us.username
                context['other_us_bitbars'] = Other_Us.bitbars
                context['users'] = Us.username
                context['bitbars'] = Us.bitbars
                context['quantity'] = quantity
                template = loader.get_template('secu/transfer_success.html')
                return HttpResponse(template.render(context, request))

        Us = User.objects.get(username=request.session['users'])
        context['users'] = Us.username
        template = loader.get_template('secu/transfer_form.html')
        context['bitbars'] = Us.bitbars
        return HttpResponse(template.render(context, request))

    return render(request, 'secu/must_login.html')
