from enum import Enum


class tokenType(Enum):
    keyword = "keyword"
    globalKeyword = "globalKeyword"
    separator = "separator"
    immed = "immed"
    register = "register"
    literal = "literal"
    directive = "directive"
    point_to = "point_to"
    identifier = "identifier"
    keywords = ["push", "pop", "ldrb", "cmp", "bge", "ble", "b", "sub", "add"]
    threeArgsKeywords = ["sub", "add"]
    twoArgsKeywords = ["cmp", "ldrb"]
    OneArgsKeywords = ["bge", "ble", "b"]
    pushPopKeywords = ["push", "pop"]
    globalKeywords = [".cpu", ".global"]
    separators = [":", " - ", ",", "{", "}"]
    registers = ["r0", "r1", "r2", "r3", "r4", "r5", "r6", "r6", "r7", "r8", "r9", "r10", "r11", "r12", "lr","pc", "sp"]
