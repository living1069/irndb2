from django.shortcuts import render, render_to_response
from django.http import HttpResponse

# Create your views here.
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

def home_method(request):
    context = {}
    return render(request, "irndb/home.html", context)

def contact_method(request):
    context = {}
    #return HttpResponse(request.path)
    return render(request, "irndb/contact.html", context)

def doc_method(request):
    context = {}
    sTab = request.GET.get('tab', 'x')
    context = {}
    if sTab not in ['1','2','3','4']:
        return render(request, "irndb/doc.html", context)
    elif sTab == '1':
        return render(request, "irndb/doc_overview.html", context)
    elif sTab == '2':
        return render(request, "irndb/doc_desc.html", context)
    elif sTab == '3':
        return render(request, "irndb/doc_resources.html", context)
    elif sTab == '4':
        return render(request, "irndb/doc_stats.html", context)    
    else:
        return render(request, "irndb/doc.html", context)

def browse_method(request):
    context = {}
    sType = request.GET.get('type', 'x')
    context = {}
    if sType == 'mirna':
        return render(request, "irndb/browse_mirna.html", context)
    elif sType == 'target':
        return render(request, "irndb/browse_target.html", context)
    elif sType == 'lncrna':
        return render(request, "irndb/browse_lncrna.html", context)
    elif sType == 'pirna':
        return render(request, "irndb/browse_pirna.html", context)
    else:
        return render(request, "irndb/home.html", context)

def browse_pw_method(request):
    context = {}
    sType = request.GET.get('type', 'x')
    context = {}
    if sType == 'mirna':
        return render(request, "irndb/browse_pw_mirna.html", context)
    elif sType == 'target':
        return render(request, "irndb/browse_pw_target.html", context)
    elif sType == 'lncrna':
        return render(request, "irndb/browse_pw_lncrna.html", context)
    elif sType == 'pirna':
        return render(request, "irndb/browse_pw_pirna.html", context)
    else:
        return render(request, "irndb/home.html", context)
    
def tables_method(request):
    context = {}
    return render(request, "irndb/tables.html", context)

def charts_method(request):
    context = {}
    return render(request, "irndb/charts.html", context)


