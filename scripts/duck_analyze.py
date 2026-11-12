#!/usr/bin/env python3
"""Đo độ duck của nhạc dưới giọng đọc: duck_analyze.py <wav 16k mono> [tên]

Nguyên lý:
  - dải 20-70 Hz nằm DƯỚI tần số cơ bản giọng nam -> đại diện cho mức NHẠC
  - dải 200-3400 Hz -> đại diện cho mức GIỌNG (có lẫn nhạc nhưng giọng áp đảo)
Độ duck = mức nhạc lúc im giọng TRỪ mức nhạc lúc đang nói, đo trong cùng vùng có nhạc.
"""
import numpy as np, wave, sys

def med(a,k):
    k=k|1; p=k//2; b=np.pad(a,p,mode="edge")
    return np.array([np.median(b[i:i+k]) for i in range(len(a))])

path=sys.argv[1]; name=sys.argv[2] if len(sys.argv)>2 else path
w=wave.open(path); sr=w.getframerate()
x=np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).astype(np.float32)/32768
W=int(sr*0.4); H=int(sr*0.2); nf=(len(x)-W)//H        # cửa sổ 0.4s, bước 0.2s
win=np.hanning(W); spec=np.empty((nf,W//2+1),dtype=np.float32)
for i in range(nf): spec[i]=np.abs(np.fft.rfft(x[i*H:i*H+W]*win))
freq=np.fft.rfftfreq(W,1/sr)
band=lambda lo,hi: spec[:,(freq>=lo)&(freq<hi)].mean(axis=1)
db=lambda a: 20*np.log10(a+1e-9)

music=db(band(20,70))         # mức nhạc
voice=db(band(200,3400))      # mức giọng

has_music = med(music,15) > np.percentile(med(music,15),8)+7
# ngưỡng giọng: lấy mốc thấp tuyệt đối, không phải phân vị
vth = np.percentile(voice,5)+8
raw_speak = voice > vth
# CHỈ tính "im giọng" khi im LIÊN TỤC >=1.5s (8 khung) — đủ để ducker nhả hết
MIN=8
quiet=np.zeros(nf,dtype=bool); run=0
for i in range(nf):
    if not raw_speak[i]: run+=1
    else:
        if run>=MIN: quiet[i-run:i]=True
        run=0
if run>=MIN: quiet[nf-run:]=True
# "đang nói" = nói liên tục >=1.5s, bỏ rìa 0.4s quanh mép để tránh thời gian nhả
speak=np.zeros(nf,dtype=bool); run=0
for i in range(nf):
    if raw_speak[i]: run+=1
    else:
        if run>=MIN: speak[i-run+2:i-1]=True
        run=0
if run>=MIN: speak[nf-run+2:]=True

on  = has_music & speak
off = has_music & quiet
print(f"\n=== {name} ===")
print(f"  khung có nhạc: {has_music.mean():.0%}")
print(f"  mẫu dùng: đang nói liên tục {on.sum()} khung ({on.sum()*0.2:.0f}s) · "
      f"im giọng >=1.5s {off.sum()} khung ({off.sum()*0.2:.0f}s)")
if off.sum() < 40:
    print("  (quá ít mẫu im giọng, bỏ qua)"); sys.exit()
m_on, m_off = np.median(music[on]), np.median(music[off])
print(f"\n  MỨC NHẠC (dải 20-70Hz)")
print(f"    lúc đang nói : {m_on:6.1f} dB")
print(f"    lúc im giọng : {m_off:6.1f} dB")
print(f"    => nhạc bị hạ **{m_off-m_on:.1f} dB** khi có giọng")
v_on, v_off = np.median(voice[on]), np.median(voice[off])
print(f"\n  MỨC DẢI GIỌNG (200-3400Hz)")
print(f"    lúc đang nói : {v_on:6.1f} dB   (giọng + nhạc)")
print(f"    lúc im giọng : {v_off:6.1f} dB   (chỉ nhạc)")
print(f"    => giọng nổi trên nhạc khoảng **{v_on-v_off:.1f} dB** trong dải giọng")
