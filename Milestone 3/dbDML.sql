USE fareshare_db;
SET FOREIGN_KEY_CHECKS = 0;

-- ============================================================
-- 1. USER (Supertype)
-- ============================================================
INSERT INTO User (user_id, phone_number, full_name, user_role, profile_photo, created_at) VALUES
-- Riders (R101-R110)
('R101', '+923001234501', 'Ahmed Ali',          'Rider',  NULL, '2025-01-10 08:00:00'),
('R102', '+923001234502', 'Fatima Noor',        'Rider',  NULL, '2025-01-12 09:00:00'),
('R103', '+923001234503', 'Usman Tariq',        'Rider',  NULL, '2025-01-15 10:00:00'),
('R104', '+923001234504', 'Sana Malik',         'Rider',  NULL, '2025-01-18 11:00:00'),
('R105', '+923001234505', 'Bilal Khan',         'Rider',  NULL, '2025-01-20 12:00:00'),
('R106', '+923001234506', 'Zara Hussain',       'Rider',  NULL, '2025-02-01 08:30:00'),
('R107', '+923001234507', 'Hamza Iqbal',        'Rider',  NULL, '2025-02-05 09:30:00'),
('R108', '+923001234508', 'Ayesha Raza',        'Rider',  NULL, '2025-02-08 10:30:00'),
('R109', '+923001234509', 'Imran Shahid',       'Rider',  NULL, '2025-02-10 11:30:00'),
('R110', '+923001234510', 'Nadia Perveen',      'Rider',  NULL, '2025-02-15 12:30:00'),
-- Drivers (D201-D208)
('D201', '+923011234501', 'Asif Mehmood',       'Driver', NULL, '2025-01-05 07:00:00'),
('D202', '+923011234502', 'Tariq Bashir',       'Driver', NULL, '2025-01-07 07:30:00'),
('D203', '+923011234503', 'Naveed Akhtar',      'Driver', NULL, '2025-01-09 08:00:00'),
('D204', '+923011234504', 'Rizwan Butt',        'Driver', NULL, '2025-01-11 08:30:00'),
('D205', '+923011234505', 'Shahid Aziz',        'Driver', NULL, '2025-01-13 09:00:00'),
('D206', '+923011234506', 'Pervaiz Ahmad',      'Driver', NULL, '2025-01-15 09:30:00'),
('D207', '+923011234507', 'Jameel Hassan',      'Driver', NULL, '2025-01-17 10:00:00'),
('D208', '+923011234508', 'Mushtaq Anwar',      'Driver', NULL, '2025-01-19 10:30:00'),
-- Admins (A301-A304)
('A301', '+923021234501', 'Dr. Saima Batool',   'Admin',  NULL, '2024-12-01 06:00:00'),
('A302', '+923021234502', 'Prof. Kamran Saeed', 'Admin',  NULL, '2024-12-05 06:30:00'),
('A303', '+923021234503', 'Ms. Rabia Shafiq',   'Admin',  NULL, '2024-12-10 07:00:00'),
('A304', '+923021234504', 'Mr. Zubair Nawaz',   'Admin',  NULL, '2024-12-15 07:30:00');

-- ============================================================
-- 2. RIDER (Subtype)
-- ============================================================
INSERT INTO Rider (user_id, rating_average) VALUES
('R101', 4.80),
('R102', 4.90),
('R103', 4.70),
('R104', 4.60),
('R105', 5.00),
('R106', 4.50),
('R107', 4.75),
('R108', 4.85),
('R109', 4.65),
('R110', 4.95);

