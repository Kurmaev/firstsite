from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login, logout
from django.template.response import TemplateResponse


# delete this. use func such as decorator. use extra_contex for state
def login_user(request):
    state = "Please log in below..."
    username = password = ''
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
#, {'template_name':'login_user/login.html','extra_context':{'state':state}}
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                state = "You're successfully logged in!"
            else:
                state = "Your account is not active, please contact the site admin."
        else:
            state = "Your username and/or password were incorrect."

    return TemplateResponse(request,'login_user/login.html',{'state':state, 'username': username})

#def logout(request): 
#    auth.logout(request)
#    return HttpResponseRedirect("/accounts/loggedout/")
