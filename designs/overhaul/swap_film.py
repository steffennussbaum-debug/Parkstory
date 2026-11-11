# swap_film.py in.html out.html old_media_dir new_media_dir : replaces embedded film clips/posters
import base64, sys
src, dst, old, new = sys.argv[1:5]; h = open(src).read()
for f in ['common.webm','common.mp4','apt.webm','apt.mp4','off.webm','off.mp4','ret.webm','ret.mp4','poster0.jpg','poster_end.jpg']:
    a = base64.b64encode(open(old+'/'+f,'rb').read()).decode(); b = base64.b64encode(open(new+'/'+f,'rb').read()).decode()
    n = h.count(a); h = h.replace(a, b); print(f, n)
open(dst,'w').write(h)
