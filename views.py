from django.shortcuts import render, render_to_response
from django.http import HttpResponse

# Create your views here.
def home_method(request):
    context = {}
    return render(request, "irndb/home.html", context)

def contact_method(request):
    context = {}
    #return HttpResponse(request.path)
    return render(request, "irndb/contact.html", context)

def doc_method(request):
    context = {}
    return render(request, "irndb/doc.html", context)

def tables_method(request):
    context = {}
    return render(request, "irndb/tables.html", context)

def charts_method(request):
    context = {}
    return render(request, "irndb/charts.html", context)

def search_method(request):
    context = {}
    if request.method == 'GET':
        query = request.GET.get('q')
        if query:
            context["search_term"] = query
            # use "query" to look up things and store in "result"
            context["search_results"] = ["Result1", "Result2"]
        else:
            context["search_term"] = "No term entered."
            context["search_results"] = []
            
        return render(request, 'irndb/search.html', context)
    # if not GET method return homepage
    else:
        return render(request, "irndb/home.html", context)

