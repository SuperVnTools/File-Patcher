# File-Patcher
Creates pathces to files so you can make changes to a file and share them without sharing the entire file.

to use this program just run 
    py ./patch.py -h
you may have to use python instead of py.
if you are making a patch and it is taking a long time, just use the cpython version which is 2 times faster for some reason.
run
    py ./setup.py build_ext --inplace
and then you can run ./main.py instead of ./patch.py with all other syntax the same.
this requires installing cpython
    py -m pip install cpython
