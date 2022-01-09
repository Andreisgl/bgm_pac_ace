##ACZ BGM.APC unpacker by death_the_d0g (death_the_d0g @ Twitter)
##
##Further expansion and experimentation by Andrei Segal (Andreisgl @ Github)
##and Luis Filipe Sales (luisfilipels @ GitHub)
##===============================================================
##TODO: clean this sorry mess of code.

import os
import shutil
import textwrap

def tbl():
    try:
        tbl_file = open("BGM_TBL.acd", "rb")
    except FileNotFoundError as x:
        print ()
        print ("///ERROR///: BGM_TBL.acd file not found.")
        print ()
        a = input("///INPUT///: Press any key to exit...")
        if a:
            exit(0)
        else:
            exit(0)
    else:
        return tbl_file

def pac():
    try:
        pac_file = open("BGM.pac", "rb")
    except FileNotFoundError as x:
        print ()
        print ("///ERROR///: BGM.pac file not found.")
        print ()
        a = input("///INPUT///: Press any key to exit...")
        if a:
            exit(0)
        else:
            exit(0)
    else:
        pac_file.seek(0, os.SEEK_END)
        pac_file_s = pac_file.tell()
        if 0:   ##pac_file_s != 832665600:      ##File checking is disabled to allow for experimentation
            print()
            print(textwrap.fill("///ERROR///: Modified BGM.PAC files are not compatible with this script", width = 72))
            print()
            a = input("///INFO///: Press any key to exit...")
            if a:
                exit(0)
            else:
                exit(0)
        else:
            return pac_file

def extraction(tbl_file, pac_file):
    if os.path.exists("BGM"):
        shutil.rmtree("BGM")

    os.mkdir("BGM")
    
    print (textwrap.fill("///INFO///: Extracting files, please wait...", width = 72))
           
    val = 0
    val2 = 1
    f_n = 0
    f_offset = 4
    offset_list = []
    tbl_file.seek(0, 0)
    tbl_nof = int.from_bytes(tbl_file.read(4), byteorder = "little")    #First byte from BGM_TBL.acd is the number of files present.
    #tbl_nof = 1 #Disable parser loop for easier experimentation and extraction

    for f in range(tbl_nof):       #File parser
        tbl_file.seek(f_offset, 0)
        offset_list.append(int.from_bytes(tbl_file.read(4), byteorder = "little"))
        f_offset = f_offset + 4
    
    last_off = pac_file.seek(0, os.SEEK_END)
    offset_list.append(last_off)
    for f in range(tbl_nof):
        pac_file.seek(offset_list[val], 0)
        f_size = (offset_list[val2]) - (offset_list[val])
        data = pac_file.read(f_size)
        pac_file.seek((offset_list[val] + 52), 0)
        tag_str = pac_file.read(64)

        try:        #Now each error will be displayed, but the code will go on!!!
            s = tag_str.decode('UTF-8', errors ='replace')    #This is the problem.
        except:
            print("Tag decoding error")


        d = s.replace("\x00", "")
        wut = d.replace("�", "")
        a = wut.replace(".wav", "")
        aif = a.replace(".aif", "")
        fname = "BGM//" + str(f_n).zfill(6) + "_" + aif + ".npsf"
        file = open(fname, "wb")    #There is an 'invalid argument' going on here.
        file.write(data)
        print (f_size, fname)
        val = val + 1
        val2 = val2 + 1
        f_n = f_n + 1

print(textwrap.fill("Ace Combat Zero BGM.PAC unpacker by death_the_d0g (death_the_d0g @ Twitter)", width = 80))
print(textwrap.fill("===========================================================================", width = 80))
print()
print("Extracts the contents found inside ACZs BGM.PAC files.")

tbl_file = tbl()
pac_file = pac()
extraction(tbl_file, pac_file)
tbl_file.close()
pac_file.close()
##os.remove("BGM.pac")  ##Disable BGM.PAC removal for easier experimentation
exit()

