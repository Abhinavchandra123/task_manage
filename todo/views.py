from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import datetime
import calendar
from django.contrib.auth.models import User
from .models import Job, Employee


def loginmanager(request):
    if request.method == "POST":
        uname = request.POST['uname']
        pwd = request.POST['pwd']
        user = authenticate(request, username=uname, password=pwd)
        if user:
            if user.is_staff == 1:
                login(request, user)
                return redirect('ind')
        # messages.error(request, 'Incorrect username or Password', extra_tags='text-danger')
    return render(request, 'login.html')


# logout function
def logoutUser(request):
    logout(request)
    return redirect('login')

# dashboard(index)


@login_required(login_url='login')
def index(request):

    return render(request, 'index.html')

# managentreport


@login_required(login_url='login')
def manage(request):
    data = request.GET
    emps = Employee.objects.all()
    now = datetime.datetime.now()
    dates = f"{now.day} - {calendar.month_name[now.month]} - {now.year} - {now.hour} : {now.minute}"
    date = f"{now.day}:{now.month}:{now.year}"
    sdate = f'{now.year}{now.month}{now.day}'

    if request.GET == True:
        empl = data.get('empl')
        jobs = Job.objects.filter(fdate=None, user_id=empl,)
        context = {'dates': dates, 'emps': emps, 'jobs': jobs}
        return render(request, 'dashboard.html', context)

    if request.method == 'POST':

        data = request.POST
        p = data['add']
        if p == 'add':

            job = data['jobadd']
            task = data['task']
            refer = data['refer']
            user = data['user']
            Job.objects.create(
                jobname=job,
                task=task,
                ref=refer,
                sdate=date,
                status='Not completed',
                user_id=user,
                day=sdate,
            )
            # filter employee details
            jobs = Job.objects.filter(user_id=user, status='Not completed')
            nub = len(jobs)
            nocmpj = Job.objects.filter(user_id=user)
            bewu = len(nocmpj)
            comp = bewu-nub
            # update table
            emps = Employee.objects.filter(id=user)
            em = Employee.objects.get(id=user)
            em.progress = nub
            em.task = bewu
            em.completed = comp
            em.save()
            context = {'date': date, 'emps': emps}
            return redirect('manage')
    context = {'dates': dates, 'emps': emps, }
    return render(request, 'dashboard.html', context)

@login_required(login_url='login')
def prev(request):
    # date time
    now = datetime.datetime.now()
    dates = f"{now.day} - {calendar.month_name[now.month]} - {now.year} - {now.hour} : {now.minute}"
    sdate = f'{now.year}{now.month}{now.day}'
    # get
    data = request.GET
    empl = data.get('empl')
    # filter employee details
    jobs = Job.objects.filter(user_id=empl, status='Not completed')
    nub = len(jobs)
    nocmpj = Job.objects.filter(user_id=empl)
    bewu = len(nocmpj)
    comp = bewu-nub
    # update table
    emps = Employee.objects.filter(id=empl)
    em = Employee.objects.get(id=empl)
    em.progress = nub
    em.task = bewu
    em.completed = comp
    em.save()
    jobtds = Job.objects.filter(
        user_id=empl, day=sdate, status='Not completed')

    # find which button clicked
    if request.method == 'POST':
        button = request.POST.get('old')
        buttonnew = request.POST.get('new')
        print(buttonnew)

        if button == 'true':
            # get form value
            data = request.POST
            job = data['job']
            task = data['task']
            remark = data['remark']
            uid = data['user']
            status = data['status']
            if status == "Completed":
                fdate = dates
            else:
                fdate = None
                print(status)

            # update table
            print(remark)
            jobs = Job.objects.get(id=uid)
            jobs.jobname = job
            jobs.task = task
            jobs.remark = remark
            jobs.status = status
            jobs.fdate = fdate
            jobs.save()
            # refresh  employee status
            jobs = Job.objects.filter(user_id=empl, status='Not completed')
            nub = len(jobs)
            nocmpj = Job.objects.filter(user_id=empl)
            bewu = len(nocmpj)
            comp = bewu-nub
            # update
            em = Employee.objects.get(id=empl)
            em.progress = nub
            em.task = bewu
            em.completed = comp
            em.save()
        #  if new task button clicked
        elif buttonnew == 'new':
            data = request.POST
            job = data['job']
            task = data['task']
            remark = data['remark']
            uid = data['user']
            status = data['status']
            if status == "Completed":
                fdate = dates
                print(status)
            else:
                fdate = None
                print(uid)

            print(remark)
            jobs = Job.objects.get(id=uid)
            jobs.jobname = job
            jobs.task = task
            jobs.remark = remark
            jobs.status = status
            jobs.fdate = dates
            jobs.save()

            jobs = Job.objects.filter(user_id=empl, status='Not completed')
            nub = len(jobs)
            nocmpj = Job.objects.filter(user_id=empl)
            bewu = len(nocmpj)
            comp = bewu-nub
            em = Employee.objects.get(id=empl)
            em.progress = nub
            em.task = bewu
            em.completed = comp
            em.save()
        return redirect('manage')

    context = {'jobs': jobs, 'emps': emps,
               'dates': dates, 'jobtds': jobtds, 'sdate': sdate}
    return render(request, 'prev.html', context)

