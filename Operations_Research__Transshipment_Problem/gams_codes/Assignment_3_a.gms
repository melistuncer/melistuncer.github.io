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

Table c(i, j) transportation costs by ship
                 1       2       3       4       5       Dummy
         1       5.5     6       8       3.5     4       0
         2       3       4.5     4       6.5     6       0
         3       11      6       3       4       4.5     0
         4       5       4.5     7       3       7.5     0    ;

Table f(i,j) monthly rent costs of ship
                 1       2       3       4       5       Dummy
         1       350     350     0       350     350     0
         2       350     350     350     350     350     0
         3       0       0       350     350     350     0
         4       350     350     350     350     0       0    ;

Variables
z total cost
x(i,j)
y(i,j) if route from supply i to j is used or not;

Integer Variables x;
Binary Variables y;

Equations
cost objective function
supply(i)   supply constraint
demand(j)   demand constraint
yisusedornot(i,j)
correction(i,j);

cost..  z =e= sum((i,j), c(i,j)*x(i,j)) + sum((i,j), y(i,j)*f(i,j)) ;
supply(i)..   sum(j, x(i,j)) =l= a(i) ;
demand(j)..   sum(i, x(i,j))  =g= b(j) ;
yisusedornot(i,j).. x(i,j)=l=99999*y(i,j)  ;
correction(i,j).. y(i,j)=l=x(i,j)  ;

Model Untitled_3 /all/;
Untitled_3.OPTFILE=1;
Solve Untitled_3 using MIP minimizing z
Display x.l, y.l, x.M, z.l;
