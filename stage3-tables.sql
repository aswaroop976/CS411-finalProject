/*!40101 SET NAMES utf8 */;
/*!40101 SET SQL_MODE=''*/;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`classicmodels` /*!40100 DEFAULT CHARACTER
SET latin1 */;
USE `classicmodels`;

DROP TABLE IF EXISTS Game;
 
CREATE TABLE Game (
ID INT NOT NULL,  
NAME VARCHAR(255) NOT NULL, 
ReleaseDate VARCHAR(100),
DeveloperCount INT, 
DLCcount INT, 
MetaCritic INT, 
Recommendation INT, 
SteamSpyOwner BIGINT, 
SteamSpyPlayer BIGINT, 
InitialPrice REAL, 
FinalPrice REAL,
PRIMARY KEY (ID)
)ENGINE=InnoDB DEFAULT CHARSET=latin1;


DROP TABLE IF EXISTS Platform;

CREATE TABLE Platform (
PlatformWindows BOOLEAN NOT NULL,
PlatformLinux BOOLEAN NOT NULL,
PlatformMac BOOLEAN NOT NULL,
WindowsMinReqs VARCHAR(500) DEFAULT NULL,
WindowsRecReqs VARCHAR(500) DEFAULT NULL,
LinuxMinReqs VARCHAR(500) DEFAULT NULL,
LinuxRecReqs VARCHAR(500) DEFAULT NULL,
MacMinReqs VARCHAR(500) DEFAULT NULL,
MacRecReqs VARCHAR(500) DEFAULT NULL,
GameID INT NOT NULL,
PRIMARY KEY GameID(GameID),
CONSTRAINT Platform_ibfk_1 FOREIGN KEY (GameID) REFERENCES Game(ID) ON UPDATE CASCADE ON DELETE CASCADE
)ENGINE=InnoDB DEFAULT CHARSET=latin1;
 
DROP TABLE IF EXISTS Genre;
CREATE TABLE Genre ( 
NonGame BOOLEAN,
Indie BOOLEAN,
Action BOOLEAN,
Adventure BOOLEAN,
Casual BOOLEAN,
Strategy BOOLEAN,
RPG BOOLEAN,
Simulation BOOLEAN,
EarlyAccess BOOLEAN,
FreeToPlay BOOLEAN,
           Sports BOOLEAN,
Racing BOOLEAN,
           MassivelyMultiplayer BOOLEAN,
      	GameID INT NOT NULL,
KEY GameID(GameID),
CONSTRAINT Genre_ibfk_1 FOREIGN KEY (GameID) REFERENCES Game(ID) ON UPDATE CASCADE ON DELETE CASCADE,
PRIMARY KEY(GameID)
)ENGINE=InnoDB DEFAULT CHARSET=latin1;
 
DROP TABLE IF EXISTS Features;
CREATE TABLE Features (
     ControllerSupport BOOLEAN, 
     Free BOOLEAN, 
     FreeVersionAvailable BOOLEAN, 
     Subscription BOOLEAN, 
     SinglePlayer BOOLEAN, 
     MultiPlayer BOOLEAN, 
     Coop BOOLEAN,
     MMO BOOLEAN,
     InAppPurchases BOOLEAN,
IncludeSrcSDK BOOLEAN,
IncludeLevelEditor BOOLEAN,
VRSupport BOOLEAN,
GameID INT NOT NULL,
                	KEY GameID(GameID),
CONSTRAINT Features_ibfk_1 FOREIGN KEY (GameID) REFERENCES Game(ID) ON UPDATE CASCADE ON DELETE CASCADE,
PRIMARY KEY(GameID)
)ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS User;
CREATE TABLE User (
UserID INT NOT NULL,
Email VARCHAR(100) NOT NULL,
Password VARCHAR(100) NOT NULL,
UserName VARCHAR(100) NOT NULL,
FriendCount INT DEFAULT 0;
PRIMARY KEY (UserID)
)ENGINE=InnoDB DEFAULT CHARSET=latin1;
 
DROP TABLE IF EXISTS WishList;
CREATE TABLE WishList (
UserID INT NOT NULL,
GameID INT NOT NULL,
DateAdded VARCHAR(255) DEFAULT NULL,
PRIMARY KEY (UserID, GameID),
CONSTRAINT WishList_ibfk_1 FOREIGN KEY (UserID) REFERENCES User(UserID) ON UPDATE CASCADE ON DELETE CASCADE,
CONSTRAINT WishList_ibfk_2 FOREIGN KEY (GameID) REFERENCES Game(ID) ON UPDATE CASCADE ON DELETE CASCADE
)ENGINE=InnoDB DEFAULT CHARSET=latin1;
 
DROP TABLE IF EXISTS FriendList;
CREATE TABLE FriendList (
FriendID INT NOT NULL,
UserID INT NOT NULL,
DateAdded VARCHAR(255) DEFAULT NULL,
PRIMARY KEY (FriendID, UserID),
KEY UserID(UserID),
CONSTRAINT Friends_ibfk_1 FOREIGN KEY (UserID) REFERENCES User(UserID) ON UPDATE CASCADE ON DELETE CASCADE
)ENGINE=InnoDB DEFAULT CHARSET=latin1;
 
DROP TABLE IF EXISTS LanguagesAndInfo;
CREATE TABLE LanguagesAndInfo (
Languages VARCHAR(255) NOT NULL,
GameID INT NOT NULL,
AboutText VARCHAR(10000) DEFAULT NULL,
PRIMARY KEY GameID(GameID),
CONSTRAINT Language_ibfk_1 FOREIGN KEY (GameID) REFERENCES Game(ID) ON UPDATE CASCADE ON DELETE CASCADE
)ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
