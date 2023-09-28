from django.shortcuts import render, redirect

# Create your views here.
from re import S
from django.contrib.auth.models import User
import cv2
from django.shortcuts import HttpResponse, render
from django import http
import pandas
import numpy as np
import os
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
from django.contrib.auth import authenticate, login, logout
from . models import Diabetes

# Create your views here.


def index(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


def upload(request):
    return render(request, 'upload.html')


def register(request):
    if request.method == 'POST':
        email1 = request.POST['useremail']
        password = request.POST['psw']
        confirmpassword = request.POST['conpassword']
        if password == confirmpassword:
            a = User.objects.create_user(
                username=email1, email=email1, password=password)
            msg = "Successfully Registered"
            return render(request, 'login.html', {"msg": msg})
        mssg = "Registration Failed, Try Again"

        return render(request, "register.html", {'msg': mssg})
    return render(request, "register.html")


def logins(request):
    if request.method == 'POST':
        email = request.POST['useremail']
        password = request.POST['psw']
        d = authenticate(username=email, password=password)
        print(d)
        if d is not None:
            login(request, d)
            return redirect("index")
    return render(request, "login.html")


def prediction(request):
    if request.method == 'POST':
        diabetes = []
        paths = os.listdir(r'app\Footdata\test')
        for i in paths:
            diabetes.append(i)

        m = int(request.POST['alg'])
        File = request.FILES['foot']
        s = Diabetes(pestimg=File)
        s.save()
        path1 = 'app/static/diabetes/' + s.Imagename()

        if m == 1:
            model = load_model(r'app/models/CNNfoot.h5')
            x1 = image.load_img(path1, target_size=(64, 64))
            x1 = image.img_to_array(x1)
            x1 = np.expand_dims(x1, axis=0)
            x1 /= 255
            result = model.predict(x1)
            b1 = np.argmax(result)
            results = diabetes[b1]
            print(results)

        elif m == 2:
            model = load_model(r'app/models/mobilenetfoot.h5')
            x2 = image.load_img(path1, target_size=(64, 64))
            x2 = image.img_to_array(x2)
            x2 = np.expand_dims(x2, axis=0)
            x2 /= 255
            result = model.predict(x2)
            b2 = np.argmax(result)
            results = diabetes[b2]
            print(results)

        # applying heatmap to img
        img = cv2.imread(path1, 2)
        img1 = cv2.applyColorMap(img, cv2.COLORMAP_JET)
        cv2.imwrite('app/static/diabetes/output.jpg', img1)

        if results == 'Abnormal(Ulcer)':
            display = "Diabetic Ulcer"

        else:
            display = 'Normal'
        return render(request, 'result.html', {'result': display, 'path1': '/static/diabetes/'+s.Imagename(), "path2": "/static/diabetes/output.jpg"})
    return render(request, 'result.html')
