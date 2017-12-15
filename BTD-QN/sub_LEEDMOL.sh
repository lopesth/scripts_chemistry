for dir in gas water; do
	cd $dir
	for file in `ls *.com | tr '\n' ' ' | sed 's/.com//g'`; do
		echo $file
		g09 $file".com" > $file".log"
	done
	cd ..
done
