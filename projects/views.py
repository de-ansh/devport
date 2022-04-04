from pickle import FALSE
from turtle import title
from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Project
from .forms import ProjectForm,ReviewForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .utils import searchProjects,paginateProjects
def projects(request):
    projects, search_query =searchProjects(request)
    custom_range , projects =paginateProjects(request,projects,6)
    context ={'projects':projects, 'custom_range':custom_range }
    return render(request,'projects/projects.html',context )

def project(request,pk):
    projectobj= Project.objects.get(id=pk)
    form = ReviewForm()
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        review = form.save( commit= FALSE)
        review.project = projectobj
        review.owner = request.user.profile
        review.save()
        #project count
        messages.success(request, 'Your review was successfully submitted!')
    return render(request,'projects/single-project.html', {'project':projectobj, 'form': form})
@login_required(login_url="login")
def createProject(request):
    profile= request.user.profile

    form = ProjectForm()
    if request.method=='POST':
        form=ProjectForm(request.POST,request.FILES)
        if form.is_valid():
            project=form.save(commit=False)
            project.owner=profile
            project.save()
            return redirect('account')

    context={'form':form}
    return render(request,"projects/project_form.html",context)

@login_required(login_url="login")
def updateProject(request,pk):
    profile= request.user.profile
    project =profile.project_set.get(id=pk)
    form = ProjectForm(instance=project)
    if request.method=='POST':
        form=ProjectForm(request.POST,request.FILES,instance=project)
        if form.is_valid():
            form.save()
            return redirect('account')

    context={'form':form}
    return render(request,"projects/project_form.html",context)


@login_required(login_url="login")
def deleteProject(request,pk):
    profile= request.user.profile
    project=profile.project_set.get(id=pk)
    if request.method =='POST':
        project.delete()
        return redirect('account')
    context={'object':project}
    return render(request,'delete_template.html',context)


