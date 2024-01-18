from django.shortcuts import render, HttpResponseRedirect, redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from .models import register, event, CompletedModel
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.views.decorators.cache import cache_control
import calendar
import datetime
from datetime import date
from django.db.models import Q
from django.contrib import messages

def cld():
    today = date.today()
    text_cal = calendar.HTMLCalendar(firstweekday=-1)
    year = today.year
    return text_cal.formatyear(year, 4)
class SignUpView(View):
    @method_decorator(cache_control(no_cache=True, must_revalidate=True, no_store=True))
    def get(self, request):
        return render(request, "Activity/signup.html")

    def post(self, request):
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        email = request.POST.get("email")
        pass1 = request.POST.get("pass1")
        pass2 = request.POST.get("pass2")
        if pass1 != pass2:
            return HttpResponse("<p>Sorry, the password doesn't match</p><a href='signup'>Try again</a>")
        else:
            reg = User.objects.create_user(username=email, first_name=fname, last_name=lname, email=email, password=pass1)
            reg.save()
            auth_user = authenticate(request, username=email, password=pass1)
            login(request, auth_user)
            return redirect('homepage')
        
class IndexView(LoginRequiredMixin,View):
    @method_decorator(cache_control(no_cache=True, must_revalidate=True, no_store=True))
    
    def get(self, request):
        user = User.objects.get(username = request.user)
        first_name = user.first_name
        return render(request, "index.html", {"year": cld(),"user": first_name})
    
class LoginView(View):
    @method_decorator(cache_control(no_cache=True, must_revalidate=True, no_store=True))
    def get(self, request):
        return render(request, 'Activity/login.html')

    def post(self, request):
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        user = authenticate(request, username=email, password=pass1)

        if user is not None:
            login(request, user)
            return redirect('homepage')
        else:
            return render(request, "Activity/login.html")

class PostView(LoginRequiredMixin,View):
    def post(self, request):
        day = int(request.POST.get('Day'))
        month = request.POST.get('Month')
        month_number = datetime.datetime.strptime(month, '%B').month
        activity = request.POST.get('activity')
        today = date.today()
        d = datetime.date(today.year,month_number,day)
        if d<today:
            messages.info(request,'The date has already past. Please try again!!')
            return HttpResponseRedirect(reverse('homepage'))
        add = event(user=request.user,due_dates = d,day=day, month=month, activity=activity)
        add.save()
        return HttpResponseRedirect(reverse('homepage'))

    def get(self, request):
        return render(request, 'task.html')

class LogoutView(View):
    @method_decorator(cache_control(no_cache=True, must_revalidate=True, no_store=True))
    def get(self, request):
        request.session.clear() 
        logout(request)
        return redirect('log_in')


class DetailView(LoginRequiredMixin,View):
    def get(self, request):
        try:
            even = event.objects.filter(user=request.user).values()
            return render(request, 'detail.html', {'data': even})
        except event.DoesNotExist:
            return render(request, 'detail.html')
    
    def post(self,request):
        even = event.objects.filter(user=request.user).values()
        data =  even
        if request.POST.get("select"):
            select = request.POST.get("select")
            if select == 'completed':
                data = even.filter(completed = True).values()
                request.session['status']='completed'

            elif select == 'due_date':
                request.session['status']='due_date'
                data = even.filter(completed=False,due_dates__gte = date.today())
            else:
                data = even
                del request.session['status']
            return render(request, 'detail.html',{'data':data})
            
        else:
            sort = request.POST.get("sort")
            session_element = request.session.get('status')
            if data is not None:
                if session_element == 'completed':
                    data = even.filter(completed = True).values()
                elif session_element == 'due_date':
                    data = even.filter(completed=False,due_dates__gte = date.today())
                else:
                    data = even 
                if sort == 'added':
                    data = data.order_by('added_date')
                else:
                    data = data.order_by('due_dates')  
            else:
                data = even
            return render(request, 'detail.html',{'data':data,'session':session_element})
               
        
             

class DeletesView(LoginRequiredMixin,View):
    def get(self, request, id):
        data = event.objects.get(id=id)
        data.delete()
        return HttpResponseRedirect(reverse('details'))
    
class EditsView(LoginRequiredMixin,View):
    def get(self, request, id):
        data = event.objects.get(id=id)
        return render(request, 'edit.html',{'data':data})
        
    def post(self, request,id):
        day = request.POST.get('Day')
        month = request.POST.get('Month')
        activity = request.POST.get('activity')
        completed =  request.POST.get('completed')
        add = event.objects.get(id = id)
        add.day = day
        add.month = month
        add.activity = activity
        if completed:
            add.completed = True
            completedmodel = CompletedModel(user = request.user,day = day,month=month,activity=activity)
            completedmodel.save() 
        else:
            add.completed = False
        add.save() 
        return HttpResponseRedirect(reverse('details'))

