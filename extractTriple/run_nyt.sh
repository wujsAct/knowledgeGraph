#!/bin/sh

#step1
dir_path="/storage1/wujs/entity/data/nyt"
if [ ! -d "${dir_path}/intermediate" ]; then
  mkdir ${dir_path}/intermediate
fi

#cd utils/;python getAllSpecialSymbosInText.py ${dir_path} nyt13_sample10k.txt symbols.txt deletes.txt;cd ../

#step2
#pay attention to how to merge the dependecy parser tag and pos tag!
#cd main1;python generateTag.py ${dir_path} nyt13_sample10k.txt_new > ${dir_path}/w2tag.txt;cd ..

#generate the NER tags 

#step4
#cd utils;python getPureSetence.py ${dir_path} w2tag.txt w2tag2E_crf.txt nyt_final.txt;cd ..

#step4-2
#python SetencePro_1.py ${dir_path}/ nyt_final.txt > ${dir_path}/extract_triple.txt

#step4-3 get the domain type schema
#cd main1;python filterFreebaseFoodType.py; cd ..
#pay attention:分领域进行type extract
#cd data/nyt;cat multidata/location/location_enthasName_type.txt_new multidata/organization/organization_enthasName_type.txt_new multidata/people/people_enthasName_type.txt_new >nyt_enthasName_type.txt_new;cd ../../
#cd data/nyt;cat multidata/location/location_mintype2populortype.txt  multidata/organization/organization_mintype2populortype.txt multidata/people/people_mintype2populortype.txt >nyt_mintype2populortype.tx;cd ../../

#step 5-1
#cd main1;python filter_knowEntityTriple.py ${dir_path}/ nyt_enthasName_type.txt_new extract_triple.txt>  ${dir_path}/ftri.txt ;cd ..


#step 5-2
#cd main1;python analysisEntAndRel.py;cd ..

#relation clustering
cd relationclustering; python kmeansclustering_1.py;cd ..

#generate the 