-- ============================================================
-- 3. DRIVER (Subtype)
-- ============================================================
INSERT INTO Driver (user_id, cnic_number, license_number, is_verified, is_online, current_location, rating_average) VALUES
('D201', '38301-1234501-1', 'LHR-2020-00101', TRUE,  TRUE,  POINT(32.5833, 71.5417), 4.80),
('D202', '38301-1234502-2', 'LHR-2020-00102', TRUE,  TRUE,  POINT(32.5900, 71.5500), 4.90),
('D203', '38301-1234503-3', 'LHR-2020-00103', TRUE,  FALSE, POINT(32.5750, 71.5350), 4.70),
('D204', '38301-1234504-4', 'LHR-2020-00104', TRUE,  TRUE,  POINT(32.5800, 71.5450), 4.60),
('D205', '38301-1234505-5', 'LHR-2020-00105', TRUE,  FALSE, POINT(32.5850, 71.5480), 4.75),
('D206', '38301-1234506-6', 'LHR-2020-00106', FALSE, FALSE, POINT(32.5780, 71.5400), 5.00),
('D207', '38301-1234507-7', 'LHR-2020-00107', TRUE,  TRUE,  POINT(32.5820, 71.5430), 4.85),
('D208', '38301-1234508-8', 'LHR-2020-00108', FALSE, FALSE, POINT(32.5760, 71.5380), 4.65);

-- ============================================================
-- 4. ADMIN (Subtype)
-- ============================================================
INSERT INTO Admin (user_id, admin_level) VALUES
('A301', 'Senior'),
('A302', 'Senior'),
('A303', 'Junior'),
('A304', 'Junior');

-- ============================================================
-- 5. VEHICLE (1:1 with Driver)
-- ============================================================
INSERT INTO Vehicle (vehicle_id, driver_id, plate_number, vehicle_type, model) VALUES
('V401', 'D201', 'MWL-001',  'Sedan',    'Toyota Corolla 2019'),
('V402', 'D202', 'MWL-002',  'Mini',     'Suzuki Alto 2021'),
('V403', 'D203', 'MWL-003',  'Bike',     'Honda CD 70 2020'),
('V404', 'D204', 'MWL-004',  'Rickshaw', 'Ravi Rickshaw 2020'),
('V405', 'D205', 'MWL-005',  'Sedan',    'Honda Civic 2020'),
('V406', 'D206', 'MWL-006',  'Mini',     'Suzuki Wagon R 2022'),
('V407', 'D207', 'MWL-007',  'Bike',     'Yamaha YBR 2021'),
('V408', 'D208', 'MWL-008',  'Rickshaw', 'Ravi Rickshaw 2019');

-- ============================================================
-- 6. RIDE (20 rides)
-- ============================================================
INSERT INTO Ride (ride_id, driver_id, vehicle_id, status, is_shared, total_fare, created_at, completed_at) VALUES
('RD01', 'D201', 'V401', 'Completed',  FALSE, 150.00, '2025-03-01 08:00:00', '2025-03-01 08:25:00'),
('RD02', 'D202', 'V402', 'Completed',  FALSE, 100.00, '2025-03-01 09:00:00', '2025-03-01 09:20:00'),
('RD03', 'D203', 'V403', 'Completed',  FALSE,  80.00, '2025-03-02 08:30:00', '2025-03-02 08:50:00'),
('RD04', 'D204', 'V404', 'Completed',  TRUE,  200.00, '2025-03-02 10:00:00', '2025-03-02 10:35:00'),
('RD05', 'D205', 'V405', 'Completed',  FALSE, 180.00, '2025-03-03 07:30:00', '2025-03-03 08:00:00'),
('RD06', 'D207', 'V407', 'Completed',  FALSE,  70.00, '2025-03-03 09:00:00', '2025-03-03 09:15:00'),
('RD07', 'D201', 'V401', 'Completed',  TRUE,  240.00, '2025-03-04 08:00:00', '2025-03-04 08:40:00'),
('RD08', 'D202', 'V402', 'Completed',  FALSE, 120.00, '2025-03-04 10:00:00', '2025-03-04 10:22:00'),
('RD09', 'D204', 'V404', 'Completed',  FALSE,  90.00, '2025-03-05 08:00:00', '2025-03-05 08:18:00'),
('RD10', 'D207', 'V407', 'Completed',  TRUE,  160.00, '2025-03-05 09:30:00', '2025-03-05 10:00:00'),
('RD11', 'D201', 'V401', 'Completed',  FALSE, 130.00, '2025-03-06 07:00:00', '2025-03-06 07:25:00'),
('RD12', 'D202', 'V402', 'Cancelled',  FALSE, 110.00, '2025-03-06 09:00:00', NULL),
('RD13', 'D203', 'V403', 'Completed',  FALSE,  60.00, '2025-03-07 08:00:00', '2025-03-07 08:12:00'),
('RD14', 'D205', 'V405', 'Completed',  TRUE,  220.00, '2025-03-07 10:00:00', '2025-03-07 10:38:00'),
('RD15', 'D207', 'V407', 'Completed',  FALSE,  75.00, '2025-03-08 08:00:00', '2025-03-08 08:16:00'),
('RD16', 'D204', 'V404', 'Completed',  FALSE, 140.00, '2025-03-09 09:00:00', '2025-03-09 09:28:00'),
('RD17', 'D201', 'V401', 'Accepted',   FALSE, 160.00, '2025-03-10 08:00:00', NULL),
('RD18', 'D202', 'V402', 'Requested',  FALSE,  95.00, '2025-03-10 09:00:00', NULL),
('RD19', 'D207', 'V407', 'InProgress', FALSE,  85.00, '2025-03-10 10:00:00', NULL),
('RD20', 'D204', 'V404', 'InProgress', TRUE,  180.00, '2025-03-10 11:00:00', NULL);

