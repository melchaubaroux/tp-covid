import numpy as np
import re 
   
#------------------------- fonction d'observation des donnees------------------------
    
def nb_props_label_info(tableau,colonne=0):
    
    """la fonction recupere liste des labels sur une feature (caracteristique)
        et leur proportion    
    
        Args:
        
            tableau(np.array): tableau dans lequel on recupere les donnees           
            colonne(int):  index correspondant a la feature souhaite 
           
            
        Return : 
             tag (dictionnaire numpy): recupere les resultats                             
    """
    
    nblig = tableau[:,1].size   #recupere les dimension
    nbcol = tableau[1,:].size   #du tableau
    
    # compte le nombre de label differents et leurs proprotion
    
    nombre_de_labels={}
    
    for ligne in range (nblig):
        if (type(tableau[ligne][colonne])!=str) and (np.isnan(tableau[ligne][colonne])==True) : 
            tableau[ligne][colonne]='nan'
        if tableau[ligne][colonne] not in nombre_de_labels :
             nombre_de_labels[tableau[ligne][colonne]]=1
        if tableau[ligne][colonne] in nombre_de_labels :
            nombre_de_labels[tableau[ligne][colonne]]+=1
            
    #calcul la proportion de donnee entre les differents labels
    
    proprotion_des_labels = {}
    
    for label in nombre_de_labels :   
        proprotion_des_labels[label]= round(nombre_de_labels[label]/nblig)
        
    #range tous cela dans le dictionnaire
    
    tag ={}
        
    for label in nombre_de_labels : 
        tag[label]=[nombre_de_labels[label],proprotion_des_labels[label]]     
          
    return tag      
    
    
    
    
def compteur_colonne(tableau,variable,nature=int):
    
    """la fonction  compte la presence d'une variable dans les colonnes
    
        Args:
        
            tableau(np.array): tableau dans lequel on recupere les donnees                     
            variable(int,float,str): la variable a observer            
            nature(int,float,str): permet de verifier le type de la variable a observer
           
            
        Return : 
                list_col(np.array) :recupere la valeur pour la colonne 
                index_col(np.array):recupere le numero de la colonne correspondante 
                                        
    """
        
    
    nblig = tableau[:,1].size   #recupere les dimension
    nbcol = tableau[1,:].size   #du tableau
    
    info=[]   # recupere la valeur pour la colonne 
    index=[]  # recupere le numero de la colonne correspondante  
    

    for col in range(nbcol):
        count=0
        for lig in range(nblig):
            if type(tableau[lig][col])==nature:
                if tableau[lig][col]==variable:
                    count+=1
        info.append(count-1)
        index.append(col)
                
    return info,index


def compteur_ligne(tableau,variable,nature=int):
    
    """la fonction  compte la presence d'une variable dans les lignes
    
        Args:
        
            tableau(np.array): tableau dans lequel on recupere les donnees                        
            variable(int,float,str): la variable a observer            
            nature(int,float,str): permet de verifier le type de la variable a observer
           
            
        Return : 
                list_lig(np.array):recupere la valeur pour la ligne
                index_lig(np.array):recupere le numero de la ligne correspondante 
                                        
    """   
    nblig = tableau[:,1].size   #recupere les dimension
    nbcol = tableau[1,:].size   #du tableau
    
    info=[]  #recupere la valeur pour la colonne 
    index=[] # recupere le numero de la ligne correspondante  
        
    for lig in range(nblig):
        count=0
        for col in range(nbcol):
            if type(tableau[lig][col])==nature:
                if tableau[lig][col]==variable:
                    count+=1
        info.append(count)
        index.append(lig)
        
        
    return info,index



