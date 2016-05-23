from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.db.models import Q, F, Count
import csv

from irndb2.models import Target, T2G, T2K, T2W, T2K, T2C7, Go, Kegg, Wikipath, Msigdb_c7, Mirna, M2T_EXP, M2T_PRED, Lncrna, L2T, Pirna, P2T # use db of irn2 needs changing to .models

# Create your views here.
def kegg_method(request, id):
    context = {}
    return render(request, "irndb2/contact.html", context)


def wp_method(request, id):
    context = {}
    return render(request, "irndb2/contact.html", context)


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
    context['num_target'] = Target.objects.all().count()
    context['num_mirna'] = Mirna.objects.all().count()
    context['num_lncrna'] = Lncrna.objects.all().count()
    context['num_pirna'] = Pirna.objects.all().count()
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
    tab = request.GET.get('tab', 'x')
    context = {}
    if tab not in ['1','2','3','4']:
        return render(request, "irndb2/doc.html", context)
    elif tab == '1':
        return render(request, "irndb2/doc_overview.html", context)
    elif tab == '2':
        return render(request, "irndb2/doc_desc.html", context)
    elif tab == '3':
        return render(request, "irndb2/doc_resources.html", context)
    elif tab == '4':
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
    entitytype = request.GET.get('type', '0')
    pathway = request.GET.get('pw', '0')
    pathwaytype = request.GET.get('pwt', 'x')

    rnalink_template = '<a class="m1" href="/irndb/%s/%s">%s</a>' # rnatype, rnasymbol/name, symbol/name
    pwlink_template = '<a title="Open in IRNdb" class="g" href="/irndb/%s/%s">%s</a>' # pathwaytype, pwid, pwname
    targetlink_template = '<a title="Open in IRNdb" class="t1" href="/irndb/target/%s">%s</a>' # symbol, symbol 
    
    context = {}
    context["entity_type"] = entitytype
    context["pwt"] = pathwaytype
    if entitytype == 'mirna':
        context["rna_title"] = "miRNA"

        # download instead of display
        if dnl == '1' and pathway != '1':  
            query_set = Mirna.objects.filter(num_immune__gt=0).distinct()
            data = create_data_mirna(query_set, 0)
            response = create_dnl_response(filename, data, ['Name','ID','NumExperimentalMouseImmuneTargets','NumPredictedMouseImmuneTargets','NumExperimentalHumanInferredImmuneTargets','NumPredictedHumanInferredImmuneTargets'])
            return response
        
        # browse pathways instead --> return pathway list
        elif pathway == '1':
            if pathwaytype not in ["wikipathway","kegg"]:
                return render_to_response("irndb2/browsepw.html", context)
            else:
                # all t2l object
                rna2t_list = M2T_EXP.objects.all().select_related('mirna','target').distinct()
                #rna2t_list = M2T_EXP.objects.filter(target__strict = 1).select_related('mirna','target').distinct()
                if dnl == '1':
                    res_list = get_pathways(entitytype, pathwaytype, '1')
                    response = create_dnl_response(filename, res_list, ['Pathway_name', 'Pathway_id', 'Target', 'RNAs'])
                    return response
                else:
                    res_list = get_pathways(entitytype, pathwaytype, '0')
                    context["data"] = res_list
                    return render(request, "irndb2/browsepw_content.html", context)
                
        # no download --> browse mirnas
        else:  
            query_set = Mirna.objects.filter(num_immune__gt=0).distinct()
            context['data'] = create_data_mirna(query_set, 1)
            return render(request, "irndb2/browse_mirna.html", context)
    
    elif entitytype == 'target':
        if dnl == '1' and pathway != '1':  # download instead of display
            query_set = Target.objects.all().distinct()
            data = create_data_targets(query_set, 0)
            response = create_dnl_response(filename, data,['symbol', 'name', 'geneid', 'ImmuneRelevanceInferredFrom', 'num_exp_miRNA', 'num_pred_miRNA', 'num_lncRNA', 'num_piRNA'])
            return response
        else:  # no download
            query_set = Target.objects.all().distinct()
            context['data'] = create_data_targets(query_set)
            return render(request, "irndb2/browse_target.html", context)

    elif entitytype == 'lncrna':
        context["rna_title"] = "lncRNA"
        if dnl == '1' and pathway != '1':  # download instead of display
            query_set = Lncrna.objects.all().distinct()
            data = create_data_lncrna(query_set, 0)
            response = create_dnl_response(filename, data, ['symbol', 'name', 'alias',  'NumMouseInferredImmuneTargets', 'NumHumanInferredImmuneTargets'])
            return response
        
        # browse pathways instead --> return pathway list
        elif pathway == '1':
            if pathwaytype not in ["wikipathway","kegg"]:
                return render_to_response("irndb2/browsepw.html", context)
            else:
                # all t2l object
                rna2t_list = L2T.objects.all().select_related('lncrna','target').distinct()
                # get list of pathways
                if dnl == '1':
                    res_list = get_pathways(entitytype, pathwaytype, '1')
                    response = create_dnl_response(filename, res_list, ['Pathway_name', 'Pathway_id', 'Target', 'RNAs'])
                    return response
                else:
                    res_list = get_pathways(entitytype, pathwaytype, '0')
                    context["data"] = res_list
                    return render(request, "irndb2/browsepw_content.html", context)

            
        else:  # no download
            query_set = Lncrna.objects.all().distinct()
            context['data'] = create_data_lncrna(query_set)
            return render(request, "irndb2/browse_lncrna.html", context)

    elif entitytype == 'pirna':
        context["rna_title"] = "piRNA"
        aQS = P2T.objects.all().select_related('pirna', 'target')
        if dnl == '1' and pathway != '1':  # download instead of display
            query_set = Pirna.objects.all().distinct()
            data = create_data_pirna(query_set, 0)
            response = create_dnl_response(filename, data, ['name', 'alias', 'accession',  'NumMouseInferredImmuneTargets',
             'NumHumanInferredImmuneTargets'])
            return response
        
        # browse pathways instead --> return pathway list
        elif pathway == '1':
            if pathwaytype not in ["wikipathway","kegg"]:
                return render_to_response("irndb2/browsepw.html", context)
            else:
                rnasymbol = "pirna__pname"
                # get list of pathways
                if dnl == '1':
                    res_list = get_pathways(entitytype, pathwaytype, '1')
                    response = create_dnl_response(filename, res_list, ['Pathway_name', 'Pathway_id', 'Target', 'RNAs'])
                    return response
                else:
                    res_list = get_pathways(entitytype, pathwaytype, '0')
                    context["data"] = res_list
                    return render(request, "irndb2/browsepw_content.html", context)

        else:
            query_set = Pirna.objects.all().distinct()
            context['data'] = create_data_pirna(query_set)
            return render(request, "irndb2/browse_pirna.html", context)

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
def create_data_pirna(entity_list, links=1):
    data = []
    for e in entity_list:
        alias = ', '.join(e.palias.split(','))
        acc_str = ', '.join(e.paccession.split(','))
        if links==1:
            name_str = '<a class="m1" href="/irndb/pirna/%s" title="Link to IRNdb piRNA entry">%s</a>' % (e.pname, e.pname)
            acc_str = '<a class="m1" href="http://www.ncbi.nlm.nih.gov/nuccore/%s" title="Link to NCBI">%s</a>' % (e.paccession, acc_str)
        else:
            name_str = e.pname
            
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


