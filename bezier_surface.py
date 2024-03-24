# 3D plots are enabled by importing the mplot3d toolkit
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np


# mouse point selecting variables
selectedPoint = None
ind = None
selected_x = None
selected_y = None
selected_z = None
mouse_x = None
mouse_y = None

def bezier_surface(X,Y,Z,uCells,wCells):
    # Binomial coefficients
    def Ci(n , i): 
        return np.math.factorial(n) / (np.math.factorial(i)*np.math.factorial(n-i))
    # bernstein basis polynomial
    def J(n,i,u):
        return np.matrix(Ci(n,i) * (u**i) * (1-u) ** (n-i))
    uCells = uCells
    wCells = wCells

    nControlPointU = np.size(X,0)
    nControlPointW = np.size(X,1)

    nSubdevisionU = nControlPointU -1
    nSubdevisionW = nControlPointW -1

    Bernstein_Basis_Polynomial_B = []
    Bernstein_Basis_Polynomial_D = []

    ParamVarU = np.linspace(0,1,uCells)
    ParamVarW = np.linspace(0,1,wCells)

    xBezier = np.zeros((uCells,wCells))
    yBezier = np.zeros((uCells,wCells))
    zBezier = np.zeros((uCells,wCells))

    for i in range(0,nControlPointU):
        for j in range(0,nControlPointW):
            Bernstein_Basis_Polynomial_B.append(J(nSubdevisionU,i,ParamVarU))
            Bernstein_Basis_Polynomial_D.append(J(nSubdevisionW,j,ParamVarW))

            J_tran = J(nSubdevisionU, i, ParamVarU).transpose()
            xBezier = J_tran * J(nSubdevisionW, j, ParamVarW) * X[i,j] + xBezier
            yBezier = J_tran * J(nSubdevisionW, j, ParamVarW) * Y[i,j] + yBezier
            zBezier = J_tran * J(nSubdevisionW, j, ParamVarW) * Z[i,j] + zBezier
    return xBezier , yBezier , zBezier

def onpick(event):    
    global selectedPoint
    global ind
    global selected_x 
    global selected_y 
    global selected_z 
    global mouse_x
    global mouse_y

    if selectedPoint != None:
        props = { 'color' : "blue" }
        selectedPoint.set(**props)

    # Getting the index of the picked point
    ind = event.ind[0]
   
    colors2 = np.array(scatter.get_facecolors())
    colors2[ind] = [1, 0, 0, 1]  # Set selected points to red
    scatter.set_facecolors(colors2)
    scatter.set_edgecolor(colors2)
    selectedPoint = event.artist
   
    # Get the position information of the point
    
    x, y, z = selectedPoint._offsets3d[0][ind] , selectedPoint._offsets3d[1][ind] , selectedPoint._offsets3d[2][ind] 

    selected_x = x
    selected_y = y
    selected_z = z
    print(event.mouseevent.xdata)
    mouse_x = event.mouseevent.xdata
    mouse_y = event.mouseevent.ydata
    # Print the position
    print(f"Point position: x={x}, y={y}, z={z}")
    plt.draw()
    
def on_motion(event):
    global selectedPoint
    global ind
    global selected_x 
    global selected_y 
    global selected_z 
    global mouse_x
    global mouse_y

    if selectedPoint is None:  return
    dx = event.xdata - mouse_x
    dy = event.ydata - mouse_y
    x = dx
    y = dy 
    z = 0

    x1  = x * np.cos(np.pi/4) - y * np.sin(np.pi/4)
    y1 = y * np.cos(np.pi/4) + x * np.sin(np.pi/4)
    z1 = z

    dx_= x1 * np.cos(np.pi/4) + z1 * np.sin(np.pi/4)
    dy_ = y1
    dz_ = z1 * np.cos(np.pi/4) - x1 * np.sin(np.pi/4)
    
    x_point[ind] += dx_*10
    y_point[ind] += dy_*10
    z_point[ind] += dz_*10

    scatter._offsets3d = ([x_point,y_point,z_point])
    fig.canvas.draw_idle()

def on_release(event):
    global selectedPoint
    global ind
    global selected_x 
    global selected_y 
    global selected_z 
    global mouse_x
    global mouse_y
    global surf
    if selectedPoint != None:
        props = { 'color' : "blue" }
        selectedPoint.set(**props)
    print("do bezier")
    xb,yb,zb = bezier_surface(x_point.reshape((20,20)), y_point.reshape((20,20)), z_point.reshape((20,20)),uCells,wCells)
    surf.remove()
    surf = ax.plot_surface(xb, yb, zb , alpha=0.9)
    """Clear button press information."""
    selectedPoint = None
    ind = None
    selected_x = None
    selected_y = None
    selected_z = None
    mouse_x = None
    mouse_y = None
    fig.canvas.draw_idle()

# With this object, we will create a subplot and add a projection attribute of type 3D.
fig = plt.figure()
ax = fig.add_subplot(111, projection = '3d')

# Disable mouse rotation
ax.disable_mouse_rotation()

fig.canvas.mpl_connect('pick_event', onpick)
fig.canvas.mpl_connect('motion_notify_event', on_motion)
fig.canvas.mpl_connect('button_release_event', on_release)

uCells = 20
wCells = 20

#pioints
x_point, y_point = np.meshgrid(np.linspace(-2, 2, 20) , np.linspace(-2, 2, 20))
z_point = np.zeros([1,400])
x_point = x_point.reshape(-1)
y_point = y_point.reshape(-1)
z_point = z_point.reshape(-1)

#labels
ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')

# showing limitations
ax.set_xlim3d(-2, 2)  # Sets the x-axis range from 0 to 6
ax.set_ylim3d(-2, 2)  # Sets the y-axis range from 0 to 12
ax.set_zlim3d(-2, 2)  # Sets the z-axis range from 0 to 18

scatter = ax.scatter(x_point, y_point, z_point, color='blue', picker = True, pickradius=5, marker='o')
xb,yb,zb = bezier_surface(x_point.reshape((20,20)), y_point.reshape((20,20)), z_point.reshape((20,20)),uCells,wCells)
surf = ax.plot_surface(xb,yb,zb,alpha=0.9)
plt.show()






