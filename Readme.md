      ___           _    _    _           ___    _                        
     (  _`\        ( )_ ( )_ (_ )        (  _`\ ( )                       
     | (_) )   _ _ | ,_)| ,_) | |    __  | ( (_)| |__     __    ___   ___ 
     |  _ <' /'_` )| |  | |   | |  /'__`\| |  _ |  _ `\ /'__`\/',__)/',__)
     | (_) )( (_| || |_ | |_  | | (  ___/| (_( )| | | |(  ___/\__, \\__, \
     (____/'`\__,_)`\__)`\__)(___)`\____)(____/'(_) (_)`\____)(____/(____/
  

---
  
  
## Abstract 
- Quick game :  
	`python battleChess.py`  
- Download :  
	`git clone https://github.com/quimnuss/battlechess.git`  


## Introduction :  
On a regular afternoon break at CVLab, a discussion was about to wake us (Pol, Raphael, Pen and Antoine) from our boredom.  
_"Chess, to brainy. BattleShip, lack some action... But wait, what if we mixed both ?"_  
BattleChess was born. Mixing rules from both games to make a new exciting one.



## Rules :  
The rules are pretty straithforward for anyone who played chess before. The board and pieces are the same. They move and capture opponents the same way. The main difference arise from the fact that at a given time each player can only see the part of the board he actually controls. That's all his pieces positions and direct neighbooring cells. No more, no less.  
That new rule has some direct consequences on the gameplay.  

- Towers, bishops, and queens may be asked to move to an position without knowing if it can be reached safely or at all. Some unseen pieces could be in the way. If that happens, the moving piece goes as far as possible and take the blocking opponent piece.  
- There is no way of preventing the king to put himself in a hazardous position without letting the player infer information about his opponent's position. So the king is free to move as he wishes and the game ends not on check-mate but on a king's death.  
- Every pawns which reaches the end of the board becomes a queen, you cannot choose, deal with it.  


## Installation : 

- What you need :
	* [python 2.7](https://www.python.org/downloads/) (or more I guess...)
	* [pygame 1.9.2](http://www.pygame.org/download.shtml). On OS X with python 2.7, you should donwload this [installation file](http://www.pygame.org/ftp/pygame-1.9.2pre-py2.7-macosx10.7.mpkg.zip)
	* the game itself. It can be downloaded via git using the following command:  
	```git clone http://git.sxbn.org/battleChess.git```

- Launching the game :  
	There is and will be a server app running on sxbn.org, so I recommend no changing the HOST and PORT parameters unless you want to host your own games.  
	In the root directory ( battleChess/ ), you can directly launch the game using the command  
	```python battleChess.py [NickName] [HOST] [PORT]```  
	with 3 optional parameters :  
	* Nickname : will be you name during the game. If not given, it will be chosen randomly  
	* HOST     : server name to connect to (see bellow). By default sxbn.org  
	* PORT     : which port to connect to. By default 8887  
 

- Replay mode :  
	You just got beaten and you don't know what just happened. Don't worry that happens a lot. Every game played are saved on the server and can be downloaded from this webpage : [http://sxbn.org/~antoine/games/](http://sxbn.org/~antoine/games/)  
	You can either download the file or replay it from the url directly using one of the following commands :  
	`python battleChess.py -p http://sxbn.org/~antoine/games/2014_03_07_14_06_37_lance_hardwood_Vs_sniper.txt`  
	`python battleChess.py -p ./2014_03_07_14_06_37_lance_hardwood_Vs_sniper.txt`

- Using the server application :  
	If you want to host your own server (you don't have to). You just need to run the server.py programm on a computer that can be reached through the network. Change the port and hostname if you want and pass those informations to the client application.

- Information sent on the network :  
	If you worry about privacy, you can launch your own server. It's pretty straigthforward to see from the source code that nothing is sent anywhere else.  
	The only information sent and stored on the server are your nickname and the moves you make.


## How to play :


- Regular game :  
	White play first. To move a piece, click on it and then click on the desired destination. Your piece will move there, if it can.  
	You know it's your turn to move when the message on the top left says your color.  
	You can exit the game anytime with ESCAPE.  

- Replay mode :  
	Use LEFT and RIGHT arrows to move step by step (and loop) into the game.  
	SPACE will reset to initial state.  


## Android & iOS Apps :


- Android .apk file can be downloaded from this link : [http://sxbn.org/~antoine/git/battlechess/BattleChess.apk](http://sxbn.org/~antoine/git/battlechess/BattleChess.apk)

- iOS app is ready and working, but thanks to Apple's App Store terms we cannot release it without paying...


### Building the app

If you are builind the app from source and it complains that cocos2dx doesn't have neon_matrix_impl.c, copy it from cocos2dmods/ to the directory where it is looking for it.


## Credits & Licence :


- Code :  
	Antoine Letouzey -- [antoine.letouzey@gmail.com](antoine.letouzey@gmail.com)    
	Pol Monsó-Purtí  -- [pol.monso@gmail.com](pol.monso@gmail.com)  

- Sprites :
	Original sprites by Wikipedia user Cburnett, under Creative Commons Licence (CC BY-SA 3.0)

- Licence : GPL

## Screenshots :
![img1](http://sxbn.org/~antoine/git/battlechess/1.jpg)  
![img2](http://sxbn.org/~antoine/git/battlechess/2.jpg)  
![img3](http://sxbn.org/~antoine/git/battlechess/3.jpg)  
![img4](http://sxbn.org/~antoine/git/battlechess/4.jpg)  
![img5](http://sxbn.org/~antoine/git/battlechess/5.jpg)  

## Screenshots Android & iOS App :

<center> ![img1](https://www.dropbox.com/s/vds1kulhv1my05e/icon.png?dl=1) </center>

![img2](https://www.dropbox.com/s/n4b25d7113u910l/m2.png?dl=1)
![img3](https://www.dropbox.com/s/fuuz4w5b7d2amco/m3.png?dl=1)
![img4](https://www.dropbox.com/s/cwtly4znbsj0n4t/m5.png?dl=1)
![img4](https://www.dropbox.com/s/mwi5b705eks01ky/m4.png?dl=1)
<center> ![img1](https://www.dropbox.com/s/72vvoty6h1na1bw/m1.png?dl=1) </center>

