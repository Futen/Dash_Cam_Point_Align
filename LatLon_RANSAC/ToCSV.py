import sys

if __name__ == '__main__':
    f_name = sys.argv[1]
    f = open(f_name, 'r')
    f_out = open('out.csv', 'w')
    f_out.write('gg\n')
    for line in f:
        line = line[0:-1].split('\t')
        s = '%s\t%s\n'%(line[1], line[2])
        f_out.write(s)
    f.close()
    f_out.close()
