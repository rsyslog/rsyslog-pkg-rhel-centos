source $(dirname "$0")/config.sh
arch=x86_64;

for distro in $PLATOPTIONS; do
	sudo mock -r $distro-$arch --clean
	sudo mock -r $distro-$arch --init
done;


