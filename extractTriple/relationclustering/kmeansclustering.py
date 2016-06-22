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
from sklearn.metrics.pairwise import pairwise_distances_argmin
from relfeaturegen import RelFeatureGen
from sklearn.decomposition import TruncatedSVD
import codecs
from sklearn import preprocessing
from sklearn.neighbors import NearestNeighbors

#def kbtree(fileName,num_neighbors):
#    print 'load the data...'
#    X = np.loadtxt(fileName)
#    print 'end load the data'
#    tree = KDTree(X, leaf_size=2)
#    dist, ind = tree.query(X, k=200)
#    print 'stop'
    
    
if __name__=='__main__':
    dir_path = '../data/food/relation_result/data_split_1/'
    n_clusters = 500
    n_components=1500
    relf = RelFeatureGen()
    proSeedTrip = relf.proSeedTriple
    rel_dict,rel2Num = proSeedTrip.analyRel()
   
    rel_list  = rel_dict.keys()
    rel_to_id = { ch:i for i,ch in enumerate(rel_list) }        
    id_to_rel = { i:ch for i,ch in enumerate(rel_list) }
    rel_num = len(rel_list)
    
    f1 = open(dir_path+'rel2id.txt','w')
    for key in id_to_rel:
        f1.write(str(key)+'\t'+id_to_rel[key]+'\n')
    f1.close()
    
    rel_typesignature,sethastypeSig,set_miss_rel = relf.getRelTypeSig(rel_list,rel_to_id,id_to_rel)
    print 'relation num:', len(rel_to_id)
    rel_contFeature = relf.getRelContextFeature(rel_dict,rel_to_id,id_to_rel)
    print 'missing type signature relation',len(set_miss_rel)
    print 'transfer the feature into computable'
    
    X = rel_contFeature.tocsr()
    X = preprocessing.normalize(X, norm='l2')
    print 'start to TruncatedSVD'
    svd = TruncatedSVD(n_components=n_components, random_state=42)
    svd.fit(X)
    print 'TruncatedSVD end'
    print sum(svd.explained_variance_ratio_)

    #np.savetxt('svdVariance.txt',svd.explained_variance_ratio_,'%.4f')
   
    TruncatedSVD_X = svd.transform(X)
    latentfileName = dir_path+'latent_relation_allRel_'+str(n_components)+'.txt'
    np.savetxt(latentfileName,TruncatedSVD_X,'%.3f')
    
    print 'start to get the typesignature relation.....'
    rel_contFeature = rel_contFeature.tocsr()
    hasTypesig_rel_typesignature = rel_typesignature[sethastypeSig,:]
    hasTypesig_rel_contFeature = rel_contFeature[sethastypeSig,:]
    
    X = preprocessing.normalize(hasTypesig_rel_contFeature, norm='l2')
    print 'start to TruncatedSVD'
    svd = TruncatedSVD(n_components=n_components, random_state=42)
    svd.fit(X)
    print 'TruncatedSVD end'
    print sum(svd.explained_variance_ratio_)

    #np.savetxt('svdVariance.txt',svd.explained_variance_ratio_,'%.4f')
    TruncatedSVD_X = svd.transform(X)
    hasTypesig_rel_typesignature = preprocessing.normalize(hasTypesig_rel_typesignature, norm='l2')
    print 'after merge, start to TruncatedSVD'
    X = np.concatenate((hasTypesig_rel_typesignature.toarray(),TruncatedSVD_X),axis=1)
    X = csr_matrix(X)
    X = preprocessing.normalize(X, norm='l2')
    svd = TruncatedSVD(n_components=n_clusters, random_state=42)
    svd.fit(X)
    print sum(svd.explained_variance_ratio_)
    TruncatedSVD_X = svd.transform(X)
    
    max_indices =np.argmax(TruncatedSVD_X, axis=1)
    id2cluster = {}
    for i in range(len(sethastypeSig)):
        no = sethastypeSig[i]
        id2cluster[no] = max_indices[i]
        #print no
    print 'start to get nearest neighbors'
    X_latent_neigh = np.loadtxt(latentfileName)
    nbrs = NearestNeighbors(n_neighbors=10, algorithm='kd_tree').fit(X_latent_neigh)
    print 'end to get nearest neighbors'
    for key in set_miss_rel:
       # print 'set_miss_rel',key
        distances, indices = nbrs.kneighbors(X_latent_neigh[key:key+1])
        neighbors = indices
        indice_num = np.shape(neighbors)[1]
        neighbours = {}
        neighbours_no = 0
        for i in range(indice_num):
            ner = neighbors[0,i]
            temp = id2cluster.get(ner) 
            if temp !=None:
                id2cluster[key] = temp
                break
