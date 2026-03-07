
var canvas;
var gl;

var program;

var near = 1;
var far = 100;


var left = -6.0;
var right = 6.0;
var ytop =6.0;
var bottom = -6.0;


var lightPosition2 = vec4(100.0, 100.0, 100.0, 1.0 );
var lightPosition = vec4(0.0, 0.0, 100.0, 1.0 );

var lightAmbient = vec4(0.2, 0.2, 0.2, 1.0 );
var lightDiffuse = vec4( 1.0, 1.0, 1.0, 1.0 );
var lightSpecular = vec4( 1.0, 1.0, 1.0, 1.0 );

var materialAmbient = vec4( 1.0, 0.0, 1.0, 1.0 );
var materialDiffuse = vec4( 1.0, 0.8, 0.0, 1.0 );
var materialSpecular = vec4( 0.4, 0.4, 0.4, 1.0 );
var materialShininess = 30.0;

var ambientColor, diffuseColor, specularColor;

var modelMatrix, viewMatrix, modelViewMatrix, projectionMatrix, normalMatrix;
var modelViewMatrixLoc, projectionMatrixLoc, normalMatrixLoc;
var eye;
var at = vec3(0.0, 0.0, 0.0);
var up = vec3(0.0, 1.0, 0.0);

var RX = 0;
var RY = 0;
var RZ = 0;

var MS = []; // The modeling matrix stack
var TIME = 0.0; // Realtime
var dt = 0.0
var prevTime = 0.0;
var resetTimerFlag = true;
var animFlag = true;
var controller;

// These are used to store the current state of objects.
// In animation it is often useful to think of an object as having some DOF
// Then the animation is simply evolving those DOF over time. You could very easily make a higher level object that stores these as Position, Rotation (and also Scale!)
var sphereRotation = [0,0,0];
var spherePosition = [-4,0,0];

var cubeRotation = [0,0,0];
var cubePosition = [-1,0,0];

var cylinderRotation = [0,0,0];
var cylinderPosition = [1.1,0,0];

var coneRotation = [0,0,0];
var conePosition = [3,0,0];

// Setting the colour which is needed during illumination of a surface


var stars = []; //initialize array of stars

for (let i = 0; i < 60; i++){ //initialize star objects.
    stars.push({
        x: -6 + Math.random() * 12,
        y: -6 + Math.random() * 12,
        z: -14,
        s: 0.01 + Math.random() * 0.05,
        update_x: 99,
        update_y: 99
    });
}


function setColor(c)
{
    ambientProduct = mult(lightAmbient, c);
    diffuseProduct = mult(lightDiffuse, c);
    specularProduct = mult(lightSpecular, materialSpecular);
    
    gl.uniform4fv( gl.getUniformLocation(program,
                                         "ambientProduct"),flatten(ambientProduct) );
    gl.uniform4fv( gl.getUniformLocation(program,
                                         "diffuseProduct"),flatten(diffuseProduct) );
    gl.uniform4fv( gl.getUniformLocation(program,
                                         "specularProduct"),flatten(specularProduct) );
    gl.uniform4fv( gl.getUniformLocation(program,
                                         "lightPosition"),flatten(lightPosition) );
    gl.uniform1f( gl.getUniformLocation(program, 
                                        "shininess"),materialShininess );
}


window.onload = function init() {


    canvas = document.getElementById( "gl-canvas" );
    
    gl = WebGLUtils.setupWebGL( canvas );
    if ( !gl ) { alert( "WebGL isn't available" ); }

    gl.viewport( 0, 0, canvas.width, canvas.height );
    gl.clearColor( 0, 0, 0, 1.0 );
    
    gl.enable(gl.DEPTH_TEST);

    //
    //  Load shaders and initialize attribute buffers
    //
    program = initShaders( gl, "vertex-shader", "fragment-shader" );
    gl.useProgram( program );


    setColor(materialDiffuse);
	
	// Initialize some shapes, note that the curved ones are procedural which allows you to parameterize how nice they look
	// Those number will correspond to how many sides are used to "estimate" a curved surface. More = smoother
    Cube.init(program);
    Cylinder.init(20,program);
    Cone.init(20,program);
    Sphere.init(36,program);

    // Matrix uniforms
    modelViewMatrixLoc = gl.getUniformLocation( program, "modelViewMatrix" );
    normalMatrixLoc = gl.getUniformLocation( program, "normalMatrix" );
    projectionMatrixLoc = gl.getUniformLocation( program, "projectionMatrix" );
    
    // Lighting Uniforms
    gl.uniform4fv( gl.getUniformLocation(program, 
       "ambientProduct"),flatten(ambientProduct) );
    gl.uniform4fv( gl.getUniformLocation(program, 
       "diffuseProduct"),flatten(diffuseProduct) );
    gl.uniform4fv( gl.getUniformLocation(program, 
       "specularProduct"),flatten(specularProduct) );	
    gl.uniform4fv( gl.getUniformLocation(program, 
       "lightPosition"),flatten(lightPosition) );
    gl.uniform1f( gl.getUniformLocation(program, 
       "shininess"),materialShininess );


    document.getElementById("animToggleButton").onclick = function() {
        if( animFlag ) {
            animFlag = false;
        }
        else {
            animFlag = true;
            resetTimerFlag = true;
            window.requestAnimFrame(render);
        }
        //console.log(animFlag);
    };

    render(0);
}

