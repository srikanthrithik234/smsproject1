# Create your views here.

def projecthomepage(request):
    return render(request,'adminapp/ProjectHomePage.html')

def printpagecall(request):
    return render(request,'adminapp/printer.html')

def printpagelogic(request):
    if request.method=="POST":
        user_input= request.POST['user_input']
        print(f'User Input: {user_input}')
    a1= {'user_input':user_input}
    return render(request,'adminapp/printer.html',a1)

def exceptionpagecall(request):
    return render(request, 'adminapp/Exception1.html')

def exceptionpagelogic(request):
    if request.method == "POST":
        user_input = request.POST['user_input']
        result = None
        error_message = None
        try:
            num = int(user_input)
            result = 10/num
        except Exception as e:
            error_message = str(e)
        return render(request, 'adminapp/Exception1.html', {'result':result, 'error':error_message})
    return render(request, 'adminapp/Exception1.html')

import random
import string
def randompagecall(request):
    return render(request,'adminapp/RandomExample.html')

def randomlogic(request):
    if request.method == "POST":
        number1 = int(request.POST['number1'])
        ran = ''.join(random.sample(string.ascii_uppercase + string.digits, k=number1))
    a1= {'ran':ran}
    return render(request,'adminapp/RandomExample.html',a1)

def calculatorlogic(request):
    result = None
    if request.method == 'POST':
        num1 = float(request.POST.get('num1'))
        num2 = float(request.POST.get('num2'))
        operation = request.POST.get('operation')

        if operation == 'add':
            result = num1 + num2
        elif operation == 'subtract':
            result = num1 - num2
        elif operation == 'multiply':
            result = num1 * num2
        elif operation == 'divide':
            result = num1 / num2 if num2 != 0 else 'Infinity'

    return render(request, 'adminapp/SimpleCalculator.html', {'result': result})


from django.shortcuts import get_object_or_404
from .models import Task, StudentList
from .forms import TaskForm


def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_task')
    else:
        form = TaskForm()
    tasks = Task.objects.all()
    return render(request,'adminapp/add_task.html',{'form': form, 'tasks': tasks})

def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.delete()
    return redirect('add_task')



def UserRegisterPageCall(request):
    return render(request,'adminapp/UserRegisterPage.html')


from django.contrib.auth.models import User, auth


def UserRegisterLogic(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        pass1 = request.POST['password']
        pass2 = request.POST['password1']

        if pass1 == pass2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'OOPS! Username already taken.')
                return render(request, 'adminapp/UserRegisterPage.html')
            else:
                user = User.objects.create_user(
                    username=username,
                    password=pass1,
                    first_name=first_name,
                    last_name=last_name,
                    email=email
                )
                user.save()
                messages.info(request, 'Account created Successfully!')
                return render(request, 'adminapp/projecthomepage.html')
        else:
            messages.info(request, 'Passwords do not match.')
            return render(request, 'adminapp/UserRegisterPage.html')
    else:
        return render(request, 'adminapp/UserRegisterPage.html')

from django.contrib import messages, auth
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# For rendering the login page
def UserLoginPageCall(request):
    return render(request, 'adminapp/UserLoginPage.html')


def UserLoginLogic(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Log the user in
            login(request, user)

            # Check the length of the username
            if len(username) == 10:
                messages.success(request, 'Login successful as student!')
                return redirect('studentapp:StudentHomePage')
            elif len(username) == 4:
                messages.success(request, 'Login successful as faculty!')
                return redirect('facultyapp:FacultyHomePage')
            else:
                # Invalid username length
                messages.error(request, 'Username length does not match student or faculty criteria.')
                return render(request, 'adminapp/UserLoginPage.html')
        else:
            # If authentication fails
            messages.error(request, 'Invalid username or password.')
            return render(request, 'adminapp/UserLoginPage.html')
    else:
        return render(request, 'adminapp/UserLoginPage.html')


def logout(request):
    auth.logout(request)
    return redirect('projecthomepage')


@login_required
def FacultyHomePage(request):
    return render(request, 'facultyapp/FacultyHomePage.html')

''''
from .forms import StudentForm
def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm()
    return render(request, 'adminapp/add_student.html', {'form': form})
'''
def student_list(request):
    students = StudentList.objects.all()
    return render(request, 'adminapp/student_list.html', {'students': students})


from .forms import UploadFileForm
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64

def upload_file(request, monthly_names=None):
    if request.method == 'POST' and request.FILES['file']:
        file = request.FILES['file']
        df = pd.read_csv(file, parse_dates=['Date'], dayfirst=True)
        total_sales = df['Sales'].sum()
        average_sales = df['Sales'].mean()

        df['Month'] = df['Date'].dt.month
        monthly_sales = df.groupby('Month')['Sales'].sum()
        monthly_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        monthly_sales.index = monthly_sales.index.map(lambda x: monthly_names[x-1])

        plt.pie(monthly_sales, labels=monthly_sales.index, autopct='%1.1f%%')
        plt.title("Sales Distribution per Month")

        #process of converting the chart and sending it to the HTML
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_data = base64.b64encode(buffer.getvalue()).decode('utf-8')
        buffer.close()

        return render(request, 'adminapp/chart.html', {
            'total_sales': total_sales,
            'average_sales': average_sales,
            'chart': image_data
        })
    return render(request, 'adminapp/chart.html', {'form': UploadFileForm()})

from datetime import datetime, timedelta
from django.shortcuts import render


def daytimepagecall(request):
    return render(request, 'adminapp/daytime.html')


def daytimepagelogic(request):
    if request.method == 'POST':
        number1 = int(request.POST['date1'])
        x = datetime.now()
        ran = x + timedelta(days=number1)
        a1 = {'ran': ran}
        return render(request, 'adminapp/datetime.html', a1)
    else:
        return render(request, 'adminapp/datetime.html')


from django.contrib.auth.models import User
from .models import StudentList
from .forms import StudentForm
from django.shortcuts import redirect, render
def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save(commit=False)
            register_number = form.cleaned_data['Register_Number']
            try:
                user = User.objects.get(username=register_number)
                student.user = user  # Assign the matching User to the student
            except User.DoesNotExist:
                form.add_error('Register_Number', 'No user found with this Register Number')
                return render(request, 'adminapp/add_student.html', {'form': form})
            student.save()
            return redirect('student_list')
    else:
        form = StudentForm()
    return render(request, 'adminapp/add_student.html', {'form': form})


# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from .models import Contact
from .forms import ContactForm

def add_contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save()
            return redirect('contact_list')
    else:
        form = ContactForm()
    return render(request, 'adminapp/add_contact.html', {'form': form})

def contact_list(request):
    contacts = Contact.objects.all()
    query = request.GET.get('q')
    if query:
        contacts = contacts.filter(name__icontains=query) | contacts.filter(email__icontains=query)
    return render(request, 'adminapp/contact_list.html', {'contacts': contacts})

def delete_contact(request, contact_id):
    contact = get_object_or_404(Contact, id=contact_id)
    contact.delete()
    return redirect('contact_list')

