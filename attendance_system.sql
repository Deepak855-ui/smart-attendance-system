-- MySQL dump 10.13  Distrib 8.0.36, for Win64 (x86_64)
--
-- Host: localhost    Database: attendance_system
-- ------------------------------------------------------
-- Server version	8.0.36

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
-- Table structure for table `attendance`
--

DROP TABLE IF EXISTS `attendance`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `attendance` (
  `roll_no` int DEFAULT NULL,
  `teacher_id` int DEFAULT NULL,
  `student_name` varchar(100) DEFAULT NULL,
  `date` date DEFAULT NULL,
  `otp` varchar(6) DEFAULT NULL,
  `status` enum('Present','Absent') DEFAULT NULL,
  `subject` varchar(200) DEFAULT NULL,
  `teacher_name` varchar(255) DEFAULT NULL,
  KEY `fk_teacher` (`teacher_id`),
  CONSTRAINT `fk_teacher` FOREIGN KEY (`teacher_id`) REFERENCES `teachers` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `attendance`
--

LOCK TABLES `attendance` WRITE;
/*!40000 ALTER TABLE `attendance` DISABLE KEYS */;
INSERT INTO `attendance` VALUES (22,31,'Deepak Deepak Bhatti','2025-02-28',NULL,'Present','MPD6',NULL),(22,31,'Deepak Deepak Bhatti','2025-03-03',NULL,'Present','MPD6',NULL),(41,2,'boss','2025-03-03',NULL,'Present','Microprocessor',NULL),(22,2,'Deep','2025-03-05',NULL,'Present','Microprocessor',NULL),(22,1,'Deep','2025-03-05',NULL,'Present','Android',NULL),(21,1,'Deepak','2025-03-05',NULL,'Present','Android',NULL),(27,1,'Gurvinder Singh','2025-03-05',NULL,'Present','Android',NULL),(21,1,'Deepak','2025-03-05',NULL,'Present','Android',''),(27,1,'Gurvinder Singh','2025-03-05',NULL,'Present','Android',''),(21,1,'Deepak','2025-03-05',NULL,'Present','Android','Ms.Meenu'),(27,1,'Gurvinder Singh','2025-03-05',NULL,'Present','Android','Ms.Meenu'),(21,1,'Deepak','2025-03-07',NULL,'Present','Android','Ms.Meenu'),(21,2,'Deepak','2025-03-07',NULL,'Present','Microprocessor','Mr.I Gill'),(27,31,'Gurvinder Singh','2025-03-07',NULL,'Present','MPD6','Ms.Reena'),(21,1,'Deepak','2025-03-11',NULL,'Present','Android','Ms.Meenu'),(21,1,'Deepak','2025-03-11',NULL,'Present','Android','Ms.Meenu'),(21,32,'Deepak','2025-03-12',NULL,'Present','Mproject','Project I/C'),(21,2,'Deepak','2025-03-16',NULL,'Present','Microprocessor','Mr.I Gill');
/*!40000 ALTER TABLE `attendance` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `attendance_codes`
--

DROP TABLE IF EXISTS `attendance_codes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `attendance_codes` (
  `id` int NOT NULL AUTO_INCREMENT,
  `teacher_id` int NOT NULL,
  `subject` varchar(100) NOT NULL,
  `code` varchar(6) NOT NULL,
  `expires_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `teacher_id` (`teacher_id`,`subject`),
  CONSTRAINT `attendance_codes_ibfk_1` FOREIGN KEY (`teacher_id`) REFERENCES `teachers` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `attendance_codes`
--

LOCK TABLES `attendance_codes` WRITE;
/*!40000 ALTER TABLE `attendance_codes` DISABLE KEYS */;
/*!40000 ALTER TABLE `attendance_codes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `login_students`
--

DROP TABLE IF EXISTS `login_students`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `login_students` (
  `roll_no` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `phone` varchar(100) NOT NULL,
  `profile_pic` varchar(200) DEFAULT NULL,
  `department` varchar(50) DEFAULT NULL,
  `sem` int DEFAULT NULL,
  `phone_no` int DEFAULT NULL,
  `password` varchar(255) NOT NULL,
  PRIMARY KEY (`roll_no`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=222081 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `login_students`
--

LOCK TABLES `login_students` WRITE;
/*!40000 ALTER TABLE `login_students` DISABLE KEYS */;
INSERT INTO `login_students` VALUES (11,'mahi','mahi11@GMAIL.COM','9115124550','IMG-20250302-WA0006.jpg','--Select Department',6,NULL,'scrypt:32768:8:1$2CcavySBW2ezRaTZ$68ea3b434e68f7cd869f5a9bac7b1fa7bacbb76bb7ce6d0fb2395ff1dfd884d0cab390fcd517a45e5fdb07f34a7a2f02d75404231f4a4508eb72b72db84330aa'),(12,'duillkp','pablomaxico262@gmail.com','1212121212','IMG-20250302-WA0006.jpg','Bsc',1,NULL,'scrypt:32768:8:1$2lSjxeSjhoXrzeYA$fa02992119659814b1b63220bc435e9ec7d92ffb2d3460dc1936885f8e2653b741f2c9007887f58d998cde890a9b6afac585db917e349eca8efd7fcae47350e6'),(13,'Arshdeep kaur','arshdeep13@gmail.com','4444444444','IMG-20250302-WA0006.jpg','Computer Aplication',6,NULL,'scrypt:32768:8:1$eZxS1zpfxmA3ukPw$f914f9d8f45c99f1e512b89feac760c4e3667d1601259305f4df3a9da47e52ee5560647765a28b3375a62dd08230f38ad8bed63431243079ae1abec35b62149c'),(21,'Deepak','Deepak21@gmail.com','7986851245','deepak_photo.jpg','Computer Aplication',6,NULL,'scrypt:32768:8:1$YU8Uerp42jEOpm6p$6011e375167bd12b7046a3ac6e0bd17e0a5d53f13fc924021ddabd0a0c5b1c7d5bf4d52a54299e86b74d2896837af8b38346c626691bc822a0b2878eddde09ac'),(27,'Gurvinder Singh','guri27@gmail.com','2222222222','arsh.jpg','Computer Aplication',6,NULL,'scrypt:32768:8:1$33dTWDIMjYRzshru$3b45ffff1390df5dbf5beb163260b94005757d096c465c22b3ee711e0ec3b506a62407d1a711d87f90d36f7820f28c8f51e71dac2537c7d8cf0803a2e934d66b'),(45,'Gurvinder Singh','IMDEEP2810@GMAIL.COM','741852963','deepak_photo.jpg','Computer Aplication',3,NULL,'scrypt:32768:8:1$5Pj5kHIyXRpW9gmW$67a0412fb1b995f0045ea4db817cf4e17859d1522bf60e57715b1830fd6ee7e568ee96af48ce9259d44b98a0a8a9729f11182ef6b7dea22ac6cd63f215d98b8e'),(88,'sagar','sagar88@gmail.com','3333333333','IMG-20250302-WA0007.jpg','Computer Aplication',6,NULL,'scrypt:32768:8:1$OqbX3M7E8936rIwF$8595e7179adaba45e204955752c91d8b41a251e5980c9d5b3e4694972b8c7eef3e6977cd2e858aa9986dcb13ac103226730db7b95e371b09fd472617f13f1570'),(108,'ideepdeep','ideepdeep13@gmail.com','1234567899','IMG-20250302-WA0007.jpg','Computer Aplication',6,NULL,'scrypt:32768:8:1$5jUPY0OoAPgeLgdW$60a9f2da1d233b539619b4e930998eb71bf0d5d5a601504d5a396b652283c50bf651c281a9a12b6e0b3eee7d2b22922dcb3b874ec047a3916148fef77c51e0ba'),(222080,'rana','rana22@gmail.com','7837816765','IMG-20250302-WA0007.jpg','Computer Aplication',6,NULL,'scrypt:32768:8:1$DPetCiPjhcCCQEpD$0b7ff2ce9bdf400ab16a4a6f2d71f4ba9d92b803f0e7c8cabe9557994d1ca15e6844cde296d4980ec3c700a74e219d03de59e6e6119aedf5e764943302a6a33a');
/*!40000 ALTER TABLE `login_students` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `teachers`
--

DROP TABLE IF EXISTS `teachers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `teachers` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `department` varchar(50) DEFAULT NULL,
  `subjects` text,
  `experience` int DEFAULT NULL,
  `profile_pic` varchar(255) DEFAULT NULL,
  `password` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=38 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `teachers`
--

LOCK TABLES `teachers` WRITE;
/*!40000 ALTER TABLE `teachers` DISABLE KEYS */;
INSERT INTO `teachers` VALUES (1,'MS.Meenu','imdeep2810@gmail.com','1111111111','Computer Application','Android',10,'IMG-20250302-WA0006.jpg','scrypt:32768:8:1$FFL4cQVYIBPIQNpg$82998e5cdbf3141f470c7c3eb67c7a279fa7749acc0b72184c443fe2454000e366426d3b7faae8191bb9b24d448a70a0be1c945bf7ed5c74d6c6c922d5055bdb'),(2,'Mr.I Gill','igill22@gmail.com','2222222222','Computer Application','microprocessor',10,'IMG-20250302-WA0007.jpg','scrypt:32768:8:1$VYqwD8AaC5mebdml$b9a5a9aa4acba72592ba6129a7b8d457bd16a6810977706c81d705fee4e7ea8f2a4d692c518bf51735bc2027621a33c4ff9111e61c3842631300d2635d40bfa6'),(3,'Ms.Bindu','bunduluthra33@gmail.com','3333333333','Computer Application','Machine Learning',10,'IMG-20250302-WA0002.jpg','scrypt:32768:8:1$hiDVGeQCMitsXOsq$bac4c5f3f61d24b7cbebdac005a6f32a7dc8b2e95a22c00b5dc52d6489bb01c40122acd7cd401be5f817f0d92141a68f630118d5f1a02dd63535c71f572471d3'),(4,'Ms.Abhilasha','Abhilasha44@gmail.com','4444444444','Computer Application','AI',10,'IMG-20250302-WA0003.jpg','scrypt:32768:8:1$wSAOCFgImw6uMW2Q$9509ffd9da65a2ca4ef6dd6b1fe1135b01a70aea1d480b77c1dc2aa387deac621586c3c963152e1952bf262340a7cdcd1853a3f45a44a58f50cf93a190b0e129'),(30,'Sagar','Sagars915575@GMAIL.COM','01234567896','Electrical','AI',10,'arsh.jpg','scrypt:32768:8:1$rPfVolDmsD1FtOim$7584d6e8d8a5deb7207459afd564c16bbb32bc3be55a1c2ce3d5727f640fce6deb46b4834ff96da94c45f7be170a3a4ce17974ba774510a4d81d3bdf304f9165'),(31,'Ms.Reena verma','reena@gmail.com','5555555555','Computer Application','MPD6',10,'IMG-20250302-WA0006.jpg','scrypt:32768:8:1$CcvhbNqNeY4lEQUv$3940f59f105c93355c495f723894891f18a16c1f5ddb29454efec5fcb44cd5897694d05ffaf621ebbe3d19aeda39cc786833ba8765877785a5699488e4447656'),(32,'mproject','mproject@gmail.com','6666666666','Computer Application','ca',10,'DALLE_2025-02-18_23.37.22_-_A_luxurious_and_elegant_Parisian-style_logo_design_for_the_brand_DEEP_incorporating_the_Eiffel_Tower_as_a_central_or_subtle_design_element._The_log.webp','scrypt:32768:8:1$px5Smj4SIMNULfnx$f4b7be66bfc7a2bd0c7285f0531f993e3a15244e37d3a61d668c0bc5079657b6c3c4fa7e1d0069f235c48efb2da90fabbe3bad16d36533ea6748626a701cd70e'),(33,'Deepak','pablomaxico262@gmail.com','7777777777','Computer Application','software ',6,'IMG-20250302-WA0006.jpg','scrypt:32768:8:1$IVln39XPpOLWnTPt$d0bf6af2cb0fd119f12949633820bab53588dfa7f6228479827ef6f45fa7e4766e7d221a3ff0a1129a891602c87dc42abbdc00cd63056009da6bf84a733cdf13'),(34,'meenu','meenu22@gmail.com','7777777777','--Select Department--','software ',6,'IMG-20250302-WA0006.jpg','scrypt:32768:8:1$LhMD2BRfjye7XVkb$fe878ca7630fca8e5ba1d30ed767bc7a67d517fc438cbd8a3731f2443ab45db2ca0b6db62af2f9a4ca8af8859c848ed19542208dbdd766e2ba4a0d58905db3f1'),(37,'Deepak Deepak Bhatti','ideepdeep13@gmail.com','7418529637','Computer Application','software ',6,'Screenshot_2025-04-06_203747.jpg','scrypt:32768:8:1$zFSGnjWG4JVnE7O1$39a48a25aee2060e5c90d8c5a3ebeec2cd0957baa2fd227e8427d9a58490a3b0dbcfafa4e48a441ab18d411f336941eb10764e4d6800ccc1096f4eb999decd8b');
/*!40000 ALTER TABLE `teachers` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-04-12 22:18:28
