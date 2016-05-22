from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.db.models import Q, F, Count
import csv

from irndb2.models import Target, T2G, T2K, T2W, T2K, T2C7, Go, Kegg, Wikipath, Msigdb_c7, Mirna, M2T_EXP, M2T_PRED, Lncrna, L2T, Pirna, P2T # use db of irn2 needs changing to .models

# Create your views here.
def search_method(request):
    context = {}
    if request.method == 'GET':
        query = request.GET.get('q')
        if query:
            context["search_term"] = query
            # use "query" to look up things and store in "result"
            
            ## context["search_term"] = query
            ## # use "query" to look up things and store in "result"
            res_target = Target.objects.filter( Q(tname__icontains=query) | \
                                        Q(symbol__icontains=query) | \
                                        Q(id__icontains=query)
                                        ).values_list('id',
                                                      'symbol',
                                                      'tname').distinct()

            res_mirna = Mirna.objects.filter( Q(mname__icontains=query) | \
                                        Q(mirbase_id__icontains=query)
                                        ).values_list('id',
                                                      'mirbase_id',
                                                      'mname').distinct()

            res_lncrna = Lncrna.objects.filter( Q(lname__icontains=query) | \
                                                Q(lsymbol__icontains=query) | \
                                                Q(lalias__icontains=query) | \
                                                Q(lgeneid__icontains=query)
                                        ).values_list('id',
                                                      'lsymbol',
                                                      'lgeneid',
                                                      'lname',
                                                      'lalias').distinct()
            res_pirna = Pirna.objects.filter( Q(pname__icontains=query) | \
                                              Q(palias__icontains=query) | \
                                              Q(paccession__icontains=query)
                                        ).values_list('id',
                                                      'palias',
                                                      'pname',
                                                      'paccession').distinct()

            context["search_target"] = res_target
            context["search_mirna"] = res_mirna
            context["search_lncrna"] = res_lncrna
            context["search_pirna"] = res_pirna
            context["search_results"] = len(res_target) + len(res_mirna) + len(res_lncrna) + len(res_pirna)
            cat_num = 0
            for res in [res_target, res_mirna, res_lncrna, res_pirna]:
                if len(res) > 0:
                    cat_num += 1
            context["search_cat"] = cat_num
            
        else:
            context["search_term"] = "No term entered."
            context["search_results"] = 0
            
        return render(request, 'irndb2/search.html', context)
    # if not GET method return homepage
    else:
        return render(request, "irndb2/home.html", context)

def home_method(request):
    context = {}
    context['tnum'] = Target.objects.count()
    context['mnum'] = Mirna.objects.count()
    context['lnum'] = Lncrna.objects.count()
    context['pnum'] = Pirna.objects.count()
    return render(request, "irndb2/home.html", context)

def contact_method(request):
    context = {}
    return render(request, "irndb2/contact.html", context)

def target_method(request, sym):
    context = {}
    a = Target.objects.filter(symbol__regex=r'^%s$'%sym) # exact match, kind of a hack as the __exact did not work
    if len(a)>1:
        context["error"] = 'Query "%s" resulted in more then 1 entitiy.'%sym
        return render(request, "irndb2/404.html", context)
    elif len(a)==0:
        context["error"] = 'Query "%s" resulted in 0 entities.'%sym
        return render(request, "irndb2/404.html", context)
    else:
        obj = a[0]
    
    return render(request, "irndb2/target.html", context)

def mirna_method(request, name):
    context = {}
    a = Mirna.objects.filter(mname__regex=r'^%s$'%name) # exact match, kind of a hack as the __exact did not work
    if len(a)>1:
        context["error"] = 'Query "%s" resulted in more then 1 entitiy.'%name
        return render(request, "irndb2/404.html", context)
    elif len(a)==0:
        context["error"] = 'Query "%s" resulted in 0 entities.'%name
        return render(request, "irndb2/404.html", context)
    else:
        obj = a[0]
    
    return render(request, "irndb2/mirna.html", context)

def lncrna_method(request, sym):
    context = {}
    a = Lncrna.objects.filter(lsymbol__regex=r'^%s$'%sym) # exact match, kind of a hack as the __exact did not work
    if len(a)>1:
        context["error"] = 'Query "%s" resulted in more then 1 entitiy.'%sym
        return render(request, "irndb2/404.html", context)
    elif len(a)==0:
        context["error"] = 'Query "%s" resulted in 0 entities.'%sym
        return render(request, "irndb2/404.html", context)
    else:
        obj = a[0]
    
    return render(request, "irndb2/lncrna.html", context)

