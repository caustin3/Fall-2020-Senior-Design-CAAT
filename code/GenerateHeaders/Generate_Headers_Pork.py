import os
from optparse import OptionParser



parser = OptionParser();
parser.add_option("-m", "--mesh", dest="mesh",
                  help="The name of the desired mesh file");
parser.add_option("-o", "--output", dest="output",
                  help="The name of the header file being generated")
parser.add_option("-e", "--endFrame", dest="endFrame", default="160",
                  help="The amount of frames to be generated")
parser.add_option("-r", "--frameRate", dest="frameRate", default="24",
                  help="The amount of frames per second")
parser.add_option("-g", "--gravity", dest="gravity", default = "-9.8",
                  help="The gravity rate")

(options, args) = parser.parse_args();
mesh = options.mesh;
output = options.output;
endFrame = options.endFrame;
frameRate = options.frameRate;
gravity = options.gravity;
                  

f = open(output, "w+", newline = "\n");




f.write('// DongPo Pork Belly\n')
f.write('// ./anisofracture -test 14\n')
f.write('\n')
f.write('//FINAL PARAMS FROM PYTHON\n')
f.write('\n')
f.write('bool orthotropic = Python::orthotropic;\n')
f.write('\n')
f.write('sim.end_frame = ' + endFrame + '; //72\n')
f.write('T frameRate = ' + frameRate + '; //24\n')
f.write('sim.step.frame_dt = (T)1 / frameRate;\n')
f.write('sim.dx = 0.01; //use 0.0025 for high res\n')
f.write('sim.gravity = ' + gravity + ' * TV::Unit(1); //no gravity\n')
f.write('sim.step.max_dt = /*1e-3*/ /*3e-4*/ 2.5e-4; //with test params can use 8e-5\n')
f.write('sim.newton.max_iterations = 5;\n')
f.write('sim.newton.tolerance = 1e-3;\n')
f.write('sim.objective.minres.max_iterations = 10000;\n')
f.write('sim.objective.minres.tolerance = 1e-4;\n')
f.write('sim.quasistatic = false;\n')
f.write('sim.symplectic = true; // want explicit!\n')
f.write('sim.objective.matrix_free = true;\n')
f.write('sim.verbose = false;\n')
f.write('sim.cfl = 0.4;\n')
f.write('// sim.transfer_scheme = MpmSimulationBase<T, dim>::APIC_blend_RPIC;  //orthotropic and trans iso use full RPIC\n')
f.write('// sim.apic_rpic_ratio = 0; //full RPIC\n')
f.write('sim.transfer_scheme = MpmSimulationBase<T, dim>::FLIP_blend_PIC;\n')
f.write('sim.flip_pic_ratio = 0.0; //isotropic uses full PIC\n')
f.write('sim.dump_F_for_meshing = true;\n')
f.write('\n')
f.write('//Test params\n')
f.write('T Youngs = Python::E;\n')
f.write('T nu = 0.25;\n')
f.write('T rho = 2;\n')
f.write('QRStableNeoHookean<T, dim> model(Youngs, nu);\n')
f.write('\n')
f.write('// sample particles from a .mesh file\n')
f.write('std::string filename = "' + mesh + '"; //50k is plenty for nice dynamics and no debris\n')
f.write('MpmParticleHandleBase<T, dim> particles_handle = init_helper.sampleFromTetWildFile(filename, rho);\n')
f.write('T total_volume = particles_handle.total_volume;\n')
f.write('T particle_count = particles_handle.particle_range.length();\n')
f.write('T per_particle_volume = total_volume / particle_count;\n')
f.write('\n')
f.write('int particle_per_cell = 7;\n')
f.write('\n')
f.write('// set dx\n')
f.write('sim.dx = std::pow(particle_per_cell * per_particle_volume, (T)1 / (T)3);\n')
f.write('\n')
f.write('//Orthotropic parameters!\n')
f.write('StdVector<TV> a_0;\n')
f.write('StdVector<T> alphas;\n')
f.write('TV a_1, a_2;\n')
f.write('if (orthotropic) { //orthotropic\n')
f.write('    a_1[0] = 1;\n')
f.write('    a_1[1] = 0;\n')
f.write('    a_1[2] = 0;\n')
f.write('    a_1.normalize();\n')
f.write('    a_0.push_back(a_1);\n')
f.write('    alphas.push_back(-1);\n')
f.write('    a_2[0] = 0;\n')
f.write('    a_2[1] = 0;\n')
f.write('    a_2[2] = 1;\n')
f.write('    a_2.normalize();\n')
f.write('    a_0.push_back(a_2);\n')
f.write('    alphas.push_back(-1);\n')
f.write('}\n')
f.write('else if (!Python::isotropic) { //transverse isotropic\n')
f.write('    a_1[0] = 1;\n')
f.write('    a_1[1] = 0; //45 deg in XZ plane\n')
f.write('    a_1[2] = 1;\n')
f.write('    a_1.normalize();\n')
f.write('    a_0.push_back(a_1);\n')
f.write('    alphas.push_back(-1);\n')
f.write('}\n')
f.write('else { //isotropic\n')
f.write('    a_1[0] = 1;\n')
f.write('    a_1[1] = 0;\n')
f.write('    a_1[2] = 0;\n')
f.write('    a_1.normalize();\n')
f.write('    a_0.push_back(a_1);\n')
f.write('    alphas.push_back(0);\n')
f.write('}\n')
f.write('\n')
f.write('T percentage = Python::percent;\n')
f.write('T l0 = 0.5 * sim.dx;\n')
f.write('T eta = Python::eta; //set this as nu since it\'s what we used before\n')
f.write('T zeta = 1;\n')
f.write('bool allow_damage = true;\n')
f.write('\n')
f.write('//Construct the file path\n')
f.write('std::string E_str = std::to_string(Youngs);\n')
f.write('E_str.erase(E_str.find_last_not_of(\'0\') + 1, std::string::npos);\n')
f.write('std::cout << "Youngs = " << Youngs << std::endl;\n')
f.write('\n')
f.write('std::string percent_str = std::to_string(percentage);\n')
f.write('percent_str.erase(percent_str.find_last_not_of(\'0\') + 1, std::string::npos);\n')
f.write('std::cout << "Percentage = " << percentage << std::endl;\n')
f.write('\n')
f.write('std::string eta_str = std::to_string(eta);\n')
f.write('eta_str.erase(eta_str.find_last_not_of(\'0\') + 1, std::string::npos);\n')
f.write('std::cout << "Eta = " << eta << std::endl;\n')
f.write('\n')
f.write('std::string dx_str = std::to_string(sim.dx);\n')
f.write('dx_str.erase(dx_str.find_last_not_of(\'0\') + 1, std::string::npos);\n')
f.write('std::cout << "SimDx = " << sim.dx << std::endl;\n')
f.write('\n')
f.write('std::string scale_str = std::to_string(Python::fiberScale);\n')
f.write('scale_str.erase(scale_str.find_last_not_of(\'0\') + 1, std::string::npos);\n')
f.write('std::cout << "FiberScale = " << Python::fiberScale << std::endl;\n')
f.write('\n')
f.write('if (Python::isotropic) {\n')
f.write('    std::string path("output/3D_Pork/3D_Pork_Isotropic_Youngs" + E_str + "_percent" + percent_str + "_eta" + eta_str + "_dx" + dx_str + "_fiberScale" + scale_str);\n')
f.write('    sim.output_dir.path = path;\n')
f.write('}\n')
f.write('else if (orthotropic) {\n')
f.write('    std::string path("output/3D_Pork/3D_Pork_Orthotropic_Youngs" + E_str + "_percent" + percent_str + "_eta" + eta_str + "_dx" + dx_str + "_fiberScale" + scale_str);\n')
f.write('    sim.output_dir.path = path;\n')
f.write('    model.setExtraFiberStiffness(0, Python::fiberScale); //only scale elasticity if anisotropic!\n')
f.write('    model.setExtraFiberStiffness(1, Python::fiberScale);\n')
f.write('}\n')
f.write('else {\n')
f.write('    std::string path("output/3D_Pork/3D_Pork_TransverseIsotropic_Youngs" + E_str + "_percent" + percent_str + "_eta" + eta_str + "_dx" + dx_str + "_fiberScale" + scale_str);\n')
f.write('    sim.output_dir.path = path;\n')
f.write('    model.setExtraFiberStiffness(0, Python::fiberScale); //only scale elasticity if anisotropic!\n')
f.write('}\n')
f.write('\n')
f.write('// dump a vtk file in the output folder for mpmmeshing\n')
f.write('if (1) {\n')
f.write('    StdVector<TV> samples;\n')
f.write('    StdVector<Vector<int, 4>> indices;\n')
f.write('    std::string absolute_path = DataDir().absolutePath(filename);\n')
f.write('    readTetMeshTetWild(absolute_path, samples, indices);\n')
f.write('    sim.output_dir.createPath();\n')
f.write('    std::string vtk_path = DataDir().path + "/../Projects/anisofracture/" + sim.output_dir.path + "/tet.vtk";\n')
f.write('    writeTetmeshVtk(vtk_path, samples, indices);\n')
f.write('}\n')
f.write('\n')
f.write('//Setup the box material\n')
f.write('T xSize = 0.4;\n')
f.write('T ySize = 0.2;\n')
f.write('T zSize = 0.4;\n')
f.write('T materialToHold = 0.03;\n')
f.write('TV boxMin(2 - (xSize / 2.0), 2 - (ySize / 2.0) - materialToHold, 2 - (zSize / 2.0)); //needs extra material at bottom to hold onto for mode 1\n')
f.write('TV boxMax(2 + (xSize / 2.0), 2 + (ySize / 2.0), 2 + (zSize / 2.0));\n')
f.write('//AxisAlignedAnalyticBox<T, dim> boxLevelSet(boxMin, boxMax);\n')
f.write('\n')
f.write('//Sample particles in the desired level set\n')
f.write('//int ppc = 7;\n')
f.write('//MpmParticleHandleBase<T, dim> particles_handle = init_helper.sampleInAnalyticLevelSet(boxLevelSet, rho, ppc);\n')
f.write('\n')
f.write('//Elasticity Handler\n')
f.write('particles_handle.addFBasedMpmForceWithAnisotropicPhaseField(a_0, alphas, percentage, l0, model, eta, zeta, allow_damage, Python::residual);\n')
f.write('\n')
f.write('//Now setup the boundaries\n')
f.write('//Holder Box\n')
f.write('TV holderMin = boxMin - TV(0.5, 1.0, 0.5);\n')
f.write('TV holderMax(boxMax[0] + 0.5, boxMin[1] + materialToHold, boxMax[2] + 0.5);\n')
f.write('AxisAlignedAnalyticBox<T, dim> holderLS(holderMin, holderMax);\n')
f.write('AnalyticCollisionObject<T, dim> holderObj(holderLS, AnalyticCollisionObject<T, dim>::STICKY);\n')
f.write('init_helper.addAnalyticCollisionObject(holderObj);\n')
f.write('\n')
f.write('//Sphere puller\n')
f.write('//TV sphereCenter(1.8, 2.1, 1.8);\n')
f.write('//T sphereRadius = 0.05;\n')
f.write('TV sphereCenter(1.865, 2.198, 1.865);\n')
f.write('T sphereRadius = 0.05;\n')
f.write('\n')
f.write('T startTime = 6; //wait some time to let it rest\n')
f.write('\n')
f.write('auto sphereTransform = [=](T time, AnalyticCollisionObject<T, dim>& object) {\n')
f.write('    T speed = 0.05;\n')
f.write('    T xVel = speed;\n')
f.write('    T yVel = speed;\n')
f.write('    T zVel = speed;\n')
f.write('\n')
f.write('    if (time < startTime) { //don\'t move yet\n')
f.write('        TV translation = TV(10, 10, 10);\n')
f.write('        TV translation_velocity(0, 0, 0);\n')
f.write('        object.setTranslation(translation, translation_velocity);\n')
f.write('    }\n')
f.write('    else { //normal translation\n')
f.write('        TV translation = TV(xVel * (time - startTime), yVel * (time - startTime), zVel * (time - startTime));\n')
f.write('        TV translation_velocity(xVel, yVel, zVel);\n')
f.write('        object.setTranslation(translation, translation_velocity);\n')
f.write('    }\n')
f.write('};\n')
f.write('\n')
f.write('Sphere<T, dim> sphere(sphereCenter, sphereRadius);\n')
f.write('AnalyticCollisionObject<T, dim> sphereObject(sphereTransform, sphere, AnalyticCollisionObject<T, dim>::STICKY);\n')
f.write('init_helper.addAnalyticCollisionObject(sphereObject);\n')
f.write('\n')
f.write('//Holder Wall\n')
f.write('//T wallX = 2 + 0.37 - (0.5 / 2.0);\n')
f.write('//HalfSpace<T, dim> holderLS(TV(wallX, 2, 2), TV(-1, 0, 0)); //origin, normal\n')
f.write('//AnalyticCollisionObject<T, dim> wallObj(holderLS, AnalyticCollisionObject<T, dim>::STICKY);\n')
f.write('//init_helper.addAnalyticCollisionObject(wallObj);\n')
f.write('\n')
f.write('//TV sphereCenter(1.61, 1.74, 2);\n')
f.write('//T sphereRadius = 0.2;\n')
f.write('//\n')
f.write('//auto sphereTransform = [](T time, AnalyticCollisionObject<T, dim>& object) {\n')
f.write('//    T speed = 0.1;\n')
f.write('//    TV translation_velocity(0, 1 * speed, 0);\n')
f.write('//    TV translation(0, 1 * speed * time, 0); //multiply each velocity by dt to get dx!\n')
f.write('//    object.setTranslation(translation, translation_velocity);\n')
f.write('//};\n')
f.write('//\n')
f.write('//Sphere<T, dim> sphere(sphereCenter, sphereRadius);\n')
f.write('//AnalyticCollisionObject<T, dim> sphereObject(sphereTransform, sphere, AnalyticCollisionObject<T, dim>::SEPARATE);\n')
f.write('//sphereObject.setFriction(0.9); //need friction to try and separate layers!\n')
f.write('//init_helper.addAnalyticCollisionObject(sphereObject);\n')

f.close();