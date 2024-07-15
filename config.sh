# SPECOPTIONS="v7-stable v7-devel-cust v8-stable v8-stable-el7 v8-stable-el7-cn v8-devel2 v8-q-debug v8-stable-gt v8-stable-sb v8-stable-cs libestr libee libgt librelp json-c liblognorm liblognorm1 liblognorm2 liblognorm5 liblogging libksi libksi1 openpgm zeromq3 czmq libmongo-client python-docutils python-sphinx jemalloc gnutls libtasn1 nettle librdkafka libfastjson libfastjson4"
# REPOOPTIONS="v8-stable v8-stable-gt v8-stable-cs v8-stable-vs v8-stable-cn v8-stable-build v8-stable-daily testing"
ARCHOPTIONS="i386 x86_64"
PLATOPTIONS="epel-8 epel-9 rhel-7 rhel-8 rhel-9"
SPECOPTIONS="$(find ./rpmbuild/SPECS/ -type f -execdir bash -c 'printf "%s\n" "${@%.*}"' bash {} + | cut -c3-)"
REPOOPTIONS="$(find ./yumrepo/ -maxdepth 1 -type d -execdir bash -c 'printf "%s\n" "${@%}"' bash {} + | cut -c3-)"

szBaseDir=$(dirname "$0")
szRpmBaseDir=$(dirname "$0")/rpmbuild
szRpmBuildDir=$szRpmBaseDir/SRPMS
szYumRepoDir=$(dirname "$0")/yumrepo
szLocalUser=pkg
