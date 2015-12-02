#!/bin/sh

# make folder $2
mkdir -p $2

# read package list from $1 and link stuff into $2 from "cache"
for package in `cat $1`
do
	ln `pwd`/cache/$package $2/ 1> /dev/null 2>&1
	# if [ $? -ne 0 ]
	# then
		# echo "[-] cache doesn't have $package"
	# fi

done

# make $2 a repository
if [ ! -f "comps.xml" ]
then
	echo "did you forget to link the desired 'comps' file to comps.xml?"
	exit -1
fi

pushd $2
createrepo -g ../comps.xml --update .
popd

# convert "template.cfg" into proper mock config file
cache="`pwd`/$2"
cat template.cfg | sed "s%PLACEHOLDER1%\"$2\"%" | sed "s%PLACEHOLDER2%$cache%" > ${2}.cfg

echo -en "\n[+] use ${2}.cfg with mock :-)"