def create_data_lncrna(entity_list, links=1):
    data = []
    for e in entity_list:
        num_immune_hsa  = e.num_immune - e.num_immune_strict
        alias = ', '.join(e.lalias.split(','))

        if links==1:
            symbol_str = '<a class="m1" href="/irndb/lncrna/%s" title="Link to IRNdb lncRNA entry">%s</a>' % (e.lsymbol, e.lsymbol)
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


def create_data_targets(entity_list, links=1):
    data = []
    for e in entity_list:
       
        # symbol, name, geneid, species, num_exp_mirna, num_pred_mirna, num_lncrna, num_piRNA
        if links==1:
            symbol_str = '<a class="t1" href="/irndb/target/%s" title="Link to IRNdb target entry">%s</a>' % (e.symbol, e.symbol)
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


def create_data_mirna(entity_list, links=1):
    data = []
    for e in entity_list:
        e.num_exp_hsa  = e.num_immune_exp - e.num_immune_strict_exp # verified targets with immune relevance inferred from humans.
        e.num_pred_mmu = e.num_immune_strict - e.num_immune_strict_exp
        e.num_pred_hsa = e.num_immune - e.num_pred_mmu - e.num_exp_hsa - e.num_immune_strict_exp  # predicted targets with immune relevance inferred from humans.
        if links==1:
            mirna_str = '<a class="m1" href="/irndb/mirna/%s" title="IRN miRNA details">%s</a>' % (e.mname, e.mname)
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


def create_dnl_response(filename, data, header):
    data = [header] + data
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="%s"' % filename
    writer = csv.writer(response)
    for row in data:
        writer.writerow(row)
    return response


def get_targets(entity_list, type):
    """ Return targets for a rna set """
    targets_exp, targets_pred = [], []
    if type == 'mirna':
        targets_exp  = M2T_EXP.objects.filter(mirna__in = entity_list).values('target').distinct()
        targets_pred = M2T_PRED.objects.filter(mirna__in = entity_list).values('target').distinct()
    elif type == 'lncrna':
        targets_exp = L2T.objects.filter(lncrna__in = entity_list).values('target').distinct()
        targets_pred = []
    elif type == 'pirna':
        targets_exp = P2T.objects.filter(pirna__in = entity_list).values('target').distinct()
        targets_pred = []
    return targets_exp, targets_pred


