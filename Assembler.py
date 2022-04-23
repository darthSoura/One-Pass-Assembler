OPTAB = {'ADD': '18', 'COMP': '28', 'DIV': '24', 'J': '3C',
         'JEQ':'30', 'JGT': '34', 'JLT': '38', 'JSUB': '48', 
         'LDA': '00', 'LDCH': '50', 'LDL': '08', 'LDX': '04',
         'MUL': '20', 'OR': '44', 'RD': 'D8', 'RSUB': '4C', 
         'STA': '0C', 'STCH': '54', 'STL': '14', 'STSW': 'E8',
         'STX': '10', 'SUB': '1C', 'TD': 'E0', 'TIX': '2C', 'WD': 'DC'}

with open('input.txt', 'r') as file:
    data = file.readlines()
    
loc = data[0].split()[-1]
start  = loc

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
        current += "^" + OPTAB[words[-1]] + '0000'
        loc = str(hex(int(loc, 16) + 3)[2:])
        continue
    
    # Handle the case of buffer and array lengths
    if words[-2] == 'START' or words[-2] == 'END':
        
        if words[-2] == 'START':
            current = 'H^'
            if(len(words[0])<6):
                current += words[0] + (" ")*(6-len(words[0]))
                current += "^00" + loc.upper() + "^00" + loc.upper()
                
            file.write(current+"\n")
            current = ""
        
        if words[-2] == 'END':
            labels[words[-2]] = loc.upper()
            length_TR = str.upper(str(hex((len(current)-7-current.count("^"))//2))[2:].zfill(2))
            current = current[:9] + length_TR + current[9:]
            file.write(current+"\n")
            current = "E^00" + labels[words[-1]] + "\n"
            file.write(current)
        continue
    
    if words[-2] in ["RESW", "RESB"] and current != "":
        length_TR = str.upper(str(hex((len(current)-7-current.count("^"))//2))[2:].zfill(2))
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
            current += "^" + ''.join([hex(ord(x))[2:] for x in words[-1][2:-1]]).upper()    # generate Object code from the the ASCII equivalent of the character
            loc = str(hex(int(loc, 16) + 3)[2:])
        else:
            current += "^" + str.upper(words[-1][2:-1])    
            loc = str(hex(int(loc, 16) + 1)[2:])
    
    elif words[-2] != 'START':
        
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

# for key, value in labels.items():
#     print(key, value, sep=" ")

# for key, value in objCode.items():
#     print(key, value, sep=" ")

# for key, value in forRef.items():
#     print(key, value, sep=" ")