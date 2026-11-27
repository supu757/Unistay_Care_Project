-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jun 11, 2026 at 08:06 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `unistay_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `bursary_monthly_records`
--

CREATE TABLE `bursary_monthly_records` (
  `id` int(11) NOT NULL,
  `index_no` varchar(50) NOT NULL,
  `bursary_month` varchar(20) NOT NULL,
  `received_status` varchar(10) NOT NULL,
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `bursary_monthly_records`
--

INSERT INTO `bursary_monthly_records` (`id`, `index_no`, `bursary_month`, `received_status`, `updated_at`) VALUES
(1, '24IT0537', 'May', 'NO', '2026-05-25 18:31:17'),
(2, '24IT0535', 'May', 'NO', '2026-06-05 05:00:41'),
(3, '24IT0537', 'June', 'NO', '2026-06-10 06:00:48'),
(5, '24IT0537', 'January', 'NO', '2026-06-10 14:18:11');

-- --------------------------------------------------------

--
-- Table structure for table `go_home_logs`
--

CREATE TABLE `go_home_logs` (
  `id` int(11) NOT NULL,
  `index_no` varchar(50) NOT NULL,
  `departure_date` date NOT NULL,
  `departure_time` time NOT NULL,
  `arrival_date` date DEFAULT NULL,
  `arrival_time` time DEFAULT NULL,
  `status` varchar(50) DEFAULT 'Away'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `go_home_logs`
--

INSERT INTO `go_home_logs` (`id`, `index_no`, `departure_date`, `departure_time`, `arrival_date`, `arrival_time`, `status`) VALUES
(1, '24IT0537', '2026-05-22', '17:25:00', '2026-05-25', '23:09:13', 'Returned'),
(2, '24IT0537', '2026-05-25', '16:35:00', '2026-05-26', '00:04:44', 'Returned'),
(3, '24IT0537', '2026-05-27', '18:25:00', '2026-05-28', '12:07:31', 'Returned'),
(4, '24IT0537', '0226-06-03', '17:20:00', '2026-06-05', '15:47:19', 'Returned'),
(5, '24IT0535', '2026-06-05', '17:30:00', NULL, NULL, 'Away'),
(6, '24IT0537', '2026-06-05', '17:30:00', '2026-06-10', '19:42:24', 'Returned'),
(7, '24IT0537', '2026-06-10', '17:30:00', '2026-06-10', '22:40:55', 'Returned');

-- --------------------------------------------------------

--
-- Table structure for table `go_out_logs`
--

CREATE TABLE `go_out_logs` (
  `id` int(11) NOT NULL,
  `index_no` varchar(50) NOT NULL,
  `out_date` date NOT NULL,
  `out_time` time NOT NULL,
  `in_date` date DEFAULT NULL,
  `in_time` time DEFAULT NULL,
  `status` varchar(50) DEFAULT 'Outside'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `go_out_logs`
--

INSERT INTO `go_out_logs` (`id`, `index_no`, `out_date`, `out_time`, `in_date`, `in_time`, `status`) VALUES
(1, '24IT0537', '2026-05-26', '08:20:00', '2026-06-03', '22:03:07', 'Inside'),
(2, '24IT0537', '2026-06-04', '09:30:00', '2026-06-05', '15:48:08', 'Inside');

-- --------------------------------------------------------

--
-- Table structure for table `student_attendance`
--

CREATE TABLE `student_attendance` (
  `id` int(11) NOT NULL,
  `index_no` varchar(50) NOT NULL,
  `date` date NOT NULL,
  `status` varchar(20) DEFAULT 'Present',
  `marked_time` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `student_profile`
--

CREATE TABLE `student_profile` (
  `index_no` varchar(50) NOT NULL,
  `fullname` varchar(255) NOT NULL,
  `name_initials` varchar(100) NOT NULL,
  `dob` date NOT NULL,
  `district` varchar(50) NOT NULL,
  `town` varchar(100) NOT NULL,
  `distance_itum` int(11) NOT NULL,
  `phone` varchar(20) NOT NULL,
  `religion` varchar(50) NOT NULL,
  `nation` varchar(50) NOT NULL,
  `mother_name` varchar(255) NOT NULL,
  `mother_phone` varchar(20) NOT NULL,
  `mother_job` varchar(100) NOT NULL,
  `father_name` varchar(255) NOT NULL,
  `father_phone` varchar(20) NOT NULL,
  `father_job` varchar(100) NOT NULL,
  `ol_year` int(11) NOT NULL,
  `ol_index` varchar(50) NOT NULL,
  `ol_science` varchar(2) NOT NULL,
  `ol_maths` varchar(2) NOT NULL,
  `ol_english` varchar(2) NOT NULL,
  `ol_religion` varchar(2) NOT NULL,
  `ol_language` varchar(2) NOT NULL,
  `ol_history` varchar(2) NOT NULL,
  `ol_basket1_name` varchar(100) NOT NULL,
  `ol_basket1_grade` varchar(2) NOT NULL,
  `ol_basket2_name` varchar(100) NOT NULL,
  `ol_basket2_grade` varchar(2) NOT NULL,
  `ol_basket3_name` varchar(100) NOT NULL,
  `ol_basket3_grade` varchar(2) NOT NULL,
  `al_year` int(11) NOT NULL,
  `al_index` varchar(50) NOT NULL,
  `al_zscore` varchar(20) NOT NULL,
  `al_maths` varchar(2) NOT NULL,
  `al_physics` varchar(2) NOT NULL,
  `al_chemistry` varchar(2) NOT NULL,
  `room_no` varchar(20) DEFAULT 'Pending'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `student_profile`
--

INSERT INTO `student_profile` (`index_no`, `fullname`, `name_initials`, `dob`, `district`, `town`, `distance_itum`, `phone`, `religion`, `nation`, `mother_name`, `mother_phone`, `mother_job`, `father_name`, `father_phone`, `father_job`, `ol_year`, `ol_index`, `ol_science`, `ol_maths`, `ol_english`, `ol_religion`, `ol_language`, `ol_history`, `ol_basket1_name`, `ol_basket1_grade`, `ol_basket2_name`, `ol_basket2_grade`, `ol_basket3_name`, `ol_basket3_grade`, `al_year`, `al_index`, `al_zscore`, `al_maths`, `al_physics`, `al_chemistry`, `room_no`) VALUES
('24IT0480', 'Dunushingha Karunasagara Mudiyanselage Nurasha Tharakee Karunasagara ', 'D.K.M.N.T.Karunasagara', '2004-07-08', 'Badulla', 'Welimada', 225, '0702459122', 'Buddhist', 'Sinhala', 'D.M.Nishanthi Pradeepika', '0766292707', 'House Wife', 'D.K.M.Chaminda Karunasagara', '0718269533', 'Job Agricultural Officer', 2020, '65624816', 'B', 'A', 'A', 'A', 'A', 'A', 'ICT', 'B', 'civic', 'A', 'dancing', 'A', 2023, '64624816', '0.3716', 'C', 'C', 'S', 'Pending'),
('24IT0535', 'Udawaththage Hasheendra Kaumith Udawaththa', 'U.H.K Udawaththa', '2005-01-11', 'Kaluthara', 'Ingiriya', 31, '0717478071', 'Buddhism', 'Sinhala', 'K.T.Kanthi', '0777973512', 'Teaching', 'J.J.Udawaththa', '0774829614', 'Teaching', 2020, '98695478', 'A', 'A', 'B', 'A', 'A', 'A', 'IT', 'A', 'commerce', 'A', 'Sinhala Literature', 'A', 2023, '72365968', '0.1123', 'C', 'C', 'S', 'Pending'),
('24IT0537', 'Subasin Kattadige Supuni Udeshika', 'S.K.S. Udeshika', '2004-02-25', 'Hambantota', 'Walasmulla', 219, '0740517117', 'Buddhist', 'Sinhala', 'M.P.Podinona', '0713828010', 'House Wife', 'S.K.Karunarathna', '0713004036', 'Mason ', 2020, '61958204', 'A', 'A', 'A', 'A', 'A', 'A', 'ICT', 'A', 'Tamil', 'A', 'Music', 'A', 2023, '7214391', '0.3374', 'B', 'S', 'S', 'Pending'),
('24IT0542', 'Walpita Gamage Vinuri Wathmavee Walpitagama', 'W.G.V.W.Walpitagama', '2003-07-24', 'Galle', 'Galle', 121, '0741603135', 'Buddhism', 'Sinhala', 'S.G.S.Deepika Samarawickrama', '0767258054', 'House wife', 'W.G.Samanthi', '0779468743', 'Farming', 2019, '9163743', 'B', 'A', 'A', 'A', 'A', 'A', 'Commerce', 'B', 'English Lit', 'A', 'ICT', 'A', 2023, '134243', '-1.2345', 'S', 'S', 'S', 'CD202');

-- --------------------------------------------------------

--
-- Table structure for table `student_welfare`
--

CREATE TABLE `student_welfare` (
  `id` int(11) NOT NULL,
  `index_no` varchar(50) NOT NULL,
  `bursary_status` varchar(50) DEFAULT 'Pending',
  `complaint_title` varchar(255) DEFAULT NULL,
  `complaint_description` text DEFAULT NULL,
  `complaint_status` varchar(50) DEFAULT 'Open',
  `submitted_date` timestamp NOT NULL DEFAULT current_timestamp(),
  `monthly_bursary_received` varchar(10) DEFAULT 'NO'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `student_welfare`
--

INSERT INTO `student_welfare` (`id`, `index_no`, `bursary_status`, `complaint_title`, `complaint_description`, `complaint_status`, `submitted_date`, `monthly_bursary_received`) VALUES
(1, '24IT0537', 'Pending', NULL, NULL, 'Open', '2026-05-25 17:54:21', 'NO');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `role` varchar(20) NOT NULL,
  `fullname` varchar(100) NOT NULL,
  `unique_id` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `role`, `fullname`, `unique_id`, `email`, `password`, `created_at`) VALUES
(1, 'student', 'Subasin Kattadige Supuni Udeshika', '24IT0537', 'supuniudeshika297@gmail.com', 'Supu@259', '2026-05-25 13:03:07'),
(2, 'student', 'Garusinghage Ishan Shanaka', '24IT551', 'shanmax@2004gmail.com', 'GI@2004', '2026-05-28 06:40:40'),
(3, 'warden', 'Garusinghage Ishan Shanaka', 'WD0005', 'ishanshanaka29@gmail.com', 'Ishan@259', '2026-05-28 17:48:23'),
(4, 'warden', 'podinona', 'WD0056', 'podinona56@gmail.com', 'Podi@56', '2026-05-28 18:13:31'),
(5, 'warden', 'ijihubuhbuhub', 'WD8963', 'mikjii@gmil.com', '12369', '2026-05-28 18:15:10'),
(6, 'warden', 'Disna Thushari', 'WD963', 'disanathushari@gmail.com', '1234', '2026-05-28 18:16:51'),
(7, 'warden', 'Nayana Sanjeewani', 'WD0030', 'nayanasanjiwani@123', '78963', '2026-05-28 18:22:22'),
(8, 'warden', 'SubasinKattadige Disna Thushari', 'WD0010', 'disnathusari@56gmail.com', 'DT@56', '2026-06-03 15:39:10'),
(9, 'student', 'W.G.V.W.Walpitagama', '24IT0542', 'vinuriwathmavi24@gmail.com', 'Vinu123', '2026-06-03 18:32:05'),
(10, 'student', 'Udawaththage Kaumith ', '24IT0535', 'kaumith.me@gmail.com', 'UD@535', '2026-06-05 04:52:00'),
(11, 'student', 'Nurasha Tarakee', '24IT0480', 'nurashatharakee1@gmail.com', 'NT@480', '2026-06-05 07:45:19'),
(12, 'student', 'Vasanthini Karunakanthan', '24IT0538', 'karunakanthanvasanthini@gmail.com', 'VK@538', '2026-06-05 08:39:33');

-- --------------------------------------------------------

--
-- Table structure for table `wardens`
--

CREATE TABLE `wardens` (
  `warden_id` varchar(50) NOT NULL,
  `full_name` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `bursary_monthly_records`
--
ALTER TABLE `bursary_monthly_records`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `unique_student_month` (`index_no`,`bursary_month`);

--
-- Indexes for table `go_home_logs`
--
ALTER TABLE `go_home_logs`
  ADD PRIMARY KEY (`id`),
  ADD KEY `index_no` (`index_no`);

--
-- Indexes for table `go_out_logs`
--
ALTER TABLE `go_out_logs`
  ADD PRIMARY KEY (`id`),
  ADD KEY `index_no` (`index_no`);

--
-- Indexes for table `student_attendance`
--
ALTER TABLE `student_attendance`
  ADD PRIMARY KEY (`id`),
  ADD KEY `index_no` (`index_no`);

--
-- Indexes for table `student_profile`
--
ALTER TABLE `student_profile`
  ADD PRIMARY KEY (`index_no`);

--
-- Indexes for table `student_welfare`
--
ALTER TABLE `student_welfare`
  ADD PRIMARY KEY (`id`),
  ADD KEY `index_no` (`index_no`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `unique_id` (`unique_id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `wardens`
