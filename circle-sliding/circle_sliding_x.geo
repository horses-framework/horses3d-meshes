// O-grid structured mesh with octagonal core and two concentric circles inside a square, rotation axis along x
// Run: gmsh circle_sliding_x.geo -format msh4 -3

SetFactory("OpenCASCADE");

lc = 0.1;
inner_radius = 0.8;
middle_radius = 1.8;
second_radius = 2.5;
quad_corner = 3;
NPointsRadial = 20;
RadialProgression = 0.9;
NPointsCircle = 11;

// Center point
Point(1) = {0, 0, 0, lc};

// Inner octagon points
Point(2) = {0, inner_radius, 0, lc};
Point(3) = {0, inner_radius*Cos(Pi/4), inner_radius*Sin(Pi/4), lc};
Point(4) = {0, 0, inner_radius, lc};
Point(5) = {0, -inner_radius*Cos(Pi/4), inner_radius*Sin(Pi/4), lc};
Point(6) = {0, -inner_radius, 0, lc};
Point(7) = {0, -inner_radius*Cos(Pi/4), -inner_radius*Sin(Pi/4), lc};
Point(8) = {0, 0, -inner_radius, lc};
Point(9) = {0, inner_radius*Cos(Pi/4), -inner_radius*Sin(Pi/4), lc};

// First circle points
Point(10) = {0, middle_radius, 0, lc};
Point(11) = {0, middle_radius*Cos(Pi/4), middle_radius*Sin(Pi/4), lc};
Point(12) = {0, 0, middle_radius, lc};
Point(13) = {0, -middle_radius*Cos(Pi/4), middle_radius*Sin(Pi/4), lc};
Point(14) = {0, -middle_radius, 0, lc};
Point(15) = {0, -middle_radius*Cos(Pi/4), -middle_radius*Sin(Pi/4), lc};
Point(16) = {0, 0, -middle_radius, lc};
Point(17) = {0, middle_radius*Cos(Pi/4), -middle_radius*Sin(Pi/4), lc};

// Second circle points
Point(18) = {0, second_radius, 0, lc};
Point(19) = {0, second_radius*Cos(Pi/4), second_radius*Sin(Pi/4), lc};
Point(20) = {0, 0, second_radius, lc};
Point(21) = {0, -second_radius*Cos(Pi/4), second_radius*Sin(Pi/4), lc};
Point(22) = {0, -second_radius, 0, lc};
Point(23) = {0, -second_radius*Cos(Pi/4), -second_radius*Sin(Pi/4), lc};
Point(24) = {0, 0, -second_radius, lc};
Point(25) = {0, second_radius*Cos(Pi/4), -second_radius*Sin(Pi/4), lc};

// Quadrangle points
Point(26) = {0, quad_corner, quad_corner, lc}; //Top right
Point(27) = {0, quad_corner, 0, lc}; //Middle right
Point(28) = {0, quad_corner, -quad_corner, lc}; //Bot right
Point(29) = {0, 0, quad_corner, lc}; //Top center
Point(30) = {0, 0, -quad_corner, lc}; //Bot center
Point(31) = {0, -quad_corner, quad_corner, lc}; //Top left
Point(32) = {0, -quad_corner, 0, lc}; //Middle left
Point(33) = {0, -quad_corner, -quad_corner, lc}; //Bot left


// Inner octagon lines
Line(1) = {2, 3};
Line(2) = {3, 4};
Line(3) = {4, 5};
Line(4) = {5, 6};
Line(5) = {6, 7};
Line(6) = {7, 8};
Line(7) = {8, 9};
Line(8) = {9, 2};

// Lines from center to octagon vertices
Line(9) = {1, 2};
Line(10) = {1, 4};
Line(11) = {1, 6};
Line(12) = {1, 8};

// Radial lines octagon to first circle
Line(13) = {2, 10};
Line(14) = {3, 11};
Line(15) = {4, 12};
Line(16) = {5, 13};
Line(17) = {6, 14};
Line(18) = {7, 15};
Line(19) = {8, 16};
Line(20) = {9, 17};

// Radial lines first to second circle
Line(21) = {10, 18};
Line(22) = {11, 19};
Line(23) = {12, 20};
Line(24) = {13, 21};
Line(25) = {14, 22};
Line(26) = {15, 23};
Line(27) = {16, 24};
Line(28) = {17, 25};

// Lines quadrangle
Line(29) = {26, 27};
Line(30) = {27, 28};
Line(31) = {28, 30};
Line(32) = {30, 33};
Line(33) = {33, 32};
Line(34) = {32, 31};
Line(35) = {31, 29};
Line(36) = {29, 26};

// Lines from second circle to quad
Line(53) = {25, 28};
Line(54) = {24, 30};
Line(55) = {23, 33};
Line(56) = {22, 32};
Line(57) = {21, 31};
Line(58) = {20, 29};
Line(59) = {19, 26};
Line(60) = {18, 27};


