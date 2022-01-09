##ACZ BGM.APC parser by by Andrei Segal (Andreisgl @ Github)
##Aid by Luis Filipe Sales (luisfilipels @ GitHub)
## Adapted from unpacker by death_the_d0g (death_the_d0g @ Twitter)
##===============================================================

import os
import shutil
import textwrap

EXPORT_OFFSETS = 1  # Change this to export offset_list for easier investigation

ORIGINAL_FILE_NAME = "BGM.PAC" # Change this for fast debugging
RESULTING_FILE_NAME = "BGM_TBL.acd"


def write_tbl_from_pac():
    print(textwrap.fill("///INFO///: Extracting files, please wait...", width=72))

    offset_list = []
    tbl_size = os.path.getsize(ORIGINAL_FILE_NAME)

    with open(ORIGINAL_FILE_NAME, 'rb') as pac_file:
        for bytes_offset in range(0, tbl_size, 4):
            data = pac_file.read(4)
            if not data:
                break
            if data == b'NPSF':
                offset_list.append(bytes_offset)

    with open(RESULTING_FILE_NAME, "wb") as tbl_file:
        tbl_file.write(len(offset_list).to_bytes(byteorder="little", length=4))
        for element in offset_list:
            tbl_file.write(element.to_bytes(4, byteorder="little"))


    if EXPORT_OFFSETS == 1: # Exports found offsets to facilitate investigation
        with open("offset_list_debug.acd", "wb") as offset_file_debug:
            offset_file_debug.write(len(offset_list).to_bytes(byteorder="little", length=4))
            for element in offset_list:
                offset_file_debug.write(element.to_bytes(4, byteorder="little"))
        print("Exporting debug offsets...")
    
    if EXPORT_OFFSETS == 1: # Exports found offsets to facilitate investigation
        with open("offset_list_debug.acd", "wb") as offset_file_debug:
            offset_file_debug.write(len(offset_list).to_bytes(byteorder="little", length=4))
            for element in offset_list:
                offset_file_debug.write(element.to_bytes(4, byteorder="little"))
        print("Exporting debug offsets...")

        
    return



print(textwrap.fill("Ace Combat Zero BGM.PAC unpacker by death_the_d0g (death_the_d0g @ Twitter)", width=80))
print(textwrap.fill("===========================================================================", width=80))
print()
print("Extracts the contents found inside ACZs BGM.PAC files.")

write_tbl_from_pac()

exit()
