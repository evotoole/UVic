1) HIERARCHICAL OBJECT IMPLEMENTED: 
shoulder => upper arm => elbow => lower arm => javelin/spear

2) 360-DEGREE CAMERA FLY AROUND IMPLEMENTED USING lookAt() and setMV()
looped to continue circling and also zooms in and slows down on the first throw.

3) REAL-TIME WORKING
time was sped up slightly so that my scene would be shorter.

4) 2+ non trivial textures implemented
-non trivial 1: faces: put texture on only one side of the cube. This was done with both a happy face and a sad face for when the figure hits the board or misses the board. The face is happy until a miss occurs then it turns sad. then if the sad face hits the board it turns happy.

-non trivial 2: dart board: put texture only on one side of the board-shaped object. The javelin is thrown at the board.

-Other textures: Box from the lab was used as the texture for the javelin and part of the clothing the people wear. The assignment also uses green, blue, and white textures for colouring. also uses a grass texture for the ground.

5) ADS SHADER CONVERTED TO FRAGMENT.
-runs per fragment using blinn phong.

6) Converted PHONG to BLINN PHONG
-using H instead of reflection.

7) SHADER EFFECT IMPLEMENTED (in the html file)
-When the figure throws the first time if they hit the board everything slowly pulses green then it fades. It turns red when the figure misses the board.
Purpose: adds feedback to what is good and bad. it is of course common to see green as good and red as bad so I used this for feedback based on the figures throw.
Effect: The shader interpolates between either red or green and the standard fragment color. this allows a gradual addition/pulse of the green or red to mix in with the natural color instead of just overwritting everything green/red.