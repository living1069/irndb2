    #-- create all tables from Models.py and migrate 
    python ../manage.py makemigrations irndb2
    python ../manage.py migrate    

    #-- fill database with data
    time python ../manage.py loaddata ../../temp/DJANGODATA4/irndb2/target.json
    time python ../manage.py loaddata ../../temp/DJANGODATA4/irndb2/kegg.json 
    time python ../manage.py loaddata ../../temp/DJANGODATA4/irndb2/t2k.json 
    time python ../manage.py loaddata ../../temp/DJANGODATA4/irndb2/wikipath.json 
    time python ../manage.py loaddata ../../temp/DJANGODATA4/irndb2/t2w.json 
    time python ../manage.py loaddata ../../temp/DJANGODATA4/irndb2/go.json 
    time python ../manage.py loaddata ../../temp/DJANGODATA4/irndb2/t2g.json 
    time python ../manage.py loaddata ../../temp/DJANGODATA4/irndb2/msigdb_c7.json
    time python ../manage.py loaddata ../../temp/DJANGODATA4/irndb2/t2c7.json

    time python ../manage.py loaddata ../../temp/DJANGODATA4/irndb2/mirna.json
    time python ../manage.py loaddata ../../temp/DJANGODATA4/irndb2/m2t_exp.json
    time python ../manage.py loaddata ../../temp/DJANGODATA4/irndb2/m2t_pred.json

    #time python ../manage.py loaddata ../../temp/DJANGODATA4/irndb2/mprimary.json   
    #time python ../manage.py loaddata ../../temp/DJANGODATA4/irndb2/mprimary2tfbs.json   

    time python ../manage.py loaddata ../../temp/DJANGODATA4/irndb2/lncrna.json
    time python ../manage.py loaddata ../../temp/DJANGODATA4/irndb2/l2t.json    

    time python ../manage.py loaddata ../../temp/DJANGODATA4/irndb2/pirna.json
    time python ../manage.py loaddata ../../temp/DJANGODATA4/irndb2/p2t.json
    
    #-- IF YOU CHANGE DB TABLES IN THE models.py RUN:
    python ../manage.py makemigrations
    python ../manage.py syncdb


    #-- store the data nicely
    gzip ../../temp/DJANGODATA4/irndb2/*.json

    #-- To collect all static content in on place for the testing and profction server do:
    python ../manage.py collectstatic

## TO DELETE TABLE CONTENTS
# paste in to a shell
# python manage.py shell

from irndb2.models import Target, T2G, T2W, T2K, T2C7, Go, Kegg, Wikipath, Msigdb_c7, Mirna, M2T_EXP, M2T_PRED, Lncrna, L2T, Pirna, P2T # use db of irn2 needs changing to .models

P2T.objects.all().delete()
T2C7.objects.all().delete()
T2K.objects.all().delete()
T2G.objects.all().delete()
T2W.objects.all().delete()
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
