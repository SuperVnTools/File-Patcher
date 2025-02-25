# File-Patcher
Creates pathces to files so you can make changes to a file and share them without sharing the entire file.

to use this program just run 
```console
foo@bar:~$ py ./patch.py -h
usage: filepatcher [-h] [-s SIZE] -i INPUT [-o OUTPUT] -p PATCH -m MODE [-c CHANGED]

Patches files

options:
  -h, --help            show this help message and exit
  -s SIZE, --size SIZE  size of int in bytes to store in the patch. 4 is default. If you need to make a patch for a
                        file of more than 4GB you should use a larger number. Using a number larger than 8 is
                        pointless
  -i INPUT, --input INPUT
                        filepath of base file to patch/make a patch for. required
  -o OUTPUT, --output OUTPUT
                        filepath of output file. only used in patch mode
  -p PATCH, --patch PATCH
                        filepath of the patch file. required for both modes
  -m MODE, --mode MODE  patch or write_patch modes. patch mode patches the input file -i using patch file -o and
                        writes the new file into file -o
  -c CHANGED, --changed CHANGED
                        path for the changed file. only used in write_patch mode. path of the file you want to make a
                        patch of -i for. using patch, -i will turn into -c

example usage
py ./main.py -i input.txt -c turnsintothis.txt -p patchtochangeinput.bin -m make_patch
py ./main.py -i input.txt -p patchtochangeinput.bin -o copyofturnsintothis.txt -m patch
```
you may have to use python instead of py.
if you are making a patch and it is taking a long time, just use the cpython version which is 2 times faster for some reason.
run
```console
foo@bar:~$ py ./setup.py build_ext --inplace
```
and then you can run ./main.py instead of ./patch.py with all other syntax the same.
this requires installing cpython
```console
foo@bar:~$ py -m pip install cpython
```
