echo "RPM Packagename:"
read szRpm

for distro in 5 6;
do for arch in i386 x86_64;
	do repo=/home/makerpm/yumrepo/v7-stable/epel-$distro/$arch;
	szDirLibEstr=`ls $repo/RPMS/$szRpm*${arch/i386/i686}.rpm`
	sudo mock -r epel-$distro-$arch --install $szDirLibEstr
        done;
done

