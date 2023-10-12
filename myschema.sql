-- MySQL dump 10.13  Distrib 8.0.34, for Linux (x86_64)
--
-- Host: localhost    Database: AdventureLog
-- ------------------------------------------------------
-- Server version	8.0.34-0ubuntu0.22.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `Activity`
--

DROP TABLE IF EXISTS `Activity`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Activity` (
  `ID` smallint NOT NULL AUTO_INCREMENT,
  `ActivityName` varchar(20) NOT NULL,
  `DifficultyLevel` enum('Beginner','Intermediate','Advanced','Expert') NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=204 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Activity`
--

LOCK TABLES `Activity` WRITE;
/*!40000 ALTER TABLE `Activity` DISABLE KEYS */;
INSERT INTO `Activity` VALUES (201,'Hiking','Beginner'),(202,'Skiing','Advanced'),(203,'Kayaking','Intermediate');
/*!40000 ALTER TABLE `Activity` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ActivityGear`
--

DROP TABLE IF EXISTS `ActivityGear`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ActivityGear` (
  `ID` smallint NOT NULL,
  `GearName` varchar(20) NOT NULL,
  PRIMARY KEY (`ID`,`GearName`),
  CONSTRAINT `ActivityGear_ibfk_1` FOREIGN KEY (`ID`) REFERENCES `Activity` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ActivityGear`
--

LOCK TABLES `ActivityGear` WRITE;
/*!40000 ALTER TABLE `ActivityGear` DISABLE KEYS */;
INSERT INTO `ActivityGear` VALUES (201,'Backpack'),(201,'Boots'),(201,'Hiking Poles'),(202,'Helmet'),(202,'Ski Boots'),(202,'Ski Poles'),(202,'Skis'),(203,'Drysack'),(203,'Helmet'),(203,'Kayak'),(203,'Paddle');
/*!40000 ALTER TABLE `ActivityGear` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `AdventureLog`
--

DROP TABLE IF EXISTS `AdventureLog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `AdventureLog` (
  `ID` smallint NOT NULL AUTO_INCREMENT,
  `Date` date NOT NULL,
  `Time` time NOT NULL,
  `LocationID` smallint NOT NULL,
  `ActivityID` smallint NOT NULL,
  `DurationInHours` smallint NOT NULL,
  PRIMARY KEY (`ID`),
  KEY `LocationID` (`LocationID`),
  KEY `ActivityID` (`ActivityID`),
  CONSTRAINT `AdventureLog_ibfk_1` FOREIGN KEY (`LocationID`) REFERENCES `Location` (`ID`),
  CONSTRAINT `AdventureLog_ibfk_2` FOREIGN KEY (`ActivityID`) REFERENCES `Activity` (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `AdventureLog`
--

LOCK TABLES `AdventureLog` WRITE;
/*!40000 ALTER TABLE `AdventureLog` DISABLE KEYS */;
INSERT INTO `AdventureLog` VALUES (1,'2023-09-20','00:09:30',101,201,3),(2,'2023-09-21','00:14:00',102,202,4),(3,'2023-09-22','00:11:15',103,203,2);
/*!40000 ALTER TABLE `AdventureLog` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `AdventureLog_Participant`
--

DROP TABLE IF EXISTS `AdventureLog_Participant`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `AdventureLog_Participant` (
  `LogID` smallint NOT NULL,
  `ParticipantID` smallint NOT NULL,
  PRIMARY KEY (`LogID`,`ParticipantID`),
  KEY `ParticipantID` (`ParticipantID`),
  CONSTRAINT `AdventureLog_Participant_ibfk_1` FOREIGN KEY (`LogID`) REFERENCES `AdventureLog` (`ID`),
  CONSTRAINT `AdventureLog_Participant_ibfk_2` FOREIGN KEY (`ParticipantID`) REFERENCES `Participants` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `AdventureLog_Participant`
--

LOCK TABLES `AdventureLog_Participant` WRITE;
/*!40000 ALTER TABLE `AdventureLog_Participant` DISABLE KEYS */;
INSERT INTO `AdventureLog_Participant` VALUES (1,901),(2,901),(1,902),(3,902),(2,903),(3,903);
/*!40000 ALTER TABLE `AdventureLog_Participant` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Location`
--

DROP TABLE IF EXISTS `Location`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Location` (
  `ID` smallint NOT NULL AUTO_INCREMENT,
  `LocationName` varchar(35) NOT NULL,
  `Region` varchar(20) NOT NULL,
  `AltitudeInFeet` smallint NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=104 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Location`
--

LOCK TABLES `Location` WRITE;
/*!40000 ALTER TABLE `Location` DISABLE KEYS */;
INSERT INTO `Location` VALUES (101,'Rocky Mtns','Colorado',9000),(102,'Lake Tahoe','California',6225),(103,'Smoky Mtns','Tennessee',6600);
/*!40000 ALTER TABLE `Location` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Participants`
--

DROP TABLE IF EXISTS `Participants`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Participants` (
  `ID` smallint NOT NULL AUTO_INCREMENT,
  `Name` varchar(15) DEFAULT 'Ken',
  `Skill` enum('Beginner','Intermediate','Advanced','Expert') NOT NULL,
  `Age` smallint NOT NULL,
  `LifeInsurance` tinyint NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=904 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Participants`
--

LOCK TABLES `Participants` WRITE;
/*!40000 ALTER TABLE `Participants` DISABLE KEYS */;
INSERT INTO `Participants` VALUES (901,'Brock','Advanced',28,0),(902,'Anne','Intermediate',29,1),(903,'Sonny','Beginner',1,0);
/*!40000 ALTER TABLE `Participants` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-10-12 16:54:28
