/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

CREATE TABLE IF NOT EXISTS `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `pseudo` varchar(100) NOT NULL,
  `hash` varchar(255) NOT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `level` int DEFAULT '1',
  `color` varchar(30) DEFAULT 'white',
  PRIMARY KEY (`id`),
  UNIQUE KEY `pseudo` (`pseudo`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO `users` (`id`, `pseudo`, `hash`, `created_at`, `level`, `color`) VALUES
	(1, 'jcy', '$2b$12$J9gVsa4/LJDAj5QT0rsxreR7JpRIHcMHaXZ8.nxKUzgB8k2rJ7L4C', '2026-04-13 16:03:36', 2, 'lightgreen'),
	(2, 'student1', '$2b$12$3PM85kZxTJWOUvBEqgkZ0uxSHn2r4IDAmq5RgUx/quvW7fipE3dE2', '2026-04-13 16:03:52', 1, 'lightblue');


CREATE TABLE IF NOT EXISTS `maps` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(200) NOT NULL,
  `author_id` int NOT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `author_id` (`author_id`),
  CONSTRAINT `maps_ibfk_1` FOREIGN KEY (`author_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;;

INSERT INTO `maps` (`id`, `title`, `author_id`, `created_at`) VALUES
	(1, 'Idées pour ProjPython', 1, '2026-04-13 16:05:05'),
	(2, 'Intérêts SI-CA1a', 1, '2026-04-13 16:05:44');

