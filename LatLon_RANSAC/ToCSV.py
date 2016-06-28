import sys

if __name__ == '__main__':
    f_name = sys.argv[1]
    f = open(f_name, 'r')
    f_out = open('out.csv', 'w')
    f_out.write('frame,1,2\n')
    for line in f:
        line = line[0:-1].split('\t')
        s = '%s,%s,%s\n'%(line[0],line[2], line[1])
        f_out.write(s)
    f.close()
    f_out.close()
