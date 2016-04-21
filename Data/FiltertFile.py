f = open('list_origin.txt', 'r')
f_out = open('list_new.txt', 'w')
for line in f:
    line = line[0:-1].split('\t')
    print line
    if ' ' in line:
        line.remove(' ')
    if len(line) == 4:
        loc = line[2][1:-1].split(',')
        print loc
        s = '%s\t%s\t%s\t%s\t%s\n'%(line[0], line[1], loc[0], loc[1], line[3])
        f_out.write(s)

f.close()
f_out.close()