-- ============================================================
-- 7. RIDE PARTICIPANT
-- ============================================================
INSERT INTO RideParticipant (participant_id, ride_id, rider_id, pickup_location, dropoff_location, segment_fare, is_primary_rider) VALUES
('P501', 'RD01', 'R101', POINT(32.5833,71.5417), POINT(32.5950,71.5550), 150.00, TRUE),
('P502', 'RD02', 'R102', POINT(32.5900,71.5500), POINT(32.6000,71.5600), 100.00, TRUE),
('P503', 'RD03', 'R103', POINT(32.5750,71.5350), POINT(32.5850,71.5450), 80.00,  TRUE),
('P504', 'RD04', 'R104', POINT(32.5800,71.5450), POINT(32.5900,71.5550), 100.00, TRUE),
('P505', 'RD04', 'R105', POINT(32.5810,71.5460), POINT(32.5920,71.5560), 100.00, FALSE),
('P506', 'RD05', 'R106', POINT(32.5850,71.5480), POINT(32.5960,71.5580), 180.00, TRUE),
('P507', 'RD06', 'R107', POINT(32.5820,71.5430), POINT(32.5880,71.5490), 70.00,  TRUE),
('P508', 'RD07', 'R108', POINT(32.5760,71.5380), POINT(32.5880,71.5500), 120.00, TRUE),
('P509', 'RD07', 'R109', POINT(32.5770,71.5390), POINT(32.5890,71.5510), 120.00, FALSE),
('P510', 'RD08', 'R110', POINT(32.5900,71.5500), POINT(32.6010,71.5610), 120.00, TRUE),
('P511', 'RD09', 'R101', POINT(32.5800,71.5450), POINT(32.5880,71.5530), 90.00,  TRUE),
('P512', 'RD10', 'R102', POINT(32.5820,71.5430), POINT(32.5920,71.5530), 80.00,  TRUE),
('P513', 'RD10', 'R103', POINT(32.5830,71.5440), POINT(32.5930,71.5540), 80.00,  FALSE),
('P514', 'RD11', 'R104', POINT(32.5833,71.5417), POINT(32.5933,71.5517), 130.00, TRUE),
('P515', 'RD13', 'R105', POINT(32.5750,71.5350), POINT(32.5810,71.5410), 60.00,  TRUE),
('P516', 'RD14', 'R106', POINT(32.5850,71.5480), POINT(32.5960,71.5590), 110.00, TRUE),
('P517', 'RD14', 'R107', POINT(32.5860,71.5490), POINT(32.5970,71.5600), 110.00, FALSE),
('P518', 'RD15', 'R108', POINT(32.5820,71.5430), POINT(32.5880,71.5490), 75.00,  TRUE),
('P519', 'RD19', 'R109', POINT(32.5833,71.5417), POINT(32.5933,71.5517), 85.00,  TRUE),
('P520', 'RD20', 'R110', POINT(32.5800,71.5450), POINT(32.5900,71.5550), 90.00,  TRUE),
('P521', 'RD20', 'R101', POINT(32.5810,71.5460), POINT(32.5910,71.5560), 90.00,  FALSE),
('P522', 'RD16', 'R102', POINT(32.5800,71.5450), POINT(32.5910,71.5560), 140.00, TRUE);