def pirna_method(request, name):
    context = {}
    a = Pirna.objects.filter(pname__regex=r'^%s$'%name) # exact match, kind of a hack as the __exact did not work
    if len(a)>1:
        context["error"] = 'Query "%s" resulted in more then 1 entitiy.'%name
        return render(request, "irndb2/404.html", context)
    elif len(a)==0:
        context["error"] = 'Query "%s" resulted in 0 entities.'%name
        return render(request, "irndb2/404.html", context)
    else:
        obj = a[0]
    return render(request, "irndb2/pirna.html", context)


def doc_method(request):
    context = {}
    sTab = request.GET.get('tab', 'x')
    context = {}
    if sTab not in ['1','2','3','4']:
        return render(request, "irndb2/doc.html", context)
    elif sTab == '1':
        return render(request, "irndb2/doc_overview.html", context)
    elif sTab == '2':
        return render(request, "irndb2/doc_desc.html", context)
    elif sTab == '3':
        return render(request, "irndb2/doc_resources.html", context)
    elif sTab == '4':
        # fetch stats from db
        num_m2t_exp_mmuhsa = M2T_EXP.objects.filter(target__strict__gt=-1).values_list('mirna_id', 'target_id').distinct().count()
        num_m_exp_mmuhsa = M2T_EXP.objects.filter(target__strict__gt=-1).values_list('mirna_id').distinct().count()
        num_t_exp_mmuhsa = M2T_EXP.objects.filter(target__strict__gt=-1).values_list('target_id').distinct().count()

        num_m2t_exp_mmu = M2T_EXP.objects.filter(target__strict = 1).values_list('mirna_id', 'target_id').distinct().count()
        num_m_exp_mmu = M2T_EXP.objects.filter(target__strict = 1).values_list('mirna_id').distinct().count()
        num_t_exp_mmu = M2T_EXP.objects.filter(target__strict = 1).values_list('target_id').distinct().count()


        num_m2t_pred_mmuhsa = M2T_PRED.objects.filter(target__strict__gt=-1).values_list('mirna_id', 'target_id').distinct().count()
        num_m_pred_mmuhsa = M2T_PRED.objects.filter(target__strict__gt=-1).values_list('mirna_id').distinct().count()
        num_t_pred_mmuhsa = M2T_PRED.objects.filter(target__strict__gt=-1).values_list('target_id').distinct().count()

        num_m2t_pred_mmu = M2T_PRED.objects.filter(target__strict = 1).values_list('mirna_id', 'target_id').distinct().count()
        num_m_pred_mmu = M2T_PRED.objects.filter(target__strict = 1).values_list('mirna_id').distinct().count()
        num_t_pred_mmu =M2T_PRED.objects.filter(target__strict = 1).values_list('target_id').distinct().count()

        num_l2t_mmu = L2T.objects.filter(target__strict = 1).values_list('lncrna_id','target_id').distinct().count()
        num_l2t_mmuhsa =  L2T.objects.filter(target__strict__gt = -1).values_list('lncrna_id','target_id').distinct().count()

        num_l2t_pirna_mmu = L2T.objects.filter(target__strict = 1).values_list('lncrna_id').distinct().count()
        num_l2t_pirna_mmuhsa =  L2T.objects.filter(target__strict__gt = -1).values_list('lncrna_id').distinct().count()

        num_l2t_target_mmu = L2T.objects.filter(target__strict = 1).values_list('target_id').distinct().count()
        num_l2t_target_mmuhsa =  L2T.objects.filter(target__strict__gt = -1).values_list('target_id').distinct().count()


        num_p2t_mmu = P2T.objects.filter(target__strict = 1).values_list('pirna_id','target_id').distinct().count()
        num_p2t_mmuhsa = P2T.objects.filter(target__strict__gt = -1).values_list('pirna_id','target_id').distinct().count()


        num_p2t_pirna_mmu = P2T.objects.filter(target__strict = 1).values_list('pirna_id',).distinct().count()
        num_p2t_pirna_mmuhsa = P2T.objects.filter(target__strict__gt = -1).values_list('pirna_id').distinct().count()


        num_p2t_target_mmu = P2T.objects.filter(target__strict = 1).values_list('target_id').distinct().count()
        num_p2t_target_mmuhsa = P2T.objects.filter(target__strict__gt = -1).values_list('target_id').distinct().count()


        context = {
                   'num_m2t_exp_mmuhsa':num_m2t_exp_mmuhsa,
                   'num_m_exp_mmuhsa':num_m_exp_mmuhsa,
                   'num_t_exp_mmuhsa':num_t_exp_mmuhsa,
                   'num_m2t_exp_mmu':num_m2t_exp_mmu,
                   'num_m_exp_mmu':num_m_exp_mmu,
                   'num_t_exp_mmu':num_t_exp_mmu,
                   'num_m2t_pred_mmuhsa':num_m2t_pred_mmuhsa,
                   'num_m_pred_mmuhsa':num_m_pred_mmuhsa,
                   'num_t_pred_mmuhsa':num_t_pred_mmuhsa,
                   'num_m2t_pred_mmu':num_m2t_pred_mmu,
                   'num_m_pred_mmu':num_m_pred_mmu,
                   'num_t_pred_mmu':num_t_pred_mmu,
                   'num_l2t_mmu': num_l2t_mmu,
                   'num_l2t_mmuhsa': num_l2t_mmuhsa,
                   'num_l2t_pirna_mmu':num_l2t_pirna_mmu,
                   'num_l2t_pirna_mmuhsa':num_l2t_pirna_mmuhsa,
                   'num_l2t_target_mmu':num_l2t_target_mmu,
                   'num_l2t_target_mmuhsa':num_l2t_target_mmuhsa,
                   'num_p2t_mmu': num_p2t_mmu,
                   'num_p2t_mmuhsa': num_p2t_mmuhsa,
                   'num_p2t_pirna_mmu':num_p2t_pirna_mmu,
                   'num_p2t_pirna_mmuhsa':num_p2t_pirna_mmuhsa,
                   'num_p2t_target_mmu':num_p2t_target_mmu,
                   'num_p2t_target_mmuhsa':num_p2t_target_mmuhsa
                   }

        return render(request, "irndb2/doc_stats.html", context)
    else:
        return render(request, "irndb2/doc.html", context)