def compteur_tableau (tableau,variable,nature=int):
    
    """la fonction  compte la presence d'une variable dans le tableau

    Args:

        tableau(np.array): tableau dans lequel on recupere les donnees   
        variable(int,float,str): la variable a observer
        nature(int,float,str): permet de verifier le type de la variable a observer


    Return : 
            tag(dictionnaire numpy): recupere les resultats

    """          
    # recupere les resultats des colonnes 
    
    resultat_colonne ={}  
    info_col,index_col=compteur_colonne(tableau,variable,nature=int)
    
    resultat_colonne ['index']=index_col
    resultat_colonne ['info']=info_col
             
    # recupere les resultats des lignes
     
    resultat_ligne ={}      
    info_lig,index_lig=compteur_ligne(tableau,variable,nature=int)
    
    resultat_ligne ['index']=index_lig
    resultat_ligne ['info']=info_lig
             
    # met tous cela dans un seul dictionnaire 
    
    tag = {'ligne':resultat_ligne,'colonne':resultat_colonne}
   
    return tag   




#-------------------------encodage + formatage------------------------
                                                       
def encodage (tableau):
    
    """la fonction encode les labels , supprime les nan, re-attribution des nombres enregistre sous forme de string,
        mise a zeros en cas d'echec
               
        Args:
        
            tableau(np.array): tableau dans lequel on recupere les donnees                 
         
         
        Return : 
                tableau
                                        
    """  
    
    nblig = tableau[:,1].size   #recupere les dimension
    nbcol = tableau[1,:].size   #du tableau
    
    
    for lig in range (0,nblig):                
        for col in range (0,nbcol):
            
            if type(tableau[lig][col])==str :  
                
                if tableau[lig][col]=="positive":                
                    tableau[lig][col]=1
                elif tableau[lig][col]=="detected":                
                    tableau[lig][col]=1
                elif tableau[lig][col]=="present":                
                    tableau[lig][col]=1    
                elif tableau[lig][col]=="nan":
                    tableau[lig][col]=0
                elif tableau[lig][col]=="not_detected":
                    tableau[lig][col]=0
                elif tableau[lig][col]=="negative":
                    tableau[lig][col]=0
            elif np.isnan(tableau[lig][col]) :                     
                tableau[lig][col]=0
                
                
                
    return tableau
    
#------------------------- fonction de suppression des donnees------------------------
                                                                                              
def suppr_col_vide (tableau,seuil=1) :
    
    """supprime les colonnes vide d'un tableau 

    Args:

        tableau(np.array):tableau dans lequel on recupere les donnees
        condition(int): default= 0, colonne de depart 
        seuil(int):  default= 1, la part de vide des colonnes a supprimer

    Return : 
            tableau(np.array): tableau- colonne vide a plus du seuil
            col_a_suppr(np.array):liste des colonnes supprime

    """
    
    nblig = tableau[:,1].size   #recupere les dimension
    nbcol = tableau[1,:].size   #du tableau 

    col_a_suppr = [] 
       
    for colonne in range (0,nbcol):
        count = 0
        for ligne in range (0,nblig) :
            if (tableau[ligne][colonne]==0):
                count = count +1 
        if  nblig*seuil <= count  :
            col_a_suppr.append(colonne)                         
    count=0
    for i in  range(len(col_a_suppr)-1,0,-1) :             # supprime les colonnes
        tableau=np.delete(tableau,(col_a_suppr[i]),1)
        
    return tableau



def suppr_lig_vide (tableau,seuil=1) :
    
    """supprime les lignes vides d'un tableau 

    Args:

        tableau(np.array): tableau dans lequel on recupere les donnees
        condition(int): default= 0, ligne  de depart 
        seuil(int):  default= 1, la part de vide des lignes a supprimer

    Return : 
            tableau(np.array): tableau - lignes vide a plus du seuil
            col_a_suppr(np.array):liste des colonnes supprime

    """
    
    nblig = tableau[:,1].size   #recupere les dimension
    nbcol = tableau[1,:].size   #du tableau
    
    lig_a_suppr = []  
    
    for ligne in range (0,nblig):
        count = 0
        for colonne in range (0,nbcol):
            if (tableau[ligne][colonne]) == 0 :
                count = count +1
        if  nbcol*seuil <= count :
            lig_a_suppr.append(ligne)
                
                
     
    for i in  range(len(lig_a_suppr)-1,0,-1) :  # supprime les lignes         
        tableau=np.delete(tableau,(lig_a_suppr[i]),0) 
       
    return tableau
        
        
