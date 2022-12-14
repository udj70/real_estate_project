from django.shortcuts import redirect, render
from django.contrib import messages,auth
from django.contrib.auth.models import User
from contacts.models import Contacts
def register(request):
    #print(request)
    if request.method == 'POST':
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        password2=request.POST['password2']

        if password ==  password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username is taken ")
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.error(request, "Email is taken ")
                return redirect('register')
            else:
                # all fine
                user = User.objects.create_user(username=username,password=password,email=email,first_name=first_name,last_name=last_name)
                # login after register
                # auth.login(request,user)
                # messages.success(request, "You are logged in")
                # return redirect('index')
                user.save()
                messages.success(request, "You are registered and you can login now")
                return redirect('login')
        else:
            messages.error(request, "Passwords didn't match")
            return redirect('register')
    else:
        return render(request, 'accounts/register.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username = username, password = password)
        if user :
            auth.login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid Credentials")
            return redirect('login')

    else:
        return render(request, 'accounts/login.html')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, "You are sucessfully logged out")
        return redirect('index')

def dashboard(request):
    user_contacts = Contacts.objects.order_by('-contact_date').filter(user_id=request.user.id)

    context = {
        'contacts': user_contacts
    }
    return render(request, 'accounts/dashboard.html',context)

