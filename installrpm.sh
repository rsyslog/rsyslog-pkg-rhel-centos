echo "RPM Packagename:"
read szRpm

for distro in 5 6;
do for arch in i386 x86_64;
	do repo=/home/makerpm/yumrepo/$distro/$arch;
	sudo mock -r epel-$distro-$arch --install $szRpm
	done;
done

