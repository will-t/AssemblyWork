BITS 32
global _start
section .data
userMsg: DW 'Please enter a String to check:'
lenUserMsg EQU $-userMsg
;usereMsg DB 'Is a Palindrome'
;lenUsereMSG EQU $-usereMsg
;usrMsg DB 'Is not a Palindrome'
;lenUsrMsg EQU $-usrMsg

;Questions

Section .bss
s:RESB 1024
w:RESB 1024


section .text
_start:
;promping the user to enter a string in which to check for palindrome
;Loop_Palindrome:
mov eax, 4
mov ebx, 1
mov ecx, userMsg
mov edx, lenUserMsg
int 80h
mov eax, 3
mov ebx, 0
mov ecx, w
mov edx, s
int 80h







print_exit:

mov eax, 4
mov ebx, 1
mov ecx, w
mov edx, s
int 80h


exit:
mov eax, 1
mov ebx, 0
int 80h