CREATE TABLE IF NOT EXISTS `nodes` (
  `id` int NOT NULL AUTO_INCREMENT,
  `map_id` int NOT NULL,
  `parent_id` int DEFAULT NULL,
  `author_id` int NOT NULL,
  `text` text NOT NULL,
  `level` int NOT NULL DEFAULT '0',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `map_id` (`map_id`),
  KEY `parent_id` (`parent_id`),
  KEY `author_id` (`author_id`),
  CONSTRAINT `nodes_ibfk_1` FOREIGN KEY (`map_id`) REFERENCES `maps` (`id`),
  CONSTRAINT `nodes_ibfk_2` FOREIGN KEY (`parent_id`) REFERENCES `nodes` (`id`) ON DELETE CASCADE,
  CONSTRAINT `nodes_ibfk_3` FOREIGN KEY (`author_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=56 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO `nodes` (`id`, `map_id`, `parent_id`, `author_id`, `text`, `level`, `created_at`) VALUES
	(1, 2, 13, 1, 'Camille', 1, '2026-04-13 16:08:44'),
	(2, 2, 1, 1, 'EPFL/CMS', 2, '2026-04-13 16:09:23'),
	(3, 2, 13, 1, 'David', 1, '2026-04-13 16:10:10'),
	(4, 2, 3, 1, 'CFC Matu / Maraîcher', 2, '2026-04-13 16:11:10'),
	(5, 2, 13, 1, 'Ruben', 1, '2026-04-13 16:12:56'),
	(6, 2, 5, 1, 'Matu', 2, '2026-04-13 16:13:47'),
	(7, 2, 5, 1, 'Théologie', 2, '2026-04-13 16:14:21'),
	(8, 2, 5, 2, 'Planificateur financier', 2, '2026-04-13 16:15:03'),
	(10, 1, 14, 2, 'gaming_hub', 1, '2026-04-13 16:17:40'),
	(11, 1, 14, 1, 'mindmaps', 1, '2026-04-13 16:18:18'),
	(12, 1, 14, 1, 'festival', 1, '2026-04-13 16:18:38'),
	(13, 2, NULL, 1, 'Intérêts des SI-CA1a', 0, '2026-04-13 17:17:21'),
	(14, 1, NULL, 1, 'Idées pour projet PythonBD', 0, '2026-04-13 17:18:46'),
	(15, 2, 7, 1, 'Est-ce à la HET-Pro ?', 3, '2026-04-13 19:18:52'),
	(17, 2, 15, 1, 'Yes of course', 4, '2026-04-13 19:22:10'),
	(18, 2, 17, 1, 'Thanks', 5, '2026-04-14 15:48:52'),
	(19, 2, 2, 1, 'Nice ', 3, '2026-04-14 15:49:18'),
	(20, 2, 4, 1, 'Beau jardin', 3, '2026-04-14 15:49:57'),
	(21, 2, 20, 1, 'Oui mais difficile', 4, '2026-04-14 15:50:15'),
	(22, 1, 12, 1, 'BD existante', 2, '2026-04-14 15:59:28'),
	(23, 1, 12, 1, 'Représentation Web existante', 2, '2026-04-14 15:59:46'),
	(24, 1, 22, 1, 'Peut être un avantage', 3, '2026-04-14 16:00:01'),
	(25, 1, 22, 1, 'Peut devenir lassant', 3, '2026-04-14 16:00:13'),
	(26, 1, 10, 1, 'Pourrait être passionnant', 2, '2026-04-14 16:00:31'),
	(27, 1, 10, 1, 'Finalement trop difficile', 2, '2026-04-14 16:00:47'),
	(28, 1, 27, 1, 'Nécessite trop de classes', 3, '2026-04-14 16:01:01'),
	(29, 1, 27, 1, 'Nécessite trop de fenêtres', 3, '2026-04-14 16:01:12'),
	(30, 1, 27, 1, 'Demande, en plus des nouveautés (BD), de programmer un jeu', 3, '2026-04-14 16:01:34'),
	(31, 1, 11, 1, 'Nouvelle BD, nouveau concept', 2, '2026-04-14 16:02:00'),
	(32, 1, 31, 1, 'Nécessite + travail JCY', 3, '2026-04-14 16:02:09'),
	(33, 1, 11, 1, 'Faisable en 3 sprints', 2, '2026-04-14 16:02:21'),
	(34, 1, 33, 1, 'Affichage simple puis complexe', 3, '2026-04-14 16:03:24'),
	(35, 1, 33, 1, 'Login / register', 3, '2026-04-14 16:03:42'),
	(36, 1, 33, 1, 'Edition du mindmap', 3, '2026-04-14 16:03:57'),
	(37, 1, 14, 1, 'Calculs de trajectoire fusée lunaire', 1, '2026-04-14 16:05:27'),
	(38, 1, 37, 1, 'Amusant', 2, '2026-04-14 16:05:41'),
	(39, 1, 37, 1, 'Risque de beaucoup de temps à chercher paramètres', 2, '2026-04-14 16:06:05'),
	(40, 1, 14, 1, 'Photos avion-lune', 1, '2026-04-14 16:07:06'),
	(41, 1, 40, 1, 'Pas forcément intéressant pour élèves', 2, '2026-04-14 16:07:32'),
	(42, 1, 40, 1, 'Images pas stockable en BD', 2, '2026-04-14 16:07:57'),
	(43, 2, 13, 2, 'Amin', 1, '2026-04-14 16:10:11'),
	(44, 2, 43, 2, 'Installateur électricien', 2, '2026-04-14 16:10:33'),
	(45, 2, 13, 2, 'Tavee', 1, '2026-04-14 16:10:55'),
	(46, 2, 45, 2, 'Gymnase / Santé', 2, '2026-04-14 16:11:09'),
	(47, 2, 13, 2, 'Eyuel', 1, '2026-04-14 16:11:33'),
	(48, 2, 47, 2, 'Gymnase', 2, '2026-04-14 16:11:46'),
	(49, 2, 13, 2, 'Marc', 1, '2026-04-14 16:11:59'),
	(50, 2, 49, 2, 'Vente auto', 2, '2026-04-14 16:12:28'),
	(51, 2, 13, 2, 'Noor', 1, '2026-04-14 16:14:18'),
	(52, 2, 51, 2, 'Gymnase  / Biochimie', 2, '2026-04-14 16:14:40'),
	(53, 2, 13, 2, 'Kodjo', 1, '2026-04-14 16:15:01'),
	(54, 2, 53, 2, 'Manutention / montage', 2, '2026-04-14 16:15:25'),
	(55, 2, 53, 2, 'Multimédia', 2, '2026-04-14 16:15:36');


/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
