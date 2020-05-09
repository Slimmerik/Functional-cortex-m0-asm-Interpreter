from source.Type import tokenType
from source.Wraps import prt



class ASTnode:
    def __init__(self, nme):
        self.name = nme
    def __str__(self):
        pass


class directiveNode(ASTnode):
    def __init__(self, nme, val, nxt):
        super().__init__(nme)
        self.value = val
        self.next = nxt
    def __str__(self):
        pass

class instructionNode(ASTnode):
    def __init__(self, name: str, args: list):
        super().__init__( name)
        self.arguments = args
    def __str__(self):
        pass

class Parser:
    def __init__(self):
        pass
    @prt
    def eval_directive(self, s: list, direcListLoc: list, prod: dict = {}, index: int = 0) -> dict:
        if len(direcListLoc) < index+1:
            return prod
        elif "directives" not in prod:
            return self.eval_directive(s, direcListLoc, {**prod, **{"directives": []}}, index)
        elif direcListLoc[index] is True:
            if direcListLoc[index+1] is False:
                if len(prod["directives"]) is not 0:
                    return self.eval_directive(s, direcListLoc, {**prod, **{"directives": prod["directives"] + [
                        directiveNode(s[index]["value"], s[index+1]["value"], prod["directives"][-1])]}}, index+1)
                elif len(prod["directives"]) is 0:
                    return self.eval_directive(s, direcListLoc, {**prod, **{"directives": prod["directives"] + [
                        directiveNode(s[index]["value"], s[index + 1]["value"], None)]}}, index + 1)
            else:
                return self.eval_directive(s, direcListLoc, prod, index+1)
        elif direcListLoc[index] is False:
            return self.eval_directive(s, direcListLoc, prod, index + 1)

    @prt
    def eval_code_block(self, s: list, blockListLoc: list, prod: dict = {}, index: int = 0, activeLabel: str = None) -> dict:
        if len(blockListLoc) < index + 1:
            return prod
        elif blockListLoc[index] is False and activeLabel is None:
            return self.eval_code_block(s, blockListLoc, prod, index + 1, activeLabel)
        elif blockListLoc[index] is False and activeLabel is not None:
            if s[index]["value"] in tokenType.keywords.value:
                if s[index]["value"] in tokenType.threeArgsKeywords.value:
                    return self.eval_code_block(s, blockListLoc, {**prod,**{activeLabel: prod[activeLabel] + [instructionNode(s[index]["value"],[s[index+1]["value"], s[index+3]["value"], s[index+5]["value"]])]}}, index + 6, activeLabel)
                elif s[index]["value"] in tokenType.twoArgsKeywords.value:
                    return self.eval_code_block(s, blockListLoc, {**prod,**{activeLabel: prod[activeLabel] + [instructionNode(s[index]["value"],[s[index+1]["value"], s[index+3]["value"]])]}}, index + 4, activeLabel)
                elif s[index]["value"] in tokenType.OneArgsKeywords.value:
                    return self.eval_code_block(s, blockListLoc, {**prod,**{activeLabel: prod[activeLabel] + [instructionNode(s[index]["value"],[s[index+1]["value"]])]}}, index + 2, activeLabel)
                elif s[index]["value"] in tokenType.pushPopKeywords.value:
                    return self.eval_code_block(s, blockListLoc, {**prod,**{activeLabel: prod[activeLabel] + [instructionNode(s[index]["value"],[])]}}, index + 8, activeLabel)
                else:
                    return self.eval_code_block(s, blockListLoc, prod, index + 1, activeLabel)
            else:
                return self.eval_code_block(s, blockListLoc, prod, index + 1, activeLabel)
        elif blockListLoc[index] is True and activeLabel is None:
            return self.eval_code_block(s, blockListLoc, {**prod, **{s[index - 1]["value"]: []}}, index + 1, s[index - 1]["value"])
        elif blockListLoc[index] is True and activeLabel is not None:
            return self.eval_code_block(s, blockListLoc, {**prod, **{s[index - 1]["value"]: []}}, index + 1, s[index - 1]["value"])

    @prt
    def make_ast_from_token_list(self, s: list,tempProd: dict = {}, pos: str = "start") -> dict:
        if pos is "start":
            return self.make_ast_from_token_list(s, self.eval_directive(s, list(map(lambda x: x["tokenType"] is tokenType.directive, s)),tempProd), "blocks")
        elif pos is "blocks":
            return self.make_ast_from_token_list(s, self.eval_code_block(s,list(map(lambda x: x["tokenType"] is tokenType.separator and x["value"] is ":", s)),tempProd), "finish")
        elif pos is "finish":
            return tempProd