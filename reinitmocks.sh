for distro in 5 6 7;
do for arch in i386 x86_64;
        do repo=/home/makerpm/yumrepo/$distro/$arch;
	sudo mock -r epel-$distro-$arch --clean
	sudo mock -r epel-$distro-$arch --init
        done;
done


