from PIL import Image
import sys
src=Image.open('img/design/snow-christmas-logo.png').convert('RGBA')
a=src.split()[3]
# crystal region (left ornament)
box=(15,380,160,560)
c=src.crop(box)
import numpy as np
from scipy import ndimage
m=np.array(c.split()[3])>20
lab,n=ndimage.label(ndimage.binary_dilation(m,iterations=2))
sizes=ndimage.sum(m,lab,range(1,n+1)); keep=lab==(1+int(np.argmax(sizes)))
arr=np.array(c); arr[...,3]=np.where(keep,arr[...,3],0); c=Image.fromarray(arr)
c=c.crop(c.split()[3].point(lambda v:255 if v>20 else 0).getbbox())
# brighten to white keeping alpha
r,g,b,al=c.split(); white=Image.new('RGBA',c.size,(255,255,255,0)); white.putalpha(al.point(lambda v:min(255,int(v*1.4))))
def tile(size,pad):
    bg=Image.new('RGBA',(size,size),(26,68,114,255))
    s=int(size*(1-2*pad)); w,h=white.size; k=s/max(w,h)
    ic=white.resize((max(1,int(w*k)),max(1,int(h*k))),Image.LANCZOS)
    bg.alpha_composite(ic,((size-ic.width)//2,(size-ic.height)//2)); return bg
tile(512,0.12).save('img/icon-512.png'); tile(192,0.12).save('img/icon-192.png')
tile(180,0.14).convert('RGB').save('apple-touch-icon.png')
tile(64,0.06).save('favicon.ico',sizes=[(16,16),(32,32),(48,48),(64,64)])
