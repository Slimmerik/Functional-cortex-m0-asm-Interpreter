        .cpu cortex-m0
        .text
        .align 1
        .global add_one

add_one:
        push { r1 - r7 , lr }
        add r0, r0, #immed1
        b return

return:
        pop { r1 - r7 , pc }