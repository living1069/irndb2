    #-- create all tables from Models.py and migrate 
    python ../manage.py makemigrations irndb2
    python ../manage.py migrate    

    #-- fill database with data
    time python ../manage.py loaddata data/target.json
    time python ../manage.py loaddata data/kegg.json 
    time python ../manage.py loaddata data/t2k.json 
    time python ../manage.py loaddata data/wikipath.json 
    time python ../manage.py loaddata data/t2w.json 
    time python ../manage.py loaddata data/reactome.json		
    time python ../manage.py loaddata data/t2r.json	
    time python ../manage.py loaddata data/go.json 
    time python ../manage.py loaddata data/t2g.json 
    time python ../manage.py loaddata data/msigdb_c7.json
    time python ../manage.py loaddata data/t2c7.json

    time python ../manage.py loaddata data/mirna.json
    time python ../manage.py loaddata data/m2t_exp.json
    time python ../manage.py loaddata data/m2t_pred.json

    time python ../manage.py loaddata data/lncrna.json
    time python ../manage.py loaddata data/l2t.json    

    time python ../manage.py loaddata data/pirna.json
    time python ../manage.py loaddata data/p2t.json

    time python ../manage.py loaddata data/m2expr.json
    time python ../manage.py loaddata data/primary2mature.json
    time python ../manage.py loaddata data/primary2tfbs.json   


    
    #-- IF YOU CHANGE DB TABLES IN THE models.py RUN:
    python ../manage.py makemigrations
    python ../manage.py syncdb


    #-- store the data nicely
    gzip data/*.json

    #-- To collect all static content in on place for the testing and profction server do:
    python ../manage.py collectstatic

## TO DELETE TABLE CONTENTS
# paste in to a shell
# python manage.py shell

from irndb2.models import Target, T2G, T2W, T2K, T2C7, Go, Kegg, Wikipath, Msigdb_c7, Mirna, M2T_EXP, M2T_PRED, Lncrna, L2T, Pirna, P2T, T2R, Reactome

P2T.objects.all().delete()
T2C7.objects.all().delete()
T2K.objects.all().delete()
T2G.objects.all().delete()
T2W.objects.all().delete()
T2R.objects.all().delete()
L2T.objects.all().delete()
M2T_EXP.objects.all().delete()
M2T_PRED.objects.all().delete()

Target.objects.all().delete()
Lncrna.objects.all().delete()
Pirna.objects.all().delete()
Mirna.objects.all().delete()
Msigdb_c7.objects.all().delete()
Wikipath.objects.all().delete()
Go.objects.all().delete()
Kegg.objects.all().delete()
Reactome.objects.all().delete()