// Sets the modelview and normal matrix in the shaders
function setMV() {
    modelViewMatrix = mult(viewMatrix,modelMatrix);
    gl.uniformMatrix4fv(modelViewMatrixLoc, false, flatten(modelViewMatrix) );
    normalMatrix = inverseTranspose(modelViewMatrix);
    gl.uniformMatrix4fv(normalMatrixLoc, false, flatten(normalMatrix) );
}

// Sets the projection, modelview and normal matrix in the shaders
function setAllMatrices() {
    gl.uniformMatrix4fv(projectionMatrixLoc, false, flatten(projectionMatrix) );
    setMV();   
}

// Draws a 2x2x2 cube center at the origin
// Sets the modelview matrix and the normal matrix of the global program
// Sets the attributes and calls draw arrays
function drawCube() {
    setMV();
    Cube.draw();
}

// Draws a sphere centered at the origin of radius 1.0.
// Sets the modelview matrix and the normal matrix of the global program
// Sets the attributes and calls draw arrays
function drawSphere() {
    setMV();
    Sphere.draw();
}

// Draws a cylinder along z of height 1 centered at the origin
// and radius 0.5.
// Sets the modelview matrix and the normal matrix of the global program
// Sets the attributes and calls draw arrays
function drawCylinder() {
    setMV();
    Cylinder.draw();
}

// Draws a cone along z of height 1 centered at the origin
// and base radius 1.0.
// Sets the modelview matrix and the normal matrix of the global program
// Sets the attributes and calls draw arrays
function drawCone() {
    setMV();
    Cone.draw();
}

// Post multiples the modelview matrix with a translation matrix
// and replaces the modeling matrix with the result, x, y, and z are the translation amounts for each axis
function gTranslate(x,y,z) {
    modelMatrix = mult(modelMatrix,translate([x,y,z]));
}

// Post multiples the modelview matrix with a rotation matrix
// and replaces the modeling matrix with the result, theta is the rotation amount, x, y, z are the components of an axis vector (angle, axis rotations!)
function gRotate(theta,x,y,z) {
    modelMatrix = mult(modelMatrix,rotate(theta,[x,y,z]));
}

// Post multiples the modelview matrix with a scaling matrix
// and replaces the modeling matrix with the result, x, y, and z are the scale amounts for each axis
function gScale(sx,sy,sz) {
    modelMatrix = mult(modelMatrix,scale(sx,sy,sz));
}

// Pops MS and stores the result as the current modelMatrix
function gPop() {
    modelMatrix = MS.pop();
}

// pushes the current modelViewMatrix in the stack MS
function gPush() {
    MS.push(modelMatrix);
}

var J1_pos = [0,0,0];
var J2_pos = [-0.65,0,0];
var increment_time = 0;


//draws the space jelly, calling other functions

function drawJellyBody(){
    //Draw First jelly unit
    gPush();
        gTranslate(J1_pos[0], J1_pos[1], J1_pos[2]);
        gScale(0.5, 1, 1);
        setColor(vec4(1,0.0,0.5,1.0));
        drawSphere();
    gPop();

    //Second jelly unit
    gPush();
        gTranslate(J2_pos[0], J2_pos[1], J2_pos[2]);
        gScale(0.4, 0.75, 0.75);
        setColor(vec4(1,0.0,0.5,1.0));
        drawSphere();
    gPop();

}

function drawTentacles(){

    for (let j = 0; j < 3; j++) { //draw tentacles
        gPush();
            //attach tentacle to body
            gTranslate(-1, 0.75 - 0.75*j, 0);

            for (let i = 0; i < 5; i++) {
                let angle = 20 * Math.cos(100*increment_time - i); //phase offset creates wave
                //rotate at joint
                if (i != 0){
                gRotate(angle, 0,0,1);
                gTranslate(-0.6, 0, 0);  //move outward along rotated axis
                }
                gPush();
                    gScale(0.3, 0.1, 0.1);
                    setColor(vec4(0.8,0.6,0.2,1.0));
                    drawSphere();
                gPop();
            }
        gPop();
    }
}

