from source.Lexer import Lexer
from source.Parser import Parser
from source.Wraps import prt
import re


class CortexM0AssemblerInterpreter:
    def __init__(self, fileLoc: str, fucName: str):
        self.fucName = fucName
        self.le = Lexer()
        self.pa = Parser()

        self.ast = self.pa.make_ast_from_token_list(self.le.Token_list_from_program(self.le.string_from_file(fileLoc)))

        self.machine = {"r0": 0, "r1": 0, "r2": 0, "r3": 0, "r4": 0, "r5": 0, "r6": 0, "r7": 0, "r8": 0, "r9": 0,
                        "r10": 0, "r11": 0, "r12": 0,
                        "Z": 0, "C": 0, "N": 0, "V": 0}

        self.instructionDict = {"ldrb": self.ldrb, "cmp": self.cmp, "sub": self.sub, "add": self.add, "b": self.b,
                                "bge": self.bge, "ble": self.ble, "pop": self.pop, "push": self.push}

    def __str__(self):
        return "".join([str(self.machine), "\n",
                        str(self.ast)]
                       )

    @prt
    def ldrb(self, machine: dict, args: list, execList: list) -> tuple:
        return {**machine, **{args[0]: ord(args[1][2])}}, execList[1:]

    @prt
    def cmp(self, machine: dict, args: list, execList: list) -> tuple:
        return {**machine, **{"N": 1 if int(machine[args[0]]) - int(machine[args[1]]) < 0 else 0,
                              "Z": 1 if int(machine[args[0]]) - int(machine[args[1]]) == 0 else 0
                              }}, execList[1:]

    @prt
    def sub(self, machine: dict, args: list, execList: list) -> tuple:
        return {**machine, **{args[0]: int(machine[args[1]]) - int(machine[args[2]])}}, execList[1:]

    @prt
    def add(self, machine: dict, args: list, execList: list) -> tuple:
        if re.match(r'#immed\d*', args[1]):
            return {**machine, **{args[0]: int(args[1][6:]) + int(machine[args[2]])}}, execList[1:]
        elif re.match(r'#immed\d*', args[2]):
            return {**machine, **{args[0]: int(machine[args[1]]) + int(args[2][6:])}}, execList[1:]
        elif re.match(r'#immed\d*', args[1]) and re.match(r'#immed\d*', args[2]):
            return {**machine, **{args[0]: int(args[1][6:]) + int(args[2][6:])}}, execList[1:]
        else:
            return {**machine, **{args[0]: int(machine[args[1]]) + int(machine[args[2]])}}, execList[1:]

    @prt
    def b(self, machine: dict, args: list, execList: list) -> tuple:
        return machine, self.ast[args[0]]

    @prt
    def bge(self, machine: dict, args: list, execList: list) -> tuple:
        return machine, execList[1:] if machine["N"] is 1 else self.ast[args[0]]

    @prt
    def ble(self, machine: dict, args: list, execList: list) -> tuple:
        return machine, execList[1:] if machine["N"] is 0 else self.ast[args[0]]

    @prt
    def pop(self, machine: dict, args: list, execList: list) -> tuple:
        return machine, []

    @prt
    def push(self, machine: dict, args: list, execList: list) -> tuple:
        return machine, execList[1:]

    @prt
    def handle_directive(self, ast: dict, machine: dict, dirList: list = None) -> dict:
        if dirList is None:
            return self.handle_directive(ast, machine, ast["directives"])
        elif dirList is not None and len(dirList) > 0:
            return self.handle_directive(ast, {**machine, **{dirList[0].name: dirList[0].value}}, dirList[1:])
        elif len(dirList) is 0:
            return machine

    @prt
    def cycle_ast_nodes(self, ast: dict, machine: dict, execList: list = None) -> dict:
        if execList is None:
            return self.cycle_ast_nodes(ast, machine, ast[machine[".global"]])
        elif execList is not None and len(execList) > 0:
            return self.cycle_ast_nodes(ast, *self.instructionDict[execList[0].name](machine, execList[0].arguments,
                                                                                     execList))
        elif len(execList) is 0:
            return machine

    @prt
    def run_funtion(self, funName: str, value: int, machine: dict = None, state: str = "direc") -> str:
        if state is "direc":
            return self.run_funtion(funName, value, self.handle_directive(self.ast, {**self.machine, **{"r0": value}}),
                                    "cycle")
        elif state is "cycle" and funName == machine[".global"]:
            return self.run_funtion(funName, value, self.cycle_ast_nodes(self.ast, machine), "return")
        elif state is "return":
            return machine["r0"]

    @prt
    def conf_char(self, args: str) -> str:
        return chr(self.run_funtion(self.fucName, ord(args)))
