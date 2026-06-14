-- ============================================================
--  FareShare Ride-Sharing System
--  Database Schema (DDL)
--  File: dbDDL.sql
--  Authors: Muhammad Naveed, Munawar Ali, Areeba Tahir
--  Namal University, Mianwali – CSC-271 Database Systems
--  Milestone 3
-- ============================================================

DROP DATABASE IF EXISTS fareshare_db;
CREATE DATABASE fareshare_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE fareshare_db;

-- ============================================================
-- 1. USER (Supertype)
-- ============================================================
CREATE TABLE User (
    user_id        CHAR(36)     NOT NULL,
    phone_number   VARCHAR(13)  NOT NULL,
    full_name      VARCHAR(100) NOT NULL,
    user_role      ENUM('Rider','Driver','Admin') NOT NULL,
    profile_photo  VARCHAR(255) NULL,
    created_at     TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT pk_user       PRIMARY KEY (user_id),
    CONSTRAINT uq_user_phone UNIQUE      (phone_number)
);

-- ============================================================
-- 2. RIDER (Subtype of User)
-- ============================================================
CREATE TABLE Rider (
    user_id        CHAR(36)     NOT NULL,
    rating_average DECIMAL(3,2) NOT NULL DEFAULT 5.00,

    CONSTRAINT pk_rider      PRIMARY KEY (user_id),
    CONSTRAINT fk_rider_user FOREIGN KEY (user_id)
        REFERENCES User(user_id)
        ON DELETE CASCADE ON UPDATE CASCADE
);