function drawJelly(dt){
    
    gPush();
    
    gRotate(increment_time*1000, 0, 1, 0); //rotate jelly at world origin
    gTranslate(0,0,3.5); //translate rotated jelly out
    
    drawJellyBody();

    drawTentacles();

    gPop();
}

function drawTorso(){
    gPush(); // draw the torso
        gScale(0.5, 0.75, 0.75);
        setColor(vec4(1,1,1,1));
        drawCube();
    gPop();
}

function drawHead(){
    gPush(); //draw the head
        setColor(vec4(1,1,1,1));
        gScale(0.5, 0.5, 0.5);
        gTranslate(0,2.2,0);
        drawSphere();
    gPop();

    gPush(); //draw the visor
        setColor(vec4(0.8,0.6,0.2,1.0));
        gScale(0.5, 0.35, 0.33);
        gTranslate(0,3.3,1);
        drawSphere();
    gPop();
}

function drawOutlets(){
    gPush(); //draw badge
            setColor(vec4(0,0,1,0.2));
            gScale(0.3,0.3,0.2);
            gTranslate(-0.8,1.6,2.95);
            drawSphere();
        gPop();

        gPush(); //draw out blue 1
            setColor(vec4(0,0,1,0.1));
            gScale(0.1,0.12,0.3);
            gTranslate(-0.5,0.3,4);
            drawSphere();
        gPop();

        gPush(); //draw out blue 2
            setColor(vec4(0,0,1,0.1));
            gScale(0.1,0.12,0.3);
            gTranslate(2.4,0.3,4);
            drawSphere();
        gPop();

        gPush(); //draw purp 1
            setColor(vec4(0.95,0.9,1,1));
            gScale(0.1,0.12,0.3);
            gTranslate(-1.2,-2.4,4);
            drawSphere();
        gPop();


        gPush(); //draw purp 2
            setColor(vec4(0.95,0.9,1,1));
            gScale(0.1,0.12,0.3);
            gTranslate(3.1,-2.4,4);
            drawSphere();
        gPop();


        gPush(); //draw Red 1
            setColor(vec4(1,0,0,1));
            gScale(0.1,0.12,0.3);
            gTranslate(-0.9,-5.1,4);
            drawSphere();
        gPop();


        gPush(); //draw Red 2
            setColor(vec4(1,0,0,1));
            gScale(0.1,0.12,0.3);
            gTranslate(2.8,-5.1,4);
            drawSphere();
        gPop();
}

function drawArms(){ 
    gPush(); //draw arm 1
        setColor(vec4(1,1,1,1));
        gRotate(-40 + 8*Math.sin(increment_time*130), 0, 0, -1)
        gScale(0.15,0.7,0.33);
        gTranslate(4.8,-0.9,0);
        drawCube();
    gPop();
        
    gPush(); //draw arm 2
        setColor(vec4(1,1,1,1));
        gRotate(40 + 8*Math.sin(increment_time*170), 0, 0, -1)
        gScale(0.15,0.7,0.33);
        gTranslate(-4.7,-0.9,0);
        drawCube();
    gPop();
}

function drawLegs(){ 
    gPush(); //draw leg 1 upper
    gRotate(-13 - 14*Math.cos(increment_time*180), -1, 0, 0)
    setColor(vec4(1,1,1,1));
    gScale(0.15,0.5,0.4);
    gTranslate(2.3,-2.2,0.5);
    drawCube();
    gPop();

    gPush(); //draw leg 2 upper
        gRotate(-13 + 14*Math.cos(increment_time*180), -1, 0, 0)
        setColor(vec4(1,1,1,1));
        //gRotate(4, 0, 0, 1)
        gScale(0.15,0.5,0.4);
        gTranslate(-1.6,-2.2,0.5);
        drawCube();
    gPop();

    gPush();
    gRotate(-18 - 19*Math.cos(increment_time*180), -1, 0, 0)
    gPush(); //draw leg 1 lower
        setColor(vec4(1,1,1,1));
        gRotate(30, 1, 0, 0)
        gScale(0.15,0.45,0.2);
        gTranslate(2.3,-3.4,5.7);
        drawCube();
    gPop();

    gPush(); //draw foot 1 
        setColor(vec4(1,1,1,1));
        gRotate(30, 1, 0, 0)
        gScale(0.15,0.05,0.25);
        gTranslate(2.3,-40,5.3);
        drawCube();
    gPop();

    gPop();
    gRotate(-18 + 19*Math.cos(increment_time*180), -1, 0, 0)
    gPush(); //draw leg 2 lower
        setColor(vec4(1,1,1,1));
        gRotate(30, 1, 0, 0)
        gScale(0.15,0.45,0.2);
        gTranslate(-1.6,-3.4,5.7);
        drawCube();
    gPop();


    gPush(); //draw foot 2
        setColor(vec4(1,1,1,1));
        gRotate(30, 1, 0, 0)
        gScale(0.15,0.05,0.25);
        gTranslate(-1.6,-40,5.3);
        drawCube();
    gPop();
    }

