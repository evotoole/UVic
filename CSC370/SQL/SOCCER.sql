/*Q1 (1 pt)
Find all the games in England between seasons 1920 and 1999 such that the total goals are at least 13.
Order by total goals descending.*/

SELECT *
FROM england
WHERE 1999 >= season AND 1920 <= season
ORDER BY totgoal DESC;

/*Sample result
"1935-12-26,1935,Tranmere Rovers,Oldham Athletic,13,4,3,17,9,H"
"1958-10-11,1958,Tottenham Hotspur,Everton,10,4,1,14,6,H"
...*/


/*Q2 (2 pt)
"For each total goal result, find how many games had that result."
Use the england table and consider only the seasons since 1980.
Order by total goal.*/


SELECT totgoal, COUNT(totgoal) AS num_games
FROM england
WHERE season >= 1980
GROUP BY totgoal
ORDER BY totgoal;

/*Sample result
"0,6085"
"1,14001"
...*/

/*Visualize the results using a barchart.*/


/*Q3 (2 pt)
Find for each team in England in tier 1 the total number of games played since 1980.
Report only teams with at least 300 games.

""Hint. Find the number of games each team has played as ""home""."
"Find the number of games each team has played as ""visitor""."
Then union the two and take the sum of the number of games.
*/


WITH R1 AS(
SELECT england.home AS team, COUNT(england.home) AS count
FROM england
WHERE tier = 1 AND season >= 1980
GROUP BY england.home
),

R2 AS(
SELECT england.visitor AS team, COUNT(england.visitor) AS count
FROM england
WHERE tier = 1 AND season >= 1980
GROUP BY england.visitor
),

U AS(
    SELECT R2.team, R2.count
    FROM R2
    UNION ALL
    SELECT R1.team, R1.count
    FROM R1
)

SELECT U.team, SUM(U.count) AS count
from U
GROUP BY U.team
HAVING SUM(U.count) >= 300
ORDER BY SUM(U.count) DESC;

/*Sample result
"Everton,1451"
"Liverpool,1451"
...*/


/*Q4 (1 pt)
"For each pair team1, team2 in England, in tier 1,"
find the number of home-wins since 1980 of team1 versus team2.
Order the results by the number of home-wins in descending order.

"Hint. After selecting the tuples needed (... WHERE tier=1 AND ...) do a GROUP BY home, visitor."
*/

SELECT E.home, E.visitor, COUNT(E.home) AS home_count
FROM england AS E
WHERE E.hgoal > E.vgoal AND E.season >= 1980 AND E.tier = 1
GROUP BY E.home, E.visitor
ORDER BY COUNT(E.home) DESC;


/*Sample result
"Manchester United,Tottenham Hotspur,27"
"Arsenal,Everton,26"
...*/


/*Q5 (1 pt)
"For each pair team1, team2 in England in tier 1"
find the number of away-wins since 1980 of team1 versus team2.
Order the results by the number of away-wins in descending order.*/



SELECT E.visitor AS team1, E.home AS team2, COUNT(E.home) as away_count
FROM england AS E
WHERE E.hgoal < E.vgoal AND E.season >= 1980 AND E.tier = 1
GROUP BY E.home, E.visitor
ORDER BY COUNT(E.home) DESC;



/*Sample result
"Manchester United,Aston Villa,18"
"Manchester United,Everton,17"
...*/


/*Q6 (2 pt)
"For each pair team1, team2 in England in tier 1 report the number of home-wins and away-wins"
since 1980 of team1 versus team2.
Order the results by the number of away-wins in descending order.

Hint. Join the results of the two previous queries. To do that you can use those
queries as subqueries. Remove their ORDER BY clause when making them subqueries.
Be careful on the join conditions.
*/


SELECT COALESCE(A.team1,B.team1), COALESCE(A.team2,B.team2), COALESCE(A.home_count,0) AS home_count, COALESCE(B.away_count,0.0) AS away_count
FROM (SELECT E.home AS team1, E.visitor AS team2, COUNT(E.home) AS home_count FROM england AS E
WHERE E.hgoal > E.vgoal AND E.season >= 1980 AND E.tier = 1 GROUP BY E.home, E.visitor)
AS A
FULL JOIN
(SELECT E.visitor AS team1, E.home AS team2, COUNT(E.home) as away_count
FROM england AS E WHERE E.hgoal < E.vgoal AND E.season >= 1980 AND E.tier = 1
GROUP BY E.visitor, E.home)
AS B
ON A.team1 = B.team1 AND A.team2 = B.team2
ORDER BY away_count DESC, home_count;


/*Sample result
"Manchester United,Aston Villa,26,18"
"Arsenal,Aston Villa,20,17"
...*/

/*
"--Create a view, called Wins, with the query for the previous question."
*/
CREATE VIEW WINS AS
SELECT COALESCE(A.team1,B.team1) AS home, COALESCE(A.team2,B.team2) AS away, COALESCE(A.home_count,0) AS home_count, COALESCE(B.away_count,0) AS away_count
FROM (SELECT E.home AS team1, E.visitor AS team2, COUNT(E.home) AS home_count FROM england AS E
WHERE E.hgoal > E.vgoal AND E.season >= 1980 AND E.tier = 1 GROUP BY E.home, E.visitor)
AS A
FULL JOIN
(SELECT E.visitor AS team1, E.home AS team2, COUNT(E.home) as away_count
FROM england AS E WHERE E.hgoal < E.vgoal AND E.season >= 1980 AND E.tier = 1
GROUP BY E.visitor, E.home)
AS B
ON A.team1 = B.team1 AND A.team2 = B.team2
ORDER BY away_count DESC;




