import sys
import platform
def knit(liste,i,j):
    strng = ''
    for i in range(i+1,len(liste)):
        if liste[i] == j:
            return strng,i
        else:
            strng+=liste[i]
 
class code():
    def __init__(self,code):
        self.code = code       #full text
        self.tokens = []       #list of tokens:lineid,assign,condition,gotoid
        self.tokendescpt = []  #token type to corresponding tokens list
        self.builtins = {'show':'prompt','ask':['var','prompt'],'int':'value','bool':'value','float':'value','str':'value'} #inbuilt functions with params
        self.gettag = ['/','/'] #lineid delimiter
        self.assigntag = ['[',']'] #assign delimiter
        self.gototag = ['|','|'] #gotoid delimiter
        self.commenttag = ['#','#'] #comment delimiter
        self.condtag = ['(',')'] #condition delimiter
        self.var_dict = {} #dict of variables with values
        self.returnpos = [] #return positions
    
    
    
    def tokenize(self):
        i=-1
        if len(self.code) == 0:
            return 0
        while i < len(self.code)-1:
            i+=1
            if self.code[i] == self.gettag[0]:
                key,pos = knit(self.code,i,self.gettag[1])
                self.tokendescpt.append('lineid')
            elif self.code[i] == self.assigntag[0]:
                key,pos = knit(self.code,i,self.assigntag[1])
                self.tokendescpt.append('assign')
            elif self.code[i] == self.gototag[0]:
                key,pos = knit(self.code,i,self.gototag[1])
                self.tokendescpt.append('gotoid')
            elif self.code[i] == self.commenttag[0]:
                key,pos = knit(self.code,i,self.commenttag[1])
                self.tokendescpt.append('comment')
            else:
                continue
            self.tokens.append(key)
            i = pos
        m=-1
        while m < len(self.tokens)-1:
            m+=1
            if self.tokendescpt[m] == 'assign':
                al = self.tokens[m]
                for i in range(len(al)):
                    if al[i] == self.condtag[0]:
                        key,pos = knit(al,i,self.condtag[1])
                        aw1 = al[0:i]
                        aw2 = key
                        aw3 = al[pos+1:len(al)]
                        del self.tokens[m]
                        del self.tokendescpt[m]
                        self.tokens.insert(m,aw3)
                        self.tokens.insert(m,aw2)
                        self.tokens.insert(m,aw1)
                        self.tokendescpt.insert(m,'assignf')
                        self.tokendescpt.insert(m,'condition')
                        self.tokendescpt.insert(m,'assignt')
                        break
        

    def clean(self):
        for i in range(len(self.tokens)):
            if "'" not in self.tokens[i]:
                self.tokens[i] = ''.join(self.tokens[i].split())
                if self.tokendescpt[i] == 'lineid':
                    self.var_dict[self.tokens[i]] = self.tokens[i]
            else:
                t = 0
                for j in range(len(self.tokens[i])):
                    if self.tokens[i][j] == "'":
                        part1 = self.tokens[i][0:j]
                        part1 = ''.join(part1.split())
                        for k in range(j+1,len(self.tokens[i])):
                            if self.tokens[i][k] == "'":
                                part2 = self.tokens[i][j:k+1]
                                part3 = self.tokens[i][k+1:len(self.tokens[i])]
                                part3 = ''.join(part3.split())
                                t=1
                                break
                    if t==1:
                        break
                self.tokens[i] = part1+part2+part3  
    
    def assign(self,i):
        al = self.tokens[i]
        ver = self.var_dict
        for i in range(len(al)):
            if al[i] == ':':
                value = eval(al[i+1:len(al)],ver)
                self.var_dict[al[0:i]] = value
                break
    def goto(self,i):
        al = self.tokens[i]
        if '&return' in al:
            al = al[0:len(al)-7]
            self.returnpos.append(i+1)
        if al == 'return':
            newi = self.returnpos[len(self.returnpos)-1]
            del self.returnpos[len(self.returnpos)-1]
            return newi
        if al == 'goto':
            al = self.var_dict['goto']
        for j in range(len(self.tokendescpt)):
            if self.tokendescpt[j] == 'lineid':  
                if al == self.tokens[j]:
                    return j

        return i+1
    def run(self):
        end = 0
        pos = 0
        for i in range(len(self.tokens)):
            if self.tokens[i] == 'start' and self.tokendescpt[i] == 'lineid':
                pos = i+1
        
        if len(self.code) == 0:
            return 0
        while pos < len(self.tokens):
            if self.tokendescpt[pos] == 'assign':
                code.assign(self,pos)
                pos+=1
            elif self.tokendescpt[pos] == 'gotoid':
                if self.tokens[pos] in self.builtins:
                    ''' builtin functions '''
                    if self.tokens[pos] == 'show':
                        print(self.var_dict['prompt'])
                    elif self.tokens[pos] == 'ask':
                        self.var_dict[self.var_dict['var']] = input(self.var_dict[self.builtins['ask'][1]])
                    elif self.tokens[pos] == 'int':
                        self.var_dict['value'] = int(eval(self.var_dict['value'],self.var_dict))
                    elif self.tokens[pos] == 'float':
                        self.var_dict['value'] = float(eval(self.var_dict['value'],self.var_dict))
                    elif self.tokens[pos] == 'bool':
                        self.var_dict['value'] = bool(eval(self.var_dict['value'],self.var_dict))
                    elif self.tokens[pos] == 'str':
                        self.var_dict['value'] = str(eval(self.var_dict['value'],self.var_dict))
                    pos+=1
                elif self.tokens[pos] == 'end':
                    break
                else:
                    pos = code.goto(self,pos)
            elif self.tokendescpt[pos] == 'condition':
                ver = self.var_dict
                if eval(self.tokens[pos],ver):
                    code.assign(self,pos-1)
                else:
                    code.assign(self,pos+1)
                pos+=2
            else:
                pos+=1






if __name__ == "__main__":
    try:
        filename = sys.argv[1]
        if filename[len(filename)-4:len(filename)] != '.rdt':
            print('This is not Rudito file')
            sys.exit()
        filee = open(filename,'r')
        text = filee.read()
        filee.close()
        q = code(code=text)
        try:
            q.tokenize()
            q.clean()
        except:
            print('invalid syntax')
            sys.exit()
        try:
            q.run()
        except:
            print('runtime error')
            sys.exit()
    except:
        print("Rudito 1.0.0 "+str(platform.system())+" "+str(platform.release())+" "+str(platform.architecture()[0]))
        print("Type '|help|','|credits|' for more information")
        aa = ''
        w = code(code=aa)
        while aa != '|end|':
            aa = input('$$$ ')
            if aa == '|credits|':
                ff = open('credits.txt','r')
                m = ff.read()
                ff.close()
                print(m)
                continue
            elif aa == '|help|':
                ff = open('help.txt','r')
                m = ff.read()
                ff.close()
                print(m)
                continue
            try:
                ver = w.var_dict
                x = eval(aa,ver)
                print(x)
            except:
                w.code = aa
                try:
                    w.tokenize()
                    w.clean()
                except:
                    print('invalid syntax')
                    continue
                try:
                    w.run()
                except:
                    print('runtime error')



