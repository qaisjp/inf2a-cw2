expected=expected.$1.txt
#echo $expected
cat input.$1.txt | tee /dev/stderr | python semantics.py | diff $expected -
