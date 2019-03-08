#!/bin/bash

# You need to generate an access token https://github.com/settings/tokens
# repo:status and public_repo

GH_USER=FILLME
TOKEN=FILLME
TIMEOUT=5
PER_PAGE=10000
OUTPUT=repos.json
ORG=FILLME

curl \
       	--connect-timeout ${TIMEOUT} \
       	--compressed \
       	-sS \
	-u "${GH_USER}:${TOKEN}" \
       	-o ${OUTPUT} \
       	"https://api.github.com/orgs/${ORG}/repos?per_page=${PER_PAGE}"
