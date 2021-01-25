from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth import authenticate,logout,login
from datetime import date
from .models import Notes, Signup

# Create your views here.
def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def index(request):
    return render(request, 'index.html')
def userlogin(request):
    error = "" 
    if request.method == 'POST':
        u = request.POST['emailid']
        p = request.POST['pwd']
        user = authenticate(username=u, password=p)
        print(user)
        try:
            if user:
                login(request,user)
                error="no"
            else:
                error="yes"
        except:
            error="yes"
    d = {'error':error}    
    return render(request, 'login.html', d)

def login_admin(request):
    error = ""
    if request.method == 'POST':
        u = request.POST['uname']
        p = request.POST['pwd']
        user = authenticate(username=u, password=p)
        # print(user)
        try:
            if user.is_staff:
                login(request,user)
                error="no"
            else:
                error="yes"
        except:
            error="yes"
    d = {'error':error}    
    return render(request, 'login_admin.html', d)

def signup1(request):
    error=""
    if request.method=='POST':
        f = request.POST['firstname']
        l = request.POST['lastname']
        c = request.POST['contact']
        e = request.POST['emailid']
        p = request.POST['password']
        b = request.POST['branch']
        r = request.POST['role']
        try:
            user = User.objects.create_user(username=e,password=p,first_name=f,last_name=l)
            Signup.objects.create(user=user, contact=c, branch=b, role=r)
            error="no"
        except:
            error="yes"
    d={'error':error}
    return render(request, 'signup.html', d)

def admin_home(request):
    if not request.user.is_staff:
        return redirect('login')
    pn = Notes.objects.filter(status="pending").count()
    an = Notes.objects.filter(status="Accept").count()
    rn = Notes.objects.filter(status="Reject").count()
    alln = Notes.objects.all().count()
    d = {'pn':pn, 'an':an, 'rn':rn, 'alln':alln}
    return render(request, 'admin_home.html', d)

def Logout(request):
    logout(request)
    return redirect('index')

def profile(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user = User.objects.get(id=request.user.id)
    data = Signup.objects.get(user=user)
    d ={'data':data,'user':user}
    return render(request, 'profile.html', d)

def edit_profile(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user = User.objects.get(id=request.user.id)
    data = Signup.objects.get(user=user)
    error = False
    if request.method == "POST":
        f = request.POST['first_name']
        l = request.POST['last_name']
        k = request.POST['contact']
        g = request.POST['branch']
        user.first_name = f
        user.last_name = l
        user.contact = k
        user.branch = g 
        user.save()
        data.save()
        error = True
    d ={'data':data,'user':user, 'error':error}
    return render(request, 'edit_profile.html', d)

def changepassword(request):
    if not request.user.is_authenticated:
        return redirect('login')
    error=""
    if request.method=="POST":
        o = request.POST['old']
        n = request.POST['new']
        c = request.POST['confirm']
        if c==n:
            u = User.objects.get(username__exact= request.user.username)
            u.set_password(n)
            u.save()
            error="no"
        else:
            error="yes"
    d = {"error":error}
    return render(request, 'changepassword.html', d)

def upload_notes(request):
    if not request.user.is_authenticated:
        return redirect('login')
    error=""
    if request.method=='POST':
        b = request.POST['branch']
        s = request.POST['subject']
        n = request.FILES['notesfile']
        f = request.POST['filetype']
        c = request.POST['description']
        u = User.objects.filter(username=request.user.username).first()
        try:
            Notes.objects.create(user=u,uploadingdate=date.today(),branch=b,subject=s,notesfile=n,filetype=f,description=c,status='pending')
            error="no"
        except:
            error="yes"
    d={'error':error}
    return render(request, 'upload_notes.html', d)


def view_mynotes(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user = User.objects.get(id=request.user.id)
    notes = Notes.objects.filter(user=user)
    
    d ={'notes':notes}
    return render(request, 'view_mynotes.html', d)

def delete_mynotes(request, pid):
    if not request.user.is_authenticated:
        return redirect('login')
    notes = Notes.objects.get(id=pid)
    notes.delete()
    return redirect("view_mynotes")

def view_users(request):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    users = Signup.objects.all()
    d ={'users':users}
    return render(request, 'view_users.html', d)

def delete_users(request, pid):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    user = User.objects.get(id=pid)
    user.delete()
    return redirect("view_users")

def pending_notes(request):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    notes = Notes.objects.filter(status="pending")
    
    d ={'notes':notes}
    return render(request, 'pending_notes.html', d)

def accepted_notes(request):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    notes = Notes.objects.filter(status="Accept")
    
    d ={'notes':notes}
    return render(request, 'accepted_notes.html', d)

def rejected_notes(request):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    notes = Notes.objects.filter(status="Reject")
    
    d ={'notes':notes}
    return render(request, 'rejected_notes.html', d)

def all_notes(request):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    notes = Notes.objects.all()
    
    d ={'notes':notes}
    return render(request, 'all_notes.html', d)



def assign_status(request, pid):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    notes = Notes.objects.get(id=pid)
    error = ""
    if request.method=='POST':
        s = request.POST['status']
        try:
            notes.status = s
            notes.save()
            error="no"
        except:
            error="yes"
    d = {'notes':notes, 'error':error}
    return render(request, 'assign_status.html', d)

def viewallnotes(request):
    if not request.user.is_authenticated:
        return redirect('login')
    notes = Notes.objects.filter(status='Accept')
    
    d ={'notes':notes}
    return render(request, 'viewallnotes.html', d)

def download_notes(request):
    notes = Notes.objects.filter(status='Accept')
    
    d ={'notes':notes}
    return render(request, 'download_notes.html', d)