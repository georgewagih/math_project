from big_ol_pile_of_manim_imports import *
import numpy as np
from test import *
import math

class generating_quadratic_bezier(Scene):
    def construct(self):
        t=ValueTracker(0)
        d=DecimalNumber(t.get_value(),num_decimal_places=2).to_corner(UP+RIGHT)
        text=TexMobject("t=").move_to(d.get_center()+1*LEFT)
        grid=ScreenGrid()

        """ defining the position of three initial control points and adding them to screen. Q0,Qp represent the linear
        interpolation between p0p1,p1p2. the parametric function here defines the curve drwan out by Q2 """
        def coords(m):
           return m[0,0]*RIGHT + m[1,0]*UP
        
        x0=np.array([[-5],[-1]])
        x1=np.array([[-5],[3]])
        x2=np.array([[-1],[-1]])
        p0=Dot(coords(x0))
        p1=Dot(coords(x1))
        p2=Dot(coords(x2))
        Q0=Dot(p0.get_center()).set_color(RED)
        Q1=Dot(p1.get_center()).set_color(RED)
        Q2=Dot(p0.get_center()).set_color(GREEN)
        self.add(p0,p1,p2,text,grid)

        def parametric(t):
            return (1-t)*(1-t)*(p0.get_center())+2*t*(1-t)*(p1.get_center())+t*t*(p2.get_center())

        curve=ParametricFunction(parametric,t_max=0).set_color(GREEN)


        """linearint is the linear interpolation function takes t, initial point, final point and gives 
        coords of a point between them """

        def linearint(t,pi,pf):
            return (1-t)*pi+t*pf

        """update functions of decimal,Q0,Q1,Q2,curve """

        def updatedecimal(m):
            m.set_value(t.get_value())

        def updateQ0(Q):
            Q.move_to(linearint(t.get_value(),p0.get_center(),p1.get_center()))
        
        def updateQ1(Q):
            Q.move_to(linearint(t.get_value(),p1.get_center(),p2.get_center()))

        def updateQ2(Q):
            Q.move_to(linearint(t.get_value(),Q0.get_center(),Q1.get_center()))

        def updatecurve(m):
            m.reset_t_max(t.get_value())

        def update_curve_while_moving_control(m):
            m.reset_parametric_function(parametric)


        """adding the update functions to the objects Q0,Q1,Q2,d,lineQ,curve """

        Q0.add_updater(updateQ0)
        Q1.add_updater(updateQ1)
        Q2.add_updater(updateQ2)
        d.add_updater(updatedecimal)
        curve.add_updater(updatecurve)
        curve.add_updater(update_curve_while_moving_control)
        

        self.add(d,Q0,Q1,Q2,curve)

        line1=Line(p0,p1)
        line2=Line(p1,p2)
        lineQ=Line(Q0,Q1).set_color(BLUE)

        """the update_curve_while_moving_control function attaches the bezier curve to its control points such that moving the control 
        will adjust the curve."""

        def updateline1(m):
            m.put_start_and_end_on(p0.get_center(),p1.get_center())

        def updateline2(m):
            m.put_start_and_end_on(p1.get_center(),p2.get_center())

        def updatelineQ(m):
            m.put_start_and_end_on(Q0.get_center(),Q1.get_center())

        """adding the update functions to the curve,lines1,2 then adding them to the screen """

        line1.add_updater(updateline1)
        line2.add_updater(updateline2)
        lineQ.add_updater(updatelineQ)
        self.add(line1,line2,lineQ)
        self.play(t.increment_value,1,run_time=4)

        """reflection about y-axis """
        reflectymatrix=np.array([[-1,0],
                                 [0,1]])
        x0r=reflectymatrix.dot(x0)
        x1r=reflectymatrix.dot(x1)
        x2r=reflectymatrix.dot(x2)
        reflection_text=TexMobject("Reflection").to_edge(UP)
        self.play(Write(reflection_text))

        """Translation_animation function:
        xi is the inital position of the point we want to translate as a numpy array
        p is the point we want to translate as a mobject,Dot.
        xf is the final position as a numpy array
        *************************************************************************** """
        def Translation_animation(xi,p,xf):
            t1=ValueTracker(1)
            t2=ValueTracker(1)
            def Translation_matrix(a,b):
                return np.array([[a,0],[0,b]])

            def updatepoint(m):
                m.move_to(coords(Translation_matrix(t1.get_value(),t2.get_value()).dot(xi)))

            p.add_updater(updatepoint)
            self.add(p)
            self.add(Q0,Q1,Q2,curve,line1,line2,lineQ)
            self.play(t1.increment_value,xf[0,0]/xi[0,0]-1,t2.increment_value,xf[1,0]/xi[1,0]-1,run_time=1)

        """***************************************************************************"""

        Translation_animation(x0,p0,x0r)
        Translation_animation(x1,p1,x1r)
        Translation_animation(x2,p2,x2r)

        """ Rotation in place"""
        rotation_text=TexMobject("Rotation").to_edge(UP)
        self.play(Transform(reflection_text,rotation_text))

        t3=ValueTracker(0)
        about_point=np.array([[3.5],[0.5]])
        self.add(Dot(coords(about_point)))

        def Rotation_matrix(theta):
            return np.array([[np.cos(theta),np.sin(-theta)],[np.sin(theta),np.cos(theta)]])

        def relative_position(position_vector,about_point):
            return np.subtract(position_vector,about_point)

        def updatep0(m):
            x=Rotation_matrix(t3.get_value()).dot(relative_position(x0r,about_point))
            m.move_to(coords(np.add(x,about_point)))

        def updatep1(m):
            x=Rotation_matrix(t3.get_value()).dot(relative_position(x1r,about_point))
            m.move_to(coords(np.add(x,about_point)))

        def updatep2(m):
            x=Rotation_matrix(t3.get_value()).dot(relative_position(x2r,about_point))
            m.move_to(coords(np.add(x,about_point)))

        p0.add_updater(updatep0)
        p1.add_updater(updatep1)
        p2.add_updater(updatep2)
        self.add(p0,p1,p2)
        self.add(Q0,Q1,Q2,curve,line1,line2,lineQ)
        self.play(t3.increment_value,2*PI,run_time=5)
        self.wait()


