CREATE TABLE `school`.`student`(
    `ID` INT NOT NULL,
    `Passwd` VARCHAR(25) NOT NULL,
    `Name` VARCHAR(50) NOT NULL,
    `Class` INT NOT NULL,
    `DOB` DATE NOT NULL,
    `Phone` INT NOT NULL,
    `Email` VARCHAR(30) NOT NULL,
    PRIMARY KEY (`ID`));