--
ALTER TABLE `wardens`
  ADD PRIMARY KEY (`warden_id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `bursary_monthly_records`
--
ALTER TABLE `bursary_monthly_records`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `go_home_logs`
--
ALTER TABLE `go_home_logs`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `go_out_logs`
--
ALTER TABLE `go_out_logs`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `student_attendance`
--
ALTER TABLE `student_attendance`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `student_welfare`
--
ALTER TABLE `student_welfare`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `go_home_logs`
--
ALTER TABLE `go_home_logs`
  ADD CONSTRAINT `go_home_logs_ibfk_1` FOREIGN KEY (`index_no`) REFERENCES `users` (`unique_id`) ON DELETE CASCADE;

--
-- Constraints for table `go_out_logs`
--
ALTER TABLE `go_out_logs`
  ADD CONSTRAINT `go_out_logs_ibfk_1` FOREIGN KEY (`index_no`) REFERENCES `users` (`unique_id`) ON DELETE CASCADE;

--
-- Constraints for table `student_attendance`
--
ALTER TABLE `student_attendance`
  ADD CONSTRAINT `student_attendance_ibfk_1` FOREIGN KEY (`index_no`) REFERENCES `users` (`unique_id`) ON DELETE CASCADE;

--
-- Constraints for table `student_welfare`
--
ALTER TABLE `student_welfare`
  ADD CONSTRAINT `student_welfare_ibfk_1` FOREIGN KEY (`index_no`) REFERENCES `users` (`unique_id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
