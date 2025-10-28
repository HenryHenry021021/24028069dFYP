CREATE DATABASE IF NOT EXISTS CapstoneProject24028069d;
USE CapstoneProject24028069d;




CREATE TABLE `booking_time_slot` (
  `id` int NOT NULL,
  `title` varchar(255) NOT NULL,
  `timeSlotGroupId` varchar(50) DEFAULT NULL,
  `start` datetime NOT NULL,
  `end` datetime NOT NULL,
  `status` enum('Available','Unavailable','Reserved','Pending') DEFAULT 'Available',
  `teacher_id` varchar(20) NOT NULL,
  `content` text,
  `capacity` int DEFAULT '0',
  `vacancy` int DEFAULT NULL,
  `deadline` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `booking_time_slot`
--

INSERT INTO `booking_time_slot` (`id`, `title`, `timeSlotGroupId`, `start`, `end`, `status`, `teacher_id`, `content`, `capacity`, `vacancy`, `deadline`) VALUES
(13, 'ymc-fyp pre', 'a', '2025-09-03 09:30:00', '2025-09-03 11:30:00', 'Available', '2', 'Lecture on Software Engineering', 4, NULL, NULL),
(14, 'asdCOMP3438 - LEC001', 'a', '2025-09-03 12:30:00', '2025-09-03 14:00:00', 'Unavailable', '2', 'Database Systems Lecture', 0, NULL, NULL),
(15, 'qweELC3524 - SEM002', 'b', '2025-09-04 16:00:00', '2025-09-04 17:30:00', 'Available', '2', 'Seminar on Communication', 30, NULL, NULL),
(16, 'aaaCOMP3438 - LAB002', 'b', '2025-09-05 13:30:00', '2025-09-05 14:30:00', 'Reserved', '4', 'Lab session', 20, NULL, NULL),
(17, 'pppDSAI4205 - LEC001', 'c', '2025-09-05 15:30:00', '2025-09-05 17:00:00', 'Available', '4', 'AI lecture', 100, NULL, NULL),
(18, 'lllDSAI4205 - TUT005', 'c', '2025-09-02 18:30:00', '2025-09-02 19:30:00', 'Unavailable', '4', 'Tutorial session', 0, NULL, NULL),
(19, '123', 'd', '2025-09-07 16:39:00', '2025-09-07 15:42:00', 'Available', '4', '331', 4, NULL, NULL),
(20, 'qq', 'd', '2025-09-02 20:53:00', '2025-09-02 21:49:00', 'Available', '4', '2334', 33, NULL, NULL),
(21, 'qweeqeq', 'e', '2025-09-02 22:50:00', '2025-09-02 23:48:00', 'Available', '4', 'qwe', 33, NULL, NULL),
(22, 'qweeqeq', 'e', '2025-09-02 19:31:00', '2025-09-02 19:53:00', 'Available', '4', 'qwe', 33, NULL, NULL),
(23, 'Henry', 'e', '2025-09-07 19:06:00', '2025-09-07 20:06:00', 'Available', '4', 'erq', 4, NULL, NULL),
(24, 'asdddd', 'e', '2025-09-07 21:06:00', '2025-09-07 22:06:00', 'Available', '4', 'qq', 123, NULL, NULL),
(25, 'eeeeeeeeeee', 'e', '2025-09-14 14:50:00', '2025-09-14 15:50:00', 'Available', '4', 'AI', 3, NULL, NULL),
(26, 'eeeeeeeeeee', 'e', '2025-09-13 14:50:00', '2025-09-13 15:50:00', 'Available', '4', 'Web', 3, NULL, NULL),
(27, 'rrr', 'JQHL896860', '2025-09-12 19:30:00', '2025-09-12 21:30:00', 'Available', '4', 'qweqwe', 4, NULL, NULL),
(28, 'rrr', 'JQHL896860', '2025-09-13 19:30:00', '2025-09-13 21:30:00', 'Available', '4', 'qweqwe', 33, NULL, NULL),
(29, 'rrr', 'JQHL896860', '2025-09-14 11:30:00', '2025-09-12 12:30:00', 'Available', '4', 'qweqwe', 33, NULL, NULL),
(30, '3', 'FQGE849591', '2025-09-27 19:33:00', '2025-09-27 22:33:00', 'Available', '4', '33', 33, NULL, NULL),
(31, '3', 'FQGE849591', '2025-09-27 19:34:00', '2025-09-27 20:34:00', 'Available', '4', '33', 33, NULL, NULL),
(33, 'asdasd', 'BHLV073437', '2025-09-25 16:26:00', '2025-09-25 22:26:00', 'Available', '4', 'aaaaaaaaaaaaaaaaaaaa', 22, 22, '2025-09-19 16:27:00'),
(34, 'ccccc', 'EVLI921642', '2025-09-27 04:56:00', '2025-09-27 09:56:00', 'Available', '4', 'ccccccc', 11, 4, '2025-09-25 16:56:00'),
(35, 'ccccc', 'EXKV585947', '2025-09-29 08:56:00', '2025-09-29 09:56:00', 'Available', '4', 'ccccccc', 11, 9, '2025-09-25 16:56:00'),
(36, 'ccccc', 'EXKV585947', '2025-09-26 16:57:00', '2025-09-26 17:00:00', 'Available', '4', 'ccccccc', 11, 7, '2025-09-25 16:56:00'),
(37, 'ccccc', 'EXKV585947', '2025-09-30 16:58:00', '2025-09-30 19:58:00', 'Available', '4', 'ccccccc', 11, 9, '2025-09-25 16:56:00');

-- --------------------------------------------------------

--
-- Table structure for table `demo`
--

CREATE TABLE `demo` (
  `id` int NOT NULL,
  `msg` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `demo`
--

INSERT INTO `demo` (`id`, `msg`) VALUES
(1, 'Hello from MySQL!');

-- --------------------------------------------------------

--
-- Table structure for table `roles`
--

CREATE TABLE `roles` (
  `id` int NOT NULL,
  `role_name` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `roles`
--

INSERT INTO `roles` (`id`, `role_name`) VALUES
(3, 'admin'),
(1, 'student'),
(2, 'teacher');

-- --------------------------------------------------------

--
-- Table structure for table `students_booking`
--

CREATE TABLE `students_booking` (
  `booking_id` int NOT NULL,
  `student_id` int NOT NULL,
  `time_slot_id` int NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `status` enum('Booked','Check-in','Cancel','Matched') NOT NULL DEFAULT 'Booked',
  `priority` int UNSIGNED NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `students_booking`
--

INSERT INTO `students_booking` (`booking_id`, `student_id`, `time_slot_id`, `created_at`, `status`, `priority`) VALUES
(4, 12, 28, '2025-09-04 22:25:51', 'Matched', 5),
(5, 11, 28, '2025-09-09 08:51:51', 'Matched', 4),
(6, 13, 27, '2025-09-11 06:24:36', 'Booked', 5),
(7, 12, 27, '2025-09-11 06:52:19', 'Booked', 6),
(9, 11, 27, '2025-09-12 07:18:44', 'Booked', 4),
(25, 1, 27, '2025-09-13 06:34:09', 'Booked', 4),
(29, 5, 27, '2025-09-14 07:19:35', 'Booked', 2),
(30, 6, 27, '2025-09-14 06:19:35', 'Booked', 2),
(31, 15, 28, '2025-09-14 08:18:52', 'Cancel', 3),
(32, 15, 27, '2025-09-14 08:18:52', 'Booked', 3);

-- --------------------------------------------------------

--
-- Table structure for table `time_slot_group_student`
--

CREATE TABLE `time_slot_group_student` (
  `id` int NOT NULL,
  `group_id` varchar(50) NOT NULL,
  `user_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `time_slot_group_student`
--

INSERT INTO `time_slot_group_student` (`id`, `group_id`, `user_id`) VALUES
(3, 'BHLV073437', 4),
(4, 'BHLV073437', 1),
(5, 'EVLI921642', 4),
(6, 'EVLI921642', 1),
(7, 'EXKV585947', 4),
(8, 'EXKV585947', 1);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL,
  `full_name` varchar(100) NOT NULL,
  `role_id` int NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `email`, `password`, `full_name`, `role_id`, `created_at`, `updated_at`) VALUES
(1, '021021hxc@gmail.com', 'abc123', 'henry', 1, '2025-09-01 15:10:24', '2025-09-13 06:31:33'),
(2, 'teacher1@polyu.edu.hk', 'pass456', 'Dr. Chan', 2, '2025-09-01 15:10:24', '2025-09-01 15:10:24'),
(3, 'admin1@polyu.edu.hk', 'admin789', 'Dr. HONG', 2, '2025-09-01 15:10:24', '2025-09-04 20:09:44'),
(4, '24028069d@connect.polyu.hk', '123456', 'Henry4', 2, '2025-09-06 01:36:35', '2025-09-06 01:36:44'),
(5, 's2025009@connect.polyu.hk', 'stu999', 'Ivy Lau', 1, '2025-09-07 03:00:00', '2025-09-07 03:00:00'),
(6, 's2025010@connect.polyu.hk', 'stu1010', 'Jason Wong', 1, '2025-09-07 03:05:00', '2025-09-07 03:05:00'),
(7, 's2025011@connect.polyu.hk', 'stu1111', 'Karen Lee', 1, '2025-09-07 03:10:00', '2025-09-07 03:10:00'),
(8, 's2025012@connect.polyu.hk', 'stu1012', 'Student 8', 1, '2025-09-14 09:12:58', '2025-09-14 09:12:58'),
(9, 's2025013@connect.polyu.hk', 'stu1013', 'Student 9', 1, '2025-09-14 09:12:58', '2025-09-14 09:12:58'),
(10, 's2025014@connect.polyu.hk', 'stu1014', 'Student 10', 1, '2025-09-14 09:12:58', '2025-09-14 09:12:58'),
(11, 's2025015@connect.polyu.hk', 'stu1015', 'Student 11', 1, '2025-09-14 09:12:58', '2025-09-14 09:12:58'),
(12, 's2025016@connect.polyu.hk', 'stu1016', 'Student 12', 1, '2025-09-14 09:12:58', '2025-09-14 09:12:58'),
(13, 's2025017@connect.polyu.hk', 'stu1017', 'Student 13', 1, '2025-09-14 09:12:58', '2025-09-14 09:12:58'),
(14, 's2025018@connect.polyu.hk', 'stu1018', 'Student 14', 1, '2025-09-14 09:12:58', '2025-09-14 09:12:58'),
(15, 's2025019@connect.polyu.hk', 'stu1019', 'Student 15', 1, '2025-09-14 09:12:58', '2025-09-14 09:12:58'),
(17, '24028069a@connect.polyu.hk', '650mQO', '', 1, '2025-09-18 08:28:20', '2025-09-18 08:28:20');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `booking_time_slot`
--
ALTER TABLE `booking_time_slot`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `demo`
--
ALTER TABLE `demo`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `roles`
--
ALTER TABLE `roles`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `role_name` (`role_name`);

--
-- Indexes for table `students_booking`
--
ALTER TABLE `students_booking`
  ADD PRIMARY KEY (`booking_id`);

--
-- Indexes for table `time_slot_group_student`
--
ALTER TABLE `time_slot_group_student`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`),
  ADD KEY `role_id` (`role_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `booking_time_slot`
--
ALTER TABLE `booking_time_slot`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=38;

--
-- AUTO_INCREMENT for table `demo`
--
ALTER TABLE `demo`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `roles`
--
ALTER TABLE `roles`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `students_booking`
--
ALTER TABLE `students_booking`
  MODIFY `booking_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=56;

--
-- AUTO_INCREMENT for table `time_slot_group_student`
--
ALTER TABLE `time_slot_group_student`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `users`
--
ALTER TABLE `users`
  ADD CONSTRAINT `users_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `roles` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
