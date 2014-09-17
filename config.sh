SPECOPTIONS="v5-stable v6-stable v7-stable v7-devel v7-devel-cust v8-stable v8-devel libestr libee libgt librelp json-c liblognorm liblognorm1 liblogging openpgm zeromq3 czmq libmongo-client python-docutils python-sphinx jemalloc gnutls libtasn1 nettle"
REPOOPTIONS="v5-stable v7-stable v8-stable v8-devel testing"
ARCHOPTIONS="i386 x86_64"
PLATOPTIONS="epel-5 epel-6 epel-7" #"opensuse-11"

szRpmBaseDir=$(dirname "$0")/rpmbuild
szRpmBuildDir=$szRpmBaseDir/SRPMS
szYumRepoDir=$(dirname "$0")/yumrepo


