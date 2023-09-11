class Utilities:
    def __init__(self, app):
        self.screenSize = app.primaryScreen().size()
        self.screenWidth = self.screenSize.width()
        self.screenHeight = self.screenSize.height()    
       
        self.propWidth = self.screenWidth / 2000
        self.propHeight = self.screenHeight / 1500

        self.manual = '\
            isless(a, b) is a less than b\n\n\
            ismore(a, b) is a more than b\n\n\
            equals(a, b) is a equal to b\n\n\
            between(a, b) does a fall in the range b-c\n\n\
            or extend another condition\n\n\
            << close a process group\n\n\
            loop(a) iterate following process a times\n\n\
            out a return a as result\n\n\
            a: b assign b to a \n\n\
                '
       
    def computeX(self,width):
        return int(width * self.propWidth )
    
    def computeY(self, height):
        return int(height * self.propHeight)
    
    def computeXY(self, width,height):
        return int(width * self.propWidth), int(height * self.propHeight)
    
    def getManual(self):
        return self.manual

     


        

