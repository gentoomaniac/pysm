# PySM
## Memory example
Some random writes to memory
```
2016-05-08 01:02:31,694 t_memory     DEBUG    Testing memory access ...
2016-05-08 01:02:32,324 t_memory     DEBUG    0000h: 23 59 54 D9 76 DE CC 85 22 00 83 EB E9 25 90 00     #YTÙvÞÌ".ëé%.
2016-05-08 01:02:32,324 t_memory     DEBUG    0010h: 00 4C 97 51 22 B5 00 00 AA 86 90 F4 00 1F 00 00     .LQ"µ..ªô...
2016-05-08 01:02:32,324 t_memory     DEBUG    0020h: 8C B4 8C 1F D0 8B 43 00 ED 01 C4 13 00 59 00 57     ´ÐC.íÄ.Y.W
2016-05-08 01:02:32,324 t_memory     DEBUG    0030h: 00 00 00 E1 00 85 E0 8A A4 00 00 B0 79 24 5A D5     ...á.à¤..°y$ZÕ
2016-05-08 01:02:32,324 t_memory     DEBUG    0040h: BE 00 FE C1 A7 21 12 E9 00 00 60 00 90 1E E1 D0     ¾.þÁ§!é..`.áÐ
2016-05-08 01:02:32,325 t_memory     DEBUG    0050h: 05 9C F1 A1 00 F0 E3 47 99 1D C3 2B FA 49 28 A2     ñ¡.ðãGÃ+úI(¢
```

## Everything working together
1. allocating memory
2. writing a string to the allocated block
3. setting registers
4. calling an interrupt to call sys_write()
5. free memory
```python
LOG.debug("Testing sys_write() ...")
core = PySM_Core()

msg = [ord(c) for c in "Hello!"]
msg.append(0x00)
addr = stdlib.malloc(len(msg))
length = len(msg)

core.set_memory_range(addr, msg)

core.EAX = 4        # sys_write
core.EBX = 2        # stderr
core.ECX = addr
core.EDX = length

core.interrupt(0x80)      # handover to core

stdlib.free(addr)
```
```
2016-05-08 01:02:32,605 t_memory     DEBUG    Testing sys_write() ...
2016-05-08 01:02:32,605 stdlib       DEBUG    Allocated 7 bytes at address 0027
2016-05-08 01:02:32,606 stdlib       DEBUG    Memory allocation table: {"0": 15, "16": 31, "32": 38, "39": 45, "48": 63, "64": 79, "80": 95, "96": 105}
2016-05-08 01:02:32,606 core         DEBUG    EAX is now 4
2016-05-08 01:02:32,606 core         DEBUG    EBX is now 2
2016-05-08 01:02:32,606 core         DEBUG    ECX is now 39
2016-05-08 01:02:32,606 core         DEBUG    EDX is now 7
2016-05-08 01:02:32,606 core         DEBUG    Printing to screen ...
2016-05-08 01:02:32,606 core         ERROR    Hello! 
2016-05-08 01:02:32,606 stdlib       DEBUG    Freed 39 bytes at address 0027
2016-05-08 01:02:32,606 stdlib       DEBUG    Memory allocation table: {"0": 15, "16": 31, "32": 38, "48": 63, "64": 79, "80": 95, "96": 105}
```
