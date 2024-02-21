#!/usr/bin/env python
from re import I
from typing import Text
from colour import Color
from big_ol_pile_of_manim_imports import *
from tutorial.formulas_txt.formulas import formulas
from numpy import *
from pathlib import Path


class Grid(VGroup):
    CONFIG = {
        "height": 6.0,
        "width": 6.0,
    }

    def __init__(self, rows, columns, **kwargs):
        digest_config(self, kwargs, locals())
        super().__init__(**kwargs)

        x_step = self.width / self.columns
        y_step = self.height / self.rows

        for x in np.arange(0, self.width + x_step, x_step):
            self.add(Line(
                [x - self.width / 2., -self.height / 2., 0],
                [x - self.width / 2., self.height / 2., 0],
            ))
        for y in np.arange(0, self.height + y_step, y_step):
            self.add(Line(
                [-self.width / 2., y - self.height / 2., 0],
                [self.width / 2., y - self.height / 2., 0]
            ))


class ScreenGrid(VGroup):
    CONFIG = {
        "rows": 8,
        "columns": 14,
        "height": FRAME_Y_RADIUS * 2,
        "width": 14,
        "grid_stroke": 0.5,
        "grid_color": WHITE,
        "axis_color": RED,
        "axis_stroke": 2,
        "labels_scale": 0.25,
        "labels_buff": 0,
        "number_decimals": 2
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        rows = self.rows
        columns = self.columns
        grid = Grid(width=self.width, height=self.height, rows=rows, columns=columns)
        grid.set_stroke(self.grid_color, self.grid_stroke)

        vector_ii = ORIGIN + np.array((- self.width / 2, - self.height / 2, 0))
        vector_si = ORIGIN + np.array((- self.width / 2, self.height / 2, 0))
        vector_sd = ORIGIN + np.array((self.width / 2, self.height / 2, 0))

        axes_x = Line(LEFT * self.width / 2, RIGHT * self.width / 2)
        axes_y = Line(DOWN * self.height / 2, UP * self.height / 2)

        axes = VGroup(axes_x, axes_y).set_stroke(self.axis_color, self.axis_stroke)

        divisions_x = self.width / columns
        divisions_y = self.height / rows

        directions_buff_x = [UP, DOWN]
        directions_buff_y = [RIGHT, LEFT]
        dd_buff = [directions_buff_x, directions_buff_y]
        vectors_init_x = [vector_ii, vector_si]
        vectors_init_y = [vector_si, vector_sd]
        vectors_init = [vectors_init_x, vectors_init_y]
        divisions = [divisions_x, divisions_y]
        orientations = [RIGHT, DOWN]
        labels = VGroup()
        set_changes = zip([columns, rows], divisions, orientations, [0, 1], vectors_init, dd_buff)
        for c_and_r, division, orientation, coord, vi_c, d_buff in set_changes:
            for i in range(1, c_and_r):
                for v_i, directions_buff in zip(vi_c, d_buff):
                    ubication = v_i + orientation * division * i
                    coord_point = round(ubication[coord], self.number_decimals)
                    label = TextMobject(f"{coord_point}",font="Arial",stroke_width=0).scale(self.labels_scale)
                    label.next_to(ubication, directions_buff, buff=self.labels_buff)
                    labels.add(label)

        self.add(grid, axes, labels)




class FirstScene(Scene):
        def construct(self):
                text=TextMobject("$\int_0^f dx$")
                text.scale(2)

                self.play(FadeInFromDown(text), run_time=3)
                self.wait()

                self.play(FadeOut(text), run_time=3)
                self.wait()

class Grafico(GraphScene):
        CONFIG = {
                "y_max": 3,
                "y_min": -3,
                "x_max": 4,
                "x_min": -4,
                "graph_origin" : ORIGIN ,
                "x_axis_label": "$t$",
                "y_axis_label": "$f(t)$",
                "x_axis_width": 8,
        }
       
        def construct(self):
                self.setup_axes(animate=True)
                f = self.get_graph(self.func, x_min = -2, x_max = 2)
                punto = Dot()
                punto.move_to(np.array([5,2,0]))
                text= TextMobject("$P$")
                text.next_to(punto, UP, buff=0.25)
                punto2 = Dot()
                punto2.move_to(np.array([-4, 8,0]))
                
                self.play(Write(f), run_time=3)
                self.wait()

                self.play(FadeIn(punto))
                self.wait()

                self.play(FadeInFromDown(text))
                self.wait()

                self.play(FadeOut(text))
                self.wait()
   
                self.play(Transform(punto, punto2))
                self.wait

                self.play(MoveAlongPath(punto, f), run_time=3)
                self.wait()

                self.play(FadeOut(punto))
                self.wait

                ss_group = self.get_secant_slope_group(
            0, f,
            dx = 0.001,
            secant_line_color = RED
                )
                self.animate_secant_slope_group_change(
            ss_group,
            target_dx = 0.01,
            target_x = 2,
                run_time=4)


                #self.play(MoveAlongPath(punto2, f), run_time=3)


        def func(self, x):

                return 0.5 * x**2


class Logo(Scene):
    def construct(self):
        logo = SVGMobject("./logoIB.svg")
        logo.scale(2)
        logo.set_color(RED)

        self.play(FadeIn(logo), Write(logo), run_time=6)
        self.wait()
        self.play(FadeOut(logo))
        self.wait()

class Flecha2(Scene):
	def construct(self):
		paso1 = TextMobject("Paso 1")
		paso2 = TextMobject("Paso 2")
		paso1.move_to(LEFT*2+DOWN*2)
		paso2.move_to(4*RIGHT+2*UP)
		flecha1 = Arrow(paso1.get_right(),paso2.get_left(),buff=0.1)
		flecha1.set_color(RED)
		flecha2 = Arrow(paso1.get_top(),paso2.get_bottom(),buff=0.1)
		flecha2.set_color(BLUE)
		self.play(Write(paso1),Write(paso2))
		self.play(GrowArrow(flecha1))
		self.play(GrowArrow(flecha2))
		self.wait()

class Prisma(Scene):
    def construct(self):
        logo = SVGMobject("./logoIB.svg")
        logo.scale(2)
        logo.set_color('#b50707')
        self.play(FadeIn(logo), Write(logo), run_time=6)
        logo2 = SVGMobject("./logoIB.svg")
        logo2.scale(0.6)
        logo2.set_color('#b50707')
        logo2.move_to(np.array([6.2,-3,0]))
        self.play(Transform(logo,logo2))
        titulo = TextMobject("Índice de refracción de un prisma")
        self.play(Write(titulo))
        self.wait(2)
        titulo2 = TextMobject("Índice de refracción de un prisma")
        titulo2.move_to(np.array([0,3,0])).scale(0.75)
        self.play(Transform(titulo,titulo2))
        self.wait(2)
        introduccion = TextMobject("Introducción").scale(0.75)
        introduccion.move_to(titulo2.get_bottom()+0.3*DOWN)
        self.play(Write(introduccion))
        self.wait(2)
        triangulo = Triangle(color = BLUE, fill_color=BLUE, fill_opacity=0.25).rotate(90*DEGREES).scale(2)
        self.add(triangulo)
        tria=TextMobject("Triángulo equilátero").scale(0.75)
        tria.move_to(triangulo.get_bottom()+DOWN*1)
        self.play(Write(triangulo, run_time=2), Write(tria))
        indx = TextMobject("$n$").scale(0.8)
        indx.move_to(np.array([1.6,-1.3,0]))
        self.play(Write(indx))
        self.wait(2)
        arcBetweenPoints=ArcBetweenPoints(start_point=np.array([-0.25,1.25,0], dtype = float),end_point=np.array([0.75,1.25,0],dtype = float))
        varphi = TextMobject("$\phi$").scale(0.6)
        varphi.move_to(np.array([0.25,0.8,0]))
        self.play(Write(varphi),ShowCreation(arcBetweenPoints))
        self.wait(2)

        tria2=TextMobject("Triángulo equilátero", color=YELLOW).scale(0.75)
        tria2.move_to(titulo2.get_center()+5*LEFT)
        indx2=TextMobject("Índice de refracción: $n$").scale(0.6)
        indx2.move_to(introduccion.get_center()+5.12*LEFT+0.07*UP)
        varphi2 = TextMobject("Ángulo: $\phi$").scale(0.6)
        varphi2.move_to(indx2.get_center()+0.43*DOWN+0.825*LEFT)
        RECT = Rectangle()
        RECT.move_to(tria2.get_center()+0.4*DOWN)
        self.play(Transform(tria,tria2), Transform(indx,indx2), Transform(varphi, varphi2), FadeOut(arcBetweenPoints),Write(RECT))
        
        self.wait(2)

        linea1 = Line(np.array([-3,-1,0]), np.array([-0.35,0.5,0]))
        linea2 = Line(np.array([-0.35,0.5,0]), np.array([0.85,0.5,0]))
        linea3 = Line(np.array([0.85,0.5,0]), np.array([3,-0.5,0]))
        linea1.set_color(WHITE)
        linea2.set_color(WHITE)
        self.play(GrowArrow(linea1), run_time=0.5)
        self.play(GrowArrow(linea2), run_time=0.5)
        self.play(GrowArrow(linea3), run_time=0.5)
        linea4 = DashedLine(np.array([-1,0.132075,0]), np.array([1.5,1.5471698,0]))
        self.play(Write(linea4))
        self.wait(1)

        triangulo2 = Triangle(color = BLUE, fill_color=BLUE, fill_opacity=0.25).rotate(90*DEGREES).scale(2)
        triangulo2.move_to(triangulo.get_center()+3*RIGHT)
        linea6 = Line(np.array([-0.34,0.5,0]), np.array([0.85,0.5,0]))
        linea7 = Line(np.array([0.85,0.5,0]), np.array([3,-0.5,0]))
        linea5 = Line(np.array([-3,-1,0]), np.array([-0.35,0.5,0]))
        linea8 = DashedLine(np.array([-1,0.132075,0]), np.array([1.5,1.5471698,0]))
        linea5.move_to(linea1.get_center()+3*RIGHT)
        linea6.move_to(linea2.get_center()+3*RIGHT)
        linea7.move_to(linea3.get_center()+3*RIGHT)
        linea8.move_to(linea4.get_center()+3*RIGHT)
        arcBetweenPoints2=ArcBetweenPoints(start_point=np.array([-0.25,1.25,0], dtype = float),end_point=np.array([0.75,1.25,0],dtype = float))
        arcBetweenPoints2.move_to(arcBetweenPoints.get_center()+3*RIGHT)

        arco2 = ArcBetweenPoints(start_point=np.array([1.2,0.32735,0], dtype = float),end_point=np.array([1.2,1.37735,0],dtype = float))
        gamma = TextMobject("$\gamma$")
        gamma.move_to(arco2.get_right()+0.4*RIGHT)
        self.wait(2)

        arco3 = ArcBetweenPoints(start_point=np.array([1.2,0.32735,0], dtype = float),end_point=np.array([1.2,1.37735,0],dtype = float))
        gamma2 = TextMobject("$\gamma$")
        arco3.move_to(arco2.get_center()+3*RIGHT)
        gamma2.move_to(gamma.get_center()+3*RIGHT)

        self.play(Transform(triangulo, triangulo2), Transform(linea2,linea6),Transform(linea3,linea7),Transform(linea1,linea5), Transform(linea4,linea8))
        self.wait(2)

        equation = TexMobject("n", "=\\frac{\\sin (\\frac{\gamma + \phi}{2})}{\\sin (\\frac{\gamma}{2})}")
        equation.move_to(np.array([-4,-0.5,0]))
        self.play(Write(equation[0]), Write(equation[1]))
        self.wait(2)

        self.play(Transform(equation[0], equation[0].copy().set_color(YELLOW)))
        self.play(Transform(equation[0], equation[0].copy().set_color(YELLOW)))
        self.wait()


class Ejercicio5(Scene):
    def construct(self):
        cuadrado = Square(fill_color=GRAY, fill_opacity=0.5)
        cuadrado.scale(2)
        cuadrado2 = Square(fill_color=GRAY, fill_opacity=0.25)
        cuadrado2.move_to(np.array([1,1,0]))
        cuadrado2.scale(2)
        start = (2,-2,0)
        end = (3,-1,0)
        recta = Line(start, end)
        start1 = (2,2,0)
        end1 = (3,3,0)
        recta1 = Line(start1, end1)
        start2 = (-2,2,0)
        end2 = (-1,3,0)
        recta2 = Line(start2, end2)
        start3 = (-2,-2,0)
        end3 = (-1,-1,0)
        recta3 = Line(start3, end3)
        #origen=Dot()
        consigna1 = TextMobject("Un recipiente lleno de aire, a temperatura y presión ambiente\\\ ","se expone a un haz de rayos X que ioniza una pequeña fracción de las", "moléculas interiores.")
        consigna1.scale(0.7)
        self.play(FadeInFromDown(consigna1[0], run_time=1.5), FadeInFromDown(consigna1[1], run_time=2), FadeInFromDown(consigna1[2], run_time=2.5))
        self.wait(3)

        #self.add(origen)
        self.add(cuadrado)
        self.play(FadeOut(consigna1[0:4], run_time=1.5), FadeIn(cuadrado, run_time=3), FadeIn(cuadrado2, run_time=3), FadeIn(recta1, run_time=3), FadeIn(recta2, run_time=3), FadeIn(recta3, run_time=3), FadeIn(recta, run_time=3), 
        DrawBorderThenFill(cuadrado, run_time=3), DrawBorderThenFill(cuadrado2, run_time=3),  Write(recta, run_time=3), Write(recta1, run_time=3), Write(recta2, run_time=3), Write(recta3, run_time=3))
        self.wait()

        metal = TextMobject("Placas de metal")
        metal.move_to(np.array([-4,1,0]))
        flechametal = Arrow(metal.get_bottom(), cuadrado.get_left())
        flechametal.set_color(YELLOW)
        self.play(Write(metal), GrowArrow(flechametal), run_time=0.75)
        self.wait(2)

        self.play(FadeOut(metal), FadeOut(flechametal))
        self.wait()

        
        aire = TextMobject("$O_2+N_2$")
        aire.move_to(np.array([4.5,2,0]))
        flechaO2 = Arrow(aire.get_bottom(), np.array([2.5,0.5,0]))
        flechaO2.set_color(YELLOW)
        self.play(Write(aire), GrowArrow(flechaO2), run_time=0.75)
        self.wait(2)

        self.play(FadeOut(aire), FadeOut(flechaO2))
        self.wait()

        
        cuadrado3 = Square(fill_color=GRAY, fill_opacity=0.5)
        cuadrado3.move_to(np.array([4,0,0]))
        cuadrado3.scale(1.5)
        cuadrado4 = Square(fill_color=GRAY, fill_opacity=0.25)
        cuadrado4.move_to(np.array([4.75,0.75,0]))
        cuadrado4.scale(1.5)
        start4 = (5.5,-1.5,0)
        end4 = (6.25,-0.75,0)
        recta4 = Line(start4, end4)
        start5 = (5.5,1.5,0)
        end5 = (6.25,2.25,0)
        recta5 = Line(start5, end5)
        start6 = (2.5,1.5,0)
        end6 = (3.25,2.25,0)
        recta6 = Line(start6, end6)
        start7 = (2.5,-1.5,0)
        end7 = (3.25,-0.75,0)
        recta7 = Line(start7, end7)

        self.play(Transform(cuadrado, cuadrado3), Transform(cuadrado2, cuadrado4), Transform(recta, recta4), Transform(recta1, recta5), 
        Transform(recta2, recta6), Transform(recta3, recta7))
        self.wait()

        temp = TextMobject("$T=298$ K")
        pres = TextMobject("$P=1$ atm")
        temp.move_to(np.array([4,0,0]))
        pres.move_to(np.array([4,0,0]))
        temp2 = TextMobject("$T=298$ K")
        pres2 = TextMobject("$P=1$ atm")
        temp2.move_to(np.array([-2,1,0]))
        pres2.move_to(np.array([-2,-1,0]))

        #Para mover más facil:
        temp.generate_target()
        temp.target.move_to(np.array([-2,1,0]))
        pres.generate_target()
        pres.target.move_to(np.array([-2,-1,0]))
        self.play(FadeIn(temp, run_time=2),FadeIn(pres, run_time=2), MoveToTarget(pres), MoveToTarget(temp))
        self.wait(2)


        #self.play(Transform(pres, pres2), Transform(temp, temp2, run_time=1.2))
        #self.wait(2)

        temp3 = TextMobject("$T=298$ K")
        temp3.move_to(np.array([-5.75,3,0]))
        temp3.scale(0.75)
        pres3 = TextMobject("$P=1$ atm")
        pres3.move_to(np.array([-5.75,2.6,0]))
        pres3.scale(0.75)
        temp3.set_color(RED)
        pres3.set_color(BLUE)

        
        self.play(Transform(temp, temp3), Transform(pres, pres3))
        self.wait()

        corr = TextMobject("$I=1.5$ $\mu$A")
        volt = TextMobject("$\Delta V=1$ kV")
        corr.move_to(np.array([3.75,0,0]))
        volt.move_to(np.array([3.75,0,0]))
        corr2 = TextMobject("$I=1.5$ $\mu$A")
        volt2 = TextMobject("$\Delta V=1$ kV")
        corr2.move_to(np.array([-2,1,0]))
        volt2.move_to(np.array([-2,-1,0]))


        self.play(Transform(corr, corr2), Transform(volt, volt2, run_time=1.2))
        self.wait()

        corr3 = TextMobject("$I=1.5$ $\mu$A")
        corr3.move_to(np.array([-5.75,2.2,0]))
        corr3.scale(0.75)
        volt3 = TextMobject("$\Delta V=1$ kV")
        volt3.move_to(np.array([-5.75,1.8,0]))
        volt3.scale(0.75)
        volt3.set_color("#7c45ba")
        corr3.set_color(YELLOW)

        
        self.play(Transform(volt, volt3), Transform(corr, corr3))
        self.wait()

        llave1 = Brace(cuadrado, LEFT, buff = SMALL_BUFF)
        llave2 = Brace(recta6, LEFT, buff = SMALL_BUFF)
        t1 = llave1.get_text("$A=10$ cm$^2$")
        t2 = llave2.get_text("$L=2$ cm")
        t2.move_to(t2.get_center()+0.6*RIGHT+0.5*UP)
        self.play(GrowFromCenter(llave1), FadeIn(t1, run_time=2))
        self.wait
        llave2.rotate(-PI/4)
        llave2.move_to(llave2.get_center()+0.4*RIGHT + 0.2*UP)
        area = TextMobject("$A=10$ cm$^2$")
        area.scale(0.75)
        area.move_to(np.array([-3.5,3.01,0]))       
        lado = TextMobject("$L=2$ cm")
        lado.move_to(np.array([-3.65,2.6,0]))
        lado.scale(0.75)
       
        self.play(FadeOut(llave1), Transform(t1,area), GrowFromCenter(llave2), FadeIn(t2))
        self.wait()

        self.play(FadeOut(llave2), Transform(t2, lado))
        self.wait()
        
        flecha1= Arrow(LEFT, RIGHT)
        flecha2= Arrow(LEFT, RIGHT)
        flecha3= Arrow(LEFT, RIGHT)
        flecha2.move_to(RIGHT*1+DOWN*0.6)
        flecha3.move_to(RIGHT*1+UP*0.6)
        flecha1.move_to(RIGHT*1)
        flecha1.set_color(YELLOW)
        flecha2.set_color(YELLOW)
        flecha3.set_color(YELLOW)
        raios = TextMobject("Rayos X")
        raios.move_to(np.array([1,-1.5,0]))

        self.play(Write(raios), GrowArrow(flecha1), GrowArrow(flecha2), GrowArrow(flecha3), run_time=0.75)
        self.wait(0.1)
        self.play(GrowArrow(flecha1), GrowArrow(flecha2), GrowArrow(flecha3), run_time=0.75)
        self.wait(0.1)
        self.play(GrowArrow(flecha1), GrowArrow(flecha2), GrowArrow(flecha3), run_time=0.75)
        self.wait(0.1)
        self.play(GrowArrow(flecha1), GrowArrow(flecha2), GrowArrow(flecha3), run_time=0.75)
        self.wait()
        self.play(Uncreate(flecha1), Uncreate(flecha2), Uncreate(flecha3), Uncreate(raios))
        self.wait()

        incisoa = TextMobject("¿Cuál es la conductividad", "(","$\sigma$",")", 
        "de \\\ este gas ligeramente ionizado?")
        incisoa.move_to(np.array([-2.25,-0.5,0]))
        self.play(Write(incisoa))
        self.wait(3)

        formula = TexMobject("\\sigma","=","\\frac{IL}{\\Delta V A}")
        formula.move_to(np.array([-2,0,0]))

        self.play(ReplacementTransform(incisoa[2].copy(), formula[0]), 
        FadeOut(incisoa, run_time=0.75), Write(formula[1:3]))
        self.wait(3)

        resultadosigma = TexMobject("\\sigma","=","3\cdot 10^{-9}"," (\\Omega\\text{m})^{-1}")
        resultadosigma.move_to(np.array([-2,0,0]))
        self.play(ReplacementTransform(formula[0].copy(), resultadosigma[0]), 
        FadeOut(formula, run_time=0.75), Write(resultadosigma[1:4]))
        self.wait(3)

        resultadosigma2 = TexMobject("\\sigma","=","3\cdot 10^{-9}"," (\\Omega\\text{m})^{-1}")
        resultadosigma2.move_to(np.array([-2.8,2.2,0]))
        resultadosigma2.scale(0.75)

        self.play(Transform(resultadosigma, resultadosigma2))
        self.wait(2)

        incisob = TextMobject("Para calcular","$\\tau$",", necesitamos \\\ los","datos de la", "velocidad media", "de \\\ iones,","y el", "recorrido libre medio")
        incisob.move_to(np.array([-2.25,-0.5,0]))

        self.play(FadeInFromDown(incisob))
        self.wait(5)

        self.play(FadeOut(incisob[0]), FadeOut(incisob[2:4]),FadeOut(incisob[5:7]))
        self.wait(3)


        formulatau = TexMobject("\\tau","=")
        formulatau2 = TexMobject ("\\text{recorrido libre medio}","\\over","\\text{velocidad media}")
        formulatau.move_to(np.array([-3.95,0,0]))
        formulatau2.move_to(np.array([-1,0,0]))

        #self.play(Write(formulatau), Write(formulatau2))
        #self.wait()



        #formulatau = TexMobject("\\tau","=","\\frac{\\text{recorrido libre medio}}{\\text{velocidad media}}")
        #formulatau.move_to(np.array([-2,0,0]))
        self.remove(incisob[1])
        self.remove(incisob[4])
        self.remove(incisob[7])
        self.play(
            ReplacementTransform(incisob[1].copy(), formulatau[0]),
            ReplacementTransform(incisob[4].copy(), formulatau2[2]), 
            ReplacementTransform(incisob[7].copy(), formulatau2[0]), 
            Write(formulatau[1]), Write(formulatau2[1]),
            #FadeOut(incisob[1], run_time=0.75),
            #FadeOut(incisob[4], run_time=0.75),
            #FadeOut(incisob[7], run_time=0.75)
            
        )
        self.wait(3)
        
        #FadeOut(incisob[1], run_time=0.75), FadeOut(incisob[4], run_time=0.75), FadeOut(incisob[7], run_time=0.75), Write(formulatau[1:4]))
        #self.wait(3)

        resultadotau = TexMobject("2 \\cdot 10^{-10}","\\text{s}")
        resultadotau.generate_target()
        resultadotau.target.move_to(np.array([-2.3,0.1,0]))
        self.play(Transform(formulatau2, resultadotau))
        self.remove(formulatau2)
        self.play(MoveToTarget(resultadotau))
        self.wait(2)

        


class Flecha1(Scene):
	def construct(self):
		paso1 = TextMobject("Paso 1")
		paso2 = TextMobject("Paso 2")
		flecha = Arrow(LEFT,RIGHT)
		paso1.move_to(LEFT*2)
		flecha.next_to(paso1,RIGHT,buff = .1)
		paso2.next_to(flecha,RIGHT,buff = .1)
		self.play(Write(paso1))
		self.wait()
		self.play(GrowArrow(flecha))
		self.play(Write(paso2))
		self.wait()


class TransformacionTexto1v1(Scene):
	def construct(self):
		texto1 = TextMobject("$bruh$")
		texto2 = TextMobject("El pana miguel")
		self.play(Write(texto1))
		self.wait()
		self.play(Transform(texto1,texto2))
		self.wait()


class PosicionCamara1(ThreeDScene):
    def construct(self):
        circulo=Circle()
        self.play(ShowCreation(circulo))
        self.wait()


class PosicionCamara2(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes()
        circulo=Circle()
        self.set_camera_orientation(phi=0 * DEGREES)
        self.play(ShowCreation(circulo),ShowCreation(axes))
        self.wait()


class MovimientoCamara1(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes()
        circulo=Circle()
        self.play(ShowCreation(circulo),ShowCreation(axes))
        self.move_camera(phi=30*DEGREES,theta=-45*DEGREES,run_time=3)
        self.wait()

class FormulaColor1(Scene): 
    def construct(self):
        texto = TexMobject("x","=","{a","\\over","b}")
        texto[0].set_color(RED)
        texto[1].set_color(BLUE)
        texto[2].set_color(GREEN)
        texto[3].set_color(ORANGE)
        texto[4].set_color("#DC28E2")
        self.play(Write(texto))
        self.wait(2)

class MovimientoLlaves(Scene):
    def construct(self):
        texto=TexMobject(
            "\\frac{d}{dx}f(x)g(x)=","f(x)\\frac{d}{dx}g(x)","+",
            "g(x)\\frac{d}{dx}f(x)"
        )
        self.play(Write(texto))
        llave1 = Brace(texto[1], UP, buff = SMALL_BUFF)
        llave2 = Brace(texto[3], UP, buff = SMALL_BUFF)
        t1 = llave1.get_text("$g'f$")
        t2 = llave2.get_text("$f'g$")
        self.play(
            GrowFromCenter(llave1),
            FadeIn(t1),
            )
        self.wait()
        self.play(
        	ReplacementTransform(llave1,llave2),
        	ReplacementTransform(t1,t2)
        	)
        self.wait()


class CopiadoTextoV2(Scene):
	def construct(self):
		formula = TexMobject("\\frac{d}{dx}",
			"(","u","+","v",")","=",
			"\\frac{d}{dx}","u","+","\\frac{d}{dx}","v"
			)
		formula.scale(2)
		self.play(Write(formula[0:7]))
		self.wait()
		self.play(
			ReplacementTransform(formula[2].copy(),formula[8]),
			ReplacementTransform(formula[4].copy(),formula[11]),
			ReplacementTransform(formula[3].copy(),formula[9]),
			run_time=3
			)
		self.wait()
		self.play(
			ReplacementTransform(formula[0].copy(),formula[7]),
			ReplacementTransform(formula[0].copy(),formula[10]),
			run_time=3
			)
		self.wait()

class Puntito(Scene):
    def construct(self):
        punto = Dot()
        punto.move_to(np.array([2,1,0]))
        grid=ScreenGrid()
        text= TextMobject("Vector $\Vec{v}$")
        #text.move_to(punto.get_center()+0.5*UP)
        text.next_to(punto, UP, buff=0.25)
        punto2 = Dot()
        punto2.move_to(punto.get_center()+3*RIGHT)
        text2 = TextMobject("Vector $\Vec{w}$")
        text2.next_to(punto2, UP, buff=0.25)

        self.add(grid)
        
        self.play(FadeIn(punto), run_time=2)
        self.wait()

        self.play(FadeInFromDown(text))
        self.wait()
   
        self.play(Transform(punto, punto2), Transform(text, text2))
        self.wait()



class Ejercicio7(GraphScene):
    CONFIG = {
        "y_max" : 5,
        "y_min" : -5,
        "x_max" : 5,
        "x_min" : -5,
        "y_tick_frequency" : 10, #Subdivisiones de y
        "x_tick_frequency" : 10, #Subdivisiones de x
        "axes_color" : WHITE, #Color de los ejes XY
        "y_labeled_nums": range(0,60,10),
        "x_labeled_nums": list(np.arange(2, 7.0+0.5, 0.5)),
        "x_label_decimal":1,
        "y_label_direction": RIGHT,
        "x_label_direction": UP,
        "y_label_decimal":3
        
    }
    def construct(self):
        self.setup_axes(animate=True) #animate=True para animar al mostrar los ejes
        #Definición de gráfica
        grafica = self.get_graph(lambda x : x**2, # Función en numpy 
                                    color = GREEN,
                                    x_min = 2, # Dominio
                                    x_max = 4
                                    )
        #Animar creación de gráfica
        self.play(
        	ShowCreation(grafica),
            run_time = 2
        )
        self.wait()