-- ============================================================
-- 8. PAYMENT
-- ============================================================
INSERT INTO Payment (payment_id, participant_id, amount, is_received, paid_at) VALUES
('PAY01', 'P501', 150.00, TRUE,  '2025-03-01 08:26:00'),
('PAY02', 'P502', 100.00, TRUE,  '2025-03-01 09:21:00'),
('PAY03', 'P503',  80.00, TRUE,  '2025-03-02 08:51:00'),
('PAY04', 'P504', 100.00, TRUE,  '2025-03-02 10:36:00'),
('PAY05', 'P505', 100.00, TRUE,  '2025-03-02 10:37:00'),
('PAY06', 'P506', 180.00, TRUE,  '2025-03-03 08:01:00'),
('PAY07', 'P507',  70.00, TRUE,  '2025-03-03 09:16:00'),
('PAY08', 'P508', 120.00, TRUE,  '2025-03-04 08:41:00'),
('PAY09', 'P509', 120.00, TRUE,  '2025-03-04 08:42:00'),
('PAY10', 'P510', 120.00, TRUE,  '2025-03-04 10:23:00'),
('PAY11', 'P511',  90.00, TRUE,  '2025-03-05 08:19:00'),
('PAY12', 'P512',  80.00, TRUE,  '2025-03-05 10:01:00'),
('PAY13', 'P513',  80.00, TRUE,  '2025-03-05 10:02:00'),
('PAY14', 'P514', 130.00, TRUE,  '2025-03-06 07:26:00'),
('PAY15', 'P515',  60.00, TRUE,  '2025-03-07 08:13:00'),
('PAY16', 'P516', 110.00, TRUE,  '2025-03-07 10:39:00'),
('PAY17', 'P517', 110.00, TRUE,  '2025-03-07 10:40:00'),
('PAY18', 'P518',  75.00, TRUE,  '2025-03-08 08:17:00'),
('PAY19', 'P519',  85.00, FALSE, NULL),
('PAY20', 'P520',  90.00, FALSE, NULL),
('PAY21', 'P521',  90.00, FALSE, NULL),
('PAY22', 'P522', 140.00, TRUE,  '2025-03-09 09:29:00');

-- ============================================================
-- 9. DRIVER VERIFICATION
-- ============================================================
INSERT INTO DriverVerification (verification_id, driver_id, admin_id, verification_status, comments, verified_at) VALUES
('DV01', 'D201', 'A301', 'Approved',  'All documents verified successfully.',         '2025-01-06 10:00:00'),
('DV02', 'D202', 'A301', 'Approved',  'License and CNIC verified.',                   '2025-01-08 10:00:00'),
('DV03', 'D203', 'A302', 'Approved',  'Documents complete and valid.',                '2025-01-10 10:00:00'),
('DV04', 'D204', 'A302', 'Approved',  'Verified by senior admin.',                    '2025-01-12 10:00:00'),
('DV05', 'D205', 'A301', 'Approved',  'All checks passed.',                           '2025-01-14 10:00:00'),
('DV06', 'D206', 'A303', 'Rejected',  'CNIC number mismatch with national database.',  '2025-01-16 10:00:00'),
('DV07', 'D207', 'A302', 'Approved',  'All documents in order.',                      '2025-01-18 10:00:00'),
('DV08', 'D208', 'A303', 'Pending',   NULL,                                           '2025-01-20 10:00:00'),
('DV09', 'D201', 'A301', 'Approved',  'Annual re-verification passed.',               '2025-06-01 10:00:00'),
('DV10', 'D202', 'A302', 'Approved',  'Re-verification successful.',                  '2025-06-02 10:00:00'),
('DV11', 'D203', 'A301', 'Approved',  'License renewed and verified.',                '2025-06-03 10:00:00'),
('DV12', 'D204', 'A302', 'Approved',  'Re-verification passed.',                      '2025-06-04 10:00:00'),
('DV13', 'D205', 'A301', 'Approved',  'Vehicle inspection passed.',                   '2025-06-05 10:00:00'),
('DV14', 'D206', 'A304', 'Pending',   NULL,                                           '2025-06-06 10:00:00'),
('DV15', 'D207', 'A302', 'Approved',  'Second year verification done.',               '2025-06-07 10:00:00'),
('DV16', 'D208', 'A304', 'Pending',   NULL,                                           '2025-06-08 10:00:00'),
('DV17', 'D201', 'A301', 'Approved',  'Spot check passed.',                           '2025-09-01 10:00:00'),
('DV18', 'D202', 'A302', 'Approved',  'Spot check passed.',                           '2025-09-02 10:00:00'),
('DV19', 'D203', 'A303', 'Approved',  'Updated license submitted.',                   '2025-09-03 10:00:00'),
('DV20', 'D204', 'A304', 'Approved',  'All documents renewed.',                       '2025-09-04 10:00:00');