@login_required(login_url='login')
def addemp(request):
    if request.method == 'POST':
        data = request.POST
        emp = data['empname']
        detail = data['details']
        phone = data['phone']
        email = data['email']
        Employee.objects.create(
            name=emp,
            email=email,
            phone=phone,
            details=detail
        )

    return render(request, 'addemployee.html')

@login_required(login_url='login')
def report(request):
    emps = Employee.objects.all()
    # form submit
    if request.method == 'POST':
        # get from and to value
        data = request.POST
        fro = data['from']
        to = data['to']
        if fro == '':
            jobs = Job.objects.get(id=1)
            fro = jobs.day
            fro = int(fro.replace("-", ""))
        else:
            fro = int(fro.replace("-", ""))
        if to == '':
            now = datetime.datetime.now()
            sdate = f'{now.year}{now.month}{now.day}'
            to = int(sdate.replace("-", ""))
        else:
            to = int(to.replace("-", ""))
        # get number of jobs
        for j in emps:
            lenj = 0
            nub = 0
            bewu = 0
            for i in range(fro, to):
                jobs = Job.objects.filter(day=i, user_id=j.id)  # total
                lenj = lenj+len(jobs)
                jobss = Job.objects.filter(
                    user_id=j.id, day=i, status='Not completed')  # not completed
                nub = nub+len(jobss)
                comp = lenj-nub
            # refresh employee status
            emp = Employee.objects.get(id=j.id)
            emp.tempt = lenj
            emp.tempp = nub
            emp.tempc = comp
            emp.save()
        return redirect('rep')
    context = {'emps': emps}
    return render(request, 'rep.html', context)

@login_required(login_url='login')
def listemp(request):
    emps = Employee.objects.all()
    context = {'emps': emps, }
    return render(request, 'listemp.html', context)

@login_required(login_url='login')
def delb(request, id):
    bks = Employee.objects.get(id=id)
    nsj = Job.objects.filter(user_id=id)

    nsj.delete()
    bks.delete()
    messages.success(request, "Employee removed successfully")
    return redirect("list")

@login_required(login_url='login')
def edit(request, pk):
    bks = Employee.objects.get(id=pk)
    if request.method == 'POST':
        data = request.POST
        emp = data['empname']
        detail = data['details']
        phone = data['phone']
        email = data['email']
        bks.name = emp
        bks.email = email
        bks.detail = detail
        bks.phone = phone
        bks.save()
        messages.success(request, "Employee details updated")
    data = {'bks': bks}
    return render(request, 'editemployee.html', data)
