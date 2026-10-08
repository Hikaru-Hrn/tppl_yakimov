; Среднее арифметическое разностей x[i] - y[i]
;
; Сборка и запуск:
;   make
;   make run  (или ./average data.txt)

%define BUFSIZE 0x100000              ; 1 МБ под файл

section .text
global _start

_start:
    ; Получаем имя файла из аргументов командной строки (argv[1])
    mov r12, [rsp + 16]

    ; Открываем файл (sys_open)
    mov rax, 2
    mov rdi, r12
    xor esi, esi                       ; O_RDONLY
    syscall
    mov ebx, eax                       ; сохраняем файловый дескриптор

    ; Читаем содержимое файла в буфер (sys_read)
    xor eax, eax
    mov edi, ebx
    lea rsi, [rel buf]
    mov edx, BUFSIZE
    syscall

    ; Завершаем прочитанные данные нулевым байтом
    lea rsi, [rel buf]
    mov byte [rsi + rax], 0

    ; Закрываем файл (sys_close)
    mov eax, 3
    mov edi, ebx
    syscall

    ; Инициализация:
    ; Сумма разностей: (x[0]-y[0]) + ... + (x[n-1]-y[n-1]) == sum(x) - sum(y)
    xor ebx, ebx                       ; rbx = общая сумма (sum)
    xor r13, r13                       ; r13 = количество элементов (count)
    lea rsi, [rel buf]                 ; rsi = указатель на текущую позицию

    ; Строка 1: прибавляем элементы массива x
.line1_loop:
.skip1:
    movzx eax, byte [rsi]
    cmp al, ' '
    je .next1
    cmp al, 9                          ; табуляция
    je .next1
    cmp al, ','
    je .next1
    cmp al, 13                         ; '\r'
    je .next1
    jmp .done_skip1
.next1:
    inc rsi
    jmp .skip1
.done_skip1:
    cmp al, 10                         ; '\n' - конец первой строки
    je .line1_done
    cmp al, 0
    je .line1_done

    call read_int
    add rbx, rax                       ; sum += x[i]
    inc r13                            ; count++
    jmp .line1_loop

.line1_done:
    inc rsi                            ; пропускаем символ '\n'

    ; Строка 2: вычитаем элементы массива y
.line2_loop:
.skip2:
    movzx eax, byte [rsi]
    cmp al, ' '
    je .next2
    cmp al, 9
    je .next2
    cmp al, ','
    je .next2
    cmp al, 13
    je .next2
    jmp .done_skip2
.next2:
    inc rsi
    jmp .skip2
.done_skip2:
    cmp al, 10                         ; '\n' или конец файла
    je .line2_done
    cmp al, 0
    je .line2_done

    call read_int
    sub rbx, rax                       ; sum -= y[i]
    jmp .line2_loop

.line2_done:

    ; Вычисляем среднее арифметическое
    mov rax, rbx
    cqo
    idiv r13                           ; rax = sum / count
    mov rbx, rax                       ; сохраняем результат

    ; Вывод: <имя_файла>: <среднее>
    ; Вычисляем длину имени файла
    mov rdi, r12
    xor edx, edx
.fn_len:
    cmp byte [rdi + rdx], 0
    je .fn_done
    inc rdx
    jmp .fn_len
.fn_done:
    mov eax, 1                         ; sys_write
    mov edi, 1                         ; stdout
    mov rsi, r12                       ; имя файла
    syscall

    ; Выводим ": "
    mov eax, 1
    mov edi, 1
    lea rsi, [rel colon]
    mov edx, 2
    syscall

    ; Выводим число и перенос строки '\n'
    mov rax, rbx
    call print_int

    ; Завершение программы (sys_exit 0)
    mov eax, 60
    xor edi, edi
    syscall

; ---------------------------------------------------------------
; read_int: считывает знаковое число из [rsi], сдвигает rsi
; Возвращает число в rax
; ---------------------------------------------------------------
read_int:
    xor eax, eax
    xor r8d, r8d                       ; r8d = 1 для отрицательных чисел
    cmp byte [rsi], '+'
    je .plus
    cmp byte [rsi], '-'
    jne .digits
    mov r8d, 1
.plus:
    inc rsi
.digits:
    movzx edx, byte [rsi]
    sub edx, '0'
    cmp edx, 9
    ja .done
    imul rax, rax, 10
    add rax, rdx
    inc rsi
    jmp .digits
.done:
    test r8d, r8d
    jz .ret
    neg rax
.ret:
    ret

; ---------------------------------------------------------------
; print_int: выводит целое число rax со знаком и '\n'
; ---------------------------------------------------------------
print_int:
    lea rdi, [rel numbuf + 31]
    mov byte [rdi], 10                 ; символ переноса строки '\n'
    mov r8, rax                        ; сохраняем знак числа
    test rax, rax
    jns .pos
    neg rax
.pos:
    mov r9, 10
.loop:
    xor edx, edx
    div r9
    add dl, '0'
    dec rdi
    mov [rdi], dl
    test rax, rax
    jnz .loop

    test r8, r8
    jns .print
    dec rdi
    mov byte [rdi], '-'
.print:
    lea rdx, [rel numbuf + 32]
    sub rdx, rdi                       ; вычисляем длину строки
    mov eax, 1                         ; sys_write
    mov rsi, rdi                       ; указатель на начало строки
    mov edi, 1                         ; stdout
    syscall
    ret

section .data
colon:      db ": "

section .bss
buf:        resb BUFSIZE + 1
numbuf:     resb 32
