from django.shortcuts import render

def base(req):
    
    return render(req, "landing.html")