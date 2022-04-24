from OpTable import OPTAB

def TR_size(cur):
    return (len(cur)-7-cur.count("^"))//2

def init_current(addr):
    return "T^00"+addr+"^" 
    
def final_current(curr):
    length = str.upper(str(hex(TR_size(curr))))[2:].zfill(2)
    return curr[:9] + length + curr[9:] + "\n"

def update_loc(loc, n, bytes):
    size = int(n)*bytes
    return str(hex(int(loc, 16) + size)[2:]).upper()

def add_to_forRef(fR, key, addr):
    if key in fR:
        fR[key].append(str(hex(int(addr,16)+1))[2:].upper())
    else:
        fR[key] = [str(hex(int(addr,16)+1))[2:].upper()]
    
    return fR
 
def write_to_file(curr, f):
    f.write(final_current(curr)) 

if __name__ == "__main__":
    
    with open('input.txt', 'r') as file:
        data = file.readlines()
        
    loc = data[0].split()[-1].upper()
    start  = loc
        
    labels = {}
    forRef = {}
    current = ""

    file = open("output.txt", 'w+')

    for line in data:
        words = line.split()
        if(words[0] == '.'):
            continue
        
        if len(words) > 1 and words[-2] not in ['RESW', 'RESB'] and current == "":
            current = init_current(loc)
            
        if len(words) == 3: # add label and address
            
            if words[0] in forRef.keys():
                write_to_file(current, file)
                for objc in forRef[words[0]]:
                    current = init_current(objc) + "02^" + loc
                    file.write(current + "\n")
                    
                del forRef[words[0]]
                current = init_current(loc)

            labels[words[0]] = loc
        
        if len(words) == 1: # for RSUB
            if TR_size(current) + 3 > 30:
                write_to_file(current, file)
                current = init_current(loc)
                continue
                
            current += "^" + OPTAB[words[-1]] + '0000'
            loc = update_loc(loc, 1, 3)
            continue
        
        # Handle the case of buffer and array lengths
        if words[-2] in ['START', 'END']:
            
            if words[-2] == 'START':
                current = 'H^' + words[0][:6]
                if(len(words[0])<6):
                    current += (" ")*(6-len(words[0]))
                current += ("^00" + loc)*2
                    
                file.write(current + "\n")
                current = ""
            
            else:
                labels[words[-2]] = loc
                write_to_file(current, file)
                current = "E^00" + labels[words[-1]] + "\n"
                file.write(current)
        
        elif words[-2] in ["RESW", "RESB"]:
            if current != "":
                write_to_file(current, file)
                current = ""
                
            if words[-2] == 'RESW':
                loc = update_loc(loc, words[-1], 3) 
            else: 
                loc = update_loc(loc, words[-1], 1)
                    
        elif words[-2] == 'BYTE':
            if words[-1][0]=='C':
                if TR_size(current) + 3 > 30:
                    write_to_file(current, file)
                    current = init_current(loc)
                        
                current += "^" + (''.join([hex(ord(x))[2:] for x in words[-1][2:-1]]).upper() + "000000")[:6]    # generate Object code from the the ASCII equivalent of the character
                loc = update_loc(loc, 1, 3)  
                
            else:
                if TR_size(current) + 1 > 30:
                    write_to_file(current, file)
                    current = init_current(loc)
                        
                current += "^" + words[-1][2:-1].upper()
                loc = update_loc(loc, 1, 1)
        
        else:
            if TR_size(current) + 3 > 30:
                write_to_file(current, file)            
                current = init_current(loc)
            
            if words[-2] == 'WORD':
                current += "^" + str(hex(int(words[-1])))[2:].zfill(6)    
            else:
                if ',' in words[-1]:
                    if words[-1][:-2] in labels:
                        current += '^' + OPTAB[words[-2]] + hex(int(labels[words[-1][:-2]],16) | int("8000",16))[2:].zfill(4).upper()
                    else:
                        forRef = add_to_forRef(forRef, words[-1][:-2], loc)
                        current += "^" + OPTAB[words[-2]] + "8000"   

                elif words[-1] in labels:
                    current += '^' + OPTAB[words[-2]] + hex(int(labels[words[-1]],16) & int("7FFF",16))[2:].zfill(4).upper()    
                    
                else:
                    forRef = add_to_forRef(forRef, words[-1], loc)
                    current += "^" + OPTAB[words[-2]] + '0000'    
                
            loc = update_loc(loc, 1, 3)

    end = loc
    file.seek(0)
    file.seek((file.readline()).rindex("^")+1)
    current = str(hex(int(end,16) - int(start,16)))[2:].upper().zfill(6)

    file.write(current)
    file.close()
