BITS 32
global k_printstr
global go
global go_rest
global dispatch
global dispatch_leave
global lidtr
extern dequeue 
extern enqueue
extern Running
extern RunningQueue
extern p1
k_printstr:
    push ebp
    mov ebp, esp
    pusha
    pushf
    mov eax, [ebp+12] 
    mov ebx, [ebp+16] 
    imul eax, 80
    add eax, ebx
    imul eax, 2
    add eax, 0xB8000
    mov edi, eax 
    mov esi, [ebp+8] 
    xor eax, eax
    xor ebx, ebx 
    mov eax, 80
    imul eax, 24
    add eax, 79
    imul eax, 2
    add eax, 0xB8000 
print_return_loop:
    cmp edi, eax
    jg loop_exit
    cmp BYTE [esi], 0
    je loop_exit
    cld
    movsb
    mov BYTE [edi], 31
    inc edi
    jmp print_return_loop 
loop_exit:
    popf
    popa
    pop ebp 
    ret 
go:
    push ebp
    mov ebp, esp
    pusha
    mov eax, [RunningQueue]
    push eax
    call dequeue
    add esp, 4
    mov [Running], eax 
go_rest:
    mov eax, [Running]
    add eax, 8 
    mov esp, [eax]
    popa
    ret
dispatch:
    call yield
dispatch_leave:
    iret
yield:
    pusha 
    mov eax, [Running]
    add eax, 8
    mov [eax], esp
    mov eax, [RunningQueue]
    mov ebx, [Running]
    push ebx
    push eax
    call enqueue
    add esp, 8
    mov ebx, [RunningQueue]
    push ebx
    call dequeue
    add esp, 4
    mov [Running], eax
    jmp go_rest
lidtr:
push ebp
mov ebp, esp
push eax
mov eax, [ebp + 8]
lidt [eax]
pop eax
pop ebp
ret