def browse_method(request):
    dnl = request.GET.get('dnl', '0')
    filename = request.GET.get('f','data.csv')
    
    entitytype = request.GET.get('type', 'x')
    context = {}
    if entitytype == 'mirna':
        query_set = Mirna.objects.filter(num_immune__gt=0).distinct()
        if dnl == '1':  # download instead of display
            data = create_data_mirna(query_set, 0)
            data = [['Name',
                     'ID',
                     'NumExperimentalMouseImmuneTargets',
                     'NumPredictedMouseImmuneTargets',
                     'NumExperimentalHumanInferredImmuneTargets',
                     'NumPredictedHumanInferredImmuneTargets']] + data
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="%s"' % filename
            writer = csv.writer(response)
            for row in data:
                writer.writerow(row)
            return response
        else:  # no download
            context['data'] = create_data_mirna(query_set, 1)
            return render(request, "irndb2/browse_mirna.html", context)
    
    elif entitytype == 'target':
        query_set = Target.objects.all().distinct()
        if dnl == '1':  # download instead of display
            data = create_data_targets(query_set, 0)
            data = [['symbol', 'name', 'geneid', 'ImmuneRelevanceInferredFrom', 'num_exp_miRNA', 'num_pred_miRNA', 'num_lncRNA', 'num_piRNA']] + data
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="%s"' % filename
            writer = csv.writer(response)
            for row in data:
                writer.writerow(row)
            return response
        else:  # no download
            context['data'] = create_data_targets(query_set)
            return render(request, "irndb2/browse_target.html", context)
    
    elif entitytype == 'lncrna':
        query_set = Lncrna.objects.all().distinct()
        if dnl == '1':  # download instead of display
            data = create_data_lncrna(query_set, 0)
            data = [['symbol', 'name', 'alias',  'NumMouseInferredImmuneTargets',
                     'NumHumanInferredImmuneTargets']] + data
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="%s"' % filename
            writer = csv.writer(response)
            for row in data:
                writer.writerow(row)
            return response
        else:  # no download
            context['data'] = create_data_lncrna(query_set)
            return render(request, "irndb2/browse_lncrna.html", context)
    elif entitytype == 'pirna':
        query_set = Pirna.objects.all().distinct()
        aQS = P2T.objects.all().select_related('pirna', 'target')
        
        if dnl == '1':  # download instead of display
            data = create_data_pirna(query_set, 0)
            data = [['name', 'alias', 'accession',  'NumMouseInferredImmuneTargets',
                     'NumHumanInferredImmuneTargets']] + data
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="%s"' % filename
            writer = csv.writer(response)
            for row in data:
                writer.writerow(row)
            return response
        else:
            context['data'] = create_data_pirna(query_set)
            return render(request, "irndb2/browse_pirna.html", context)
    else:
        return render(request, "irndb2/home.html", context)

