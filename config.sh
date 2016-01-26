SPECOPTIONS="v5-stable v6-stable v7-stable v7-devel-cust v8-stable libestr libee libgt librelp json-c liblognorm liblognorm1 liblognorm2 liblogging libksi libksi1 openpgm zeromq3 czmq libmongo-client python-docutils python-sphinx jemalloc gnutls libtasn1 nettle librdkafka libfastjson"
REPOOPTIONS="v5-stable v7-stable v8-stable testing"
ARCHOPTIONS="i386 x86_64"
PLATOPTIONS="epel-5 epel-6 epel-7" #"opensuse-11"

szBaseDir=$(dirname "$0")
szRpmBaseDir=$(dirname "$0")/rpmbuild
szRpmBuildDir=$szRpmBaseDir/SRPMS
szYumRepoDir=$(dirname "$0")/yumrepo
szLocalUser=makerpm 
