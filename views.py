from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.db.models import Q, F, Count

import collections

# Create your views here.
def search_method(request):
    context = {}
    if request.method == 'GET':
        query = request.GET.get('q')
        if query:
            context["search_term"] = query
            # use "query" to look up things and store in "result"
            context["search_results"] = ["Result1", "Result2"]

            ## context["search_term"] = query
            ## # use "query" to look up things and store in "result"
            ## aE = Entity.objects.filter( Q(name__icontains=query) | \
            ##                             Q(symbol__icontains=query) | \
            ##                             Q(id__icontains=query) | \
            ##                             Q(alt__icontains=query) | \
            ##                             Q(uniprot__upid__icontains=query) | \
            ##                             Q(uniprot__upacc__icontains=query) \
            ##                             ).values_list('id', 'symbol', 'name','species','alt','type','uniprot__upid', 'uniprot__upacc').distinct()

            
        else:
            context["search_term"] = "No term entered."
            context["search_results"] = []
            
        return render(request, 'irndb/search.html', context)
    # if not GET method return homepage
    else:
        context["error"] = 'Not a GET request.'
        return render(request, "irndb/404.html", context)

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
        context["error"] = 'Tab "%s" not known.'%sTab
        return render(request, "irndb/404.html", context)

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
        context["error"] = 'Type "%s" not known.'%sType
        return render(request, "irndb/404.html", context)

def browse_pw_method(request, pid):
    context = {}
    sType = request.GET.get('type', 'x')
    context = {}
    if sType == 'mirna':
        return render(request, "irndb/browse_pw.html", context)
    elif sType == 'target':
        return render(request, "irndb/browse_pw.html", context)
    elif sType == 'lncrna':
        return render(request, "irndb/browse_pw.html", context)
    elif sType == 'pirna':
        return render(request, "irndb/browse_pw.html", context)
    else:
        context["error"] = 'Type "%s" not known.'%sType
        return render(request, "irndb/404.html", context)