def browse_pw_method(request):
    context = {}
    entitytype = request.GET.get('type', 'x')
    context = {}
    if entitytype == 'mirna':
        return render(request, "irndb2/browse_pw_mirna.html", context)
    elif entitytype == 'target':
        return render(request, "irndb2/browse_pw_target.html", context)
    elif entitytype == 'lncrna':
        return render(request, "irndb2/browse_pw_lncrna.html", context)
    elif entitytype == 'pirna':
        return render(request, "irndb2/browse_pw_pirna.html", context)
    else:
        return render(request, "irndb2/home.html", context)
    
def tables_method(request):
    context = {}
    return render(request, "irndb2/tables.html", context)

def charts_method(request):
    context = {}
    return render(request, "irndb2/charts.html", context)


#----------------------------------------------------------------
# NON-VIEW methods
#----------------------------------------------------------------
def create_data_pirna(aList, links=1):
    data = []
    for e in aList:
        alias = ', '.join(e.palias.split(','))
        acc_str = ', '.join(e.paccession.split(','))
        if links==1:
            name_str = '<a class="m1" href="" title="Link to IRNdb piRNA entry">%s</a>' % (e.pname)
            acc_str = '<a class="m1" href="http://www.ncbi.nlm.nih.gov/nuccore/%s" title="Link to NCBI">%s</a>' % (e.paccession, acc_str)
        else:
            name_str = e.lname
            
        aTemp = [
            name_str,
            alias,
            acc_str,
            e.num_targets_mmu,
            e.num_targets_hsa
            ]
        a = [str(s) for s in aTemp]
        data.append(a)
    return data

def create_data_lncrna(aList, links=1):
    data = []
    for e in aList:
        num_immune_hsa  = e.num_immune - e.num_immune_strict
        alias = ', '.join(e.lalias.split(','))

        if links==1:
            symbol_str = '<a class="m1" href="" title="Link to IRNdb lncRNA entry">%s</a>' % (e.lsymbol)
            name_str = '<a class="m1" href="%s" title="Link to NCBI gene">%s</a>' % (e.llink, e.lname)
            alias_str = '<a class="m1" href="%s" title="Link to NCBI gene">%s</a>' % (e.llink, alias)
        else:
            symbol_str = e.lsymbol
            name_str = e.lname
            alias_str = alias
        aTemp = [
            symbol_str,
            name_str,
            alias_str,
            e.num_immune_strict,
            num_immune_hsa
            ]
        a = [str(s) for s in aTemp]
        data.append(a)
    return data

def create_data_targets(aList, links=1):
    data = []
    for e in aList:
       
        # symbol, name, geneid, species, num_exp_mirna, num_pred_mirna, num_lncrna, num_piRNA
        if links==1:
            symbol_str = '<a class="t1" href="" title="Link to IRNdb target entry">%s</a>' % (e.symbol)
            name_str = '<a class="t1" href="http://www.ncbi.nlm.nih.gov/gene/%s" title="Link to NCBI gene">%s</a>' % (e.id, e.tname)
            geneid_str = '<a class="t1" href="http://www.ncbi.nlm.nih.gov/gene/%s" title="Link to NCBI gene">%s</a>' % (e.id, e.id)
        else:
            symbol_str = e.symbol
            name_str = e.tname
            geneid_str = e.id

        if e.strict == 1:
            species = 'mouse'
        else:
            species = 'human'
        aTemp = [
            symbol_str,
            name_str,
            geneid_str,
            species,
            e.num_mirnas_exp,
            e.num_mirnas_pred,
            e.num_lncrnas,
            e.num_pirnas
            ]
        a = [str(s) for s in aTemp]
        data.append(a)
    return data


def create_data_mirna(aList, links=1):
    data = []
    for e in aList:
        e.num_exp_hsa  = e.num_immune_exp - e.num_immune_strict_exp # verified targets with immune relevance inferred from humans.
        e.num_pred_mmu = e.num_immune_strict - e.num_immune_strict_exp
        e.num_pred_hsa = e.num_immune - e.num_pred_mmu - e.num_exp_hsa - e.num_immune_strict_exp  # predicted targets with immune relevance inferred from humans.
        if links==1:
            mirna_str = '<a class="m1" href="" title="IRN miRNA details">%s</a>' % (e.mname)
            mirnaid_str = '<a class="m1" href="http://mirbase.org/cgi-bin/mature.pl?mature_acc=%s" title="Open miRNA in mirBase">%s</a>' % (e.mirbase_id, e.mirbase_id)
        else:
            mirna_str = e.mname
            mirnaid_str = e.mirbase_id

        aTemp = [
            mirna_str,
            mirnaid_str,
            e.num_immune_strict_exp,
            e.num_pred_mmu,
            e.num_exp_hsa,
            e.num_pred_hsa
            ]
        a = [str(s) for s in aTemp]
        data.append(a)
    return data