// Circle arcs
Circle(37) = {10, 1, 11}; Circle(38) = {11, 1, 12}; Circle(39) = {12, 1, 13}; Circle(40) = {13, 1, 14};
Circle(41) = {14, 1, 15}; Circle(42) = {15, 1, 16}; Circle(43) = {16, 1, 17}; Circle(44) = {17, 1, 10};

Circle(45) = {18, 1, 19}; Circle(46) = {19, 1, 20}; Circle(47) = {20, 1, 21}; Circle(48) = {21, 1, 22};
Circle(49) = {22, 1, 23}; Circle(50) = {23, 1, 24}; Circle(51) = {24, 1, 25}; Circle(52) = {25, 1, 18};

// Inner core surfaces
Curve Loop(1) = {9, 1, 2, -10}; Plane Surface(1) = {1};
Curve Loop(2) = {10, 3, 4, -11}; Plane Surface(2) = {2};
Curve Loop(3) = {11, 5, 6, -12}; Plane Surface(3) = {3};
Curve Loop(4) = {12, 7, 8, -9}; Plane Surface(4) = {4};

// First layer surfaces
Curve Loop(5) = {1, 14, -37, -13}; Plane Surface(5) = {5};
Curve Loop(6) = {2, 15, -38, -14}; Plane Surface(6) = {6};
Curve Loop(7) = {3, 16, -39, -15}; Plane Surface(7) = {7};
Curve Loop(8) = {4, 17, -40, -16}; Plane Surface(8) = {8};
Curve Loop(9) = {5, 18, -41, -17}; Plane Surface(9) = {9};
Curve Loop(10) = {6, 19, -42, -18}; Plane Surface(10) = {10};
Curve Loop(11) = {7, 20, -43, -19}; Plane Surface(11) = {11};
Curve Loop(12) = {8, 13, -44, -20}; Plane Surface(12) = {12};

// Second layer surfaces
Curve Loop(13) = {37, 22, -45, -21}; Plane Surface(13) = {13};
Curve Loop(14) = {38, 23, -46, -22}; Plane Surface(14) = {14};
Curve Loop(15) = {39, 24, -47, -23}; Plane Surface(15) = {15};
Curve Loop(16) = {40, 25, -48, -24}; Plane Surface(16) = {16};
Curve Loop(17) = {41, 26, -49, -25}; Plane Surface(17) = {17};
Curve Loop(18) = {42, 27, -50, -26}; Plane Surface(18) = {18};
Curve Loop(19) = {43, 28, -51, -27}; Plane Surface(19) = {19};
Curve Loop(20) = {44, 21, -52, -28}; Plane Surface(20) = {20};

// Third layer surfaces: second circle to quad
Curve Loop(21) = {53, 31, -54, 51}; Plane Surface(21) = {21};
Curve Loop(22) = {60, 30, -53, 52}; Plane Surface(22) = {22};
Curve Loop(23) = {59, 29, -60, 45}; Plane Surface(23) = {23};
Curve Loop(24) = {58, 36, -59, 46}; Plane Surface(24) = {24};
Curve Loop(25) = {57, 35, -58, 47}; Plane Surface(25) = {25};
Curve Loop(26) = {56, 34, -57, 48}; Plane Surface(26) = {26};
Curve Loop(27) = {55, 33, -56, 49}; Plane Surface(27) = {27};
Curve Loop(28) = {54, 32, -55, 50}; Plane Surface(28) = {28};

// Structured meshing
Transfinite Curve {1,2,3,4,5,6,7,8} = NPointsCircle;
Transfinite Curve {9,10,11,12} = NPointsCircle;
Transfinite Curve {13,14,15,16,17,18,19,20} = NPointsRadial Using Progression RadialProgression;
Transfinite Curve {21,22,23,24,25,26,27,28} = NPointsRadial Using Progression RadialProgression;
Transfinite Curve {29,30,31,32,33,34,35,36} = NPointsCircle;
Transfinite Curve {37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60} = NPointsCircle;

Extrude {1,0,0} {
  Surface{1:28}; Layers{ 1 }; Recombine;
}

Transfinite Surface "*";
Recombine Surface "*";

// Physical groups (this is a pure manual process but can be easen with the attached python script)
Physical Surface("front") = {1:28};
Physical Surface("back") = {33, 37, 41, 44, 48, 51, 54, 57, 60, 63, 66, 68, 72, 75, 78, 81, 84, 87, 90, 92, 96, 99, 102, 105, 108, 111, 114, 116};
Physical Surface("left") = {110, 113};
Physical Surface("right") = {98, 101};
Physical Surface("top") = {104, 107};
Physical Surface("bottom") = {94, 115};

Physical Volume("fluid") = {1:28};
