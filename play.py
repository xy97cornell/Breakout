# play.py
# Xiaoyu Yan (xy97) and Jeremy Glassman (jrg348)
# 12/04/16
"""Subcontroller module for Breakout

This module contains the subcontroller to manage a single game in the Breakout App. 
Instances of Play represent a single game.  If you want to restart a new game, you are 
expected to make a new instance of Play.

The subcontroller Play manages the paddle, ball, and bricks.  These are model objects.  
Their classes are defined in models.py.

Most of your work on this assignment will be in either this module or models.py.
Whether a helper method belongs in this module or models.py is often a complicated
issue.  If you do not know, ask on Piazza and we will answer."""
from constants import *
from game2d import *
from models import *


# PRIMARY RULE: Play can only access attributes in models.py via getters/setters
# Play is NOT allowed to access anything in breakout.py (Subcontrollers are not
# permitted to access anything in their parent. To see why, take CS 3152)

class Play(object):
    """An instance controls a single game of breakout.
    
    This subcontroller has a reference to the ball, paddle, and bricks. It animates the 
    ball, removing any bricks as necessary.  When the game is won, it stops animating.  
    You should create a NEW instance of Play (in Breakout) if you want to make a new game.
    
    If you want to pause the game, tell this controller to draw, but do not update.  See 
    subcontrollers.py from Lecture 25 for an example.
    
    INSTANCE ATTRIBUTES:
        _paddle [Paddle]: the paddle to play with 
        _bricks [list of Brick]: the list of bricks still remaining 
        _ball   [Ball, or None if waiting for a serve]:  the ball to animate
        _tries  [int >= 0]: the number of tries left 
    
    As you can see, all of these attributes are hidden.  You may find that you want to
    access an attribute in class Breakout. It is okay if you do, but you MAY NOT ACCESS 
    THE ATTRIBUTES DIRECTLY. You must use a getter and/or setter for any attribute that 
    you need to access in Breakout.  Only add the getters and setters that you need for 
    Breakout.
    
    You may change any of the attributes above as you see fit. For example, you may want
    to add new objects on the screen (e.g power-ups).  If you make changes, please list
    the changes with the invariants.
                  
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    _score = the score of the player (number of bricks removed)
    paddleSound = sound when the ball hits the paddle
    brickSound = sound when ball hits the brick
    
    """
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    
    def getBricks(self):
        """returns: the number of bricks"""
        return self._bricks
    
    def getScore(self):
        """returns: the score of the player"""
        return self._score
    
    def getTries(self):
        """Returns: the number of lives/tries left in the game"""
        return self._tries
    
    def setTries(self, x):
        """Sets the number of tries in a given game.
        
        Parameter x: the value to change to
        Precondition: x is an int"""
        self._tries = x
        
    # INITIALIZER (standard form) TO CREATE PADDLES AND BRICKS
    def __init__(self):
        """Initializes the game"""
        self._tries = NUMBER_TURNS
        self._paddle = Paddle(GAME_WIDTH/2)
        self._bricks = []
        self._score = 0
        self._ball = None
        
    # UPDATE METHODS TO MOVE PADDLE, SERVE AND MOVE THE BALL
    def updatePaddle(self, direction):
        """Calls the movePaddle functino in models.py
        This function passes the direction of the paddle and tells the
        paddle where to move
        
        Parameter direction: direction to move the paddle
        Precondition: direction is a valid direction from input and is a string
        """
        self._paddle.movePaddle(direction)
         
    def updateBall(self):
        """Updates the ball's position"""

        if self.checkCollision():
            self._ball.collideBally()
        self._ball.moveBall()
                 
    def serveBall(self):
        """Creates a ball to serve"""
        self._ball = Ball(GAME_WIDTH/2, GAME_HEIGHT/2)   

    # DRAW METHOD TO DRAW THE PADDLES, BALL, AND BRICKS
    def drawNewBricks(self,view,l):
        """Draws the starting bricks as a result of STATE_NEWGAME.
        It also handles the colors of the brick rows.
        
        Parameter view: the screen where the bricks will draw
        Precondition: view is a valid GView object
        
        Parameter l: the lvl of the game
        Precondition: l is an int
        """
        i = 0
        k = 0
        Y = GAME_HEIGHT - BRICK_Y_OFFSET
        for p in range(BRICK_ROWS+l-1):
            X = BRICK_WIDTH / 2 + BRICK_SEP_H/2
            for q in range(BRICKS_IN_ROW):
                a = self.getBricks().append(Brick(X, Y, BRICK_COLOR[i]))
                self.getBricks()[-1].draw(view)
                X = X + BRICK_SEP_H + BRICK_WIDTH
            k+=1
            if k >= 2:
                i += 1
                k = 0
            if i == len(BRICK_COLOR):
                i = 0
            Y = Y - BRICK_SEP_V - BRICK_HEIGHT

    def drawBricks(self, view):
        """Updates the bricks once the game has started
        
        Parameter view: the screen where the bricks will draw
        Precondition: view is a valid GView object
        """
        for b in self._bricks:
            b.draw(view)
          
    def drawPaddle(self,view):
        """Draws the paddle at various locations
        
        Parameter view: the screen where the bricks will draw
        Precondition: view is a valid GView object
        """
        if (self._paddle.getPaddleX()+PADDLE_WIDTH/2 >= GAME_WIDTH or
            self._paddle.getPaddleX()-PADDLE_WIDTH/2<= 0):
            self._paddle.setPaddleX(max(self._paddle.getPaddleX()-
                                        PADDLE_SPEED, PADDLE_WIDTH/2))
        self._paddle = Paddle(self._paddle.getPaddleX())
        self._paddle.draw(view)
 
    def drawBall(self, view):
        """Draws the ball
        
        Parameter view: the screen where the bricks will draw
        Precondition: view is a valid GView object"""
        self._ball.draw(view)
     
    # HELPER METHODS FOR PHYSICS AND COLLISION DETECTION
    def checkCollision(self):
        """Returns: True if a collision has occurred between the ball and
        the paddle or between the ball and the bricks."""
        boolb = False
        for a in self._bricks:
            if a.collidesB(self._ball):
                s = random.randint(0,len(BREAK_SOUNDS)-1)
                self.brickSound = Sound(BREAK_SOUNDS[s])
                self.brickSound.play()
                self._bricks.remove(a)
                self._score += 1
                boolb = True
        
        boolp = self._paddle.collidesP(self._ball)
        if boolp == True:
            self.paddleSound = Sound('bounce.wav')
            self.paddleSound.play()
            self._ball.collidePaddle(self._paddle)
        return boolp or boolb
        
        
        
    # ADD ANY ADDITIONAL METHODS (FULLY SPECIFIED) HERE
