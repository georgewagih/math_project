%generating the unit circle and the line segment
%-----------------------------------------------
uc=[];  %vector that contains the sample points of the unit circle
ls=[];  %vector that contains the sample points of the line segment
theta=0;
for k = 1:360
    uc(k)=cos(theta)+i*sin(theta);
    ls(k)=1+(k/360)*i;
    theta=theta+(pi/180);
end
%plotting the unit circle
%------------------------
figure(1); %figure containing the unit circle
figure(2); %figure containing the unit circle mappings
figure(3); %figure containing the line segment mappings
figure(1);
plot(real(uc),imag(uc));
axis equal;
%generating the image of the unit circle and the line under the complex mapping 
%f(z) = z^2 +(1+i)*z-3
%---------------------------------------------------------------------------
u1=uc;
u1=u1.^2+u1.*(1+i)-3;
l1=ls;
l1=l1.^2+l1.*(1+i)-3;
figure(2);
subplot(2,2,1);
plot(real(u1),imag(u1));
title('f(z) = z^2 +(1+i)*z-3');
axis equal;
figure(3);
subplot(2,2,1);
plot(real(l1),imag(l1));
title('f(z) = z^2 +(1+i)*z-3');
axis equal;
%generating the image of the unit circle and the line under the complex mapping 
%f(z)=i*z^3+z-i
%-----------------------------------------------------------------------------
u2=uc;
u2=(u2.^3).*i+u2-i;
l2=ls;
l2=(l2.^3).*i+l2-i;
figure(2);
subplot(2,2,2);
plot(real(u2),imag(u2));
title('f(z)=i*z^3+z-i');
axis equal;
figure(3);
subplot(2,2,2);
plot(real(l2),imag(l2));
title('f(z)=i*z^3+z-i');
axis equal;
%generating the image of the unit circle and the line under the complex mapping 
%f(z)=z^4-z
%------------------------------------------------------------------------------
u3=uc;
u3=u3.^4-u3;
l3=ls;
l3=l3.^4-l3;
figure(2);
subplot(2,2,3);
plot(real(u3),imag(u3));
title('f(z)=z^4-z');
axis equal;
figure(3);
subplot(2,2,3);
plot(real(l3),imag(l3));
title('f(z)=z^4-z');
axis equal;
%generating the image of the unit circle and the line under the complex mapping 
%f(z)=z^3-z'
%----------------------------------------------------------------------------
u4=uc;
u4=u4.^3-conj(u4);
l4=ls;
l4=l4.^3-conj(l4);
figure(2);
subplot(2,2,4);
plot(real(u4),imag(u4));
title("f(z)=z^3-z'");
axis equal;
figure(3);
subplot(2,2,4);
plot(real(l4),imag(l4));
title("f(z)=z^3-z'");
axis equal;