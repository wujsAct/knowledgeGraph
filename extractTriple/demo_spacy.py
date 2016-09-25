from spacy.en import English

nlp = English()
#doc = nlp(u'''Popovich earlier admitted some feelings of awkwardness , having also served as a mentor to Avery Johnson .''')
doc = nlp(u'''2077	The event 's sponsors include the Chamber of Commerce ; FWD.us , a political action group founded by Mark Zuckerberg , the creator of Facebook ; the National Immigration Forum ; and the Partnership for a New American Economy , which is led by Mayor Michael R. Bloomberg of New York , Rupert Murdoch and Bill Marriott Jr.	DT NN NN NNS VBP DT NNP IN NNP : NNP , DT JJ NN NN VBN IN NNP NNP , DT NN IN NNP : DT NNP NNP NNP : CC DT NNP IN DT NNP NNP NNP , WDT VBZ VBN IN NNP NNP NNP NNP IN NNP NNP , NNP NNP CC NNP NNP NNP	B-NP I-NP I-NP I-NP B-VP B-NP I-NP B-PP B-NP O B-NP O B-NP I-NP I-NP I-NP B-VP B-PP B-NP I-NP O B-NP I-NP B-PP B-NP O B-NP I-NP I-NP I-NP O O B-NP I-NP B-PP B-NP I-NP I-NP I-NP O B-NP B-VP I-VP B-PP B-NP I-NP I-NP I-NP B-PP B-NP I-NP O B-NP I-NP O B-NP I-NP I-NP''')
i =0

for sentence in doc.sents:
    print i,'\t',sentence.text
    i = i + 1
    t = {token.idx:i for i,token in enumerate(sentence)}
    dep_triple = []
    for token in sentence:
        print token.tag_
        print token.pos_
        temp = []
        temp.append([token.orth_,t[token.idx]])
        temp.append(nlp.vocab.strings[token.dep])
        temp.append([token.head.orth_,t[token.head.idx]])
        dep_triple.append(temp)
        print temp

#
###use the knn to find the nearest neighbors
##from sklearn.neighbors import NearestNeighbors
##import numpy as np
##
##X = np.loadtxt('relationclustering/latent_relation.txt')
##nbrs = NearestNeighbors(n_neighbors=10, algorithm='ball_tree').fit(X)
##distances, indices = nbrs.kneighbors(X)
##print indices[0]
##print distances[0]