#                if neighbours.get(temp)!=None:
#                    neighbours[temp] = neighbours[temp] + 1
#                else:
#                    neighbours[temp] = 1
#                neighbours_no = neighbours_no + 1
#            if neighbours_no >=20:
#            #get the most populor type
#                neighbours = sorted(neighbours.items(), key=lambda d: d[1],reverse=True)
#                id2cluster[key] = neighbours[0][0]
#                break
    if len(id2cluster) == rel_num:
        print 'all the relations has the cluster ids'
        
    f1 = codecs.open(dir_path+'rel2clusterid_r'+str(n_clusters)+'_max'+'.txt','w','utf-8')
    for i in range(rel_num):
        cluster_no = id2cluster[i]
        f1.write(str(cluster_no)+'\n')
    f1.close()
    
#    
#    f1 = codecs.open(dir_path+'rel2id.txt','w','utf-8')
#    for key in id_to_rel:
#        f1.write(str(key)+'\t'+id_to_rel[key]+'\n')
#    f1.close()   

##    ##############################################################################
#    # Compute clustering with Means
    k_means = KMeans(init='k-means++', n_clusters=n_clusters, n_init=10)
    t0 = time.time()
    k_means.fit(TruncatedSVD_X)
    t_batch = time.time() - t0
    k_means_labels = k_means.labels_
    k_means_cluster_centers = k_means.cluster_centers_
    k_means_labels_unique = np.unique(k_means_labels)
    #may cost a lot of times
    #silmetric1 = metrics.silhouette_score(TruncatedSVD_X, k_means_labels)  
    #print("Silhouette Coefficient: %0.3f" % silmetric1)

#    ##############################################################################
#    # Compute clustering with MiniBatchKMeans
#    print 'start to clustering'
#    batch_size =200
#    mbk = MiniBatchKMeans(init='k-means++', n_clusters=n_clusters, batch_size=batch_size,
#                          n_init=10, max_no_improvement=10, verbose=0)
#    t0 = time.time()
#    mbk.fit(TruncatedSVD_X)
#    t_mini_batch = time.time() - t0
#    mbk_means_labels = mbk.labels_
#    mbk_means_cluster_centers = mbk.cluster_centers_
#    mbk_means_labels_unique = np.unique(mbk_means_labels)
#    #silmetric2 = metrics.silhouette_score(TruncatedSVD_X, mbk_means_labels)
#    #print("Silhouette Coefficient: %0.3f" % silmetric2)
#    #print mbk_means_cluster_centers
    
#    if silmetric1 >= silmetric2:
#        final_label = k_means_labels
#    else:
#    final_label  = mbk_means_labels
    final_label = k_means_labels
    #f1 = codecs.open(dir_path+'rel2clusterid_cluster'+str(n_clusters)+'_nontypesig.txt','w','utf-8')
    #此处需要用最近邻算法去获取没有typesig特征的relation
    id2cluster = {}
    for i in range(len(final_label)):
        no = sethastypeSig[i]
        id2cluster[no] = final_label[i]
    #relNeighbors = getRelNeighbors(latentfileName,200)
    for key in set_miss_rel:
        distances, indices = nbrs.kneighbors(X_latent_neigh[key:key+1])
        neighbors = indices
        indice_num = np.shape(neighbors)[1]
        neighbours = {}
        neighbours_no = 0
        for i in range(indice_num):
            ner = neighbors[0,i]
            temp = id2cluster.get(ner) 
            if temp !=None:
                id2cluster[key] = temp
                break
    if len(id2cluster) == rel_num:
        print 'all the relations has the cluster ids'