class generating_cubic_bezier(Scene):
    def construct(self):
        t=ValueTracker(0)
        grid=ScreenGrid()
        self.add(grid)
        d=DecimalNumber(t.get_value(),num_decimal_places=2).to_corner(UP+RIGHT)
        text=TexMobject("t=").move_to(d.get_center()+1*LEFT)
        def coords(m):
           return m[0,0]*RIGHT + m[1,0]*UP
        x0=np.array([[-4],[-2]])
        x1=np.array([[-4],[2]])
        x2=np.array([[4],[-2]])
        x3=np.array([[4],[2]])
        p0=Dot(coords(x0)).set_color(BLUE)
        p1=Dot(coords(x1)).set_color(BLUE)
        p2=Dot(coords(x2)).set_color(BLUE)
        p3=Dot(coords(x3)).set_color(BLUE)
        Q0=Dot(p0.get_center()).set_color(GREEN)
        Q1=Dot(p1.get_center()).set_color(GREEN)
        Q2=Dot(p2.get_center()).set_color(GREEN)
        Q3=Dot(p0.get_center())
        Q4=Dot(p1.get_center())
        Q5=Dot(p0.get_center()).set_color(RED)

        self.add(d,text,p0,p1,p2,p3)
        
        def linearint(t,pi,pf):
            return (1-t)*pi+t*pf

        def parametric(t):
            x=np.array([pow((1-t),3)*p0.get_center()+3*pow((1-t),2)*t*p1.get_center()+3*(1-t)*t*t*p2.get_center()+t*t*t*p3.get_center()])
            return x[0]

        curve=ParametricFunction(parametric,t_max=0).set_color(RED)

        def updatedecimal(m):
            m.set_value(t.get_value())

        def updatecurve(m):
            m.reset_t_max(t.get_value())

        def update_curve_while_moving_control(m):
            m.reset_parametric_function(parametric)
        
        def updateQ0(m):
            m.move_to(linearint(t.get_value(),p0.get_center(),p1.get_center()))

        def updateQ1(m):
            m.move_to(linearint(t.get_value(),p1.get_center(),p2.get_center()))

        def updateQ2(m):
            m.move_to(linearint(t.get_value(),p2.get_center(),p3.get_center()))

        def updateQ3(m):
            m.move_to(linearint(t.get_value(),Q0.get_center(),Q1.get_center()))

        def updateQ4(m):
            m.move_to(linearint(t.get_value(),Q1.get_center(),Q2.get_center()))

        def updateQ5(m):
            m.move_to(linearint(t.get_value(),Q3.get_center(),Q4.get_center()))


        d.add_updater(updatedecimal)
        curve.add_updater(updatecurve)
        curve.add_updater(update_curve_while_moving_control)
        Q0.add_updater(updateQ0)
        Q1.add_updater(updateQ1)
        Q2.add_updater(updateQ2)
        Q3.add_updater(updateQ3)
        Q4.add_updater(updateQ4)
        Q5.add_updater(updateQ5)
        self.add(Q0,Q1,Q2,Q3,Q4,Q5,d,curve)

        
        line1=Line(p0,p1)
        line2=Line(p1,p2)
        line3=Line(p2,p3)
        line4=Line(Q0,Q1).set_color(GREEN)
        line5=Line(Q1,Q2)
        line6=Line(Q3,Q4).set_color(RED)

        def updateline1(m):
            m.put_start_and_end_on(p0.get_center(),p1.get_center())

        def updateline2(m):
            m.put_start_and_end_on(p1.get_center(),p2.get_center())

        def updateline3(m):
            m.put_start_and_end_on(p2.get_center(),p3.get_center())
        
        def updateline4(m):
            m.put_start_and_end_on(Q0.get_center(),Q1.get_center())

        def updateline5(m):
            m.put_start_and_end_on(Q1.get_center(),Q2.get_center())

        def updateline6(m):
            m.put_start_and_end_on(Q3.get_center(),Q4.get_center())

        line1.add_updater(updateline1)
        line2.add_updater(updateline2)
        line3.add_updater(updateline3)    
        line4.add_updater(updateline4)
        line5.add_updater(updateline5)
        line6.add_updater(updateline6)
        self.add(line1,line2,line3,line4,line5,line6)
        self.play(t.increment_value,1,run_time=4)
        
        def Translation_animation(xi,p,xf):
            t1=ValueTracker(1)
            t2=ValueTracker(1)
            def Translation_matrix(a,b):
                return np.array([[a,0],[0,b]])

            def updatepoint(m):
                m.move_to(coords(Translation_matrix(t1.get_value(),t2.get_value()).dot(xi)))

            p.add_updater(updatepoint)
            self.add(p)
            self.add(Q0,Q1,Q2,Q3,Q4,Q5,d,curve,line1,line2,line3,line4,line5,line6)
            self.play(t1.increment_value,xf[0,0]/xi[0,0]-1,t2.increment_value,xf[1,0]/xi[1,0]-1)

        Translation_animation(x0,p0,np.array([[-4],[-1]]))
        Translation_animation(x1,p1,np.array([[-2],[2]]))
        Translation_animation(x2,p2,np.array([[4],[2]]))
        Translation_animation(x3,p3,np.array([[4],[-2]]))
        self.wait()