-- ============================================================
-- 10. SOS ALERT
-- ============================================================
INSERT INTO SOSAlert (alert_id, ride_id, triggered_by, alert_status, location, triggered_at) VALUES
('SOS01', 'RD19', 'R109', 'Resolved',   POINT(32.5870,71.5470), '2025-03-10 10:05:00'),
('SOS02', 'RD20', 'R110', 'Active',     POINT(32.5860,71.5460), '2025-03-10 11:10:00');

-- ============================================================
-- 11. EMERGENCY CONTACT
-- ============================================================
INSERT INTO EmergencyContact (contact_id, user_id, contact_name, phone_number, relationship) VALUES
('EC01', 'R101', 'Khalid Ali',      '+923001111101', 'Father'),
('EC02', 'R101', 'Amna Ali',        '+923001111102', 'Mother'),
('EC03', 'R101', 'Saad Ali',        '+923001111103', 'Brother'),
('EC04', 'R102', 'Noor Ahmad',      '+923001111104', 'Father'),
('EC05', 'R102', 'Hina Noor',       '+923001111105', 'Sister'),
('EC06', 'R103', 'Tariq Usman',     '+923001111106', 'Father'),
('EC07', 'R103', 'Rukhsana Tariq',  '+923001111107', 'Mother'),
('EC08', 'R104', 'Malik Ashraf',    '+923001111108', 'Father'),
('EC09', 'R105', 'Zafar Khan',      '+923001111109', 'Father'),
('EC10', 'R105', 'Shabana Khan',    '+923001111110', 'Mother'),
('EC11', 'R106', 'Hussain Raza',    '+923001111111', 'Father'),
('EC12', 'R107', 'Iqbal Hamza',     '+923001111112', 'Father'),
('EC13', 'R107', 'Nasreen Iqbal',   '+923001111113', 'Mother'),
('EC14', 'R108', 'Raza Ahmad',      '+923001111114', 'Father'),
('EC15', 'R108', 'Ayesha Bibi',     '+923001111115', 'Mother'),
('EC16', 'R109', 'Shahid Imran',    '+923001111116', 'Brother'),
('EC17', 'R110', 'Perveen Bibi',    '+923001111117', 'Mother'),
('EC18', 'D201', 'Mehmood Asif',    '+923001111118', 'Father'),
('EC19', 'D201', 'Razia Mehmood',   '+923001111119', 'Mother'),
('EC20', 'D202', 'Bashir Ahmad',    '+923001111120', 'Father'),
('EC21', 'D203', 'Akhtar Naveed',   '+923001111121', 'Father'),
('EC22', 'D204', 'Butt Riaz',       '+923001111122', 'Father');

