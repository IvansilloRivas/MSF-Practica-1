"""
Práctica 0: Mecánica pulmonar

Departamento de Ingeniería Eléctrica y Electrónica, Ingeniería Biomédica
Tecnológico Nacional de México [TecNM - Tijuana]
Blvd. Alberto Limón Padilla s/n, C.P. 22454, Tijuana, B.C., México

Nombre del alumno: Edgar Iván Rivas Rosas
Número de control: 21212748
Correo institucional: l21212748@tectijuana.edu.mx

Asignatura: Modelado de Sistemas Fisiológicos
Docente: Dr. Paul Antonio Valle Trujillo; paul.valle@tectijuana.edu.mx
"""
# Instalar librerias en consola
#!pip install control
#!pip install slycot

# Librerías para cálculo numérico y generación de gráficas
import numpy as np
import math as m
import matplotlib.pyplot as plt
import control as ctrl


# Datos de la simulación
x0,t0,tend,dt,w,h = 0,0,10,1E-3,6,3
N = round((tend-t0)/dt) + 1
t = np.linspace(t0,tend,N)

u1 = np.ones(N) #Escalón unitario
u2 = np.zeros(N); u2[round(1/dt):round(2/dt)] = 1 #Impulso
u3 = (np.linspace(0,tend,N))/tend #Rampa con pendiente 1/10
u4 = np.sin(m.pi/2*t) #Función sinusoidal, pi/2 = 250 mHz

u = np.stack((u1,u2,u3,u4), axis = 1)
signal = ["Escalon", "Impulso","Rampa","Sin"]


# Componentes del circuito RLC y función de transferencia
R = 10E3
L = 47E-6
C = 1000E-6
num = [R*C*L,R*R*C+L,R]
den = [3*R*C*L,5*R*R*C+L,2*R]
sys = ctrl.tf(num,den)
print(sys)


# Componentes del controlador
Cr = 1E-6
kI= 207
Re = 1/(kI*Cr); print('Re = ', Re)

numPID = [1]
denPID = [Re*Cr,0]
PID = ctrl.tf(numPID,denPID)
print(PID)

# Sistema de control en lazo cerrado
X = ctrl.series(PID,sys)
sysPID = ctrl.feedback(X,1, sign= -1)
print(sysPID)




# Respuesta del sistema en lazo abierto y en lazo cerrado
morado =[68/255, 23/255, 82/255]
rosa =[255/255, 116/255, 139/255]
naranja =[255/255, 101/255, 0/255]
verde =[228/255, 241/255, 172/255]



fig1 = plt.figure();
plt.plot(t,u1,"-", color = morado, label = "Ve(t)")
_,PA = ctrl.forced_response(sys,t,u1,x0)
plt.plot(t,PA,"-", color = rosa, label = "Vs(t)")

_,VPID = ctrl.forced_response(sysPID,t,u1,x0)
plt.plot(t,VPID,":", linewidth = 3, color = verde, label = "VID(t)")

plt.xlim(-0.25,10); plt.xticks(np.arange(0,11,1.0))
plt.ylim(0,1.2); plt.yticks(np.arange(0,1.2,0.1))
plt.xlabel("t [s]", fontsize = 11)
plt.ylabel("V_i(t) [v]", fontsize = 11)
plt.legend(bbox_to_anchor = (0.5,-0.3), loc= "center", ncol=3,
           fontsize = 8, frameon = False)
plt.show()
fig1.savefig("step.pdf",bbox_inches = "tight")


fig2 = plt.figure();
plt.plot(t,u2,"-", color = rosa, label = "Ve(t)")
_,PA = ctrl.forced_response(sys,t,u2,x0)
plt.plot(t,PA,"-", color = verde, label = "Vs(t)")

_,VPID = ctrl.forced_response(sysPID,t,u2,x0)
plt.plot(t,VPID,":", linewidth = 3, color = naranja, label = "VID(t)")

plt.xlim(-0.25,10); plt.xticks(np.arange(0,11,1.0))
plt.ylim(0,1.2); plt.yticks(np.arange(0,1.2,0.1))
plt.xlabel("t [s]", fontsize = 11)
plt.ylabel("V_i(t) [v]", fontsize = 11)
plt.legend(bbox_to_anchor = (0.5,-0.3), loc= "center", ncol=3,
           fontsize = 8, frameon = False)

plt.show()
fig2.savefig("pulse.pdf",bbox_inches = "tight")


fig3 = plt.figure();
plt.plot(t,u3,"-", color = naranja, label = "Ve(t)")
_,PA = ctrl.forced_response(sys,t,u3,x0)
plt.plot(t,PA,"-", color = verde, label = "Vs(t)")

_,VPID = ctrl.forced_response(sysPID,t,u3,x0)
plt.plot(t,VPID,":", linewidth = 3, color = morado, label = "VID(t)")

plt.xlim(-0.25,10); plt.xticks(np.arange(0,11,1.0))
plt.ylim(0,1.1); plt.yticks(np.arange(0,1.2,0.1))
plt.xlabel("t [s]", fontsize = 11)
plt.ylabel("V_i(t) [v]", fontsize = 11)
plt.legend(bbox_to_anchor = (0.5,-0.3), loc= "center", ncol=3,
           fontsize = 8, frameon = False)

plt.show()
fig3.savefig("ramp.pdf",bbox_inches = "tight")


fig4 = plt.figure();
plt.plot(t,u4,"-", color = verde, label = "Ve(t)")
_,PA = ctrl.forced_response(sys,t,u4,x0)
plt.plot(t,PA,"-", color = morado, label = "Vs(t)")

_,VPID = ctrl.forced_response(sysPID,t,u4,x0)
plt.plot(t,VPID,":", linewidth = 3, color = naranja, label = "VID(t)")

plt.xlim(-0.25,10); plt.xticks(np.arange(0,11,1.0))
plt.ylim(-1.2,1.2); plt.yticks(np.arange(-1.2,1.2,0.1))
plt.xlabel("t [s]", fontsize = 11)
plt.ylabel("V_i(t) [v]", fontsize = 11)
plt.legend(bbox_to_anchor = (0.5,-0.3), loc= "center", ncol=3,
           fontsize = 8, frameon = False)

plt.show()
fig4.savefig("sin.pdf",bbox_inches = "tight")
