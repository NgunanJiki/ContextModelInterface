import re


class Interpreter:
    def __init__(self):
        self.indent = '\n\t\t'

    def isLess(self, a, b):
        return f'{self.indent}if ({a} < {b})'+ ' {'
    
    def isMore(self, a, b):
        return f'{self.indent}if ({a} > {b})'+ ' {'
    
    def equals(self, a, b):
        return f'{self.indent}if ({a} == {b})'+ ' {'
    
    def truth(self, a):
        return f'{self.indent}if ({a} == true)'+ ' {'
    
    def orCombine(self, args):
        res = ''
        for i in args.split(','):
            res+= i+'||'
        res = res.rstrip('||')
        return f'{self.indent}if ({res})'+ ' {'
    
    def andCombine(self, args):
        res = ''
        for i in args.split(','):
            res+= i+'&&'
        res = res.rstrip('&&')
        return f'{self.indent}if ({res})'+ ' {'
    
    def between(self, a, b, c):
        return f'{self.indent}if ({b} <= {a} && {a} <= {c})'+ ' {'
    
    def appendElse(self):
        return f'{self.indent}else'+ ' {'
    
    def imply(self, data):
        return f'{self.indent}{data};'
    
    def finalize(self):
        return f'{self.indent}' + '}'
    
    def loop(self, count):
        return f'{self.indent}for (int i=0; i<{count}; i++)'+' {'

    def out(self, data):
        return f'{self.indent}return {data};'
    
    def assign(self, var, data):
        return f'{self.indent}{var} = {data};'
    
    def interprete(self, str):
        result = ''
        prev = ''

        data = str.splitlines()

        for item in data:
            start = item.find('(')
            comma = item.find(',')
            rcomma = item.rfind(',')
            end =  item.find(')')
            colon =  item.find(':')

            if (':' in item):
                result += self.assign(item[0 : colon], item[colon+1:])
            elif ('isless' in item.lower()):
                result += self.isLess(item[start+1 : comma], item[comma+1 : end])
            elif ('ismore' in item.lower()):
                result += self.isMore(item[start+1 : comma], item[comma+1 : end])
            elif ('equals' in item.lower()):
                result += self.equals(item[start+1 : comma], item[comma+1 : end])
            elif ('truth' in item.lower()):
                result += self.truth(item[start+1 : end])
            elif ('orcombine' in item.lower()):
                result += self.orCombine(item[start+1 : end])
            elif ('andcombine' in item.lower()):
                result += self.andCombine(item[start+1 : end])
            elif ('between' in item.lower()):
                result += self.between(item[start+1 : comma], item[comma+1 : rcomma], item[rcomma+1 : end])
            elif ('or' in item.lower()):
                result += self.appendElse()
            elif ('>>' in item.lower()):
                result += self.imply(item.replace('>>', '').strip())
            elif ('<<' in item.lower()):
                self.indent = self.indent[:-1]
                result += self.finalize()
            elif ('loop' in item.lower()):
                result += self.loop(item[start+1 : end])
            elif ('out' in item.lower()):
                result += self.out(item.replace('out', '').strip())
            else:
                result += self.imply(item.strip())

            if (result[-1] == '{' and 'or' not in prev):
                self.indent += '\t'

            prev = item

        result = re.sub(r'else {\s*if', 'else if', result)                    
        return result
    

class PyInterpreter:
    def __init__(self):
        self.indent = '\n\t\t'
    
    def isLess(self, a, b):
        return f'{self.indent}if ({a} < {b}):'
    
    def isMore(self, a, b):
        return f'{self.indent}if ({a} > {b}):'
    
    def equals(self, a, b):
        return f'{self.indent}if ({a} == {b}):'
    
    def truth(self, a):
        return f'{self.indent}if ({a} == True):'
    
    def orCombine(self, args):
        res = ''
        for i in args.split(','):
            res+= i+'or'
        res = res.rstrip('or')
        return f'{self.indent}if ({res}):'
    
    def andCombine(self, args):
        res = ''
        for i in args.split(','):
            res+= i+'and'
        res = res.rstrip('and')
        return f'{self.indent}if ({res}):'
    
    def between(self, a, b, c):
        return f'{self.indent}if ({b} <= {a} && {a} <= {c}):'
    
    def appendElse(self):
        return f'{self.indent}else:'
    
    def imply(self, data):
        return f'{self.indent}{data};'
    
    def loop(self, count):
        return f'{self.indent}for i in range({count}):'

    def out(self, data):
        return f'{self.indent}return {data}'
    
    def assign(self, var, data):
        return f'{self.indent}{var} = {data}'
    
    def interprete(self, str):
        result = ''
        prev = ''

        data = str.splitlines()

        for item in data:
            start = item.find('(')
            comma = item.find(',')
            rcomma = item.rfind(',')
            end =  item.find(')')
            colon =  item.find(':')

            if (':' in item):
                result += self.assign(item[0 : colon], item[colon+1:])
            elif ('isless' in item.lower()):
                result += self.isLess(item[start+1 : comma], item[comma+1 : end])
            elif ('ismore' in item.lower()):
                result += self.isMore(item[start+1 : comma], item[comma+1 : end])
            elif ('equals' in item.lower()):
                result += self.equals(item[start+1 : comma], item[comma+1 : end])
            elif ('truth' in item.lower()):
                result += self.truth(item[start+1 : end])
            elif ('orcombine' in item.lower()):
                result += self.orCombine(item[start+1 : end])
            elif ('andcombine' in item.lower()):
                result += self.andCombine(item[start+1 : end])
            elif ('between' in item.lower()):
                result += self.between(item[start+1 : comma], item[comma+1 : rcomma], item[rcomma+1 : end])
            elif ('or' in item.lower()):
                result += self.appendElse()
            elif ('>>' in item.lower()):
                result += self.imply(item.replace('>>', '').strip())
            elif ('<<' in item.lower()):
                self.indent = self.indent[:-1]
            elif ('loop' in item.lower()):
                result += self.loop(item[start+1 : end])
            elif ('out' in item.lower()):
                result += self.out(item.replace('out', '').strip())
            else:
                result += self.imply(item.strip())

            if (result[-1] == ':' and 'or' not in prev):
                self.indent += '\t'

            prev = item
            
        result = re.sub(r'else:\s*if', 'elif', result)
        return result