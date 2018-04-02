# models.py
# Xiaoyu Yan (xy97) and Jeremy Glassman (jrg348)
# 12/04/16
"""Models module for Breakout

This module contains the model classes for the Breakout game. That is anything that you
interact with on the screen is model: the paddle, the ball, and any of the bricks.

Technically, just because something is a model does not mean there has to be a special 
class for it.  Unless you need something special, both paddle and individual bricks could
just be instances of GRectangle.  However, we do need something special: collision 
detection.  That is why we have custom classes.

You are free to add new models to this module.  You may wish to do this when you add
new features to your game.  If you are unsure about whether to make a new class or 
not, please ask on Piazza."""
import random # To randomly generate the ball velocity
from constants import *
from game2d import *


# PRIMARY RULE: Models are not allowed to access anything except the module constants.py.
# If you need extra information from Play, then it should be a parameter in your method, 
# and Play should pass it as a argument when it calls the method.


class Paddle(GRectangle):
    """An instance is the game paddle.
    
    This class contains a method to detect collision with the ball, as well as move it
    left and right.  You may wish to add more features to this class.
    
    The attributes of this class are those inherited from GRectangle.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    _paddleX = x position of the paddle
    """
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getPaddleX(self):
        """Get's the paddle's x position
        """
        return self._paddleX
    
    def setPaddleX(self,x):
        """Sets the paddle's x position
       
        Parameter x: the specific x position  on the screen to change to
        Precondition: x is an int or a float
        """
        self._paddleX = x

    # INITIALIZER TO CREATE A NEW PADDLE
    def __init__(self, x):
        self._paddleX = x
        GRectangle.__init__(self,x=self._paddleX,y=PADDLE_OFFSET,
                            width=PADDLE_WIDTH,height = PADDLE_HEIGHT,
                            fillcolor = colormodel.BLACK)
        
        
    # METHODS TO MOVE THE PADDLE AND CHECK FOR COLLISIONS
    def movePaddle(self, direction):
        """Moves the paddle by changing the paddle's x position
        
        Parameter direction: direction to move the paddle
        Precondition: direction is a valid direction from input and is a string
        """
        if direction == "left":
            self._paddleX -= PADDLE_SPEED
        if direction == "right":
            self._paddleX += PADDLE_SPEED
            
    def collidesP(self,ball):
        """Returns: True if the ball collides with this paddle
        
        Parameter ball: The ball to check
        Precondition: ball is of class Ball"""
        PADDLE_COL = [
            [ball.x,ball.y],
            [ball.x+ball.width/2, ball.y+ball.height/2],
            [ball.x+ball.width/2, ball.y-ball.height/2],
            [ball.x-ball.width/2, ball.y-ball.height/2],
            [ball.x-ball.width/2, ball.y+ball.height/2],
            [ball.x+ball.width/2, ball.y],
            [ball.x-ball.width/2, ball.y],
            [ball.x, ball.y+ball.height/2]
        ]
        if ball.getBallvy() >= 0:
            return False
        for x in range(len(PADDLE_COL)):
            if self.contains(PADDLE_COL[x][0], PADDLE_COL[x][1]):
                return True
        return False    
    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY
    
    
class Brick(GRectangle):
    """An instance is the game paddle.
    
    This class contains a method to detect collision with the ball.  You may wish to 
    add more features to this class.
    
    The attributes of this class are those inherited from GRectangle.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    """
    
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    
    # INITIALIZER TO CREATE A BRICK
    def __init__(self,x,y,fillcolor):
        GRectangle.__init__(self,x=x,y=y,width=BRICK_WIDTH,
                            height = BRICK_HEIGHT,fillcolor = fillcolor)
    
    # METHOD TO CHECK FOR COLLISION
    def collidesB(self,ball):
        """Returns: True if the ball collides with this brick
        
        Parameter ball: The ball to check
        Precondition: ball is of class Ball"""
        BRICK_COL = [
            [ball.x,ball.y],
            [ball.x+ball.width/2, ball.y+ball.height/2],
            [ball.x+ball.width/2, ball.y-ball.height/2],
            [ball.x-ball.width/2, ball.y-ball.height/2],
            [ball.x-ball.width/2, ball.y+ball.height/2],
            [ball.x+ball.width/2, ball.y],
            [ball.x-ball.width/2, ball.y],
            [ball.x, ball.y+ball.height/2]
        ]
        for x in range(len(BRICK_COL)):
            if self.contains(BRICK_COL[x][0], BRICK_COL[x][1]):
                return True 
    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY


class Ball(GImage):
    """Instance is a game ball.
    
    We extend GEllipse because a ball must have additional attributes for velocity.
    This class adds this attributes and manages them.
    
    INSTANCE ATTRIBUTES:
        _vx [int or float]: Velocity in x direction 
        _vy [int or float]: Velocity in y direction 
    
    The class Play will need to look at these attributes, so you will need
    getters for them.  However, it is possible to write this assignment with no
    setters for the velocities.
    
    How? The only time the ball can change velocities is if it hits an obstacle
    (paddle or brick) or if it hits a wall.  Why not just write methods for these
    instead of using setters?  This cuts down on the amount of code in Gameplay.
    
    NOTE: The ball does not have to be a GEllipse. It could be an instance
    of GImage (why?). This change is allowed, but you must modify the class
    header up above.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    """
    
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getBallvx(self):
        """Gets the ball's _vx"""
        return self._vx
    
    def getBallvy(self):
        """Gets the ball's _vy"""
        return self._vy
        
    # INITIALIZER TO SET RANDOM VELOCITY
    def __init__(self, x, y):
        GImage.__init__(self,x = x, y = y, width=BALL_DIAMETER,
                        height=BALL_DIAMETER, source = 'walkerwhite.png')
        self._vx = random.uniform(1.0,5.0)
        self._vx = self._vx * random.choice([-1, 1])
        self._vy = -1*BALL_SPEED
        
    # METHODS TO MOVE AND/OR BOUNCE THE BALL
    def moveBall(self):
        """moves the ball in accordance with the x and y velocities and changes
        velocites when the ball hits the sides or top or bottom"""
        self.y += self._vy
        self.x += self._vx
        if self.top > GAME_HEIGHT or self.bottom < 0:
            self._vy = - self._vy
        if self.left < 0 or self.right > GAME_WIDTH:
            self._vx = - self._vx
           
    def collideBally(self):
        """changes the direction of the ball (veritcally) when it hits
        an obstacle"""
        self._vy = -1*self._vy
    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY
    
    def collidePaddle(self, paddle):
        """The physics of how the ball will move in the +-x direction
        (horizontally) when hit by the paddle
        
        Parameter paddle: the paddle that the ball collides with
        Precondition: paddle must be a GObject
        """
        ballxRelToPaddlex = self.x - paddle.x
        k = ballxRelToPaddlex/(PADDLE_WIDTH/2.0)
        self._vx = BALL_SPEED * k


# IF YOU NEED ADDITIONAL MODEL CLASSES, THEY GO HERE