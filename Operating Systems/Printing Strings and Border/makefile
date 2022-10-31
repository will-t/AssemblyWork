param1=-g -m32 -fno-stack-protector -c -o kernel_c.o kernel.c
param2=-g -f elf -F dwarf -o kernel_asm.o kernel.asm
param3=-g -m32 -fno-stack-protector -c -o convert_c.o convert.c
param4=-g -m32 -fno-stack-protector -c -o buddy_c.o buddy.c
param5=-g -melf_i386 -Ttext 0x10000 -e main -o kernel.exe kernel_c.o kernel_asm.o convert_c.o buddy_c.o
param6=-DENTRY=0x$(shell nm kernel.exe |grep main | cut -d " " -f 1) boot1.asm #maybe remove shell to execute dif
param8=-j .text* -j .data* -j .rodata* -S -O binary kernel.exe boot2
param9=-drive format=raw,file=a.img,if=floppy
param10=if=/dev/zero of=a.img bs=512 count=2880
param11=if=boot1 of=a.img bs=1 count=512 conv=notrunc
param12=-o boot2 a:BOOT2

clean1=kernel_c.o
clean2=kernel_asm.o
clean3=convert_c.o
clean4=buddy_c.o
clean5=a.img
clean6=kernel.exe

debug1= -S -s -drive format=raw,file=a.img,if=floppy & ddd --debugger 'gdb -ex "target remote localhost:1234" -ex "break main" -ex "continue"' kernel.exe
all: boot1 boot2

boot1: boot1.asm kernel.exe
	nasm $(param6)
boot2: kernel.exe 
	objcopy $(param8)
kernel.exe: kernel_c.o kernel_asm.o convert_c.o buddy_c.o
	ld $(param5)
kernel_c.o: kernel.c
	gcc $(param1)
kernel_asm.o: kernel.asm
	nasm $(param2)
convert_c.o: convert.c
	gcc $(param3)
buddy_c.o: buddy.c
	gcc $(param4)

install:
	dd $(param10)
	/sbin/mkdosfs a.img
	dd $(param11)
	mcopy $(param12)
run:
	qemu-system-i386 $(param9)
clean:
	rm $(clean1)
	rm $(clean2)
	rm $(clean3)
	rm $(clean4)
	rm $(clean5)
	rm $(clean6)
debug:
	qemu-system-i386 $(debug1)