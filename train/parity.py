import subprocess, sys, random
import numpy as np, torch
from tok import Tokenizer, USER, BOT, END
from export import load, dequant_model
import gen
HOST="../host/espite_host"
tk=Tokenizer.load("tokenizer.json")

gen.init("x","1024")
rng=random.Random(5)
tests=["hi","What's a cat?","what is 3+4","My name is Zyx'qor!!","  double  spaces ","tab\there","émoji ☃ test","esp32-s3 rocks","I'm Amrio","x"*80]
for c in gen.generate(300,11):
    for u,b in c: tests+= [u,b]
bad=0
for t in tests:
    py=tk.encode(t)
    c=list(map(int,subprocess.run([HOST,"encode",t],capture_output=True,text=True).stdout.split()))
    if py!=c: bad+=1; print("MISMATCH",repr(t),py[:20],c[:20])
print(f"tokenizer: {len(tests)-bad}/{len(tests)} match")

m,c,ck=load(sys.argv[1])
dq=dequant_model(load(sys.argv[1])[0])
seq=[USER]+tk.encode("hello! what is a cat?")+[BOT]+tk.encode("A cat is a small")
x=torch.tensor([seq]);pos=torch.arange(len(seq))[None];am=torch.ones(1,1,len(seq),len(seq),dtype=torch.bool).tril()
with torch.no_grad():
    lf=m(x,pos,am)[0,-1].numpy(); lq=dq(x,pos,am)[0,-1].numpy()
lc=np.array(list(map(float,subprocess.run([HOST,"logits"]+[str(i) for i in seq],capture_output=True,text=True).stdout.split())))
print("max |C - torch(int8 weights)| =",np.abs(lc-lq).max(), " argmax equal:",lc.argmax()==lq.argmax())
print("max |C - torch(float)|        =",np.abs(lc-lf).max(), " argmax equal:",lc.argmax()==lf.argmax())
print("next token:",repr(tk.vocab[lc.argmax()]))
