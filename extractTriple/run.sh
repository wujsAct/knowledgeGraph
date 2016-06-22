#!/bin/sh

#step1
dir_path="/storage1/wujs/entity/data/food"
if [ ! -d "${dir_path}/intermediate" ]; then
  mkdir ${dir_path}/intermediate
fi

#cd utils/;python getAllSpecialSymbosInText.py ${dir_path} yelp_sample50k.txt symbols.txt deletes.txt;cd ../

#step2
#pay attention to how to merge the dependecy parser tag and pos tag!
#cd main1;python generateTag.py ${dir_path} yelp_sample50k.txt_new > ${dir_path}/w2tag.txt;cd ..

#generate the NER tags 

#step4
#cd utils;python getPureSetence.py ${dir_path} w2tag.txt w2tag2E_crf.txt yelp_final.txt;cd ..

#step4-2
#python SetencePro.py ${dir_path}/ yelp_final.txt > ${dir_path}/extract_triple.txt

#step5 get the domain type schema
#cd main1;python filterFreebaseFoodType.py; cd ..

#step6
#cd main1;python filter_knowEntityTriple.py ${dir_path}/ yelp_enthasName_type.txt_new extract_triple.txt> ${dir_path}/ftri.txt ;cd ..
#cd main1;python filter_knowEntityTriple.py ${dir_path}/ yelp_enthasName_type.txt_new extract_triple_entRent.txt> ${dir_path}/ftri_entRent.txt ;cd ..
#step7 generate type2num
#cd main1;python analysisEntAndRel.py;cd ..

#step8 we need to split the entity to training data and test data

#relation clustering
cd relationclustering; python kmeansclustering.py; cd ..
