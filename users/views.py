from django.shortcuts import render,redirect
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.contrib import messages
from django .urls import conf
from .utils import searchProfiles,paginateProfiles
from .forms import CustomUserCreationForm, ProfileForm,SkillForm


def loginUser(request):
    page='login'

    if request.user.is_authenticated:
        return redirect('profiles')
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST["password"]

        try:
            user=User.objects.get(username=username)
        except:
            messages.error(request,'username Does not exist')
        user= authenticate(request,username=username,password=password)
        if user is not None:
            login(request, user)
            return redirect('profiles')
        else:
            messages.error(request,'Username or password is incorrect ')
    return render(request, 'users/login_register.html')



def logoutUser(request):
    logout(request)
    messages.info(request,'user Succesfully logged out!')
    return redirect('login')


def registerUser(request):
    page='register'
    form= CustomUserCreationForm()
    if request.method == 'POST':
        form =CustomUserCreationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request,'User account was created')
            login(request, user)
            return redirect('edit-account')
        else:
             messages.error(request,'Error has occurred while creating the user') 
    context={'page':page, 'form':form}
    return render(request,'users/login_register.html',context)

def profiles(request):
    profiles,search_query=searchProfiles(request)
    custom_range,profiles= paginateProfiles(request,profiles,3)
    context ={'profiles':profiles,'custom_range':custom_range}
    return render(request,'users/profiles.html',context)

def userProfile(request,pk):
    profile= Profile.objects.get(id=pk)
    topSkills = profile.skill_set.exclude(description__exact="")
    otherSkills = profile.skill_set.filter(description="")

    context = {'profile': profile, 'topSkills': topSkills,
               "otherSkills": otherSkills, }
    return render(request, 'users/user-profile.html',context)


@login_required(login_url='login')
def userAccount(request):
    profile = request.user.profile
    Skills = profile.skill_set.all()
    projects= profile.project_set.all()
   

    context={'profile': profile,'Skills': Skills,'projects': projects }
    return render(request,'users/account.html',context)


@login_required(login_url='login')
def editAccount(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)
    if request.method == 'POST':
        form= ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('account')
    context = { 'form': form }
    return render(request, 'users/profile_form.html',context)

@login_required(login_url='login')
def createSkill(request):
    profile = request.user.profile
    form= SkillForm()
    if request.method == 'POST':
        form =SkillForm(request.POST)
        if form.is_valid():
            skill=form.save(commit=False)
            skill.owner=profile
            skill.save()
            messages.success(request,'Skill Added!') 
            return redirect('account')

    context={'form':form}
    return render(request, 'users/skill_form.html', context)


@login_required(login_url='login')
def updateSkill(request,pk):
    profile = request.user.profile
    skill=profile.skill_set.get(id=pk)

    form= SkillForm(instance=skill)
    if request.method == 'POST':
        form =SkillForm(request.POST, instance= skill)
        if form.is_valid():
            form.save()
            messages.success(request,'Skill was Updated Successfully!')
            return redirect('account')

    context={'form':form}
    return render(request, 'users/skill_form.html', context)


@login_required(login_url='login')
def deleteSkill(request,pk):
    profile= request.user.profile
    skill= profile.skill_set.get(id=pk)
    if request.method =='POST':
        skill.delete()
        messages.success(request,'Skill was deleted Successfully!')
        return redirect('account')

    context={'object':skill}
    return render(request,'delete_template.html',context)
