import sys
from source.CortexM0AssemblerInterpreter import CortexM0AssemblerInterpreter
from source.Lexer import Lexer
sys.setrecursionlimit(0x100000)
cor = CortexM0AssemblerInterpreter("conv_char.asm", "conv_char")


print(cor.conf_char("Z"))
print(cor.conf_char("z"))
print(cor.conf_char("a"))
print(cor.conf_char("A"))
print(cor.conf_char("f"))

a = "nO tHiS iS patRIcK"

print(''.join(list(map(cor.conf_char, a))))


add_one = CortexM0AssemblerInterpreter("add_one.asm", "add_one")
print(add_one.run_funtion("add_one", 1))