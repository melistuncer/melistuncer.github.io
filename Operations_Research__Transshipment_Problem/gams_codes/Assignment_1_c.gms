Sets
i supply /1, 2, 3, 4/
j demand /1, 2, 3, 4, 5, Dummy/;

Parameters
a(i) i supply
                 /1 290
                  2 220
                  3 180
                  4 280/
b(j) j demand
                 /1 180
                  2 200
                  3 160
                  4 140
                  5 250
                  Dummy 40/;
Table c(i, j) transport cost of shipment
                 1       2       3       4       5       Dummy
         1       7.5     7       8       5.5     8       0
         2       6       6.5     7       7.5     8       0
         3       11      6       6.5     7       7       0
         4       9       7       10      6       7.5     0    ;

Positive Variables
x(i,j) flow between supply node i to demand node j;
Variables
z total cost
x(i,j);
Equations
cost objective function
supply(i)   supply constraint
demand(j)   demand constraint  ;

cost..  z =e= sum((i,j), c(i,j)*x(i,j)) ;
supply(i)..   sum(j, x(i,j)) =l= a(i) ;
demand(j)..   sum(i, x(i,j))  =g= b(j) ;

Model assignment1a /all/;
assignment1a.OPTFILE=1;
Solve assignment1a using lp minimizing z
Display x.l, x.M, z.l;
