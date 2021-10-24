**AB TESTING**

Here we use AB testing to analyze the impact of gate placement on player retention within the mobile game Cookie Cats (Tactile Entertainment).

As players progress through the game, they encounter gates that force them to wait some time before they can progress to the next level, or they can proceed immediately by making an in-app purchase.  

In this project, we analyze the rentention results of an A/B test where the first gate in Cookie Cats was moved from level 30 to level 40. 

**Results**
99.8% probability that 7-day retention is higher when the gate is at level 30 than when it is at level 40.
95 % probability that 1-day retention is higher when the gate is at level 30 than when it is at level 40.

**Conclusion** 
The current gate location results in higher player rentention. 
To optimize both 1 and 7-day rentention, we should not move the gate from level 30 to level 40.

Dataset source: **Data Camp**

Libraries & packages used: Pandas, Pyplot 

The data provides insight from 90,189 players who installed the game while the AB-test was running. 
When a player installed the game, they were randomly assigned to either gate30 or gate40.

Dataset variables:
**userid**: Unique player identification number 
**version**: Idenfifies if the user reached the gate at level 30 or level 40
**sum_gamerounds**: Amount of game roundes played within first 14 days after the game installation. 
**retention_1**: User returned to play 1 day after installing 
**retention_7**: User returned to play 7 days after installing 