class generate_4thdegree_bezier(Scene):
    def construct(self):

        """bezier function takes:
            1.the degree of the curve(n).
            2.the position of the control points as a numpy array(control).
        *********************************************************************** """
        def bezier(n,control):
            grid=ScreenGrid()
            self.add(grid)
            t=ValueTracker(0)
            """adding the control points to the screen """
            for i in range(n+1):
                self.add(Dot(control[i]))
            self.wait()
            
            """Writing the lines between the control points """
            for i in range(n):
                self.play(Write(Line(control[i],control[i+1])))
            
            """definig the parametric EQN of the curve then animating the curve """
            def linearint(t,pi,pf):
                return (1-t)*pi+t*pf

            def combination(s,r):
                return (math.factorial(s))/(math.factorial(r)*math.factorial(s-r))


            def parametric(t):
                x=pow(1-t,n)*control[0]
                for i in range(1,n+1):
                    x=x+combination(n,i)*pow(1-t,n-i)*pow(t,i)*control[i]

                return x

            curve=ParametricFunction(parametric,t_max=0).set_color(RED)
            def updatecurve(m):
                m.reset_t_max(t.get_value())

            curve.add_updater(updatecurve)
            self.add(curve)
            self.play(t.increment_value,1,run_time=3)
            self.wait()
        """***********************************************************************"""
        

        """creating the control array of the 4th degree curve  """
        def coords(m):
           return m[0,0]*RIGHT + m[1,0]*UP
        x0=np.array([[-4],[-2]])
        x1=np.array([[-4],[2]])
        x2=np.array([[4],[-2]])
        x3=np.array([[4],[2]])
        x4=np.array([[0],[3]])
        control=np.array([coords(x0),coords(x1),coords(x2),coords(x3),coords(x4)])

        """passing the degree of the curve(4) and the control array to our function"""
        bezier(4,control)
        self.wait()


class higher_degree_bezier(Scene):
    def construct(self):
        """modified bezier function takes only the degree of the curve(n)
        and scatters the n+1 control pts along the perimeter of a circle of radius 3
        **************************************************************************** """
        def bezier(n):
            t=ValueTracker(0)
            control=np.array([
                3*np.cos(a) * RIGHT + 3*np.sin(a) * UP
                for a in np.linspace(0,2*PI,n+2)
            ])

            """adding the control points to the screen """
            control_pts_as_Dots=[]
            for i in range(n+1):
                control_pts_as_Dots.append(Dot(control[i]))
                self.add(control_pts_as_Dots[i])
            
            """adding the lines between the control points """
            lines=[]
            for i in range(n):
                lines.append(Line(control[i],control[i+1]))
                self.add(lines[i])
            
            """definig the parametric EQN of the curve then animating the curve """
            def linearint(t,pi,pf):
                return (1-t)*pi+t*pf

            def combination(s,r):
                return (math.factorial(s))/(math.factorial(r)*math.factorial(s-r))


            def parametric(t):
                x=pow(1-t,n)*control[0]
                for i in range(1,n+1):
                    x=x+combination(n,i)*pow(1-t,n-i)*pow(t,i)*control[i]

                return x

            curve=ParametricFunction(parametric,t_max=0).set_color(RED)
            def updatecurve(m):
                m.reset_t_max(t.get_value())

            curve.add_updater(updatecurve)
            self.add(curve)
            self.play(t.increment_value,1,run_time=3)
            self.wait()
            """Removing the curve,pts and lines """
            self.remove(curve)
            for i in range(n+1):
                self.remove(control_pts_as_Dots[i])
            for i in range(n):
                self.remove(lines[i])

            self.wait(2)
            
        """****************************************************************************"""

        for i in range(5,15):
            bezier(i)
            

            


        



            






        
        
            
