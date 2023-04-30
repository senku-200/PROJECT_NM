import threading
from django.http import StreamingHttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate
from . import models,forms
from django.contrib import messages
from django.contrib.auth import login,logout
import cvlib
import cv2 as cv
from cvlib.object_detection import draw_bbox
import matplotlib.pyplot as plt
from cvzone.HandTrackingModule import HandDetector
import time,random
import cvzone
from cvzone.HandTrackingModule import HandDetector
from django.contrib.auth.decorators import login_required
# Create your vews here.

def home(request):
    project1= models.Project.objects.get(id = 1)
    project2= models.Project.objects.get(id = 2)
    context = {'project1':project1,'project2':project2}
    return render(request,'home.html',context)
def project(request,pk):
    project  = models.Project.objects.get(id = pk)
    print(project.template)
    template = str(project.template)[7:]
    context = {'project':project,"template":template}
    return render(request,'project.html',context)
def register(request):
    form_name = 'register'
    form = forms.RegisterForm()
    if request.method == 'POST':
        form = forms.RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = True
            user.save()
            return redirect('login')
    context = {"form_name":form_name,'form':form}
    return render(request,'login_register.html',context)

def signup_edit(request):
    form_name = 'register'
    model = models.User.objects.get(id = request.user.id)
    if request.method == 'POST':
        form = forms.RegisterForm(instance = model) 
        model.email = request.POST.get('email')
        model.username = request.POST.get('username')
        model.firstname = request.POST.get('firstname')
        model.lastname = request.POST.get('lastname')
        model.save()
        return redirect('home')
    context = {"form_name":form_name,'form':model}
    return render(request,'signup_edit.html',context)
def upload_image(request):
    model = models.User.objects.get(id = request.user.id)
    if request.method == 'POST':
        model.profile_image = request.FILES['image']
def logout_form(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('home')
def loginform(request):
    if request.user.is_authenticated:
        return redirect('home')
    form_name = 'login'
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = models.User.objects.get(email = email)
        except:
            messages.error(request,"user doesn't exist")
        
        user = authenticate(request,email = email,password=password)

        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,"wrong email or password")
        return redirect('login')
        
    context = {"form_name":form_name}
    return render(request,'login_register.html',context)


