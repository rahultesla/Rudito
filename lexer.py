import symbols


class code():
    def __init__(self,code,exp = symbols.symbol):
        self.code = code
        self.exp = exp
        self.tokens = []
    def clean(self,element = " "):
        p = 0
        while p<len(self.tokens):
            if self.tokens[p] == element and self.tokens[p+1] == element:
                del self.tokens[p+1]
            else:
                p+=1
    def join(self,element1,element2):
        p = 0
        while p<len(self.tokens):
            if self.tokens[p] == element1 and self.tokens[p+1] == element2:
                self.tokens[p] = self.tokens[p]+self.tokens[p+1]
                del self.tokens[p+1]
            else:
                p+=1
    
    def lex(code,exp=sym):
        head = 0
        tail = 0
        while head <= len(code):
            change = 0
            for i in sym:
                if i in code[tail:head]:
                    change = 1
                    if self.tokens[len(tokens)-1] in code[tail:head]:
                        self.tokens.append(i)
                    else:
                        self.tokens.append(code[tail:head-len(i)])
                        self.tokens.append(i)    
                    break
            if change:
                tail = head
            else:
                head+=1
        
        

        

        
        

    
    
        


