
SEMVERMGR="./semvermanager/semvermgr.py"
VERSION_FILES=
help:
	@echo "Pick a release type by looking at the Makefile"

patch:
	python ${SEMVERMGR} --bump patch  setup.py semvermanager/semvermanager.py semvermanager/semvermgr.py
	python ${SEMVERMGR} --bump patch  --label release docs/conf.py

minor:
	python ${SEMVERMGR} --bump minor  setup.py semvermanager/semvermanager.py semvermanager/semvermgr.py
	python ${SEMVERMGR} --bump minor  --label release docs/conf.py

major:
	python ${SEMVERMGR} --bump major  setup.py semvermanager/semvermanager.py semvermanager/semvermgr.py
	python ${SEMVERMGR} --bump major  --label release docs/conf.py

tag:
	python ${SEMVERMGR} --bump tag  setup.py semvermanager/semvermanager.py semvermanager/semvermgr.py
	python ${SEMVERMGR} --bump tag  --label release docs/conf.py

tag_version:
	python3 semvermanager/semvermgr.py --bump tag_version setup.py semvermanager/semvermgr.py
	python3 semvermanager/semvermgr.py --bump tag_version --label release docs/conf.py

test_semvermgr:
	python ${SEMVERMGR} --make --overwrite tests/TMP_VERSION
	rm tests/TMP_VERSION
	
test: test_semvermgr
	python3 setup.py test

push:
	git add -u
	git commit -m"WIP"
	git push

release: test
	git add -u
	git commit -m"Checkin for release to pypi"
	python3 setup.py upload

init:
	keyring set https://test.pypi.org/legacy/ jdrumgoole
	keyring set https://upload.pypi.org/legacy/ jdrumgoole
