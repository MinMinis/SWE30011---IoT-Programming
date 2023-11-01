CREATE TABLE sensor_data (
    dataID INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
    humidity VARCHAR(1O) NOT NULL,
    temperature VARCHAR(1O) NOT NULL,
    time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
