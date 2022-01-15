-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jan 15, 2022 at 03:56 AM
-- Server version: 10.4.21-MariaDB
-- PHP Version: 7.4.24

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `bp`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `id` int(11) NOT NULL,
  `username` varchar(10) NOT NULL,
  `no_identitas` varchar(15) NOT NULL,
  `nama` varchar(100) NOT NULL,
  `gender` char(1) NOT NULL,
  `no_hp` varchar(14) NOT NULL,
  `email` varchar(64) NOT NULL,
  `tanggal_lahir` date NOT NULL,
  `alamat` varchar(100) NOT NULL,
  `tanggal_masuk` date NOT NULL,
  `password` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`id`, `username`, `no_identitas`, `nama`, `gender`, `no_hp`, `email`, `tanggal_lahir`, `alamat`, `tanggal_masuk`, `password`) VALUES
(26, 'srndhn23_', '19090102', 'Susi Nurindahsari', 'P', '088228925608', 'susinurindahsari74@gmail.com', '2002-04-23', 'Kota Tegal, Jawa Tengah', '2022-01-02', '$2b$12$Go7pNYT2aCXSSbdxATpgmunFXJxfP74NeHigqkj6SDuh4e.cxMo3S');

-- --------------------------------------------------------

--
-- Table structure for table `enter_parking`
--

CREATE TABLE `enter_parking` (
  `id` int(11) NOT NULL,
  `no_identitas` varchar(15) NOT NULL,
  `no_plat` varchar(10) NOT NULL,
  `waktu_masuk` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `enter_parking`
--

INSERT INTO `enter_parking` (`id`, `no_identitas`, `no_plat`, `waktu_masuk`) VALUES
(1, '19090102', 'G 1234 SN', '2021-12-21 13:11:52'),
(2, '19090102', 'G 1234 SN', '2021-12-23 14:08:08'),
(10, '19090076', 'G 6970 SN', '2022-01-14 03:02:40');

-- --------------------------------------------------------

--
-- Table structure for table `exit_parking`
--

CREATE TABLE `exit_parking` (
  `id` int(11) NOT NULL,
  `no_identitas` varchar(15) NOT NULL,
  `no_plat` varchar(10) NOT NULL,
  `waktu_keluar` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `exit_parking`
--

INSERT INTO `exit_parking` (`id`, `no_identitas`, `no_plat`, `waktu_keluar`) VALUES
(1, '19090102', 'G 1234 SN', '2021-12-21 13:10:50'),
(2, '19090102', 'G 1234 SN', '2021-12-23 14:06:14'),
(5, '19090076', 'G 6970 SN', '2022-01-14 04:12:17');

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `username` varchar(10) NOT NULL,
  `no_identitas` varchar(15) NOT NULL,
  `nama` varchar(100) NOT NULL,
  `gender` char(1) NOT NULL,
  `status` varchar(20) NOT NULL,
  `no_hp` varchar(14) NOT NULL,
  `email` varchar(30) NOT NULL,
  `alamat` varchar(100) NOT NULL,
  `no_plat` varchar(10) NOT NULL,
  `stnk` text NOT NULL,
  `tanggal_masuk` date NOT NULL,
  `password` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`id`, `username`, `no_identitas`, `nama`, `gender`, `status`, `no_hp`, `email`, `alamat`, `no_plat`, `stnk`, `tanggal_masuk`, `password`) VALUES
(1, 'sari23', '19090102', 'Susi Nurindahsari', 'P', 'Mahasiswa', '088228925608', 'sarindahsn23@gmail.com', 'Tegal Selatan', 'G 1234 SN', 'platnomor.jpg', '2021-12-21', 'fe6db529af'),
(2, 'srndhn23', '19090200', 'Susi Nurindahsari', 'P', 'Mahasiswa', '088228925608', 'susinurindahsari74@gmail.com', 'Tegal Selatan', 'G 4321 SN', 'TestSubject- 01.png', '2021-12-21', '9ca20291db'),
(8, 'afanrisand', '19090076', 'Afan Risandi', 'L', 'Mahasiswa', '0881234567890', 'risandiafan@gmail.com', 'Cabawan', 'G 6970 SN', '', '2021-12-26', '12345'),
(12, 'meimei', '19090399', 'Meimei', 'P', 'Mahasiswa', '0811111141111', 'meimeicans@gmail.com', 'Debong Kidul, Tegal Selatan', 'G 1213 SN', '', '2022-01-01', '$2b$12$uj1'),
(15, 'srndhn23', '19090102', 'Susi Nurindahsari', 'P', 'Mahasiswa', '088228925608', 'susinurindahsari74@gmail.com', 'fggggggg', 'G 1213 SN', '', '2022-01-04', '$2b$12$8Yg'),
(21, 'srndhn23', '19090102', 'Susi Nurindahsari', 'P', 'Mahasiswa', '088228925608', 'susinurindahsari74@gmail.com', 'Cabawan', 'G 1213 SN', '', '2022-01-04', '$2b$12$Xm1'),
(22, 'sari', '19090102', 'Susi Nurindahsari', 'P', 'Mahasiswa', '088228925608', 'sarindahsn23@gmail.com', 'Tegal', 'G 1234 SN', 'r', '0000-00-00', '12345');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `enter_parking`
--
ALTER TABLE `enter_parking`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `exit_parking`
--
ALTER TABLE `exit_parking`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admin`
--
ALTER TABLE `admin`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=27;

--
-- AUTO_INCREMENT for table `enter_parking`
--
ALTER TABLE `enter_parking`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `exit_parking`
--
ALTER TABLE `exit_parking`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
