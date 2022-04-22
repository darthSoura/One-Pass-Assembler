OPTAB = {'ADD': '18', 'COMP': '28', 'DIV': '24', 'J': '3C',
         'JEQ':'30', 'JGT': '34', 'JLT': '38', 'JSUB': '48', 
         'LDA': '00', 'LDCH': '50', 'LDL': '08', 'LDX': '04',
         'MUL': '20', 'OR': '44', 'RD': 'D8', 'RSUB': '4C', 
         'STA': '0C', 'STCH': '54', 'STL': '14', 'STSW': 'E8',
         'STX': '10', 'SUB': '1C', 'TD': 'E0', 'TIX': '2C', 'WD': 'DC'}

with open('input.txt', 'r') as file:
    data = file.readlines()
    
loc = data[0].split()[-1]
print(loc)

objCode = {}
labels = {}
backRef = {}

def hex_add(addr, bytes):
    
    pass

for line in data:
    words = line.split()
    if len(words) == 3: # add label and address
        labels[words[0]] = loc
        
    if words[-2] != 'START' and words[-2] != 'BYTE':
        loc += 3
    
    else:
        continue
    
    if words[-2] == 'BYTE':
        if words[-3] == 'EOF':
            loc += 3
        else:
            loc += 1

print(labels)