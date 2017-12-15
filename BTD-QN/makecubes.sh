for i in "gas" "water"; do
        cd $i
        for file in `ls *PBE1PBE.fchk | sed 's/.fchk//g'`; do 
                echo $file
                echo "su" > file_cubeman_$file".dat"
                echo $file"_ex1.cube" >> file_cubeman_$file".dat"
                echo "yes" >> file_cubeman_$file".dat"
                echo $file"_gs.cube" >> file_cubeman_$file".dat"
                echo "yes" >> file_cubeman_$file".dat"
                echo $file"_diff.cube" >> file_cubeman_$file".dat"
                echo "yes" >> file_cubeman_$file".dat"
                echo "GS cubegen"
                cubegen 0 density=scf $file".fchk" $file"_gs.cube" 120 h
                echo "Ex1 cubegen"
                cubegen 0 density=ci $file".fchk" $file"_ex1.cube" 120 h
                echo "Orbitals cubegen"
                cubegen 0 mo=homo,lumo $file".fchk" $file"_orb.cube" 120 h
                echo "Cubman"
                cubman < file_cubeman_$file".dat"
        done
        cd ..
done