import watlab

mesh_path = '../W13_environment_setup/watlab-field-case/msh/laonong_gmsh_size_10.msh'
DEM_path = '../W13_environment_setup/watlab-field-case/raster/raw/laonongDEM_5m.tif'

mesh = watlab.Mesh(mesh_path)
mesh.set_nodes_elevation_from_tif(DEM_path)
model = watlab.HydroflowModel(mesh)

model.name = "laonong_Simulation"
model.ending_time = 86400
model.Cfl_number = 0.9

model.set_friction_coefficient("domain",0.05)
model.set_initial_water_level("domain", 0.001)

model.set_boundary_hydrogram('Qin', 'hydrogramme.txt')
model.set_transmissive_boundaries("Qout")
model.set_wall_boundaries(["East", "West"])

model.set_picture_times(n_pic = 49)

model.export.input_folder_name = "inputs_unsteady"
model.export.output_folder_name = "outputs_unsteady"

model.export_data()
model.solve(isParallel=True)