/*Q7 (2 pt)
"For each pair ('Arsenal', team2), report the number of home-wins and away-wins"
of Arsenal versus team2 and the number of home-wins and away-wins of team2 versus Arsenal
(all since 1980).
Order the results by the second number of away-wins in descending order.
Use view W1.*/


SELECT W1.home as home, W1.away as away, W1.home_count AS home_count2 , W1.away_count AS away_count2, W2.home_count AS home_count1, W2.away_count AS away_count1
FROM WINS as W1 JOIN WINS as W2
ON W2.away = W1.home AND W2.home = W1.away AND W1.home = 'Arsenal'
ORDER BY W2.home_count DESC;


/*Sample result
"Arsenal,Liverpool,14,8,20,11"
"Arsenal,Manchester United,16,5,19,11"
...*/

/*Drop view Wins.*/
DROP VIEW Wins;

/*Build two bar-charts, one visualizing the two home-wins columns, and the other visualizing the two away-wins columns.*/


/*Q8 (2 pt)
Winning at home is easier than winning as visitor.
"Nevertheless, some teams have won more games as a visitor than when at home."
Find the team in Germany that has more away-wins than home-wins in total.
"Print the team name, number of home-wins, and number of away-wins.*/


WITH R1 AS (
SELECT G1.home, COUNT(G1.hgoal) AS home_wins
FROM germany G1
WHERE G1.hgoal > G1.vgoal
GROUP BY G1.home
),

R2 AS(
SELECT G2.visitor, COUNT(G2.vgoal) AS away_wins
FROM germany G2
WHERE G2.hgoal < G2.vgoal
GROUP BY G2.visitor
)

SELECT R1.home, R1.home_wins, R2.away_wins
FROM R2 JOIN R1 ON R1.home = R2.visitor
WHERE R2.away_wins > R1.home_wins;


/*Q9 (3 pt)
One of the beliefs many people have about Italian soccer teams is that they play much more defense than offense.
Catenaccio or The Chain is a tactical system in football with a strong emphasis on defence.
""In Italian, catenaccio means ""door-bolt"", which implies a highly organised and effective backline defence
focused on nullifying opponents' attacks and preventing goal-scoring opportunities.
In this question we would like to see whether the number of goals in Italy is on average smaller than in England.

Find the average total goals per season in England and Italy since the 1970 season.
"The results should be (season, england_avg, italy_avg) triples, ordered by season."

Hint.
Subquery 1: Find the average total goals per season in England.
Subquery 2: Find the average total goals per season in Italy
   (there is no totgoal in table Italy. Take hgoal+vgoal).
Join the two subqueries on season.
*/


SELECT E.season, E.england_avg, I.italy_avg
FROM (SELECT E.season, AVG(E.totgoal) AS england_avg
    FROM england AS E
    WHERE E.season >= 1970
    GROUP BY E.season) E
    JOIN
    (SELECT I.season, AVG(I.hgoal + I.vgoal) AS italy_avg
    FROM italy AS I
    WHERE I.season >= 1970
    GROUP BY I.season) I
    ON E.season = I.season
    ORDER BY E.season;


--Build a line chart visualizing the results. What do you observe?

/*Sample result
1970,2.5290927021696252,2.1041666666666667
1971,2.5922090729783037,2.0125
...*/


/*Q10 (3 pt)
Find the number of games in France and England in tier 1 for each goal difference.
"Return (goaldif, france_games, eng_games) triples, ordered by the goal difference."
"Normalize the number of games returned dividing by the total number of games for the country in tier 1,"
e.g. 1.0*COUNT(*)/(select count(*) from france where tier=1)  */


WITH R1 AS (SELECT E.hgoal - E.vgoal AS diff, 1.0*COUNT(*)/(select count(*) from england where tier=1) AS eng_count
FROM england AS E
WHERE E.tier = 1
GROUP BY diff
),

R2 AS (
SELECT F.hgoal - F.vgoal AS diff, 1.0*COUNT(*)/(select count(*) from france where tier=1) AS fra_count
FROM france AS F
WHERE F.tier = 1
GROUP BY diff
)

SELECT R1.diff::text as diff, SUM(fra_count) AS norm_fra_count, SUM(eng_count) AS norm_eng_count
FROM R1 JOIN R2 ON R1.diff = R2.diff
GROUP BY R1.diff;

/*Sample result
"-8,0.00011369234850494562,0.000062637018477920450987"
"-7,0.00011369234850494562,0.00010439503079653408"
...*/

/*Visualize the results using a barchart.*/


/*Q11 (2 pt)
Find all the seasons when England had higher average total goals than France.
Consider only tier 1 for both countries.
"Return (season,england_avg,france_avg) triples."
Order by season.*/

/*Your query here*/

SELECT E.season, E.avg, F.avg
FROM (SELECT E.season, AVG(E.totgoal) AS avg
      FROM england AS E
      WHERE E.tier = 1
      GROUP BY E.season
      ) E
    JOIN
    (SELECT F.season, AVG(F.totgoal) AS avg
     FROM france AS F
     WHERE F.tier = 1
     GROUP BY F.season
     ) F
ON F.season = E.season
WHERE E.avg > F.avg
ORDER BY E.season;

/*Sample result
"1936,3.3658008658008658,3.3041666666666667"
"1952,3.2640692640692641,3.1437908496732026"
...*/





