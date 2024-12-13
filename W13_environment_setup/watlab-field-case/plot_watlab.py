import watlab
import matplotlib.pyplot as plt
import gis

mesh_path = 'msh/laonong_gmsh_size_10.msh'
DEM_path = 'raster/raw/laonongDEM_5m.tif'
profile_shp_path = 'shape/plotting/profile_polyline/polyline.shp'
outputFolder = 'outputs_laonong'
pic_path_template = outputFolder + '/pic_{:d}_{:02d}.txt'

mesh = watlab.Mesh(mesh_path)
mesh.set_nodes_elevation_from_tif(DEM_path)

#create the mesh and plotter object
plotter = watlab.Plotter(mesh)

#time of the plot
time0 = "0_00"
time1 = "320_00"
time2 = "600_00"
time3 = "720_00"
time4 = "920_00"
time5 = "960_00"


#path of the pic at the corresponding times
myPic0 = outputFolder + "\\pic_"+ time0 +".txt"
myPic1 = outputFolder + "\\pic_"+ time1 +".txt"
myPic2 = outputFolder + "\\pic_"+ time2 +".txt"
myPic3 = outputFolder + "\\pic_"+ time3 +".txt"
myPic4 = outputFolder + "\\pic_"+ time4 +".txt"
myPic5 = outputFolder + "\\pic_"+ time5 +".txt"

plotter.plot(myPic0, "h")
plt.title("Time: " + time0 +" s")
plt.show()

plotter.plot(myPic1, "h")
plt.title("Time: " + time1 +" s")
plt.show()

plotter.plot_on_hillshade(myPic1,"h",DEM_path)
plt.title("Time: " + time1 +" s on hillshade")
plt.show()

plotter.plot(myPic2, "h")
plt.title("Time: " + time2 +" s")
plt.show()

plotter.plot(myPic3, "h")
plotter.show_velocities(myPic3, scale=150, velocity_ds=0.2)
plt.title("Time: " + time3 +" s")

plotter.plot(myPic4, "h")
plt.title("Time: " + time4 +" s")
plt.show()

plotter.plot(myPic5, "h")
plt.title("Time: " + time5 +" s")
plt.show()

# #cross section plot
polylines = gis.get_polyline_coordinates_from_shapefile(profile_shp_path)
plotter.plot_profile_along_polyline(myPic0, "h", x_coordinate=polylines[0], y_coordinate=polylines[1], new_fig = True, label = time0)
plotter.plot_profile_along_polyline(myPic1, "h", x_coordinate=polylines[0], y_coordinate=polylines[1], label = time1)
plotter.plot_profile_along_polyline(myPic2, "h", x_coordinate=polylines[0], y_coordinate=polylines[1], label = time2)
plotter.plot_profile_along_polyline(myPic3, "h", x_coordinate=polylines[0], y_coordinate=polylines[1], label = time3)
plotter.plot_profile_along_polyline(myPic4, "h", x_coordinate=polylines[0], y_coordinate=polylines[1], label = time4)
plotter.plot_profile_along_polyline(myPic4, "h", x_coordinate=polylines[0], y_coordinate=polylines[1], label = time5)


plotter.create_video_on_hillshade(pic_path_template,'laonong_1500cms',time_step = 40, variable_name = "h",dem_path=DEM_path)


plt.show(block = True)