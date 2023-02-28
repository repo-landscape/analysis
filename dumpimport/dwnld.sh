#!/bin/bash

##########
# Downdloads compressed OpenAIRE data dump from Zenodo
#
# The Zenodo resource id can be optionally provided as a first parameter
# (if not, 6616871 is assumed) although it's likely that other resources
# have slightly different internal structure and the download will (partially)
# fail for them.
##########

RECORD="$1"
RECORD=${RECORD:=7488618}
curl -L https://zenodo.org/record/$RECORD/files/communities_infrastructures.tar?download=1 | tar -x
curl -L https://zenodo.org/record/$RECORD/files/dataset_1.tar?download=1 | tar -x
curl -L https://zenodo.org/record/$RECORD/files/dataset_2.tar?download=1 | tar -x
curl -L https://zenodo.org/record/$RECORD/files/datasource.tar?download=1 | tar -x
curl -L https://zenodo.org/record/$RECORD/files/organization.tar?download=1 | tar -x
curl -L https://zenodo.org/record/$RECORD/files/otheresearchproduct.tar?download=1 | tar -x
curl -L https://zenodo.org/record/$RECORD/files/project.tar?download=1 | tar -x
curl -L https://zenodo.org/record/$RECORD/files/publication_1.tar?download=1 | tar -x
curl -L https://zenodo.org/record/$RECORD/files/publication_2.tar?download=1 | tar -x
curl -L https://zenodo.org/record/$RECORD/files/publication_3.tar?download=1 | tar -x
curl -L https://zenodo.org/record/$RECORD/files/publication_4.tar?download=1 | tar -x
curl -L https://zenodo.org/record/$RECORD/files/publication_5.tar?download=1 | tar -x
curl -L https://zenodo.org/record/$RECORD/files/publication_6.tar?download=1 | tar -x
curl -L https://zenodo.org/record/$RECORD/files/publication_7.tar?download=1 | tar -x
curl -L https://zenodo.org/record/$RECORD/files/publication_8.tar?download=1 | tar -x
curl -L https://zenodo.org/record/$RECORD/files/publication_9.tar?download=1 | tar -x
curl -L https://zenodo.org/record/$RECORD/files/publication_10.tar?download=1 | tar -x
curl -L https://zenodo.org/record/$RECORD/files/publication_11.tar?download=1 | tar -x
curl -L https://zenodo.org/record/$RECORD/files/relation_1.tar?download=1 | tar -x
curl -L https://zenodo.org/record/$RECORD/files/relation_2.tar?download=1 | tar -x
curl -L https://zenodo.org/record/$RECORD/files/relation_3.tar?download=1 | tar -x
curl -L https://zenodo.org/record/$RECORD/files/relation_4.tar?download=1 | tar -x
curl -L https://zenodo.org/record/$RECORD/files/relation_5.tar?download=1 | tar -x
curl -L https://zenodo.org/record/$RECORD/files/relation_6.tar?download=1 | tar -x
curl -L https://zenodo.org/record/$RECORD/files/relation_7.tar?download=1 | tar -x
curl -L https://zenodo.org/record/$RECORD/files/relation_8.tar?download=1 | tar -x
curl -L https://zenodo.org/record/$RECORD/files/relation_9.tar?download=1 | tar -x
curl -L https://zenodo.org/record/$RECORD/files/relation_10.tar?download=1 | tar -x
curl -L https://zenodo.org/record/$RECORD/files/software.tar?download=1 | tar -x
