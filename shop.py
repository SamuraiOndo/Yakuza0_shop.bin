from platform import node
from unicodedata import name
from binary_reader import BinaryReader
import sys
import json
from pathlib import Path
import os
import shutil

path = open(sys.argv[1], "rb")
reader = BinaryReader(path.read())
reader.set_endian(True) # big endian
array = []
if(reader.read_uint32()==0):
    directory = os.path.splitext(sys.argv[1])[0]
    filejson1 = open(directory + ".json","w",encoding='cp932')
    i = 0
    gay = dict()
    reader.seek(4)
    shared1 = 30
    reader.set_encoding("cp932")
    count1 = reader.read_uint32()
    pad = reader.read_uint32()
    pointer1 = reader.read_uint32()
    header = {
        "Count": count1,
        }
    yes = {
        "Shared Count": shared1
    }
    reader.seek(pointer1)
    for i in range(count1):
        ID = reader.read_uint16()
        pad1 = reader.read_uint16()
        pad2 = reader.read_uint32(4)
        price1 = reader.read_uint32()
        pad3 = reader.read_uint32()
        price2 = reader.read_uint32()
        pointer3 = reader.read_uint32()
        stay2 = reader.pos()
        reader.seek(pointer3)
        string2 = reader.read_str()
        reader.seek(stay2)
        pad4 = reader.read_uint32()
        unk1 = reader.read_uint32()
        pad5 = reader.read_uint32()
        taylorswift = {
            "Item ID": ID,
            "Price 1": price1,
            "Price 2": price2,
            "Description": string2,
            "Unk 1": unk1,
            }
        header.update({i: taylorswift})
        i+=1
    reader.seek(0x10)
    for i in range(shared1):
        pointer2 = reader.read_uint32()
        stay = reader.pos()
        reader.seek(pointer2)
        string = reader.read_str()
        reader.seek(stay)
        shared = {
                "String": string,
        }
        yes.update({i: shared})
        i+=1
    output = { 'Shared Text': yes, 'Items': header }
    filejson1.write(json.dumps(output,ensure_ascii = False, indent = 2))
    # string point start = 272 + count1 * 48
else:
    f = open(sys.argv[1], encoding='cp932')
    fe = open(sys.argv[1] + ".bin", "wb") 
    w = BinaryReader()
    w.set_encoding("cp932")
    w.set_endian(True)
    p = json.loads(f.read()) 
    shared = p["Shared Text"]
    items = p["Items"]
    nodecount = p["Items"]["Count"]
    sharedcount = (shared["Shared Count"])
    stringpointstart = 272 + nodecount * 48
    # write header
    w.write_uint32(0)
    w.write_uint32(nodecount)
    w.write_uint32(0)
    w.write_uint32(272)
    w.align(stringpointstart)
    w.seek(16)
    for i in range(sharedcount):
        shared2 = p["Shared Text"][str(i)]
        stay = w.pos()
        pointer = w.size() + 1
        w.align(pointer)
        w.seek(0, whence=2)
        w.write_str(shared2["String"])
        w.seek(stay)
        w.write_uint32(pointer)
    w.seek(272)
    for i in range(nodecount):
        items2 = p["Items"][str(i)]
        w.write_uint16(items2["Item ID"])
        w.write_uint16(0)
        w.write_uint32(0)
        w.write_uint32(0)
        w.write_uint32(0)
        w.write_uint32(0)
        w.write_uint32(items2["Price 1"])
        w.write_uint32(0)
        w.write_uint32(items2["Price 2"])
        stay3 = w.pos()
        pointer = w.size() + 1
        w.align(pointer)
        w.seek(0, whence=2)
        w.write_str(items2["Description"])
        w.seek(stay3)
        w.write_uint32(pointer)
        w.write_uint32(0)
        w.write_uint32(items2["Unk 1"])
        w.write_uint32(0)
    w.seek(0, whence=2)
    w.write_uint8(0)
    fe.write(w.buffer())