####################################################################################################################################
####################################################################################################################################    
    f1 = codecs.open(dir_path+'rel2clusterid_cluster'+str(n_clusters)+'.txt','w','utf-8')
    for i in range(rel_num):
        cluster_no = id2cluster[i]
        f1.write(str(cluster_no)+'\n')
    f1.close()
#    ##############################################################################
    # Plot result
    
#    fig = plt.figure(figsize=(8, 3))
#    fig.subplots_adjust(left=0.02, right=0.98, bottom=0.05, top=0.9)
#    colrange = range(0x000001,0xfffff0)
#    lent  = len(colrange)/n_clusters
#    colors=[]
#    tr = 0
#    for t in range(n_clusters):
#        tr = tr + lent
#        temp = str(hex(tr))
#        temp = temp.replace('0x','')
#        if len(temp)!=6:
#            temp = '#0'+temp
#        else:
#            temp = '#'+temp
#        colors.append(temp)
#    print colors
#    
#    # We want to have the same colors for the same cluster from the
    # MiniBatchKMeans and the KMeans algorithm. Let's pair the cluster centers per
    # closest one.
    
#    order = pairwise_distances_argmin(k_means_cluster_centers,
#                                      mbk_means_cluster_centers)
#    
#    X = TruncatedSVD_X[:,0:2]
#    # KMeans
#    ax = fig.add_subplot(1, 3, 1)
#    for k, col in zip(range(n_clusters), colors):
#        my_members = k_means_labels == k
#        cluster_center = k_means_cluster_centers[k]
#        ax.plot(X[my_members, 0], X[my_members, 1], 'w',
#                markerfacecolor=col, marker='.')
#        ax.plot(cluster_center[0], cluster_center[1], 'o', markerfacecolor=col,
#                markeredgecolor='k', markersize=6)
#    ax.set_title('KMeans')
#    ax.set_xticks(())
#    ax.set_yticks(())
#    plt.text(-3.5, 1.8,  'train time: %.2fs\ninertia: %f' % (
#        t_batch, k_means.inertia_))
#    
#    # MiniBatchKMeans
#    ax = fig.add_subplot(1, 3, 2)
#    for k, col in zip(range(n_clusters), colors):
#        my_members = mbk_means_labels == k
#        cluster_center = mbk_means_cluster_centers[order[k]]
#        ax.plot(X[my_members, 0], X[my_members, 1], 'w',
#                markerfacecolor=col, marker='.')
#        ax.plot(cluster_center[0], cluster_center[1], 'o', markerfacecolor=col,
#                markeredgecolor='k', markersize=6)
#    ax.set_title('MiniBatchKMeans')
#    ax.set_xticks(())
#    ax.set_yticks(())
#    plt.text(-3.5, 1.8, 'train time: %.2fs\ninertia: %f' %
#             (t_mini_batch, mbk.inertia_))
#    
#    # Initialise the different array to all False
#    different = (mbk_means_labels == 4)
#    ax = fig.add_subplot(1, 3, 3)
#    
#    for l in range(n_clusters):
#        different += ((k_means_labels == k) != (mbk_means_labels == order[k]))
#    
#    identic = np.logical_not(different)
#    ax.plot(X[identic, 0], X[identic, 1], 'w',
#            markerfacecolor='#bbbbbb', marker='.')
#    ax.plot(X[different, 0], X[different, 1], 'w',
#            markerfacecolor='m', marker='.')
#    ax.set_title('Difference')
#    ax.set_xticks(())
#    ax.set_yticks(())
#    
#    #plt.show()
#    plt.savefig('test_nyt.png')
