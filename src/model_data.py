# Model java class

class ModelData():
    def __init__(self, name, desc, params, rules):
        self.name = name.capitalize()
        self.desc = desc.capitalize()
        self.params = params
        self.rules = rules

        self.model = ''

    def createModel(self):
        res = '/**\n* '+self.desc+'\n*/'
        res += '\npublic class '
        res += self.name + '{'
        # attributes
        for data in self.params:
            res += '\n\t private ' + self.extractType(data[1]) + ' ' + data[0]+';'
        # methods
        for rule in self.rules:
            res += '\n\t public ' + self.extractType(rule[2]) + ' ' + rule[0]+'('+ rule[1]+')  {'
            res += '\n\t\t// method definition'
            res += '\n\t }'
        res += '\n}'

        # save model class
        self.model = res

    def getModel(self):
        return self.model

    def getName(self):
        return self.name

    def extractType(self, type):
        if (type == 'text'):
            return 'String'
        elif (type == 'number'):
            return 'int'
        elif (type == 'decimal'):
            return 'double'
        else:
            return type
