        .cpu cortex-m0
        .text
        .align 1
        .global conv_char

conv_char:
        push { r1 - r7 , lr }
        ldrb r1, ='Z'
        ldrb r2, ='z'
        ldrb r3, ='A'
        ldrb r4, ='a'
        cmp r0, r4
        bge to_upper_check2
        cmp r0, r1
        ble to_lower_check2
        b return

to_upper_check2:
        cmp r0, r2
        ble to_upper_conv
        b return

to_upper_conv:
        sub r5, r0, r4
        add r0, r5, r3
        b return

to_lower_check2:
        cmp r0, r3
        bge to_lower_conv
        b return

to_lower_conv:
        sub r5, r0, r3
        add r0, r5, r4
        b return

return:
        pop { r1 - r7 , pc }