from django.shortcuts import render, redirect
from .models import Room, Topic, Message,User
from .forms import RoomForm,UserForm,MessageForm,CustomUser
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from random import shuffle



def loginUser(request):

    page = 'login'
    if request.user.is_authenticated:
        messages.error(request, "Logout first")
        return redirect('home')
        

    if request.method == 'POST': #if the user enter their information and login
        email = request.POST.get('email') and request.POST.get('email').lower() #get the username
        password = request.POST.get('password') # get the password

        #check if the user exits
        try:
            user = User.objects.get(email=email)

        except:
            messages.error(request, 'User does not exit')

        #authenticate the user 
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user) #logs the user in
            return redirect('home')# redirects the user back to the home page
        
        else:
          messages.error(request, "User or Password does not exit")

    context = {'page':page}
    return render (request, 'studyroom/login_signup.html', context)


# logs out the user
def logoutUser(request):
    logout(request)
    return redirect('home')



def signupView(request):
    if request.user.is_authenticated:
        messages.error(request, "Logout first")
        return redirect('home')
    
    form = CustomUser()
    page = 'signup'
    
    if request.method == 'POST':
        form = CustomUser(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'An error occurred during registration')
            
    context={
        'page':page,
        'form':form
        }
    return render(request, 'studyroom/login_signup.html', context )



def userProfile(request,pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_activity = user.message_set.all()
    topics = Topic.objects.all()
    count=rooms.count()
    context={'user':user,'rooms':rooms,
             'room_activity':room_activity,'topics':topics,
             'count':count
             }
    return render(request,'studyroom/profile.html',context)



@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)
    
    if request.method == 'POST':
        form = UserForm(request.POST,  request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile',pk=user.id)

    context={'form':form}   
    return render(request, 'studyroom/edit-user.html', context)




def homeView(request):
    q =  request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q)|
        Q(name__icontains=q)|
        Q(description__icontains=q)
        )
    count=rooms.count()
    topics = Topic.objects.all()[0:5]
    room_activity = Message.objects.filter(Q(room__topic__name__icontains=q))

    context = {'rooms':rooms, 'topics':topics,'count':count, 'room_activity':room_activity}
    return render (request, 'studyroom/home.html', context )

    
def roomView(request,pk):
    room = Room.objects.get(id=pk)
    room_messages= room.message_set.all().order_by('created')
    participants = room.participants.all()

    if request.method == "POST":
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)
    

    context={'room':room, 'room_messages':room_messages, 'participants':participants}
    return render (request, 'studyroom/room.html', context) 



@login_required(login_url='login')
def create_room(request):
    page = 'create'
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name) #get or create a new topic

        Room.objects.create(
            host= request.user,
            topic = topic,
            name = request.POST.get('name'),
            description = request.POST.get('description')
        )

        return redirect('home')
    context = {'form':form,'topics':topics,'page':page}
    return render(request, 'studyroom/room_form.html', context)



@login_required(login_url='login')
def update_room(request, pk):
    page='update'
    room = Room.objects.get(id=pk)
    form = RoomForm(instance= room)
    topics = Topic.objects.all()

    if request.user != room.host:
        return HttpResponse('You are not allowed here!!  ')

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room )
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')
        
    context={'form':form,'topics':topics,'room':room,'page':page}

    return render (request, 'studyroom/room_form.html', context  )


@login_required(login_url='login')
def delete_room (request, pk):
    room = Room.objects.get(id=pk) #to get that particular room we use the ID

    if request.user != room.host:
        return HttpResponse('You are not allowed here!!')

    if request.method == "POST":
        room.delete()
        return redirect('home')
    return render(request, 'studyroom/delete.html', {'obj':room})



@login_required(login_url='login')
def edit_message(request, pk):
    room_message = Message.objects.get(id=pk)
    form = MessageForm(instance= room_message)

    if request.user != room_message.user:
        return HttpResponse('You are not allowed here!!')

    if request.method == 'POST':
        form = MessageForm(request.POST, instance=room_message )
        if form.is_valid():
            form.save()
            return redirect('room',pk=room_message.room.id)
        
    context={'form':form}

    return render (request, 'studyroom/room_form.html', context  )


@login_required(login_url='login')
def delete_message (request, pk):
    room_message = Message.objects.get(id=pk) #to get that particular room we use the ID

    if request.user != room_message.user:
        return HttpResponse('You are not allowed here!!')

    if request.method == "POST":
        room_message.delete()
        return redirect('room',pk=room_message.room.id)
    return render(request, 'studyroom/delete.html', {'obj':room_message})


def topicpage(request):
    q =  request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    context = {'topics':topics}
    return render (request, 'studyroom/topics.html', context)

def activitypage(request):
    room = Room.objects.all()
    topics = Topic.objects.all()
    room_activity = Message.objects.all()
    context={'room':room,'topics':topics,'room_activity':room_activity}
    return render(request, 'studyroom/activity.html',context)