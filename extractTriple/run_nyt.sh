#!/bin/sh

dir_path="/storage1/wujs/entity/data/nyt"
if [ ! -d "${dir_path}/intermediate" ]; then
  mkdir ${dir_path}/intermediate
fi

:<<!
step1:
data preprocessing: delete the special symbol
!
#cd utils/;python getAllSpecialSymbosInText.py ${dir_path} nyt13_sample10k.txt symbols.txt deletes.txt;cd ../

:<<!
step2: generate the word's tag
!
#cd main1;python generateTag.py ${dir_path} nyt13_sample10k.txt_new > ${dir_path}/w2tag.txt;cd ..

:<<!
step3: sequence learning to recognize the entity phrase and relation phrase with CRF model
!
#generate the NER tags 


:<<!
step4: Triple extraction
step4-1 merge the tag and sentence information
step4-2 relation and entity statisitic(to extract popular and meaningful mentions)
attetion: entity pattern statistic based on the extracted relation
step4-3 utilize spacy to generate the dependecy parse!
step4-4 utilize Reverb-DP to extract (ent1,rel,ent2)triples
!
#cd utils;python getPureSetence.py ${dir_path} w2tag.txt w2tag2E_crf.txt nyt_final.txt;cd ..

#python relStatistic.py ${dir_path}/ nyt_final.txt

#python entStatistic.py ${dir_path}/ nyt_final.txt

#python generateDT.py ${dir_path}/ nyt_final.txt

python SetencePro_1.py ${dir_path}/ nyt_final.txt extract_triple.txt


:<<!
step5: extract entity and triples information from Freebase within a domain.
!
#get the domain type schema
#cd main1;python filterFreebaseFoodType.py; cd ..
#pay attention:分领域进行type extract
#cd data/nyt;cat multidata/location/location_enthasName_type.txt_new multidata/organization/organization_enthasName_type.txt_new multidata/people/people_enthasName_type.txt_new >nyt_enthasName_type.txt_new;cd ../../

:<<!
step6: extract seed triples!
!
#cd main1;python filter_knowEntityTriple.py ${dir_path}/ nyt_enthasName_type.txt_new extract_triple.txt>  ${dir_path}/ftri.txt ;cd ..