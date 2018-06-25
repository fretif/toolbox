#/bin/bash

while true; do 
        echo "SYMPHONIE rename configuration tool"
	echo "'$1' to '$2'" 
	read -p "Are you sure to rename this configuration ?" yn
        case $yn in
		[Yy]* )
grep -rl --exclude=\*.{nc,exe,tmp,GRAPHIQUES,o,mod} $1 configuration_V2015/* | xargs sed -i 's/\/'$1'\//\/'$2'\//g'
grep -rl --exclude=\*.{nc,exe,tmp,GRAPHIQUES,o,mod} $1 configuration_V2015/* | xargs sed -i 's/'$1'$/'$2'/g'
			break;;
		[Nn]* ) exit 1 ;;
		*) echo "Please answer yes or no." ;;
	esac
done

