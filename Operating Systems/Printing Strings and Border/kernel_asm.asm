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
    add eax, 0xB8000
    mov edi, eax ; Move into edi for manipulation
    mov esi, [ebp+8] ;Addresss of String
    xor eax, eax
    xor ebx, ebx ; clean up registers used for calculations


    mov eax, 80
    imul eax, 24
    add eax, 79
    imul eax, 2
    add eax, 0xB8000 ; variable to check edi too

print_return_loop:
    ; clear register ebx 
    cmp edi, eax
    jg loop_exit
    ;change value if greater than screen bounds
    cmp BYTE [esi], 0
    je loop_exit
    
    ;mov ebx, [ebp+8] ; string mabye not needed
    cld
    movsb
    mov BYTE [edi], 31
    inc edi
    jmp print_return_loop ; return to top to finish the rest of string

loop_exit:
    popf
    popa
    pop ebp ;maybe not need to pop of stack due to popa command
    ret
    

;reset_variable:
;xor edi, edi
;mov edi, 0xB000
;jmp print_return_loop    