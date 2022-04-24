from OpTable import OPTAB

with open('input.txt', 'r') as file:
    data = file.readlines()
    
loc = data[0].split()[-1]
start  = loc

def TR_size(cur):
    return (len(cur)-7-cur.count("^"))//2

labels = {}
forRef = {}

file = open("output.txt", 'w+')

current = ""

for line in data:
    words = line.split()
    if(words[0] == '.'):
        continue
    
    if len(words) > 1 and words[-2] not in ['RESW', 'RESB'] and current == "":
        current = "T^00"+loc.upper()+"^" 
        
    if len(words) == 3: # add label and address
        
        if words[0] in forRef.keys():
            length_TR = str.upper(str(hex((len(current)-7-current.count("^"))//2))[2:].zfill(2))
            current = current[:9] + length_TR + current[9:]
            file.write(current+"\n")
            for objc in forRef[words[0]]:
                current = "T^00" + objc + "^02^" + loc.upper()
                file.write(current + "\n")
                
            del forRef[words[0]]
            current = "T^00"+loc.upper()+"^"

        labels[words[0]] = loc.upper()
    
    if len(words) == 1: # for RSUB
        if TR_size(current) + 3 > 30:
            length_TR = str.upper(str(hex(TR_size(current))))[2:].zfill(2)
            current = current[:9] + length_TR + current[9:]
            file.write(current+"\n")
            current = "T^00"+loc.upper()+"^"
            continue
            
        current += "^" + OPTAB[words[-1]] + '0000'
        loc = str(hex(int(loc, 16) + 3)[2:])
        continue
    
    # Handle the case of buffer and array lengths
    if words[-2] == 'START' or words[-2] == 'END':
        
        if words[-2] == 'START':
            current = 'H^' + words[0][:6]
            if(len(words[0])<6):
                current += (" ")*(6-len(words[0]))
            current += "^00" + loc.upper() + "^00" + loc.upper()
                
            file.write(current+"\n")
            current = ""
        
        if words[-2] == 'END':
            labels[words[-2]] = loc.upper()
            length_TR = str.upper(str(hex(TR_size(current))))[2:].zfill(2)
            current = current[:9] + length_TR + current[9:]
            file.write(current+"\n")
            current = "E^00" + labels[words[-1]] + "\n"
            file.write(current)
        continue
    
    if words[-2] in ["RESW", "RESB"] and current != "":
        length_TR = str.upper(str(hex(TR_size(current)))[2:].zfill(2))
        current = current[:9] + length_TR + current[9:]
        file.write(current+ "\n")
        current = ""
    
    if words[-2] == 'RESW':
        size = int(words[-1])*3
        loc = str(hex(int(loc, 16) + size)[2:]) 
    
    elif words[-2] == 'RESB':
        size = int(words[-1])
        loc = str(hex(int(loc, 16) + size)[2:])
    
    elif words[-2] == 'BYTE':
        if words[-1][0]=='C':
            if TR_size(current) + 3 > 30:
                length_TR = str.upper(str(hex(TR_size(current))))[2:].zfill(2)
                current = current[:9] + length_TR + current[9:]
                file.write(current+"\n")
                current = "T^00"+loc.upper()+"^"
            
            current += "^" + ''.join([hex(ord(x))[2:] for x in words[-1][2:-1]]).upper()    # generate Object code from the the ASCII equivalent of the character
            loc = str(hex(int(loc, 16) + 3)[2:])
        else:
            if TR_size(current) + 1 > 30:
                length_TR = str.upper(str(hex(TR_size(current))))[2:].zfill(2)
                current = current[:9] + length_TR + current[9:]
                file.write(current+"\n")
                current = "T^00"+loc.upper()+"^"
            
            current += "^" + str.upper(words[-1][2:-1])    
            loc = str(hex(int(loc, 16) + 1)[2:])
    
    elif words[-2] != 'START':
        if TR_size(current) + 3 > 30:
            # print(TR_size(current), " -- ", current)
            length_TR = str.upper(str(hex(TR_size(current))))[2:].zfill(2)
            current = current[:9] + length_TR + current[9:]
            file.write(current+"\n")
            current = "T^00"+loc.upper()+"^"
        
        if words[-2] == 'WORD':
            current += "^" + str(hex(int(words[-1])))[2:].zfill(6)    
        else:
            if ',' in words[-1]:
                if words[-1][:-2] in labels:
                    current += '^' + OPTAB[words[-2]] + hex(int(labels[words[-1][:-2]],16) | int("8000",16))[2:].zfill(4).upper()
                else:
                    if words[-1][:-2] in forRef:
                        forRef[words[-1][:-2]].append(str.upper(str(hex(int(loc,16)+1))[2:]))
                    else:
                        forRef[words[-1][:-2]] = [str.upper(str(hex(int(loc,16)+1))[2:])]
                        
                    current += "^" + OPTAB[words[-2]] + "8000"   

            elif words[-1] in labels:
                current += '^' + OPTAB[words[-2]] + hex(int(labels[words[-1]],16) & int("7FFF",16))[2:].zfill(4).upper()    
                
            else:
                if words[-1] in forRef:
                    forRef[words[-1]].append(str.upper(str(hex(int(loc,16)+1))[2:]))
                else:
                    forRef[words[-1]]= [str.upper(str(hex(int(loc,16)+1))[2:])]
                
                current += "^" + OPTAB[words[-2]] + '0000'    
            
        loc = str(hex(int(loc, 16) + 3)[2:])
    
end = loc
file.seek(0)
file.seek((file.readline()).rindex("^")+1)
current = str(hex(int(end,16) - int(start,16)))[2:].upper().zfill(6)

file.write(current)
file.close()
