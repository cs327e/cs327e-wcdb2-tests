# lets grab the library
import WCDB2

factory1 = WCDB2.Factory()

# import
factory1.import_xml("RunWCDB2.in.xml")

# export
factory1.export_xml("RunWCDB2.out.xml")

factory2 = WCDB2.Factory()

# importing the export and re-exporting it
factory2.import_xml("RunWCDB2.out.xml")
factory2.export_xml("RunWCDB2data2.out.xml")

file1 = open("RunWCDB2.out.xml", 'r')
file2 = open("RunWCDB2data2.out.xml", 'r')

# comparing the initial export with its own export

file1xml = []
file2xml = []

for line in file1:
    file1xml.append(line)
for line in file2:
    file2xml.append(line)

flag = True

for line in file1xml:
    if line not in file2xml:
        flag = False
        break
    else:
        pass
    
assert flag

# done!
