SPECOPTIONS="v5-stable v6-stable v7-stable v7-devel-cust v8-stable v8-stable-el7 v8-devel2 v8-q-debug v8-stable-gt v8-stable-sb v8-stable-cs libestr libee libgt librelp json-c liblognorm liblognorm1 liblognorm2 liblognorm5 liblogging libksi libksi1 openpgm zeromq3 czmq libmongo-client python-docutils python-sphinx jemalloc gnutls libtasn1 nettle librdkafka libfastjson libfastjson4"
REPOOPTIONS="v5-stable v7-stable v8-stable v8-devel2 v8-q-debug v8-stable-gt v8-stable-cs v8-stable-sb testing"
ARCHOPTIONS="i386 x86_64"
PLATOPTIONS="epel-6 epel-7" #epel-5 "opensuse-11"

szBaseDir=$(dirname "$0")
szRpmBaseDir=$(dirname "$0")/rpmbuild
szRpmBuildDir=$szRpmBaseDir/SRPMS
szYumRepoDir=$(dirname "$0")/yumrepo
szLocalUser=test
