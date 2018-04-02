# breakout.py
# Xiaoyu Yan (xy97) and Jeremy Glassman (jrg348)
# 12/04/16
# Credit to Walker White for his provided files, such as arrow.py and algorithms.py, and the use of his face for the ball
"""Primary module for Breakout application

This module contains the main controller class for the Breakout application. There is no
need for any any need for additional classes in this module.  If you need more classes, 
99% of the time they belong in either the play module or the models module. If you 
are ensure about where a new class should go, 
post a question on Piazza."""
from constants import *
from game2d import *
from play import *


# PRIMARY RULE: Breakout can only access attributes in play.py via getters/setters
# Breakout is NOT allowed to access anything in models.py

class Breakout(GameApp):
    """Instance is the primary controller for the Breakout App
    
    This class extends GameApp and implements the various methods necessary for processing 
    the player inputs and starting/running a game.
    
        Method start begins the application.
        
        Method update either changes the state or updates the Play object
        
        Method draw displays the Play object and any other elements on screen
    
    Because of some of the weird ways that Kivy works, you SHOULD NOT create an
    initializer __init__ for this class.  Any initialization should be done in
    the start method instead.  This is only for this class.  All other classes
    behave normally.
    
    Most of the work handling the game is actually provided in the class Play.
    Play should have a minimum of two methods: updatePaddle(input) which moves
    the paddle, and updateBall() which moves the ball and processes all of the
    game physics. This class should simply call that method in update().
    
    The primary purpose of this class is managing the game state: when is the 
    game started, paused, completed, etc. It keeps track of that in an attribute
    called _state.
    
    INSTANCE ATTRIBUTES:
        view    [Immutable instance of GView; it is inherited from GameApp]:
                the game view, used in drawing (see examples from class)
        input   [Immutable instance of GInput; it is inherited from GameApp]:
                the user input, used to control the paddle and change state
        _state  [one of STATE_INACTIVE, STATE_COUNTDOWN, STATE_PAUSED, STATE_ACTIVE]:
                the current state of the game represented a value from constants.py
        _game   [Play, or None if there is no game currently active]: 
                the controller for a single game, which manages the paddle, ball, and bricks
        _mssg   [GLabel, or None if there is no message to display]
                the currently active message
    
    STATE SPECIFIC INVARIANTS: 
        Attribute _game is only None if _state is STATE_INACTIVE.
        Attribute _mssg is only None if  _state is STATE_ACTIVE or STATE_COUNTDOWN.
    
    For a complete description of how the states work, see the specification for the
    method update().
    
    You may have more attributes if you wish (you might need an attribute to store
    any text messages you display on the screen). If you add new attributes, they
    need to be documented here.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    _last_keys = the number of keys last pressed
    _lastState = the last STATE of the game
    _numbricks = number of bricks: equal to total/2 before power up, then zero
    while drawing, then total bricks
    
    _smssg = message that displays the score
    _tmssg = message that displays the number of tries left
    _emssg = message at end of game
    _lmssg = level message
    _pmssg = message when player gets a power up
    _tsmssg = Total Score through win streaks
    _Countmssg = messsage displaying the countdown
    
    Keep track of time
    _frameTime = amount of time that has passed 
    _count = use to count time
    _count2 = a second counting tool that helps to keep track of time
    
    Immutable variables:
    _level = level/stage in the game. This is used to keep track of what bricks
    to draw, starts at 1 for first game
    _lives = number of lives, used to carry through the streak
    _totalscore = Total score through streak of wins
    """      
    #background variables that doesn't reset whenever start() is called
    _level = 1
    _lives = 0
    _totalscore = 0
    _rows = BRICK_ROWS
    # DO NOT MAKE A NEW INITIALIZER!
    
    # THREE MAIN GAMEAPP METHODS
    def start(self):
        """Initializes the application.
        
        This method is distinct from the built-in initializer __init__ (which you 
        should not override or change). This method is called once the game is running. 
        You should use it to initialize any game specific attributes.
        
        This method should make sure that all of the attributes satisfy the given 
        invariants. When done, it sets the _state to STATE_INACTIVE and create a message 
        (in attribute _mssg) saying that the user should press to play a game."""
        # IMPLEMENT ME
        self._game = None
        self._state = STATE_INACTIVE
        #message variables
        self._mssg = GLabel(
            text = "Press any key to start",
            font_size = 30,
            font_name = 'TimesBold.ttf',
            x = GAME_WIDTH/2,
            y = GAME_HEIGHT/2,
            linecolor = colormodel.BLACK
            )
        self._tmssg = None
        self._emssg = None
        self._Countmssg = None
        self._smssg = None
        self._pmssg = None
        self._tsmssg = None
        self._lmssg = None
        
        #Variables to keep track of time
        self._frameTime = 0
        self._count = 0
        self._count2 = 0
        
        #outside variables
        self._numbricks = (float(BRICKS_IN_ROW*Breakout._rows))/2.0
        self._last_keys = 0
        
        #music
        self.winSound = Sound(WIN_SOUND)
        self.loseSound = Sound(LOSE_SOUND)

    def update(self,dt):
        """Animates a single frame in the game.
        
        It is the method that does most of the work. It is NOT in charge of playing the
        game.  That is the purpose of the class Play.  The primary purpose of this
        game is to determine the current state, and -- if the game is active -- pass
        the input to the Play object _game to play the game.
        
        As part of the assignment, you are allowed to add your own states.  However, at
        a minimum you must support the following states: STATE_INACTIVE, STATE_NEWGAME,
        STATE_COUNTDOWN, STATE_PAUSED, and STATE_ACTIVE.  Each one of these does its own
        thing, and so should have its own helper.  We describe these below.
        
        STATE_INACTIVE: This is the state when the application first opens.  It is a
        paused state, waiting for the player to start the game.  It displays a simple
        message on the screen.
        
        STATE_NEWGAME: This is the state creates a new game and shows it on the screen.  
        This state only lasts one animation frame before switching to STATE_COUNTDOWN.

        STATE_COUNTDOWN: This is a 3 second countdown that lasts until the ball is 
        served.  The player can move the paddle during the countdown, but there is no
        ball on the screen.  Paddle movement is handled by the Play object.  Hence the
        Play class should have a method called updatePaddle()
        
        STATE_ACTIVE: This is a session of normal gameplay.  The player can move the
        paddle and the ball moves on its own about the board.  Both of these
        should be handled by methods inside of class Play (NOT in this class).  Hence
        the Play class should have methods named updatePaddle() and updateBall().
        
        STATE_PAUSED: Like STATE_INACTIVE, this is a paused state. However, the game is
        still visible on the screen.

        The rules for determining the current state are as follows.
        
        STATE_INACTIVE: This is the state at the beginning, and is the state so long
        as the player never presses a key.  In addition, the application switches to 
        this state if the previous state was STATE_ACTIVE and the game is over 
        (e.g. all balls are lost or no more bricks are on the screen).

        STATE_NEWGAME: The application switches to this state if the state was 
        STATE_INACTIVE in the previous frame, and the player pressed a key.
        
        STATE_COUNTDOWN: The application switches to this state if the state was
        STATE_NEWGAME in the previous frame (so that state only lasts one frame).
        
        STATE_ACTIVE: The application switches to this state after it has spent 3
        seconds in the state STATE_COUNTDOWN.
        
        STATE_PAUSED: The application switches to this state if the state was 
        STATE_ACTIVE in the previous frame, the ball was lost, and there are still
        some tries remaining.
        
        You are allowed to add more states if you wish. Should you do so, you should 
        describe them here.
        
        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        if self._state == STATE_INACTIVE:
            self.start()
        self._lastState = self._state
        self._determineState()
        
        if self._state == STATE_NEWGAME:
            self.stateNewgame()
        if self._state == STATE_COUNTDOWN:
            self.stateCountdown()
        if self._state == STATE_PAUSED:
            self.statePaused()
        if self._state == STATE_ACTIVE:
            self.stateActive()
        if self._state == STATE_COMPLETE:
            self.stateComplete()  
                   
    def draw(self):
        """Draws the game objects to the view.
        
        Every single thing you want to draw in this game is a GObject.  To draw a GObject 
        g, simply use the method g.draw(self.view).  It is that easy!
        
        Many of the GObjects (such as the paddle, ball, and bricks) are attributes in Play. 
        In order to draw them, you either need to add getters for these attributes or you 
        need to add a draw method to class Play.  We suggest the latter.  See the example 
        subcontroller.py from class."""
        # IMPLEMENT ME
        if self._state == STATE_INACTIVE:
            self.start()
            self._mssg.draw(self.view)
        if self._state == STATE_NEWGAME:
            self._game.drawNewBricks(self.view,self._level)
        if self._state > STATE_NEWGAME:
            self._game.drawPaddle(self.view)
            self._game.drawBricks(self.view)
            self._Countmssg.draw(self.view)
            self._smssg.draw(self.view)
            self._tmssg.draw(self.view)
            self._tsmssg.draw(self.view)
            self._lmssg.draw(self.view)
            if self._numbricks == 0:
                self._frameTime += 1
                if self._frameTime <= 60:
                    self._mssgbuilder("pmssg", 'Extra Life!', 30, GAME_WIDTH/2,
                                      GAME_HEIGHT/2 - 50)
                    self._pmssg.draw(self.view)
                elif self._frameTime > 60:
                    self._pmssg = None
                    self._frameTime = 0
                    if len(self._game.getBricks()) == 0: 
                        self._numbricks = (float(BRICKS_IN_ROW*
                                                 Breakout._rows))/2.0
                    else:
                        self._numbricks = float((BRICKS_IN_ROW*Breakout._rows))
        if self._state > STATE_COUNTDOWN and self._state is not STATE_COMPLETE:
            self._game.drawBall(self.view)
        if self._state == STATE_PAUSED:
            self._mssgbuilder("mssg", 'Press Any Key for a New Ball', 30,
                              GAME_WIDTH/2, GAME_HEIGHT/2)
            self._mssg.draw(self.view)
        if self._state == STATE_COMPLETE:
            self._mssg.draw(self.view)
            self._emssg.draw(self.view)
            self._tmssg.draw(self.view)
            self._tsmssg.draw(self.view)
            self._lmssg.draw(self.view)
         
    # HELPER METHODS FOR THE STATES GO HERE
    def _determineState(self):
        """Determines the current state and assigns it to self.state
    
        This method checks for a key press, and if there is one, changes the state 
        to the next value. A key press is when a key is pressed for the FIRST TIME.
        We do not want the state to continue to change as we hold down the key.  The
        user must release the key and press it again to change the state."""
        #used state.py Provided by Professor White
        if self._lastState == STATE_INACTIVE and self.input.key_count > 0:
            self._frameTime = 0
            self._count = 0
            self._count2 = 0
            self._state = STATE_NEWGAME
        if self._lastState == STATE_NEWGAME:
            self._state = STATE_COUNTDOWN
        if self._state == STATE_COUNTDOWN:
            if self._checkTime():
                self._state = STATE_ACTIVE
                self._frameTime = 0
                self._count = 0
                self._count2 = 0
        if self._lastState == STATE_ACTIVE and (
            self._game.getTries() == 0 or len(self._game.getBricks()) == 0):
            self._state = STATE_COMPLETE
    
    def stateNewgame(self):
        """Function for when self._state == STATE_NEWGAME"""
        self._game = Play()
        if self._level == 1:
            self._lives = self._game.getTries()
        else:
            self._game.setTries(self._lives)
        self._mssgbuilder("smssg", 'Current Score: ' +
                          str(self._game.getScore()), 15,
                          GAME_WIDTH - 70,GAME_HEIGHT-12)
        self._mssgbuilder("tmssg", 'Lives: ' +
                          str(self._game.getTries()), 15,
                          GAME_WIDTH/2,GAME_HEIGHT-12)
        self._mssgbuilder("tsmssg", 'Total Score: ' +
                          str(Breakout._totalscore), 15, 75, GAME_HEIGHT-12)
        self._mssgbuilder("lmssg", 'Current Level: ' +
                          str(self._level), 15,GAME_WIDTH/2,GAME_HEIGHT-28)

    def stateCountdown(self):        
        """Function for when self._state == STATE_COUNTDOWN"""
        self._mssg = None
        self._game.serveBall()
        self.updatePaddle()
    
    def statePaused(self):
        """Function for when self._state == STATE_PAUSED"""
        #used state.py provided by Professor Walker White
        
        curr_keys = self.input.key_count
        if curr_keys > 0 and self._last_keys == 0:
            self._state = STATE_COUNTDOWN 
            self._frameTime = 0

    def stateActive(self):
        """Function for when self._state == STATE_ACTIVE"""
        self._game.updateBall()
        self.updatePaddle()
        self._mssg = None
        self._smssg.text = 'Current Score: ' + str(self._game.getScore())
        if (self._numbricks*2)%2== 0:
            if float(self._game.getScore()) == self._numbricks:
                self._game.setTries(self._game.getTries() + 1)
                if len(self._game.getBricks()) == 0:
                    Breakout._level += 1
                    Breakout._totalscore += self._game.getScore()
                    Breakout._rows += 1
                self._numbricks = 0
                self._tmssg.text = 'Lives: ' + str(self._game.getTries()) 
        else:
            if float(self._game.getScore()) - 0.5 == self._numbricks:
                self._game.setTries(self._game.getTries() + 1)
                if len(self._game.getBricks()) == 0:
                    Breakout._level += 1
                    Breakout._totalscore += self._game.getScore()
                    Breakout._rows += 1
                self._numbricks = 0
                self._tmssg.text = 'Lives: ' + str(self._game.getTries()) 
        self._loseLife()
        self._youWin()

    def stateComplete(self):
        """Function for when self._state == STATE_COMPLETE"""
        curr_keys = self.input.key_count
        self._lives = self._game.getTries()
        if self._game.getTries() > 0:
            if self._frameTime < 180:
                self._count += 0.15
                self._mssgbuilder("mssg", 'CONGRATULATIONS YOU WIN!',
                                  self._count, GAME_WIDTH/2,GAME_HEIGHT/2+5)
                self._mssgbuilder("emssg", 'Press Any Key To Continue',
                                  self._count, GAME_WIDTH/2,GAME_HEIGHT/2 - 23)
                self._frameTime += 1
            
        elif self._game.getTries() == 0:
            if self._frameTime < 180:
                self._count += 0.15
                self._mssgbuilder("mssg", 'Game Over. Better Luck Next Time,',
                                  self._count, GAME_WIDTH/2,GAME_HEIGHT/2+5)
                self._mssgbuilder("emssg", 'Press Any Key To Try Again',
                                  self._count, GAME_WIDTH/2,GAME_HEIGHT/2 - 23)
                self._frameTime += 1

        if curr_keys > 0 and self._last_keys == 0:
                self._mssg = None
                self._state = STATE_INACTIVE
                
    def updatePaddle(self):
        """Updates the paddle's position when the arrow keys are pressed"""
        if self.input.is_key_down('left'):
            self._game.updatePaddle('left')
        if self.input.is_key_down('right'):
            self._game.updatePaddle('right')

    def _youWin(self):
        """checks to see if the player won"""
        if len(self._game.getBricks()) == 0:
            self.winSound.play()
            self._state = STATE_COMPLETE

    def _loseLife(self):
        """When a player loses a life, updates the number of tries and checks
        to see if the player has lost the game"""
        if self._game._ball.bottom <= 0.0:
            self._game.setTries(self._game.getTries()-1)
            self._tmssg.text = 'Lives: ' + str(self._game.getTries())
            self._state = STATE_PAUSED
            if self._game.getTries() == 0:
                self.loseSound.play()
                self._state = STATE_COMPLETE
                self._level = 1
                self.stateComplete()
           
    def _checkTime(self):
        """determines the number of frames, and time passed.
        
        Increments the frame time by 1
        Returns: True if time meets certain requirements only if self._state
        == STATE_COUNTDOWN"""
        
        self._frameTime += 1
        if self._state == STATE_COUNTDOWN:
            if self._frameTime <= 1:
                self._count = 3
            if self._frameTime%60==0:
                self._count -= 1
                self._count2 = 0
            self._mssgbuilder("Countmssg", str(self._count), self._count2,
                              GAME_WIDTH/2, GAME_HEIGHT/2.2)
            self._count2 += 0.75
                
            if self._frameTime >= 180:
                self._frameTime = 0
                return True        

    def _mssgbuilder(self, mssg, t, f, x, y):
        """Changes the GLabel object of the mssg.
        This is a template to build the GLabel object to help with
        organization and make the codes less cluttered.
    
        Parameter mssg: the message to change
        Precondition: mssg already exists as a variable
        
        Parameter t: text for the message
        Precondition: t is a string
        
        Parameter f: message font
        Precondition: f is an int
        
        Parameter x: x position of the message
        Precondition: x is an int or float
        
        Parameter y: y position of the message
        Precondition: x is an int or float
        """
        a = GLabel(text = t,font_size = f,font_name = 'TimesBold.ttf',
                   x = x,y = y,linecolor = colormodel.BLACK)
        if mssg == "mssg":
            self._mssg = a
        if mssg == "emssg":
            self._emssg = a
        if mssg == "smssg":
            self._smssg = a
        if mssg == "tmssg":
            self._tmssg = a
        if mssg == "Countmssg":
            self._Countmssg = a
        if mssg == "pmssg":
            self._pmssg = a
        if mssg == "tsmssg":
            self._tsmssg = a
        if mssg == "lmssg":
            self._lmssg = a
        
        

        