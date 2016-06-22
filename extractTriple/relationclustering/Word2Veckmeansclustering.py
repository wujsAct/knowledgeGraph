# -*- coding: utf-8 -*-
#!/usr/bin/env python
"""
Created on Wed Mar 23 10:19:43 2016

@author: DELL
"""
import time

import numpy as np
import matplotlib.pyplot as plt
from scipy.sparse import csr_matrix
from sklearn import metrics
from sklearn.cluster import MiniBatchKMeans, KMeans
from relfeaturegen import RelFeatureGen
from sklearn.metrics.pairwise import pairwise_distances_argmin
from sklearn.decomposition import TruncatedSVD
import codecs
from sklearn.decomposition import PCA
from sklearn import preprocessing
import sys
if __name__=='__main__':
    if len(sys.argv) !=2:
        print 'usage: python pyfile n_cluter'
        exit(1)
        
    n_clusters = int(sys.argv[1])
    relf = RelFeatureGen()
    proSeedTrip = relf.proSeedTriple
    rel_dict = proSeedTrip.analyRel()
    rel_list  = rel_dict.keys()
    rel_to_id = { ch:i for i,ch in enumerate(rel_list) }        
    id_to_rel = { i:ch for i,ch in enumerate(rel_list) }
    rel_typesignature = relf.getRelTypeSig(rel_list,rel_to_id)
    rel_contFeature = relf.getRelContextFeature(rel_dict,rel_to_id,id_to_rel)
    
    X = rel_contFeature.tocsr()
    X_normalized = preprocessing.normalize(X, norm='l2')
    print 'start to TruncatedSVD'
    svd = TruncatedSVD(n_components=100, random_state=42)
    
    svd.fit(X_normalized)
    
    print 'TruncatedSVD end'
    
    print svd.explained_variance_ratio_

    
    TruncatedSVD_X = svd.transform(X_normalized)
        
    
    
    
    dir_path ='../data/food/'
    print 'load features'
    rel_w2v_feature = np.loadtxt('../relVec.txt')
    rel_w2v_feature = preprocessing.normalize(rel_w2v_feature, norm='l2')
    X = np.concatenate((TruncatedSVD_X,rel_w2v_feature),axis=1)
    X = preprocessing.normalize(X, norm='l2')
    pca = PCA(n_components=30)
    print 'start to PCA'
    
    pca.fit(X)
    
    print 'PCA end'
    
    print pca.explained_variance_ratio_
    print pca.explained_variance_
    pca_X = pca.transform(X)


    X = np.concatenate((rel_typesignature.toarray(),pca_X),axis=1)
    X = preprocessing.normalize(X, norm='l2')
    pca = PCA(n_components=10)
    print 'start to PCA'
    
    pca.fit(X)
    
    print 'PCA end'
    
    print pca.explained_variance_ratio_
    print pca.explained_variance_
    pca_X = pca.transform(X)
    
    print 'start to clustering ......'
    ##############################################################################
    # Compute clustering with Means
    
    k_means = KMeans(init='k-means++', n_clusters=n_clusters, n_init=20)
    t0 = time.time()
    k_means.fit(pca_X)
    t_batch = time.time() - t0
    k_means_labels = k_means.labels_
    k_means_cluster_centers = k_means.cluster_centers_
    k_means_labels_unique = np.unique(k_means_labels)
    silmetric1 = metrics.silhouette_score(pca_X, k_means_labels)  
    print("Silhouette Coefficient: %0.3f" % silmetric1)
    
    
#    f1 = codecs.open('../data/yelp_food_full/rel2id.txt','w','utf-8')
#    for key in id_to_rel:
#        f1.write(str(key)+'\t'+id_to_rel[key]+'\n')
#    f1.close()
    
    f1 = codecs.open(dir_path+'rel2clusterid.txt','w','utf-8')
    for key in k_means_labels:
        f1.write(str(key)+'\n')
    f1.close()
    ##############################################################################
    # Plot result
    
    fig = plt.figure(figsize=(8, 3))
    fig.subplots_adjust(left=0.02, right=0.98, bottom=0.05, top=0.9)
    colrange = range(0x000001,0xfffff0)
    lent  = len(colrange)/n_clusters
    colors=[]
    tr = 0
    for t in range(n_clusters):
        tr = tr + lent
        temp = str(hex(tr))
        temp = temp.replace('0x','')
        if len(temp)!=6:
            temp = '#0'+temp
        else:
            temp = '#'+temp
        colors.append(temp)
    print colors
    
    # We want to have the same colors for the same cluster from the
    # MiniBatchKMeans and the KMeans algorithm. Let's pair the cluster centers per
    # closest one.
    
    X = pca_X[:,0:2]
    # KMeans
    ax = fig.add_subplot(1, 1, 1)
    for k, col in zip(range(n_clusters), colors):
        my_members = k_means_labels == k
        cluster_center = k_means_cluster_centers[k]
        ax.plot(X[my_members, 0], X[my_members, 1], 'w',
                markerfacecolor=col, marker='.')
        ax.plot(cluster_center[0], cluster_center[1], 'o', markerfacecolor=col,
                markeredgecolor='k', markersize=6)
    ax.set_title('KMeans')
    ax.set_xticks(())
    ax.set_yticks(())
    plt.text(-3.5, 1.8,  'train time: %.2fs\ninertia: %f' % (
        t_batch, k_means.inertia_))
    
    #plt.show()
    plt.savefig('test.png')
    sys.exit(silmetric1)
