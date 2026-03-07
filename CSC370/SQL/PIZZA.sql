DROP TABLE IF EXISTS Person;
DROP TABLE IF EXISTS Frequents;
DROP TABLE IF EXISTS Eats;
DROP TABLE IF EXISTS Serves;

create table Person(name VARCHAR(30), age int, gender VARCHAR(10));
create table Frequents(name VARCHAR(30), pizzeria VARCHAR(30));
create table Eats(name VARCHAR(30), pizza VARCHAR(30));
create table Serves(pizzeria VARCHAR(30), pizza VARCHAR(30), price float);

insert into Person values('Amy', 16, 'female');
insert into Person values('Ben', 21, 'male');
insert into Person values('Cal', 33, 'male');
insert into Person values('Dan', 13, 'male');
insert into Person values('Eli', 45, 'male');
insert into Person values('Fay', 21, 'female');
insert into Person values('Gus', 24, 'male');
insert into Person values('Hil', 30, 'female');
insert into Person values('Ian', 18, 'male');

insert into Frequents values('Amy', 'Pizza Hut');
insert into Frequents values('Ben', 'Pizza Hut');
insert into Frequents values('Ben', 'Chicago Pizza');
insert into Frequents values('Cal', 'Straw Hat');
insert into Frequents values('Cal', 'New York Pizza');
insert into Frequents values('Dan', 'Straw Hat');
insert into Frequents values('Dan', 'New York Pizza');
insert into Frequents values('Eli', 'Straw Hat');
insert into Frequents values('Eli', 'Chicago Pizza');
insert into Frequents values('Fay', 'Dominos');
insert into Frequents values('Fay', 'Little Caesars');
insert into Frequents values('Gus', 'Chicago Pizza');
insert into Frequents values('Gus', 'Pizza Hut');
insert into Frequents values('Hil', 'Dominos');
insert into Frequents values('Hil', 'Straw Hat');
insert into Frequents values('Hil', 'Pizza Hut');
insert into Frequents values('Ian', 'New York Pizza');
insert into Frequents values('Ian', 'Straw Hat');
insert into Frequents values('Ian', 'Dominos');

insert into Eats values('Amy', 'pepperoni');
insert into Eats values('Amy', 'mushroom');
insert into Eats values('Ben', 'pepperoni');
insert into Eats values('Ben', 'cheese');
insert into Eats values('Cal', 'supreme');
insert into Eats values('Dan', 'pepperoni');
insert into Eats values('Dan', 'cheese');
insert into Eats values('Dan', 'sausage');
insert into Eats values('Dan', 'supreme');
insert into Eats values('Dan', 'mushroom');
insert into Eats values('Eli', 'supreme');
insert into Eats values('Eli', 'cheese');
insert into Eats values('Fay', 'mushroom');
insert into Eats values('Gus', 'mushroom');
insert into Eats values('Gus', 'supreme');
insert into Eats values('Gus', 'cheese');
insert into Eats values('Hil', 'supreme');
insert into Eats values('Hil', 'cheese');
insert into Eats values('Ian', 'supreme');
insert into Eats values('Ian', 'pepperoni');

insert into Serves values('Pizza Hut', 'pepperoni', 12);
insert into Serves values('Pizza Hut', 'sausage', 12);
insert into Serves values('Pizza Hut', 'cheese', 9);
insert into Serves values('Pizza Hut', 'supreme', 12);
insert into Serves values('Little Caesars', 'pepperoni', 9.75);
insert into Serves values('Little Caesars', 'sausage', 9.5);
insert into Serves values('Little Caesars', 'cheese', 7);
insert into Serves values('Little Caesars', 'mushroom', 9.25);
insert into Serves values('Dominos', 'cheese', 9.75);
insert into Serves values('Dominos', 'mushroom', 11);
insert into Serves values('Straw Hat', 'pepperoni', 8);
insert into Serves values('Straw Hat', 'cheese', 9.25);
insert into Serves values('Straw Hat', 'sausage', 9.75);
insert into Serves values('New York Pizza', 'pepperoni', 8);
insert into Serves values('New York Pizza', 'cheese', 7);
insert into Serves values('New York Pizza', 'supreme', 8.5);
insert into Serves values('Chicago Pizza', 'cheese', 7.75);
insert into Serves values('Chicago Pizza', 'supreme', 8.5);



/*Q1 (1 pt)
Find all persons under the age of 18.*/

SELECT *
FROM Person
WHERE Person.age < 18;

/*Q2 (2 pts)
Find all pizzerias that serve at least one pizza Amy eats for less than $10.
"Output: pizzeria name, pizza name, price.*/

WITH R AS (
    SELECT *
    FROM Frequents JOIN Serves
    USING (pizzeria)
)


SELECT DISTINCT R.pizzeria, R.pizza, R.price
FROM R JOIN Eats ON Eats.name = R.name
WHERE R.price < 10 AND Eats.name = 'Amy';


/*Q3 (2 pts)
Find all pizzerias frequented by at least one person under the age of 18.
"Output: pizzeria name, person's name, person's age.*/

SELECT F.pizzeria, F.name, P.age
FROM Frequents F JOIN Person P on F.name = P.name
WHERE P.age < 18;


/*Q4 (2 pts)
Find all pizzerias frequented by at least one person under 18 and at least one person over 30.
Output: pizzeria name.*/


SELECT F.pizzeria
FROM Frequents F JOIN Person P on F.name = P.name
WHERE P.age > 30 OR P.age < 18
GROUP BY F.pizzeria
HAVING COUNT(P.age) >= 2;


/*Q5 (2 pts)
Find all pizzerias frequented by at least one person under 18 and at least one person over 30.
"Output: all quintuples (pizzeria, person1, age1, person2, age2), "
where person1 is under 18 and person2 is over 30.*/


SELECT F.pizzeria, P.name, P.age, P2.name, P2.age
FROM Frequents F JOIN Person P
ON F.name = P.name AND P.age < 18
JOIN Frequents F2 ON F.pizzeria = F2.pizzeria
JOIN Person P2 ON F2.name = P2.name AND P2.age > 30;



/*Q6 (2 pts)
"For each person, find how many types of pizzas they eat. "
Show only those who eat at least two types of pizza.
Sort results in descending order by number of pizza types.*/


SELECT Eats.name, COUNT(Distinct Eats.pizza) AS pizza_num
FROM Eats
GROUP BY Eats.name
HAVING COUNT(Distinct Eats.pizza) >= 2
ORDER BY COUNT(Distinct Eats.pizza) DESC;



/*Q7 (2 pts)
"For each type of pizza, find its average price. "
Sort results in descending order by average price.*/


SELECT S.pizza, AVG(S.price) AS avg_price
FROM Serves S
GROUP BY S.pizza
ORDER BY AVG(S.price) DESC;
