# Definitions common to these scripts
source $(dirname "$0")/config.sh

#ALLREPOS="Yes"
#REPOOPTIONS="v5-stable v7-stable v8-stable v8-devel v8-devel2 v8-q-debug testing"
#ARCHOPTIONS="i386 x86_64"
#PLATOPTIONS="epel-5 epel-6" #"opensuse-11"

echo "-------------------------------------"
echo "--- Update Repos!                 ---"
echo "-------------------------------------"
echo "Choose Repos for updating?:"
select szRepos in $ALLREPOS $REPOOPTIONS
do
        case $szRepos in "Yes")
                szRepos=$REPOOPTIONS;
        esac
        echo "Updating Repos for '$szRepos'
        "
        break;
done

for rsyslogver in $szRepos
	do for distro in 5 6 7;
	do for arch in i386 x86_64;
	        do repo=$szYumRepoDir/$rsyslogver/epel-$distro/$arch;
		echo "Updating Repository: $repo"
                sudo rm $repo/repodata/repomd.xml.asc
                sudo chown $szLocalUser $repo/* -R
                rpm --resign $repo/RPMS/*.rpm
		sudo createrepo -q -s sha256 -o $repo -d -p $repo/RPMS/;
	        sudo gpg --detach-sign --armor $repo/repodata/repomd.xml
		done;
	done;
done

