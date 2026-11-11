#!/usr/bin/env python3
"""Experimental local OID2/OID3 renderer calling user-supplied binary routines."""
import argparse, hashlib, struct, zipfile
from pathlib import Path
from PIL import Image
from unicorn import Uc, UC_ARCH_X86, UC_MODE_32
from unicorn.x86_const import UC_X86_REG_ESP

EXPECTED = '44db3732933fab38be70e202937f0896c92d3c78fe7f39fcc50814578cc561f8'

def load_binary(path):
    path = Path(path)
    if zipfile.is_zipfile(path):
        with zipfile.ZipFile(path) as archive:
            data = next((archive.read(z) for z in archive.infolist() if z.file_size == 434176 and hashlib.sha256(archive.read(z)).hexdigest() == EXPECTED), None)
        if data is None: raise ValueError('ZIP 中未找到匹配的原程序。')
    else: data = path.read_bytes()
    if hashlib.sha256(data).hexdigest() != EXPECTED: raise ValueError('原程序哈希不匹配；不支持此版本。')
    return data

def render(binary, kind, code, size):
    limit = 65535 if kind == 2 else (1 << 28) - 1
    if not 0 <= code <= limit: raise ValueError(f'码值需在 0 至 {limit} 范围内。')
    if not 64 <= size <= 12000: raise ValueError('尺寸需在 64 至 12000 像素范围内。')
    u = Uc(UC_ARCH_X86, UC_MODE_32)
    u.mem_map(0x400000, 0x80000)
    u.mem_write(0x400000, binary[:0x66000])
    u.mem_map(0x1000000, 0x40000)
    u.mem_map(0x2000000, 0x40000)
    u.mem_write(0x103f000,b'\x90')
    def run(addr, args):
        sp=0x1030000
        u.mem_write(sp,struct.pack('<'+'I'*(1+len(args)),0x103f000,*args))
        u.reg_write(UC_X86_REG_ESP,sp)
        u.emu_start(addr,0x103f000,count=1_000_000)
    u.mem_write(0x465ef0,struct.pack('<I',128))
    u.mem_write(0x465ecc,struct.pack('<I',0x2000000))
    u.mem_write(0x2000000,b'\xff'*(128*128//8))
    run(0x4026d0 if kind==2 else 0x401000,[code,0x1020000])
    run(0x402950 if kind==2 else 0x401980,[0x1020000,16,0])
    data=bytes(u.mem_read(0x2000000,128*128//8))
    tile=Image.new('1',(64,64),1)
    for y in range(65):
        for x in range(128):
            if not (data[y*16+x//8] >> (7-x%8) & 1):
                tile.putpixel(((x-16)%64,(64-y)%64),0)
    out=Image.new('1',(size,size),1)
    for y in range(0,size,64):
        for x in range(0,size,64): out.paste(tile,(x,y))
    return out

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source',required=True,help='原工具 ZIP 或菲林程序路径')
    parser.add_argument('--type',type=int,choices=[2,3],required=True)
    parser.add_argument('--code',type=int,required=True)
    parser.add_argument('--pixels',type=int,default=1536)
    parser.add_argument('--output',required=True)
    args=parser.parse_args()
    try:
        image=render(load_binary(args.source),args.type,args.code,args.pixels)
        image.save(args.output,dpi=(1200,1200))
    except (ValueError,OSError) as exc: parser.error(str(exc))
    print(f'已生成候选点阵：{args.output}。尚未验证点读笔兼容性。')

if __name__=='__main__': main()