-- ============================================================
-- 3. DRIVER (Subtype of User)
-- ============================================================
CREATE TABLE Driver (
    user_id          CHAR(36)     NOT NULL,
    cnic_number      VARCHAR(15)  NOT NULL,
    license_number   VARCHAR(20)  NOT NULL,
    is_verified      BOOLEAN      NOT NULL DEFAULT FALSE,
    is_online        BOOLEAN      NOT NULL DEFAULT FALSE,
    current_location POINT        NULL,
    rating_average   DECIMAL(3,2) NOT NULL DEFAULT 5.00,

    CONSTRAINT pk_driver         PRIMARY KEY (user_id),
    CONSTRAINT fk_driver_user    FOREIGN KEY (user_id)
        REFERENCES User(user_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT uq_driver_cnic    UNIQUE (cnic_number),
    CONSTRAINT uq_driver_license UNIQUE (license_number)
);

-- ============================================================
-- 4. ADMIN (Subtype of User)
-- ============================================================
CREATE TABLE Admin (
    user_id     CHAR(36)                NOT NULL,
    admin_level ENUM('Junior','Senior') NOT NULL,

    CONSTRAINT pk_admin      PRIMARY KEY (user_id),
    CONSTRAINT fk_admin_user FOREIGN KEY (user_id)
        REFERENCES User(user_id)
        ON DELETE CASCADE ON UPDATE CASCADE
);

-- ============================================================
-- 5. VEHICLE (1:1 with Driver)
-- ============================================================
CREATE TABLE Vehicle (
    vehicle_id   CHAR(36)                               NOT NULL,
    driver_id    CHAR(36)                               NOT NULL,
    plate_number VARCHAR(10)                            NOT NULL,
    vehicle_type ENUM('Bike','Rickshaw','Mini','Sedan') NOT NULL,
    model        VARCHAR(50)                            NULL,

    CONSTRAINT pk_vehicle        PRIMARY KEY (vehicle_id),
    CONSTRAINT fk_vehicle_driver FOREIGN KEY (driver_id)
        REFERENCES Driver(user_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT uq_vehicle_driver UNIQUE (driver_id),
    CONSTRAINT uq_vehicle_plate  UNIQUE (plate_number)
);

-- ============================================================
-- 6. RIDE
-- ============================================================
CREATE TABLE Ride (
    ride_id      CHAR(36)      NOT NULL,
    driver_id    CHAR(36)      NOT NULL,
    vehicle_id   CHAR(36)      NOT NULL,
    status       ENUM('Requested','Accepted','InProgress','Completed','Cancelled') NOT NULL,
    is_shared    BOOLEAN       NOT NULL DEFAULT FALSE,
    total_fare   DECIMAL(10,2) NOT NULL,
    created_at   TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP     NULL,

    CONSTRAINT pk_ride         PRIMARY KEY (ride_id),
    CONSTRAINT fk_ride_driver  FOREIGN KEY (driver_id)
        REFERENCES Driver(user_id)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_ride_vehicle FOREIGN KEY (vehicle_id)
        REFERENCES Vehicle(vehicle_id)
        ON DELETE RESTRICT ON UPDATE CASCADE
);

-- ============================================================
-- 7. RIDE PARTICIPANT (Associative Entity – resolves M:N Rider <-> Ride)
-- ============================================================
CREATE TABLE RideParticipant (
    participant_id   CHAR(36)      NOT NULL,
    ride_id          CHAR(36)      NOT NULL,
    rider_id         CHAR(36)      NOT NULL,
    pickup_location  POINT         NOT NULL,
    dropoff_location POINT         NOT NULL,
    segment_fare     DECIMAL(10,2) NOT NULL,
    is_primary_rider BOOLEAN       NOT NULL DEFAULT FALSE,

    CONSTRAINT pk_rideparticipant  PRIMARY KEY (participant_id),
    CONSTRAINT fk_rp_ride          FOREIGN KEY (ride_id)
        REFERENCES Ride(ride_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_rp_rider         FOREIGN KEY (rider_id)
        REFERENCES Rider(user_id)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT uq_rp_ride_rider    UNIQUE (ride_id, rider_id)
);

-- ============================================================
-- 8. PAYMENT (1:1 with RideParticipant)
-- ============================================================
CREATE TABLE Payment (
    payment_id     CHAR(36)      NOT NULL,
    participant_id CHAR(36)      NOT NULL,
    amount         DECIMAL(10,2) NOT NULL,
    is_received    BOOLEAN       NOT NULL DEFAULT FALSE,
    paid_at        TIMESTAMP     NULL,

    CONSTRAINT pk_payment             PRIMARY KEY (payment_id),
    CONSTRAINT fk_payment_rp          FOREIGN KEY (participant_id)
        REFERENCES RideParticipant(participant_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT uq_payment_participant UNIQUE (participant_id)
);

-- ============================================================
-- 9. DRIVER VERIFICATION
-- ============================================================
CREATE TABLE DriverVerification (
    verification_id     CHAR(36)                              NOT NULL,
    driver_id           CHAR(36)                              NOT NULL,
    admin_id            CHAR(36)                              NOT NULL,
    verification_status ENUM('Approved','Rejected','Pending') NOT NULL DEFAULT 'Pending',
    comments            TEXT                                  NULL,
    verified_at         TIMESTAMP                             NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT pk_driververification PRIMARY KEY (verification_id),
    CONSTRAINT fk_dv_driver          FOREIGN KEY (driver_id)
        REFERENCES Driver(user_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_dv_admin           FOREIGN KEY (admin_id)
        REFERENCES Admin(user_id)
        ON DELETE RESTRICT ON UPDATE CASCADE
);

-- ============================================================
-- 10. SOS ALERT
-- ============================================================
CREATE TABLE SOSAlert (
    alert_id     CHAR(36)                               NOT NULL,
    ride_id      CHAR(36)                               NOT NULL,
    triggered_by CHAR(36)                               NOT NULL,
    alert_status ENUM('Active','Responding','Resolved') NOT NULL DEFAULT 'Active',
    location     POINT                                  NOT NULL,
    triggered_at TIMESTAMP                              NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT pk_sosalert   PRIMARY KEY (alert_id),
    CONSTRAINT fk_sos_ride   FOREIGN KEY (ride_id)
        REFERENCES Ride(ride_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_sos_user   FOREIGN KEY (triggered_by)
        REFERENCES User(user_id)
        ON DELETE RESTRICT ON UPDATE CASCADE
);

-- ============================================================
-- 11. EMERGENCY CONTACT (Weak Entity – max 3 per user via trigger)
-- ============================================================
CREATE TABLE EmergencyContact (
    contact_id   CHAR(36)     NOT NULL,
    user_id      CHAR(36)     NOT NULL,
    contact_name VARCHAR(100) NOT NULL,
    phone_number VARCHAR(13)  NOT NULL,
    relationship VARCHAR(50)  NULL,

    CONSTRAINT pk_emergencycontact PRIMARY KEY (contact_id),
    CONSTRAINT fk_ec_user          FOREIGN KEY (user_id)
        REFERENCES User(user_id)
        ON DELETE CASCADE ON UPDATE CASCADE
);

-- ============================================================
-- 12. RATING (max 2 per ride via trigger; unique per rater per ride)
-- ============================================================
CREATE TABLE Rating (
    rating_id     CHAR(36)   NOT NULL,
    ride_id       CHAR(36)   NOT NULL,
    rater_user_id CHAR(36)   NOT NULL,
    rated_user_id CHAR(36)   NOT NULL,
    score         TINYINT(1) NOT NULL,
    comment       TEXT       NULL,
    created_at    TIMESTAMP  NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT pk_rating             PRIMARY KEY (rating_id),
    CONSTRAINT fk_rating_ride        FOREIGN KEY (ride_id)
        REFERENCES Ride(ride_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_rating_rater       FOREIGN KEY (rater_user_id)
        REFERENCES User(user_id)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_rating_rated       FOREIGN KEY (rated_user_id)
        REFERENCES User(user_id)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT chk_score             CHECK (score BETWEEN 1 AND 5),
    CONSTRAINT uq_rating_ride_rater  UNIQUE (ride_id, rater_user_id)
);

-- ============================================================
-- INDEXES
-- ============================================================
CREATE INDEX idx_ride_driver      ON Ride(driver_id);
CREATE INDEX idx_ride_status      ON Ride(status);
CREATE INDEX idx_rp_ride          ON RideParticipant(ride_id);
CREATE INDEX idx_rp_rider         ON RideParticipant(rider_id);
CREATE INDEX idx_payment_received ON Payment(is_received);
CREATE INDEX idx_dv_driver        ON DriverVerification(driver_id);
CREATE INDEX idx_sos_ride         ON SOSAlert(ride_id);
CREATE INDEX idx_rating_ride      ON Rating(ride_id);
CREATE INDEX idx_ec_user          ON EmergencyContact(user_id);

-- ============================================================
-- TRIGGERS
-- ============================================================

DELIMITER $$

-- T1: DI01 – Driver cannot go online without being verified
CREATE TRIGGER trg_driver_online_check
BEFORE UPDATE ON Driver
FOR EACH ROW
BEGIN
    IF NEW.is_online = TRUE AND NEW.is_verified = FALSE THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'DI01: Driver must be verified before going online.';
    END IF;
END$$

-- T2: DI07 – Max 3 emergency contacts per user
CREATE TRIGGER trg_max_emergency_contacts
BEFORE INSERT ON EmergencyContact
FOR EACH ROW
BEGIN
    DECLARE contact_count INT;
    SELECT COUNT(*) INTO contact_count
    FROM EmergencyContact
    WHERE user_id = NEW.user_id;

    IF contact_count >= 3 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'DI07: A user cannot have more than 3 emergency contacts.';
    END IF;
END$$

-- T3: DI09 – Max 2 ratings per ride
CREATE TRIGGER trg_max_ratings_per_ride
BEFORE INSERT ON Rating
FOR EACH ROW
BEGIN
    DECLARE rating_count INT;
    SELECT COUNT(*) INTO rating_count
    FROM Rating
    WHERE ride_id = NEW.ride_id;

    IF rating_count >= 2 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'DI09: A ride cannot have more than 2 ratings.';
    END IF;
END$$

-- T4: DI03 – SOSAlert only for InProgress rides
CREATE TRIGGER trg_sos_inprogress_only
BEFORE INSERT ON SOSAlert
FOR EACH ROW
BEGIN
    DECLARE ride_status VARCHAR(20);
    SELECT status INTO ride_status
    FROM Ride WHERE ride_id = NEW.ride_id;

    IF ride_status != 'InProgress' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'DI03: SOS Alert can only be triggered for InProgress rides.';
    END IF;
END$$

-- T5: Auto-update Driver.is_verified when DriverVerification status changes
CREATE TRIGGER trg_auto_verify_driver
AFTER UPDATE ON DriverVerification
FOR EACH ROW
BEGIN
    IF NEW.verification_status = 'Approved' AND OLD.verification_status != 'Approved' THEN
        UPDATE Driver SET is_verified = TRUE WHERE user_id = NEW.driver_id;
    END IF;

    IF NEW.verification_status = 'Rejected' AND OLD.verification_status != 'Rejected' THEN
        UPDATE Driver SET is_verified = FALSE, is_online = FALSE WHERE user_id = NEW.driver_id;
    END IF;
END$$

-- T6: Auto-update rating_average after a new Rating is inserted
CREATE TRIGGER trg_update_rating_average
AFTER INSERT ON Rating
FOR EACH ROW
BEGIN
    DECLARE avg_score DECIMAL(3,2);

    IF EXISTS (SELECT 1 FROM Driver WHERE user_id = NEW.rated_user_id) THEN
        SELECT AVG(score) INTO avg_score FROM Rating WHERE rated_user_id = NEW.rated_user_id;
        UPDATE Driver SET rating_average = avg_score WHERE user_id = NEW.rated_user_id;
    END IF;

    IF EXISTS (SELECT 1 FROM Rider WHERE user_id = NEW.rated_user_id) THEN
        SELECT AVG(score) INTO avg_score FROM Rating WHERE rated_user_id = NEW.rated_user_id;
        UPDATE Rider SET rating_average = avg_score WHERE user_id = NEW.rated_user_id;
    END IF;
END$$

DELIMITER ;

-- ============================================================
-- VIEWS
-- ============================================================

-- V1: Full user profile with role details
CREATE VIEW vw_user_profiles AS
SELECT
    u.user_id,
    u.full_name,
    u.phone_number,
    u.user_role,
    u.created_at,
    CASE
        WHEN u.user_role = 'Driver' THEN d.rating_average
        WHEN u.user_role = 'Rider'  THEN r.rating_average
        ELSE NULL
    END AS rating_average,
    d.is_verified,
    d.is_online
FROM User u
LEFT JOIN Driver d ON u.user_id = d.user_id
LEFT JOIN Rider  r ON u.user_id = r.user_id;

-- V2: Currently active rides
CREATE VIEW vw_active_rides AS
SELECT
    ri.ride_id,
    u.full_name    AS driver_name,
    u.phone_number AS driver_phone,
    v.plate_number,
    v.vehicle_type,
    ri.is_shared,
    ri.total_fare,
    COUNT(rp.participant_id) AS passenger_count
FROM Ride ri
JOIN Driver           d  ON ri.driver_id  = d.user_id
JOIN User             u  ON d.user_id     = u.user_id
JOIN Vehicle          v  ON ri.vehicle_id = v.vehicle_id
LEFT JOIN RideParticipant rp ON ri.ride_id = rp.ride_id
WHERE ri.status = 'InProgress'
GROUP BY ri.ride_id, u.full_name, u.phone_number,
         v.plate_number, v.vehicle_type, ri.is_shared, ri.total_fare;

-- V3: Pending driver verifications for admin dashboard
CREATE VIEW vw_pending_verifications AS
SELECT
    dv.verification_id,
    u.full_name    AS driver_name,
    u.phone_number AS driver_phone,
    d.cnic_number,
    d.license_number,
    dv.verification_status,
    dv.verified_at
FROM DriverVerification dv
JOIN Driver d ON dv.driver_id = d.user_id
JOIN User   u ON d.user_id   = u.user_id
WHERE dv.verification_status = 'Pending';

-- V4: Fare breakdown per ride participant
CREATE VIEW vw_ride_fare_summary AS
SELECT
    r.ride_id,
    r.total_fare,
    r.is_shared,
    rp.participant_id,
    u.full_name  AS rider_name,
    rp.segment_fare,
    p.is_received AS payment_received,
    p.paid_at
FROM Ride r
JOIN RideParticipant rp ON r.ride_id      = rp.ride_id
JOIN Rider  rd          ON rp.rider_id    = rd.user_id
JOIN User   u           ON rd.user_id     = u.user_id
LEFT JOIN Payment p     ON rp.participant_id = p.participant_id;

-- ============================================================
-- STORED PROCEDURES
-- ============================================================

DELIMITER $$

-- SP1: Register a new Rider
CREATE PROCEDURE sp_register_rider(
    IN p_user_id       CHAR(36),
    IN p_phone         VARCHAR(13),
    IN p_full_name     VARCHAR(100),
    IN p_profile_photo VARCHAR(255)
)
BEGIN
    INSERT INTO User(user_id, phone_number, full_name, user_role, profile_photo)
    VALUES (p_user_id, p_phone, p_full_name, 'Rider', p_profile_photo);

    INSERT INTO Rider(user_id)
    VALUES (p_user_id);
END$$

-- SP2: Register a new Driver with Vehicle
CREATE PROCEDURE sp_register_driver(
    IN p_user_id      CHAR(36),
    IN p_phone        VARCHAR(13),
    IN p_full_name    VARCHAR(100),
    IN p_cnic         VARCHAR(15),
    IN p_license      VARCHAR(20),
    IN p_vehicle_id   CHAR(36),
    IN p_plate_number VARCHAR(10),
    IN p_vehicle_type ENUM('Bike','Rickshaw','Mini','Sedan'),
    IN p_model        VARCHAR(50)
)
BEGIN
    INSERT INTO User(user_id, phone_number, full_name, user_role)
    VALUES (p_user_id, p_phone, p_full_name, 'Driver');

    INSERT INTO Driver(user_id, cnic_number, license_number)
    VALUES (p_user_id, p_cnic, p_license);

    INSERT INTO Vehicle(vehicle_id, driver_id, plate_number, vehicle_type, model)
    VALUES (p_vehicle_id, p_user_id, p_plate_number, p_vehicle_type, p_model);
END$$

-- SP3: Book a ride (Ride + primary RideParticipant + Payment)
CREATE PROCEDURE sp_book_ride(
    IN p_ride_id        CHAR(36),
    IN p_driver_id      CHAR(36),
    IN p_vehicle_id     CHAR(36),
    IN p_is_shared      BOOLEAN,
    IN p_total_fare     DECIMAL(10,2),
    IN p_participant_id CHAR(36),
    IN p_rider_id       CHAR(36),
    IN p_pickup_lat     DOUBLE,
    IN p_pickup_lng     DOUBLE,
    IN p_dropoff_lat    DOUBLE,
    IN p_dropoff_lng    DOUBLE,
    IN p_payment_id     CHAR(36)
)
BEGIN
    INSERT INTO Ride(ride_id, driver_id, vehicle_id, status, is_shared, total_fare)
    VALUES (p_ride_id, p_driver_id, p_vehicle_id, 'Requested', p_is_shared, p_total_fare);

    INSERT INTO RideParticipant(participant_id, ride_id, rider_id,
                                pickup_location, dropoff_location,
                                segment_fare, is_primary_rider)
    VALUES (p_participant_id, p_ride_id, p_rider_id,
            POINT(p_pickup_lat,  p_pickup_lng),
            POINT(p_dropoff_lat, p_dropoff_lng),
            p_total_fare, TRUE);

    INSERT INTO Payment(payment_id, participant_id, amount)
    VALUES (p_payment_id, p_participant_id, p_total_fare);
END$$

-- SP4: Complete a ride and confirm cash payment
CREATE PROCEDURE sp_complete_ride(
    IN p_ride_id        CHAR(36),
    IN p_participant_id CHAR(36)
)
BEGIN
    UPDATE Ride
    SET status = 'Completed', completed_at = CURRENT_TIMESTAMP
    WHERE ride_id = p_ride_id;

    UPDATE Payment
    SET is_received = TRUE, paid_at = CURRENT_TIMESTAMP
    WHERE participant_id = p_participant_id;
END$$

-- SP5: Submit a rating
CREATE PROCEDURE sp_submit_rating(
    IN p_rating_id     CHAR(36),
    IN p_ride_id       CHAR(36),
    IN p_rater_user_id CHAR(36),
    IN p_rated_user_id CHAR(36),
    IN p_score         TINYINT(1),
    IN p_comment       TEXT
)
BEGIN
    INSERT INTO Rating(rating_id, ride_id, rater_user_id, rated_user_id, score, comment)
    VALUES (p_rating_id, p_ride_id, p_rater_user_id, p_rated_user_id, p_score, p_comment);
END$$

-- SP6: Trigger an SOS Alert
CREATE PROCEDURE sp_trigger_sos(
    IN p_alert_id     CHAR(36),
    IN p_ride_id      CHAR(36),
    IN p_triggered_by CHAR(36),
    IN p_lat          DOUBLE,
    IN p_lng          DOUBLE
)
BEGIN
    INSERT INTO SOSAlert(alert_id, ride_id, triggered_by, location)
    VALUES (p_alert_id, p_ride_id, p_triggered_by, POINT(p_lat, p_lng));
END$$

-- SP7: Admin verifies a driver
CREATE PROCEDURE sp_verify_driver(
    IN p_verification_id CHAR(36),
    IN p_driver_id       CHAR(36),
    IN p_admin_id        CHAR(36),
    IN p_status          ENUM('Approved','Rejected','Pending'),
    IN p_comments        TEXT
)
BEGIN
    INSERT INTO DriverVerification(verification_id, driver_id, admin_id,
                                   verification_status, comments)
    VALUES (p_verification_id, p_driver_id, p_admin_id, p_status, p_comments);
END$$

DELIMITER ;

-- ============================================================
-- End of dbDDL.sql
-- ============================================================