@login_required(login_url='login')
def stone_paper_scissor(request):
    if request.method == 'POST':
        count = int(request.POST.get('count'))
        match_count = count

        video = cv.VideoCapture(0)
        video.set(3,900)
        video.set(4,480)

        values = {
            str([0,0,0,0,0]):1,
            str([0,1,1,0,0]):2,
            str([1,1,1,1,1]):3,
        }

        keys = [[0,0,0,0,0],[0,1,1,0,0],[1,1,1,1,1]]
        start = False
        video = cv.VideoCapture(0)
        video.set(3,900)
        video.set(4,480)
        detector = HandDetector(maxHands=1)
        initial_time = 0
        points_ai = 0
        points_user = 0
        result = False
        user_name = 'player'
        w = ((305 - len(user_name))/4 + 590) + 20
        state = ""
        while 1:
            
            success,img = video.read()
            hands, frame = detector.findHands(img)
            imgBG = cv.imread('D:\PROJECT NM\Scripts\project\main\images\BG 2.jpg')
            paper = cv.imread('D:\PROJECT NM\Scripts\project\main\images\paper.png', cv.IMREAD_UNCHANGED)
            rock = cv.imread('D:\PROJECT NM\Scripts\project\main\images\_rock.png' , cv.IMREAD_UNCHANGED)
            scissors = cv.imread('D:\PROJECT NM\Scripts\project\main\images\scissors.png', cv.IMREAD_UNCHANGED)
            
            papermini = cv.imread('D:\PROJECT NM\Scripts\project\main\images\papermini.png', cv.IMREAD_UNCHANGED)
            rockmini = cv.imread('D:\PROJECT NM\Scripts\project\main\images\_rockmini.png' , cv.IMREAD_UNCHANGED)
            scissorsmini = cv.imread('D:\PROJECT NM\Scripts\project\main\images\scissorsmini.png', cv.IMREAD_UNCHANGED)
            
            scaled = cv.resize(frame,(0,0),None,.625,.625)
            scaled = scaled[:,66:496]
            imgBG[130:430,529:959] = scaled

            if start:
                if result is False:
                    timer = int(time.time() - initial_time)
                    if timer == 0:
                        imgBG = cvzone.overlayPNG(imgBG,rockmini,(428,276))
                    if timer == 1:
                        imgBG = cvzone.overlayPNG(imgBG,papermini,(428,276))
                    if timer == 2:
                        imgBG = cvzone.overlayPNG(imgBG,scissorsmini,(428,276))
                    if timer > 2:
                        timer = 0
                        start = False
                        if hands:
                            result = True
                            hand = hands[0]
                            fingers = detector.fingersUp(hand)
                            ai_choice = random.choice(keys)
                            if values[str(ai_choice)] == 1:
                                imgBG = cvzone.overlayPNG(imgBG,rock,(110,190))
                            elif values[str(ai_choice)] == 2:
                                imgBG = cvzone.overlayPNG(imgBG,scissors,(110,190))
                            elif values[str(ai_choice)] == 3:
                                imgBG = cvzone.overlayPNG(imgBG,paper,(110,190))
                            for key in keys:
                                if fingers == key:
                                    validation = True
                                    break
                            else:
                                validation = False

                            if validation:
                                if values[str(ai_choice)] == 1 and values[str(fingers)] == 2 or values[str(ai_choice)] == 2 and  values[str(fingers)] == 3 or values[str(ai_choice)] == 3  and values[str(fingers)] == 1:
                                    state = "computer"
                                    points_ai += 1
                                    
                                elif values[str(ai_choice)] ==2  and  values[str(fingers)] == 1 or values[str(ai_choice)] == 3 and  values[str(fingers)] == 2 or values[str(ai_choice)] == 1  and values[str(fingers)] == 3:
                                    state = "user"
                                    points_user += 1
                                    
                                else:
                                    state = "tie"
                                count-=1
                            else:
                                state = "retry"
                        else:
                            state = "retry"

                                
                                   
            if result:

                if values[str(ai_choice)] == 1:
                    imgBG = cvzone.overlayPNG(imgBG,rock,(113,190))
                elif values[str(ai_choice)] == 2:
                    imgBG = cvzone.overlayPNG(imgBG,scissors,(113,190))
                elif values[str(ai_choice)] == 3:
                    imgBG = cvzone.overlayPNG(imgBG,paper,(113,190))
            
            if state == "computer":
                cv.putText(imgBG,"computer win",(300,42),cv.FONT_HERSHEY_COMPLEX_SMALL,2,(0,0,255),1)
            elif state == "user":
                cv.putText(imgBG,"user win",(390,42),cv.FONT_HERSHEY_COMPLEX_SMALL,2,(0,0,255),1)
            elif state == "tie":
                cv.putText(imgBG,"match ties",(350,40),cv.FONT_HERSHEY_COMPLEX_SMALL,2,(0,0,255),1)
            elif state == 'retry':
                cv.putText(imgBG,"retry",(400,45),cv.FONT_HERSHEY_COMPLEX_SMALL,2,(0,0,255),1)
            
            cv.putText(imgBG,str(points_ai),(200,170),cv.FONT_HERSHEY_COMPLEX_SMALL,1,(255,0,0),1)
            cv.putText(imgBG,str(points_user),(740,123),cv.FONT_HERSHEY_COMPLEX_SMALL,1,(0,255,0),1)
            cv.putText(imgBG,f"{user_name}",(int(w),502),cv.FONT_HERSHEY_COMPLEX,1,(251, 133, 0),2)
            cv.putText(imgBG,f"Games left: {str(count)}",(74,572),cv.FONT_HERSHEY_COMPLEX_SMALL,1,(255,255,255),1)
            cv.imshow("imgBG",imgBG)
       
            key = cv.waitKey(1) 
            if key & 0xFF == ord('q'):

                break
            if key & 0xFF == ord('s'):
                start = True
                initial_time = time.time()
                result = False
            if count == 0:
                timer = time.time()
                timer_inc = int(timer)+3
                while 1:
                    timer = time.time()
                    if int(timer) == timer_inc:
                        break
                break 
        video.release()
        cv.destroyAllWindows()

        context = {
            'points_ai': points_ai,
            'points_user': points_user,
            'match_count':match_count,
        }

    
        return render(request,'RPS_match.html',context)
    context = {"mode":"match getter"}
    return render(request,'RPS_match.html',context)

@login_required(login_url='login')
def object_detecter(request):
    form = forms.ObjectDectectorForm()
    if request.method == "POST":
        form = forms.ObjectDectectorForm(request.POST)
        if form.is_valid:
            form = form.save(commit=False)
            form.image = request.FILES['image']
            form.save()
        img = cv.imread(f"D:\PROJECT NM\Scripts\project\data\{request.FILES['image']}")
        box,label,count = cvlib.detect_common_objects(img) 
        output =   draw_bbox(img,box,label,count)
        output = cv.cvtColor(output,cv.COLOR_BGR2RGB)
        plt.figure(figsize=(10,10))
        plt.axis('off')
        plt.imshow(output)
        plt.show()
        context = {"label":label,"mode":"display"}
        return render(request,'object_detecter.html',context)
    context = {"label":"","mode":""}
    return render(request,'object_detecter.html',context)

def profile(request):
    print(request.POST)
    profile_model = models.User.objects.get(id = request.user.id)
    print(profile_model.profile_image)
    if request.method == 'POST' and 'remove' in request.POST:
        if profile_model.profile_image != "":
            profile_model.profile_image.delete()
        return redirect('profile')
    if request.method == 'POST' and 'remove' not in request.POST:
        profile_model.profile_image = request.FILES['image']
        profile_model.save()
        return redirect('profile')
    context = {'form':profile_model}
    return render(request,'profile.html',context)


