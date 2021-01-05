clear;
%%domain
%space
Lx = 100; %length of x interval
dx = 0.1; %x step 
nx = fix(Lx/dx); %number of total sample points in the interval 
x = linspace(0, Lx, nx); %the x vector containing all the sample points

%time
T = 0.3;
%variables
un = zeros(nx, 1); %vector that holds the values of the function at different locations for a specific time t
unm1 = un; %vector that holds the values of the function at different locations for time t-dt
unp1 = un; %vector that holds the values of the function at time t+dt
CFL = 1;   %CFL=c*(dt/dx)
c = 340;   %wave veloctiy (340 m/s for sound waves in air)
dt = CFL * dx / c; %calculating the time step 
%initial conditions;
%first initial condition(u(x,0)=f(x)=sin(2*pi*(1/50)*x))
%-----------------------------------
for i=1:1000
    un(i)=sin(2*pi*(1/50)*x(i));
end
%-----------------------------------
%second intial condition(ut(x,0)=0)
%-----------------------------------
unp1(:) = un(:);
%-----------------------------------
%timestopping loop
t = 0;
while (t < T)
    
    %absorbing boundary conditions to simulate the open boundaries
    %-------------------------------------------------------------
    unp1(1) = un(2) + ((CFL - 1) / (CFL + 1)) * (unp1(2) - un(1));
    unp1(end) = un(end - 1) + ((CFL - 1) / (CFL + 1)) * (unp1(end - 1) - unp1(end));
    %-------------------------------------------------------------
    t = t + dt;
    unm1 = un;
    un = unp1;
    for i = 2 : nx - 1
        unp1(i) = 2*un(i) - unm1(i) ...
                    + CFL^2 * (un(i+1) - 2*un(i) + un(i - 1));
    end
    clf;
    plot(x, un);
    title(sprintf('t = %0.2f',t));
    axis([0 Lx -1 1]);
    shg;
end