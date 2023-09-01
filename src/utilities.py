class Utilities:
    def __init__(self, app):
        self.screenSize = app.primaryScreen().size()
        self.screenWidth = self.screenSize.width()
        self.screenHeight = self.screenSize.height()    
       
        self.propWidth = self.screenWidth / 2000
        self.propHeight = self.screenHeight / 1500
       
    def computeX(self,width):
        return int(width * self.propWidth )
    
    def computeY(self, height):
        return int(height * self.propHeight)
    
    def computeXY(self, width,height):
        return int(width * self.propWidth), int(height * self.propHeight)

     


        

