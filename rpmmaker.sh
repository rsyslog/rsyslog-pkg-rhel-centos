
SPECOPTIONS="v5-stable v6-stable v7-stable v7-devel v7-devel-cust v8-stable v8-devel libestr libee libgt librelp json-c liblognorm liblognorm1 liblogging openpgm zeromq3 czmq libmongo-client python-docutils jemalloc gnutls libtasn1 nettle"
# util-linux popt udev gobject-introspection python db4 util-linux"
REPOOPTIONS="v5-stable v6-stable v7-stable v7-devel v8-stable v8-devel testing"
ARCHOPTIONS="i386 x86_64"				   
PLATOPTIONS="epel-5 epel-6" #"opensuse-11"


echo "-------------------------------------"
echo "--- RPMMaker                      ---"
echo "-------------------------------------"
echo "SPEC Filebasename?"
select szSpec in $SPECOPTIONS
do
	echo "Making RPM for '$szSpec.spec'
	"
	break;
done

echo "Which Linux Plattform?:"
select szDist in $PLATOPTIONS "All"
do
	case $szDist in "All")
		szDist=$PLATOPTIONS;
	esac
	echo "Making RPM for EPEL '$szDist'
	"
        break;
done

echo "Which Architecture?:"
select szArch in $ARCHOPTIONS "All"
do
	case $szArch in "All")
		szArch=$ARCHOPTIONS;
	esac
	echo "Making RPM for Plattforms '$szArch'
	"
        break;
done

echo "Which YUM repository?":
select szSubRepo in $REPOOPTIONS
do
        break;
done

szRpmBuildDir=/home/makerpm/rpmbuild/SRPMS/
	
	for distro in $szDist;
	do for arch in $szArch;
        do repo=/home/makerpm/yumrepo/$szSubRepo/$distro/$arch;
                echo "Making Source RPM for '$szSpec.spec' - $distro-$arch"
		sudo mock -r $distro-$arch --buildsrpm --spec /home/makerpm/rpmbuild/SPECS/$szSpec.spec --sources /home/makerpm/rpmbuild/SOURCES
                szSrcDirFile=`ls /var/lib/mock/$distro-$arch/result/*src.rpm`
		szSrcFile=`basename $szSrcDirFile`
                echo "Makeing RPMs from sourcefile '$szSrcDirFile'"
                sudo mv $szSrcDirFile $szRpmBuildDir
		sudo mock -r $distro-$arch $szRpmBuildDir$szSrcFile;
                chown makerpm /var/lib/mock/$distro-$arch/result/*.rpm
		sudo rpm --addsign /var/lib/mock/$distro-$arch/result/*.rpm
		sudo mv /var/lib/mock/$distro-$arch/result/*rpm $repo/RPMS/;
                echo "Moving RPMs to $repo"
		sudo createrepo -q -s sha -o $repo -d -p $repo;
                sudo rm $repo/repodata/repomd.xml.asc
                sudo gpg --passphrase-file passfile.txt --detach-sign --armor $repo/repodata/repomd.xml
        done;
	done;
exit;
