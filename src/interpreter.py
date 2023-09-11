class Interpreter:
    def isLess(self, a, b):
        return f'\n\t\tif ({a} < {b})'+ ' {'
    
    def isMore(self, a, b):
        return f'\n\t\tif ({a} > {b})'+ ' {'
    
    def equals(self, a, b):
        return f'\n\t\tif ({a} == {b})'+ ' {'
    
    def between(self, a, b, c):
        return f'\n\t\tif ({b} <= {a} && {a} <= {c})'+ ' {'
    
    def appendElse(self):
        return '\n\t\t else '
    
    def imply(self, data):
        return f'\n\t\t\t{data};'
    
    def finalize(self):
        return f'\n\t\t' + '}'
    
    def loop(self, count):
        return f'\n\t\tfor (int i=0; i<{count}; i++)'+' {'

    def out(self, data):
        return f'\n\t\treturn {data}'
    
    def assign(self, var, data):
        return f'\n\t\t\t{var} = {data};'
    
    def interprete(self, str):
        result = ''

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
            elif ('between' in item.lower()):
                result += self.between(item[start+1 : comma], item[comma+1 : rcomma], item[rcomma+1 : end])
            elif ('or' in item.lower()):
                result += self.appendElse()
            elif ('>>' in item.lower()):
                result += self.imply(item.replace('>>', '').strip())
            elif ('<<' in item.lower()):
                result += self.finalize()
            elif ('loop' in item.lower()):
                result += self.loop(item[start+1 : end])
            elif ('out' in item.lower()):
                result += self.out(item.replace('out', '').strip())
            else:
                result += self.imply(item.strip())
                    
        return result