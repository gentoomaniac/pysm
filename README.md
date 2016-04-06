=== Example Output ===
```
2016-04-07 00:05:33,314 interpreter  DEBUG    Interpreting 4 instructions
2016-04-07 00:05:33,314 interpreter  DEBUG    MOV EAX, 123
2016-04-07 00:05:33,314 core         DEBUG    EAX is now 123
2016-04-07 00:05:33,314 interpreter  DEBUG    
        EAX:                          1111011
        EBX:                                0
        ECX:                                0
        EDX:                                0
        
2016-04-07 00:05:33,314 interpreter  DEBUG    MOV EBX, 302
2016-04-07 00:05:33,315 core         DEBUG    EBX is now 302
2016-04-07 00:05:33,315 interpreter  DEBUG    
        EAX:                          1111011
        EBX:                        100101110
        ECX:                                0
        EDX:                                0
        
2016-04-07 00:05:33,315 interpreter  DEBUG    MOV ECX, 1234132
2016-04-07 00:05:33,315 core         DEBUG    ECX is now 1234132
2016-04-07 00:05:33,315 interpreter  DEBUG    
        EAX:                          1111011
        EBX:                        100101110
        ECX:            100101101010011010100
        EDX:                                0
        
2016-04-07 00:05:33,315 interpreter  DEBUG    MOV DH, 1
2016-04-07 00:05:33,315 core         DEBUG    DH is now 1
2016-04-07 00:05:33,315 interpreter  DEBUG    
        EAX:                          1111011
        EBX:                        100101110
        ECX:            100101101010011010100
        EDX:                        100000000
```