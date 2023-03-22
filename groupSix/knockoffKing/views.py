from django.shortcuts import render

# Create your views here.

# ~~~~~ Home ~~~~~
def Home(request):

    
    # ~~~~~ Return Generated Values ~~~~~
    context = {

    }
    return render(request, 'knockoffKing/home.html', context=context)
    # ~~~~~
# ~~~~~