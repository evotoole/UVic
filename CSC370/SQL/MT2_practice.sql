CREATE TABLE Product(
    maker varchar(20) PRIMARY KEY,
    model int,
    type varchar(20),
    CONSTRAINT uni UNIQUE(maker, model,type)
);

CREATE TABLE PC(
    model int REFERENCES Product,
    speed int,
    ram int,
    hd int,
    rd int,
    price int
);
CREATE TABLE Laptop(

);
CREATE TABLE Printer(

);

/*a*/
INSERT INTO Product VALUES('C',1100,'PC');
INSERT INTO PC VALUES(1100, 1800,64, 2, NULL, 2000);
/*b*/
INSERT INTO Product
SELECT maker, model+1000,type
FROM Product
    WHERE type ='PC';

INSERT INTO PC
SELECT model + 1000, speed, ram, hd, rd, price +500


DELETE FROM PC
    WHERE hd < 500;

DELETE FROM laptop WHERE laptop L JOIN maker



DROP TABLE Product;
DROP TABLE PC;
DROP TABLE Laptop;
DROP TABLE Printer;









CREATE VIEW new AS
SELECT * FROM
Members where city = 'victoria'
WITH CHECK OPTION;

CREATE VIEW mem AS
SELECT * FROM
Reviewed
WHERE (mid, bid) IN
      (SELECT mid, bid
       FROM Borrowed)                )
WITH CHECK OPTION;