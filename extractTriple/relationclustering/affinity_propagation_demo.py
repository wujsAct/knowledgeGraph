# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 19:57:43 2016

@author: DELL
"""

from sklearn.cluster import AffinityPropagation
from sklearn import metrics
#from sklearn.datasets.samples_generator import make_blobs
from relfeaturegen import RelFeatureGen
from sklearn.decomposition import TruncatedSVD
import numpy as np
from scipy.sparse import csr_matrix

if __name__=='__main__':
    relf = RelFeatureGen()
    proSeedTrip = relf.proSeedTriple
    rel_dict = proSeedTrip.analyRel()
    rel_list  = rel_dict.keys()
    rel_to_id = { ch:i for i,ch in enumerate(rel_list) }        
    id_to_rel = { i:ch for i,ch in enumerate(rel_list) }
    rel_typesignature = relf.getRelTypeSig(rel_list,rel_to_id)
    rel_contFeature = relf.getRelContextFeature(rel_dict,rel_to_id,id_to_rel)
    print 'transfer the feature into computable'
    
    #直接merge然后再降维感觉不行呢！
    #先将rel_contFeature.toarray(),降维然后咱们在merge吧！
    #X = np.concatenate((rel_typesignature.toarray(),rel_contFeature.toarray()),axis=1)
    #X = csr_matrix(X)
    
    X = rel_contFeature.tocsr()
    
    print 'start to TruncatedSVD'
    svd = TruncatedSVD(n_components=50, random_state=42)
    
    svd.fit(X)
    
    print 'TruncatedSVD end'
    
    print svd.explained_variance_ratio_

    
    TruncatedSVD_X = svd.transform(X)
    
    print 'after merge, start to TruncatedSVD'
    X = np.concatenate((rel_typesignature.toarray(),TruncatedSVD_X),axis=1)
    X = csr_matrix(X)
    svd = TruncatedSVD(n_components=2, random_state=42)
    svd.fit(X)
    TruncatedSVD_X = svd.transform(X)
    
    print 'start to clustering'
    #Compute Affinity Propagation
    af = AffinityPropagation(preference=-50).fit(TruncatedSVD_X)
    cluster_center_indices = af.cluster_centers_indices_
    labels =af.labels_

    n_cluters_ = len(cluster_center_indices)
    print('Estimated number of clusters: %d' %n_cluters_)
    #print('Homogeneity: %0.3f' %metrics.homogeneity_score(labels_true,labels))

    print('Silhouette Coefficient: %0.3f'  %metrics.silhouette_score(TruncatedSVD_X,labels,metric='sqeuclidean'))

    #plot result
    import matplotlib.pyplot as plt
    from itertools import cycle
    
    plt.close('all')
    plt.figure(1)
    plt.clf()
#    colrange = range(0x000001,0xfffff0)
#    lent  = len(colrange)/n_cluters_
#    colors=[]
#    tr = 0
#    for t in range(n_cluters_):
#        tr = tr + lent
#        temp = str(hex(tr))
#        temp = temp.replace('0x','')
#        if len(temp)!=6:
#            temp = '#0'+temp
#        else:
#            temp = '#'+temp
#        colors.append(temp)
#    print colors
    
    colors = cycle('bgrcmykbgrcmykbgrcmykbgrcmyk')
    X = TruncatedSVD_X[:,0:2]
    for k, col in zip(range(n_cluters_),colors):
        class_members = labels ==k
        cluster_center = X[cluster_center_indices[k]]
        plt.plot(X[class_members,0],X[class_members,1],col+'.')
        plt.plot(cluster_center[0],cluster_center[1],'o',markerfacecolor=col,
                 markeredgecolor='k',markersize=14)
        for x in X[class_members]:
            plt.plot([cluster_center[0],x[0]],[cluster_center[1],x[1]],col)
    plt.title('Estimated number of clusters: %d' %n_cluters_)
    #plt.show()
    plt.savefig('test_affinity.png')