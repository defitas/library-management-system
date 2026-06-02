-- phpMyAdmin SQL Dump
-- version 4.8.5
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Feb 06, 2022 at 01:24 PM
-- Server version: 10.1.38-MariaDB
-- PHP Version: 7.3.3

SET SQL_MODE = "";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `lms`
--

-- --------------------------------------------------------

-- Bersihkan tabel lama untuk menghindari tabrakan struktur
SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS `reserve`;
DROP TABLE IF EXISTS `books`;
DROP TABLE IF EXISTS `users`;
DROP TABLE IF EXISTS `admin`;
SET FOREIGN_KEY_CHECKS = 1;

-- 1. Struktur Tabel `admin` (AUTO_INCREMENT langsung dipasang di awal)
CREATE TABLE `admin` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(255) NOT NULL,
  `password` varchar(1000) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO `admin` (`id`, `email`, `password`) VALUES
(1, 'hamza@gmail.com', '025db420560617303c2ba988d050ec62562343bc0fb0358d31d2f0bae8dbede8');


-- 2. Struktur Tabel `books`
CREATE TABLE `books` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `desc` longtext NOT NULL,
  `author` varchar(255) NOT NULL,
  `availability` tinyint(1) NOT NULL,
  `edition` varchar(255) NOT NULL,
  `count` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO `books` (`id`, `name`, `desc`, `author`, `availability`, `edition`, `count`) VALUES
(1, '101 Ways To Be A Software Engineer', 'Lorem ipsum dolor sit amet, consectetur adipisicing elit.', 'Mr. Johnny Test', 1, '1', 3),
(2, 'JAVA For Absolute Beginners', 'Step into the basics of java programmming along with globally famed programmer', '', 1, '1', 5);


-- 3. Struktur Tabel `users` (Menyesuaikan kompatibilitas database Azure)
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(1000) NOT NULL,
  `bio` longtext NOT NULL,
  `mob` varchar(255) NOT NULL,
  `lock` tinyint(1) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO `users` (`id`, `name`, `email`, `password`, `bio`, `mob`, `lock`, `created_at`) VALUES
(1, 'Hamza', 'hamza@gmail.com', '025db420560617303c2ba988d050ec62562343bc0fb0358d31d2f0bae8dbede8', 'They watch you from the shelf while you sleep 👀.', '', 0, '2021-11-09 00:00:00'),
(6, 'Naveed Ali', 'naveed@gmail.com', '025db420560617303c2ba988d050ec62562343bc0fb0358d31d2f0bae8dbede8', 'Hi :)! Long time no see ❤️', '', 0, '2021-11-18 23:07:53');


-- 4. Struktur Tabel `reserve`
CREATE TABLE `reserve` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `book_id` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO `reserve` (`id`, `user_id`, `book_id`) VALUES
(1, 1, 1),
(2, 6, 1);