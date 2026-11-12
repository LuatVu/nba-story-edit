#!/usr/bin/env python3
"""Dò nhạc nền trong bản mix có cả lời: music_analyze.py <wav 16k mono> [tên]
Ý tưởng: dải 20-70Hz nằm dưới tần số cơ bản giọng nam -> gần như chỉ còn nhạc.
Đổi bản nhạc dò bằng novelty trên đặc trưng phổ ở các dải nhạc chiếm ưu thế."""
import numpy as np, wave, sys

def med(a,k):
    k=k|1; p=k//2
    b=np.pad(a,p,mode="edge")
    return np.array([np.median(b[i:i+k]) for i in range(len(a))])

path=sys.argv[1]; name=sys.argv[2] if len(sys.argv)>2 else path
w=wave.open(path); sr=w.getframerate()
x=np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).astype(np.float32)/32768
W=int(sr); H=int(sr*0.5); nf=(len(x)-W)//H
win=np.hanning(W); spec=np.empty((nf,W//2+1),dtype=np.float32)
for i in range(nf): spec[i]=np.abs(np.fft.rfft(x[i*H:i*H+W]*win))
freq=np.fft.rfftfreq(W,1/sr)
band=lambda lo,hi: spec[:,(freq>=lo)&(freq<hi)].mean(axis=1)
db=lambda a: 20*np.log10(a+1e-9)

sub=med(db(band(20,70)), 9)                      # mượt ~4.5s
thr=np.percentile(sub,8)+7
on=sub>thr
dur=nf*0.5
print(f"\n=== {name} ({dur/60:.1f} phút) ===")
print(f"  có nhạc {on.mean():.0%} · vắng nhạc {1-on.mean():.0%}")

seg=[];cur=on[0];st=0
for i in range(1,nf):
    if on[i]!=cur: seg.append([cur,st*0.5,i*0.5]); cur=on[i]; st=i
seg.append([cur,st*0.5,nf*0.5])
gaps=[s for s in seg if not s[0] and s[2]-s[1]>=4]
runs=[s for s in seg if s[0] and s[2]-s[1]>=4]
print(f"  {len(runs)} đoạn CÓ nhạc (>=4s): trung vị {np.median([s[2]-s[1] for s in runs]):.0f}s · "
      f"dài nhất {max(s[2]-s[1] for s in runs):.0f}s")
if gaps:
    print(f"  {len(gaps)} đoạn VẮNG nhạc (>=4s): trung vị {np.median([s[2]-s[1] for s in gaps]):.0f}s · "
          f"dài nhất {max(s[2]-s[1] for s in gaps):.0f}s")
    print("    " + " · ".join(f"{int(a//60)}:{a%60:04.1f}({b-a:.0f}s)" for _,a,b in gaps[:10]))

# ---- đổi bản nhạc: novelty trên dải nhạc chiếm ưu thế, bỏ dải giọng ----
feat=np.stack([db(band(40,80)),db(band(80,150)),db(band(150,200)),
               db(band(4000,6000)),db(band(6000,8000))],axis=1)
K=8                                              # 4s mỗi khối
nb=nf//K
blk=np.array([feat[i*K:(i+1)*K].mean(axis=0) for i in range(nb)])
blk=(blk-blk.mean(0))/(blk.std(0)+1e-9)
nov=np.array([np.linalg.norm(blk[i+1]-blk[i]) if 0<i<nb-1 else 0 for i in range(nb)])
nov=med(nov,3)
pk=np.percentile(nov,93)
cand=[i for i in range(2,nb-2) if nov[i]>pk and nov[i]==max(nov[i-2:i+3])]
merged=[]
for c in cand:
    if merged and c-merged[-1]<6: continue       # >=24s mới tính là đổi bản
    merged.append(c)
print(f"  ~{len(merged)} điểm đổi tính chất nhạc  =>  trung bình {dur/max(1,len(merged)+1):.0f}s mỗi đoạn nhạc")
print("    mốc: " + " · ".join(f"{int(c*4//60)}:{c*4%60:02d}" for c in merged[:16]))
