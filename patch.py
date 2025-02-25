import argparse
int_size=4

def lcs_bytearray(bytearray1, bytearray2):
    len1 = len(bytearray1)
    len2 = len(bytearray2)
    #if len2>len1:
    #    temp1=len1
    #    len1=len2
    #    len2=temp1
    #    temp2=bytearray1
    #    bytearray1=bytearray2
    #    bytearray2=temp2
    
    # Create two rows for dynamic programming
    prev = [0]*(len2 + 1)  # Previous row
    curr = [0]*(len2 + 1)  # Current row
    # Build the LCS table
    tab=0
    goal=len1*len2
    mult=1
    for i in range(1, len1 + 1):
        for j in range(1, len2 + 1):
            tab+=1
            if(tab>10000000):
                tab=0
                mult+=1
                print((tab+10000000*mult)*100/goal, "percent there")
            if bytearray1[i - 1] == bytearray2[j - 1]:
                curr[j] = prev[j - 1] + 1  # If bytes match, increment the length
            else:
                curr[j] = max(prev[j], curr[j - 1])  # Take max of the previous row or current column
            
        prev, curr = curr, prev  # Swap rows for next iteration

    # Reconstruct the LCS from the DP table
    lcs = []
    i, j = len1, len2
    while i > 0 and j > 0:
        if bytearray1[i - 1] == bytearray2[j - 1]:
            lcs.append(bytearray1[i - 1])  # Match found, add to the LCS
            i -= 1
            j -= 1
        elif prev[j] >= curr[j - 1]:
            i -= 1  # Move in the first bytearray
        else:
            j -= 1  # Move in the second bytearray
    lcs.reverse()  # Reverse the list since we built it backwards
    return bytearray(lcs)  # Convert back to bytearray

def make_patch(str1,str2,match,patch_file):
    match_counter=0
    counter1=0
    added=[]
    added_char=[]
    removed=[]
    i=0
    while i < len(match):
        if str1[counter1] != match[i]:
            removed.append(counter1)
            i-=1
        counter1+=1
        i+=1
    while(counter1<len(str1)):
        removed.append(counter1)
        counter1+=1
    for i in range(len(str2)):
        if str2[i]!=match[match_counter]:
            added.append(i)
            added_char.append(str2[i])
        else:
            match_counter+=1
        if match_counter>=len(match): #this is new
            temp_index=i
            break
    while(temp_index<len(str2)):
        added.append(temp_index)
        added_char.append(str2[temp_index])
        temp_index+=1
    f=open(patch_file,"wb")
    f.write(len(removed).to_bytes(int_size, 'big'))
    f.write(len(added).to_bytes(int_size,'big'))
    for a in removed:
        f.write(a.to_bytes(int_size,'big'))
    for i in range((len(added))):
        f.write(added[i].to_bytes(int_size,'big'))
        f.write(added_char[i].to_bytes(1,'big'))
    f.close()

def write_patch(str1,patch_path,out):
    added_counter=0
    removed_counter=0
    removed_indexer=0
    added_indexer=0
    f=open(patch_path,"rb")
    removed_counter=int.from_bytes(f.read(int_size),'big')
    added_counter=int.from_bytes(f.read(int_size),'big')
    added=[]
    added_char=[]
    removed=[]
    outt=[]
    for a in range(removed_counter):
        removed.append(int.from_bytes(f.read(int_size),'big'))
    for i in range(added_counter):
        added.append(int.from_bytes(f.read(int_size),'big'))
        added_char.append(int.from_bytes(f.read(1),'big'))
    for i in range(len(str1)):
        if removed_indexer < removed_counter:
            if removed[removed_indexer]!=i:
                outt.append(str1[i])
            else:
                removed_indexer+=1
        else:
            outt.append(str1[i])
        while added_indexer < added_counter and added[added_indexer]==len(outt):
            outt.append(added_char[added_indexer])
            added_indexer+=1
    outt.pop(-1)#i have no idea why theres an extra byte
    f.close()
    f=open(out,"wb")
    f.write(bytes(outt))
    f.close()
def run():
    parser = argparse.ArgumentParser(prog="filepatcher",description="Patches files",epilog="example usage py ./main.py -i input.txt -p patchtochangeinput.bin -o newchangedfile.txt -m patch")
    parser.add_argument("-s","--size",type=int,required=False,default=4,help="size of int in bytes to store in the patch. 4 is default. If you need to make a patch for a file of more than 4GB you should use a larger number. Using a number larger than 8 is pointless")
    parser.add_argument("-i","--input",type=str,required=True,help="filepath of base file to patch/make a patch for. required")
    parser.add_argument("-o","--output",type=str,required=False,help="filepath of output file. only used in patch mode")
    parser.add_argument("-p","--patch",type=str,required=True,help="filepath of the patch file. required for both modes")
    parser.add_argument("-m","--mode",type=str,required=True,help="patch or write_patch modes. patch mode patches the input file -i using patch file -o and writes the new file into file -o")
    parser.add_argument("-c","--changed",required=False,help="path for the changed file. only used in write_patch mode. path of the file you want to make a patch of -i for. using patch, -i will turn into -c")
    args=parser.parse_args()

    int_size=args.size
    if args.mode=="make_patch":
        file1=args.input
        file2=args.changed
        patch_path=args.patch
        f=open(file1,"rb")
        a=bytearray(f.read())
        f.close()
        f=open(file2,"rb")
        b=bytearray(f.read())
        f.close()
        seq=lcs_bytearray(a,b)
        make_patch(a,b,seq,patch_path)
    elif args.mode=="patch":
        file1=args.input
        outpath=args.output
        patch_path=args.patch
        f=open(file1,"rb")
        a=bytearray(f.read())
        f.close()
        write_patch(a,patch_path,outpath)
    else:
        print(args.help)

if __name__=="__main__":
    run()

