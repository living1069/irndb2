from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Mirna(models.Model):
    mname                 = models.CharField(max_length=32,
                                             blank=False,
                                             unique=True,
                                             db_index=True)
    mirbase_id            = models.CharField(max_length=14,
                                             blank=True,
                                             db_index=True)
    num_targets           = models.IntegerField(blank=False)
    num_targets_exp       = models.IntegerField(blank=False)
    num_immune_strict_exp = models.IntegerField(blank=False)
    num_immune_strict     = models.IntegerField(blank=False)
    num_immune_exp        = models.IntegerField(blank=False)
    num_immune            = models.IntegerField(blank=False)

class Target(models.Model):
    """"""
    symbol         = models.CharField(max_length=32, db_index=True, unique=True)
    tname          = models.CharField(max_length=150)
    immusources    = models.CharField(max_length=180)
    strict         = models.IntegerField(db_index=True)  # 0: human, 1: mouse (ansd potentially human))
    num_mirnas_pred = models.IntegerField()
    num_mirnas_exp = models.IntegerField()
    num_mirnas     = models.IntegerField()
    num_lncrnas  = models.IntegerField()
    num_pirnas = models.IntegerField()

class M2T_EXP(models.Model):
    target  = models.ForeignKey(Target)
    mirna   = models.ForeignKey(Mirna) 
    sources = models.CharField(max_length=128)

class M2T_PRED(models.Model):
    target  = models.ForeignKey(Target) 
    mirna   = models.ForeignKey(Mirna) 
    sources = models.CharField(max_length=128)
    numsources = models.IntegerField()

## TARGET ANNOTATION
class Wikipath(models.Model):
    wikipathid   = models.CharField(max_length=8, db_index=True)
    wikipathname = models.CharField(max_length=80)

class T2W(models.Model):
    target   = models.ForeignKey(Target)
    wikipath = models.ForeignKey(Wikipath)
    mirna_exp = models.CharField(max_length=700, db_index=True)
    mirna_pred = models.CharField(max_length=4000, db_index=True)
    lncrna = models.CharField(max_length=320, db_index=True)
    pirna = models.CharField(max_length=100, db_index=True)

class Kegg(models.Model):
    keggid   = models.CharField(max_length=20)
    keggname = models.CharField(max_length=80)

class T2K(models.Model):
    target = models.ForeignKey(Target) # Target gene id
    kegg   = models.ForeignKey(Kegg) # kegg
    mirna_exp = models.CharField(max_length=700, db_index=True)
    mirna_pred = models.CharField(max_length=4200, db_index=True)
    lncrna = models.CharField(max_length=250, db_index=True)
    pirna = models.CharField(max_length=100, db_index=True)

class Go(models.Model):
    goid   = models.CharField(max_length=10, db_index=True)
    goname = models.CharField(max_length=200)
    gocat  = models.CharField(max_length=10, db_index=True)
    
class T2G(models.Model):
    target = models.ForeignKey(Target) # Target gene id
    go     = models.ForeignKey(Go)
    pmid   = models.CharField(max_length=600) # changed to Char from Integer
    mirna_exp = models.CharField(max_length=700, db_index=True)
    mirna_pred = models.CharField(max_length=5100, db_index=True)
    lncrna = models.CharField(max_length=320, db_index=True)
    pirna = models.CharField(max_length=100, db_index=True)
    
class Msigdb_c7(models.Model):
    geoid      = models.CharField(max_length=12)
    c7name     = models.CharField(max_length=90)
    c7expr     = models.CharField(max_length=2)
    c7url      = models.CharField(max_length=150)
    c7organism = models.CharField(max_length=16)
    c7pmid     = models.CharField(max_length=12)
    c7author   = models.CharField(max_length=30)
    c7desc     = models.CharField(max_length=256)

class T2C7(models.Model):
    target    = models.ForeignKey(Target) # Target gene id
    msigdb_c7 = models.ForeignKey(Msigdb_c7)
    
# OTHER NCRNAs
class Lncrna(models.Model):
    lsymbol     = models.CharField(max_length=24,
                                   blank=False,
                                   unique=True,
                                   db_index=True)
    lgeneid     = models.CharField(max_length=12)
    lname       = models.CharField(max_length=96)
    lalias      = models.CharField(max_length=96, db_index=True)
    llink       = models.CharField(max_length=64)
    num_immune_strict  = models.IntegerField()
    num_immune  = models.IntegerField()

class L2T(models.Model):
    lncrna         = models.ForeignKey(Lncrna) 
    target         = models.ForeignKey(Target)
    pmid           = models.CharField(max_length=64)
    source         = models.CharField(max_length=64)

class Pirna(models.Model):
    pname = models.CharField(max_length=16,
                             blank=False,
                             unique=True,
                             db_index=True)
    palias = models.CharField(max_length=64,
                              db_index=True)
    paccession = models.CharField(max_length=64,
                                  db_index=True)
    pseq = models.CharField(max_length=64)
    pspecies = models.IntegerField()
    ppmid = models.CharField(max_length=128)
    num_targets_mmu = models.IntegerField()
    num_targets_hsa = models.IntegerField()

class P2T(models.Model):
    pirna = models.ForeignKey(Pirna) 
    target = models.ForeignKey(Target)
    experimenttype = models.CharField(max_length=32, db_index=True)
    verified =  models.CharField(max_length=1, db_index=True)
    pmid = models.CharField(max_length=12)

class M2EXPR(models.Model):
    mirbase_id  = models.CharField(max_length=14,
                                   db_index=True)
    celltype = models.CharField(max_length=64)
    exprfreq = models.FloatField()
