TLDIR="twinlisp"
mkdir $TLDIR
cp -r core $TLDIR/
cp -r tests $TLDIR/
cp -r dist-packages $TLDIR/
cp -r site-packages $TLDIR/
cp *.twl $TLDIR/
cp *.txt $TLDIR/
echo "Translating core files"
tlisp -t $TLDIR/*.twl
tlisp -t $TLDIR/core/*.twl
tar cfz $TLDIR.tar.gz $TLDIR
rm -rf $TLDIR
echo "Done."