function drawAstronaut(dt){
    gPush();

        gRotate(15, 0,-1,0);
        gTranslate(Math.sin(increment_time*60),Math.sin(increment_time*60), 0);

        drawTorso();
        
        drawHead();

        drawOutlets();

        drawArms();

        drawLegs();

    gPop();
}


function drawStars(dt){
    gPush();
    setColor(vec4(1,1,1,1));
    for (let star of stars){
        gPush();
        if (star.update_x == 99){
            star.update_x = star.x;
            star.update_y = star.y;

        }
        if (star.update_x > -6.1) {
            star.update_x -= 0.01
        }
        else{
            star.update_x = star.x + (6.1 - star.x)
        }
        if (star.update_y > -6.1){
            star.update_y -= 0.01
        }
        else{
            star.update_y = star.y + (6.1 - star.y)
        }
    
        gTranslate(star.update_x,star.update_y,star.z);
        gScale(star.s,star.s,star.s);
        drawSphere();
        gPop();
    }
    gPop();
}


function render(timestamp) {
    
    gl.clear( gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);
    
    eye = vec3(0,0,10);
    MS = []; // Initialize modeling matrix stack
	
	// initialize the modeling matrix to identity
    modelMatrix = mat4();
    
    // set the camera matrix
    viewMatrix = lookAt(eye, at , up);
   
    // set the projection matrix
    projectionMatrix = ortho(left, right, bottom, ytop, near, far);
    
    
    // set all the matrices
    setAllMatrices();
    
    
    
	if( animFlag )
    {
		// dt is the change in time or delta time from the last frame to this one
		// in animation typically we have some property or degree of freedom we want to evolve over time
		// For example imagine x is the position of a thing.
		// To get the new position of a thing we do something called integration
		// the simpelst form of this looks like:
		// x_new = x + v*dt
		// That is, the new position equals the current position + the rate of of change of that position (often a velocity or speed) times the change in time
		// We can do this with angles or positions, the whole x,y,z position, or just one dimension. It is up to us!
		dt = (timestamp - prevTime) / 1000.0;
		prevTime = timestamp;
	}
	
	// Sphere example
    
    drawJelly(dt);
    drawAstronaut(dt);
    drawStars(dt);

    /*
    gPush();
    setColor(vec4(1,1,1,1));
    gTranslate(-6,6,-14);
    gScale(1,1,1);
    drawSphere();
    gPop();
    */

    increment_time = increment_time + dt*0.007;
   
   /*
    
	// Cube example
	gPush();
		gTranslate(cubePosition[0],cubePosition[1],cubePosition[2]);
		gPush();
		{
			setColor(vec4(0.0,1.0,0.0,1.0));
			// Here is an example of integration to rotate the cube around the y axis at 30 degrees per second
			// new cube rotation around y = current cube rotation around y + 30deg/s*dt
			cubeRotation[1] = cubeRotation[1] + 30*dt;
			// This calls a simple helper function to apply the rotation (theta, x, y, z), 
			// where x,y,z define the axis of rotation. Here is is the y axis, (0,1,0).
			gRotate(cubeRotation[1],0,1,0);
			drawCube();
		}
		gPop();
	gPop();
    
	// Cylinder example
	gPush();
		gTranslate(cylinderPosition[0],cylinderPosition[1],cylinderPosition[2]);
		gPush();
		{
			setColor(vec4(0.0,0.0,1.0,1.0));
			cylinderRotation[1] = cylinderRotation[1] + 60*dt;
			gRotate(cylinderRotation[1],0,1,0);
			drawCylinder();
		}
		gPop();
	gPop();	
    
	// Cone example
	gPush();
		gTranslate(conePosition[0],conePosition[1],conePosition[2]);
		gPush();
		{
			setColor(vec4(1.0,1.0,0.0,1.0));
			coneRotation[1] = coneRotation[1] + 90*dt;
			gRotate(coneRotation[1],0,1,0);
			drawCone();
		}
		gPop();
	gPop();
    */
    if( animFlag )
        window.requestAnimFrame(render);
}