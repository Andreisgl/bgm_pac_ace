##ACZ BGM.APC repacker by death_the_d0g (death_the_d0g @ Twitter)
##===============================================================
##Creates a new BGM.PAC file from the contents in the BGM folder.
##TODO: clean this sorry mess of code.

import os
import textwrap

basedir = "BGM"
if not os.path.isdir(basedir):
    print(textwrap.fill("///ERROR///: BGM folder not found.", width = 72))
    a = input("///INPUT///: Press a key to exit...")
    if a:
        exit(0)
    else:
        exit(0)

true_nof = len(os.listdir(basedir))


try:
    misc = open("BGM_MISC.acd","rb")
except FileNotFoundError as x:
    print(textwrap.fill("///ERROR///: BGM_MISC.acd file is missing!.", width = 72))
    print(textwrap.fill("///INFO///: Place the BGM_MISC.acd file in the same folder as this script.", width = 72))
    a = input("///INPUT///: Press a key to exit...")
    if a:
        exit(0)
    else:
        exit(0)

if 0: #true_nof != 317: #Disable file checking for debbuging purposes
    print(textwrap.fill("///ERROR///: The amount of NPSF files in the BGM folder is different than 317.", width = 72))
    print(textwrap.fill("///INFO///: Make sure the BGM folder has this exact amount of NPSF files because this script won't work otherwise.", width = 72))
    a = input("///INPUT///: Press any key to exit...")
    if a:
        exit(0)
    else:
        exit(0)

true_nof_hex = true_nof.to_bytes(4, "little")
pad = 0
val = 0
f_offset = 0

filenames = []
f_size_table = []
f_offset_table = []
f_offset_table.append(f_offset)


bgm_file = open("BGM.PAC","wb")
tbl_file = open("temp.dat","wb")

tbl_file.write(true_nof_hex)


for f in os.listdir(basedir):
    path = os.path.join(basedir, f)
    fsize = os.path.getsize(path)
    f_size_table.append(fsize)
    filenames.append(path)


for f in os.listdir(basedir):
    f_offset = f_offset + f_size_table[val]
    f_offset_table.append(f_offset)
    
    file_offset = f_offset_table[val].to_bytes(4, "little")
    tbl_file.write(file_offset)
    
    val = val + 1

tbl_file.write(bytearray(8))

for fname in filenames:
    with open(fname, "rb") as infile:
        bgm_file.write(infile.read())

tbl_file.close()
bgm_file.close()

try:
    file_data = open("temp.dat","rb")
except FileNotFoundError as x:
    print("///ERROR///: temp.dat file is missing!.")
    a = input("///INPUT///: Press any key to exit...")
    if a:
        exit(0)
    else:
        exit(0)

print(textwrap.fill("Ace Combat Zero BGM.PAC repacker by death_the_d0g (death_the_d0g @ Twitter)", width = 80))
print(textwrap.fill("===========================================================================", width = 80))
print()
print("Merges the contents inside the BGM folder into a new BGM.PAC file.")

new = open("0000.dat","wb")
t = misc.read()
x = file_data.read()
new.write(t)
new.seek(72176, 0)
new.write(x)
new.close()
file_data.close()
#os.remove("temp.dat")  # Keep file for analysis
exit()