-- ============================================================
-- 12. RATING
-- ============================================================
INSERT INTO Rating (rating_id, ride_id, rater_user_id, rated_user_id, score, comment, created_at) VALUES
('RT01', 'RD01', 'R101', 'D201', 5, 'Very smooth ride, on time.',        '2025-03-01 08:30:00'),
('RT02', 'RD01', 'D201', 'R101', 5, 'Polite and punctual rider.',         '2025-03-01 08:32:00'),
('RT03', 'RD02', 'R102', 'D202', 4, 'Good driver, slight delay.',         '2025-03-01 09:25:00'),
('RT04', 'RD02', 'D202', 'R102', 5, 'Great passenger.',                   '2025-03-01 09:27:00'),
('RT05', 'RD03', 'R103', 'D203', 4, 'Decent ride.',                       '2025-03-02 08:55:00'),
('RT06', 'RD03', 'D203', 'R103', 4, 'Good.',                              '2025-03-02 08:57:00'),
('RT07', 'RD04', 'R104', 'D204', 5, 'Excellent shared ride experience.',  '2025-03-02 10:40:00'),
('RT08', 'RD04', 'D204', 'R104', 5, 'Very cooperative.',                  '2025-03-02 10:42:00'),
('RT09', 'RD05', 'R106', 'D205', 5, 'Very professional driver.',          '2025-03-03 08:05:00'),
('RT10', 'RD05', 'D205', 'R106', 4, 'Nice rider.',                        '2025-03-03 08:07:00'),
('RT11', 'RD06', 'R107', 'D207', 5, 'Quick and safe.',                    '2025-03-03 09:20:00'),
('RT12', 'RD06', 'D207', 'R107', 5, 'Very good.',                         '2025-03-03 09:22:00'),
('RT13', 'RD07', 'R108', 'D201', 4, 'Good shared ride.',                  '2025-03-04 08:45:00'),
('RT14', 'RD07', 'D201', 'R108', 5, 'Excellent rider.',                   '2025-03-04 08:47:00'),
('RT15', 'RD08', 'R110', 'D202', 5, 'On time and polite.',                '2025-03-04 10:27:00'),
('RT16', 'RD08', 'D202', 'R110', 5, 'Perfect passenger.',                 '2025-03-04 10:29:00'),
('RT17', 'RD09', 'R101', 'D204', 3, 'Average ride, took longer route.',   '2025-03-05 08:22:00'),
('RT18', 'RD09', 'D204', 'R101', 4, 'Good rider.',                        '2025-03-05 08:24:00'),
('RT19', 'RD11', 'R104', 'D201', 5, 'Excellent as always.',               '2025-03-06 07:30:00'),
('RT20', 'RD11', 'D201', 'R104', 5, 'Great rider, very friendly.',        '2025-03-06 07:32:00');

-- ============================================================
-- RE-ENABLE FK CHECKS
-- ============================================================
SET FOREIGN_KEY_CHECKS = 1;

-- ============================================================
-- VERIFICATION QUERIES
-- ============================================================
SELECT 'User' AS TableName, COUNT(*) AS TotalRows FROM User
UNION ALL
SELECT 'Rider', COUNT(*) FROM Rider
UNION ALL
SELECT 'Driver', COUNT(*) FROM Driver
UNION ALL
SELECT 'Admin', COUNT(*) FROM Admin
UNION ALL
SELECT 'Vehicle', COUNT(*) FROM Vehicle
UNION ALL
SELECT 'Ride', COUNT(*) FROM Ride
UNION ALL
SELECT 'RideParticipant', COUNT(*) FROM RideParticipant
UNION ALL
SELECT 'Payment', COUNT(*) FROM Payment
UNION ALL
SELECT 'DriverVerification', COUNT(*) FROM DriverVerification
UNION ALL
SELECT 'SOSAlert', COUNT(*) FROM SOSAlert
UNION ALL
SELECT 'EmergencyContact', COUNT(*) FROM EmergencyContact
UNION ALL
SELECT 'Rating', COUNT(*) FROM Rating;


SET FOREIGN_KEY_CHECKS = 1;
