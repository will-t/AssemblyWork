BITS 32
global k_printstr

; char *string +8?, int row +12?, int col +16?
k_printstr:
    push ebp
    mov ebp, esp
    pusha
    pushf
    mov eax, [ebp+12] ; row 
    mov ebx, [ebp+16] ; col
    imul eax, 80
    add eax, ebx
    imul eax, 2
    add eax, 0xb8000
    mov edi, eax ; Move into edi for manipulation
    mov ecx, [ebp+12] ;String Length
    mov esi, [ebp+8] ;Addresss of String
    xor eax, eax
    xor ebx, ebx ; clean up registers used for calculations


    mov eax, 80
    imul eax, 24
    add eax, 79
    imul eax, 2
    add eax, 0x8000 ; variable to check edi too

print_return_loop:
    ; clear register ebx 
    cmp edi, eax
    jg reset_variable
    ;change value if greater than screen bounds
    cmp ecx, 0
    je loop_exit
    
    ;mov ebx, [ebp+8] ; string mabye not needed
    movsb BYTE es, ds
    mov BYTE es, 31
    inc edi
    dec ecx

    jmp print_return_loop ; return to top to finish the rest of string

loop_exit:
    popf
    popa
    ret


reset_variable:
xor edi, edi
mov edi, 0xB000
jmp print_return_loop    