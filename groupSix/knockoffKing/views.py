from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

def Home(request):
    # check if the request method is POST
    if request.method == 'POST':
        # get the username and password from the form
        username = request.POST.get('username')
        password = request.POST.get('password')

        # authenticate the user
        user = authenticate(request, username=username, password=password)

        # if the user is authenticated, log them in and redirect to a new page
        if user is not None:
            login(request, user)
            return redirect('home')


    # if the request method is not POST, return the login page
    return render(request, 'knockoffKing/home.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            error = 'Invalid username or password'
    else:
        error = None

    return render(request, 'knockoffKing/login.html', {'error': error})