#------------------------- fonction decoupage  --------------------------------

    
def separation_des_targets (tableau,colonne=0) :
    
    """ cree des 2 tableau positif et negatif pour dissocier les cibles afin de faire des comparaison
        statistique 

    Args:

        tableau(np.array): tableau dans lequel on recupere les donnees 
        colonne(int): default= 0, colonne cible 

    Return : 
           positif(np.array)
           negatif (np.array)
    """
    
    nblig=tableau[:,1].size     # recupere les dimensions des colonnes 
    nbcol=tableau[1,:].size     # recupere  les dimensions des lignes 
    
     
    positif=np.empty([0,nbcol])              
    negatif=np.empty([0,nbcol])              

    for lig in range (0,nblig): 
        if tableau[lig][0]==1 : 
            positif=np.r_[positif,[tableau[lig,:]]]                                   
        else:        
            negatif=np.r_[negatif,[tableau[lig,:]]]
            
    return positif,negatif



#------------------------- fonction de test statistique ------------------------        
        
        
def test_colonnes(tableau,fonction):
        
    """ test des fonctions d'etude statistique

    Args:

        tableau(np.array): tableau dans lequel on recupere les donnees
        fonction(np.array(str)): les differents tests a faire
      

    Return : 
           liste(np.array) resultat des tests 
           
    """
    nbcol = tableau[1,:].size 
    liste=[] 
    
    for x in range (0,nbcol) :
        try : 
            somme = eval('np.'+fonction+'(tableau[:,'+str(x)+'])')
            liste.append(somme)
        except:  
            print('fail at attempts',x)

    return liste
                
                
                
#------------------------- fonction d affichage ------------------------     

def affiche_lignes (tableau,lst_lig,seuil_start=0,seuil_stop=100) :
    nblig=tableau[:,1].size # recupere  dim col
    nbcol=tableau[1,:].size # recupere  dim lig
    
    
    for x in range(nblig):
        if ((lst_lig[x]/len(tableau[1,:]))*100) > seuil_start :
            if ((lst_lig[x]/len(tableau[1,:]))*100) < seuil_stop:
                message = "ligne {} \n donnee manquantes {}  soit {} % ".format(x,lst_lig[x],(lst_lig[x]/len(tableau[1,:]))*100)
                print (message)



def affiche_features(dictionnaire,titre,tableau):
    nblig=tableau[:,1].size      
    element ={}
    count=0
    for x in (dictionnaire['colonne']['index']):
        element[x]=dictionnaire['colonne']['info'][count]
        count+=1
    for k,v  in sorted(element.items(),key=lambda x: x[1]):
        print("%s: %s" % (round(v/nblig*100,2), titre[k]))                       
        
    return 

def affichage_label(tableau,titre) :
    
    """ affiches les differents labels en fonction de leur nature et nombre

    Args:

        tableau(np.array): tableau dans lequel on recupere les donnees
        titre(np.array): noms des colonnes des labels              

    Return : 
           None 
           
    """    
    nbcol=tableau[1,:].size # recupere  dim lig    
    label_info={}

    # utilise les noms comme cle 
    for x in range(nbcol):
        Tag={}
        label_info[titre[x]]=(nb_props_label_info(tableau,colonne= x))
    
    for labels in label_info :
        if len(label_info[labels])<10: 
            print(labels,'\n',label_info[labels],'\n')       

        else : 
            print(labels) 
            nb_info=0
            for label in label_info[labels]:
                if type(label)== str :
                    print(label,label_info[labels][label],end ='  ') 
                elif label==0:
                    print(label,label_info[labels][label],end ='  ')
                else:
                    nb_info += label_info[labels][label][0]                   
                    
            print('  nb_info  {} '.format(nb_info),'\n')      
            
    return 