def get_pathways(entitytype, pathwaytype, dnl='0'):
    rnalink_template = '<a class="m1" href="/irndb/%s/%s">%s</a>' # rnatype, rnasymbol/name, symbol/name
    pwlink_template = '<a title="Open in IRNdb" class="g" href="/irndb/%s/%s">%s</a>' # pathwaytype, pwid, pwname
    targetlink_template = '<a title="Open in IRNdb" class="t1" href="/irndb/target/%s">%s</a>' # symbol, symbol 
  
    dPW = {}
    res_list = []
    if pathwaytype == 'kegg':
        if entitytype == 'pirna':
            t2pw_list = T2K.objects.filter(~Q(pirna = '0')).select_related('target', 'kegg').distinct()
        elif entitytype == 'lncrna':
            t2pw_list = T2K.objects.filter(~Q(lncrna = '0')).select_related('target', 'kegg').distinct()
        elif entitytype == 'mirna':
            t2pw_list = T2K.objects.filter(~Q(mirna_exp = '0')).select_related('target', 'kegg').distinct()

        for t2pw in t2pw_list:
            if t2pw.kegg not in dPW:
                dPW[t2pw.kegg] = []

            if dnl != '1':
                if entitytype == 'pirna':
                    rnas = '; '.join([str(rnalink_template % (entitytype,
                                                rna.strip(),
                                                rna.strip())) for rna in t2pw.pirna.split(',')])
                elif entitytype == 'lncrna':
                    rnas = '; '.join([str(rnalink_template % (entitytype,
                                                rna.strip(),
                                                rna.strip())) for rna in t2pw.lncrna.split(',')])
                elif entitytype == 'mirna':
                    rnas = '; '.join([str(rnalink_template % (entitytype,
                                                rna.strip(),
                                                rna.strip())) for rna in t2pw.mirna_exp.split(',')])


                dPW[t2pw.kegg].append([ str(targetlink_template % (t2pw.target.symbol,
                                                                   t2pw.target.symbol)),
                                                                   rnas])
            else:
                if entitytype == 'pirna':
                    rnas = str(t2pw.pirna)
                elif entitytype == 'lncrna':
                    rnas = str(t2pw.lncrna)
                elif entitytype == 'mirna': 
                    rnas = str(t2pw.mirna_exp)

                dPW[t2pw.kegg].append([ str(t2pw.target.symbol), rnas])

        for kegg, targetlist in dPW.items():
            if dnl != '1':
                targetlist.sort()
                str_table = '<table><tbody>'
                for t_entry in targetlist:
                    row_str = '<tr><td style="width:120px; vertical-align: top;">%s</td><td>%s</td></tr>' % (t_entry[0], t_entry[1])
                    str_table += row_str
                str_table += '</tbody></table>'
                res_list.append([str(pwlink_template % (pathwaytype, str(kegg.keggid), str(kegg.keggname))), str_table])
            else:
                # here make one row per target
                for tlist in targetlist:
                    res_list.append([str(kegg.keggname), str(kegg.keggid), tlist[0], tlist[1]])
        
    elif pathwaytype == 'wikipathway':
        if entitytype == 'pirna':
            t2pw_list = T2W.objects.filter(~Q(pirna = '0')).select_related('target', 'wikipath').distinct()
        elif entitytype == 'lncrna':
            t2pw_list = T2W.objects.filter(~Q(lncrna = '0')).select_related('target', 'wikipath').distinct()
        elif entitytype == 'mirna':
            t2pw_list = T2W.objects.filter(~Q(mirna_exp = '0')).select_related('target', 'wikipath').distinct()

        for t2pw in t2pw_list:
            if t2pw.wikipath not in dPW:
                dPW[t2pw.wikipath] = []

            if dnl != '1':
                if entitytype == 'pirna':
                    rnas = '; '.join([str(rnalink_template % (entitytype,
                                                rna.strip(),
                                                rna.strip())) for rna in t2pw.pirna.split(',')])
                elif entitytype == 'lncrna':
                    rnas = '; '.join([str(rnalink_template % (entitytype,
                                                rna.strip(),
                                                rna.strip())) for rna in t2pw.lncrna.split(',')])
                elif entitytype == 'mirna':
                    rnas = '; '.join([str(rnalink_template % (entitytype,
                                                rna.strip(),
                                                rna.strip())) for rna in t2pw.mirna_exp.split(',')])


                dPW[t2pw.wikipath].append([ str(targetlink_template % (t2pw.target.symbol,
                                                                   t2pw.target.symbol)),
                                                                   rnas])
            else:
                if entitytype == 'pirna':
                    rnas = str(t2pw.pirna)
                elif entitytype == 'lncrna':
                    rnas = str(t2pw.lncrna)
                elif entitytype == 'mirna': 
                    rnas = str(t2pw.mirna_exp)

                dPW[t2pw.wikipath].append([ str(t2pw.target.symbol), rnas])

        for wp, targetlist in dPW.items():
            if dnl != '1':
                targetlist.sort()
                str_table = '<table><tbody>'
                for t_entry in targetlist:
                    row_str = '<tr><td style="width:120px; vertical-align: top;">%s</td><td>%s</td></tr>' % (t_entry[0], t_entry[1])
                    str_table += row_str
                str_table += '</tbody></table>'
                res_list.append([str(pwlink_template % (pathwaytype, str(wp.wikipathid), str(wp.wikipathname))), str_table])
            else:
                # here make one row per target
                for tlist in targetlist:
                    res_list.append([ str(wp.wikipathid), str(wp.wikipathname), tlist[0], tlist[1]])

    return res_list
