from random import shuffle
import Image
from numpy import *
from pylab import *

fn = 'logo4_rgb.png'
im = Image.open(fn)
w = im.size[0]
h = im.size[1]


data = array(im.getdata())[:,:3]
print data.shape
rgbs = array(data).reshape((h, w, 3)).transpose((1, 0, 2))

hfn = 'logo_gs.h'
f = open(hfn, 'w')
print >> f, 'uint8_t rgb565_width = %d;' % (w, )
print >> f, 'uint8_t rgb565_height = %d;' % (h, )

keep = []
lens = []

for i, row in enumerate(rgbs):
    for j, rgb in enumerate(row):
        l = linalg.norm(rgb)
        lens.append(l)
        if l < 256: ## change this for more colors
            r, b, g = rgb 
            keep.append([i, j, r, g, b])

def rgb565(r, b, g):
    get_bin = lambda x, n: format(x, 'b').zfill(n)
    out = 0xFFFF & (int((byte(r) & 0xF8) << 8) | 
                    int((byte(g) & 0xFC) << 3) | 
                    int(byte(b) >> 3))
    # print '%s %s %s' % tuple([get_bin(c, 8) for c in (r, g, b)]), 
    # print get_bin(out, 16)
    return out;

#hist(lens, 100);show()
shuffle(keep)
keep = array(keep).astype(int)
n = len(keep)

def printArray(a, type, name, f, n_name, per_row=15):
    n = len(a)
    print >> f, '%s %s[%s] = {' %  (type, name, n_name)
    i = 0
    while i < n:
        for j in range(per_row):
            if i < n:
                print >> f, '%d,' % a[i],
            i += 1
        print >> f, ''
    print >> f, '};\n'
print >> f, 'const unsigned int n_rgb565 = %d;' % len(keep)
printArray(keep[:,0], 'uint8_t', 'rgb565_rows', f, 'n_rgb565')
printArray(keep[:,1], 'uint8_t', 'rgb565_cols', f, 'n_rgb565')
rgb565 = array([rgb565(*l[2:]) for l in keep])
printArray(rgb565.astype(uint16), 'uint16_t', 'rgb565', f, 'n_rgb565', per_row=5)
print len(keep)
print 'wrote', hfn
im2 = Image.new('RGB', (w, h), (255, 255, 255))
print keep.shape
print keep[0, 0].shape
for ijrgb in keep:
    i, j, r, g, b = ijrgb
    im2.putpixel((i, j), tuple([r, g, b]))
im2.show()
