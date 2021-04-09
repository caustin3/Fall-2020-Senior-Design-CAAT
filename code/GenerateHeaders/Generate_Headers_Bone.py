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


f.write('// 3D Bone Twist Test -- twist bone and top and bottom to see if we can get some nice torsion fractures\n')
f.write('// ./anisofracture -test 25\n')
f.write('\n')
f.write('int fracture_type = 1; //0:twisting 1:bending 2:pulling\n')
f.write('\n')
f.write('sim.end_frame = ' + endFrame + ';\n')
f.write('T frameRate = ' + frameRate + ';\n')
f.write('sim.step.frame_dt = (T)1 / frameRate;\n')
f.write('sim.dx = 0.005;\n')
f.write('sim.gravity = ' + gravity + ' * TV::Unit(1); //no gravity\n')
f.write('sim.step.max_dt = 1e-6; //3e-5;2e-6;6e-6;4e-6;1e-6;1e-5;2e-5;5e-6  //bending:200k->1e-6 50k->5e-6 //pulling:50k->7e-6 400k->2.9e-6 //twisting: 200k->5e-6\n')
f.write('sim.newton.max_iterations = 5;\n')
f.write('sim.newton.tolerance = 1e-3;\n')
f.write('sim.objective.minres.max_iterations = 10000;\n')
f.write('sim.objective.minres.tolerance = 1e-4;\n')
f.write('sim.quasistatic = false;\n')
f.write('sim.symplectic = true; // want explicit!\n')
f.write('sim.objective.matrix_free = true;\n')
f.write('sim.verbose = false;\n')
f.write('sim.dump_F_for_meshing = true;\n')
f.write('sim.cfl = 0.4;\n')
f.write('sim.transfer_scheme = MpmSimulationBase<T, dim>::APIC_blend_RPIC;\n')
f.write('sim.apic_rpic_ratio = 0; //full RPIC\n')
f.write('//sim.rpic_damping_iteration = 5;\n')
f.write('\n')
f.write('//Test params\n')
f.write('T Youngs = Python::E; //need to crank this for bone\n')
f.write('T nu = 0.25;\n')
f.write('T rho = 800; //2\n')
f.write('QRStableNeoHookean<T, dim> model(Youngs, nu);\n')
f.write('\n')
f.write('// sample particles from a .mesh file\n')
f.write('std::string filename = "' + mesh + '"; //50k is plenty for nice dynamics and no debris\n')
f.write('MpmParticleHandleBase<T, dim> particles_handle = init_helper.sampleFromTetWildFile(filename, rho);\n')
f.write('T total_volume = particles_handle.total_volume;\n')
f.write('T particle_count = particles_handle.particle_range.length();\n')
f.write('T per_particle_volume = total_volume / particle_count;\n')
f.write('\n')
f.write('// set dx\n')
f.write('int particle_per_cell = 6;\n')
f.write('sim.dx = std::pow(particle_per_cell * per_particle_volume, (T)1 / (T)3);\n')
f.write('\n')
f.write('T suggested_dt = evaluateTimestepLinearElasticityAnalysis(Youngs, nu, rho, sim.dx, sim.cfl);\n')
f.write('if (sim.symplectic) { ZIRAN_ASSERT(sim.step.max_dt <= suggested_dt, suggested_dt); }\n')
f.write('\n')
f.write('StdVector<TV> node_wise_fiber;\n')
f.write('if (fracture_type == 2) {\n')
f.write('    StdVector<TV> samples;\n')
f.write('    StdVector<Vector<int, 4>> indices;\n')
f.write('    std::string absolute_path = DataDir().absolutePath(filename);\n')
f.write('    readTetMeshTetWild(absolute_path, samples, indices);\n')
f.write('    std::function<bool(TV, int)> inflow = [](TV X, int vertex) {\n')
f.write('        return ((X - TV(5.13, 5.83, 5.18)).norm() < 0.1);\n')
f.write('    };\n')
f.write('    std::function<bool(TV, int)> outflow = [](TV X, int vertex) {\n')
f.write('        return ((X - TV(5.16, 5.14, 5.17)).norm() < 0.1);\n')
f.write('    };\n')
f.write('    StdVector<TV> tet_wise_fiber;\n')
f.write('    fiberGen(samples, indices, inflow, outflow, tet_wise_fiber, node_wise_fiber);\n')
f.write('}\n')
f.write('\n')
f.write('//Anisotropic fracture params, grab these from the flags\n')
f.write('StdVector<TV> a_0;\n')
f.write('StdVector<T> alphas;\n')
f.write('TV a_1, a_2;\n')
f.write('a_1[0] = 0; //y direction fiber\n')
f.write('a_1[1] = 1;\n')
f.write('a_1[2] = 0;\n')
f.write('a_1.normalize();\n')
f.write('a_0.push_back(a_1);\n')
f.write('alphas.push_back(-1);\n')
f.write('\n')
f.write('T percentage = Python::percent;\n')
f.write('T l0 = 0.5 * sim.dx;\n')
f.write('T eta = Python::eta; //set this as nu since it's what we used before\n')
f.write('T zeta = 1;\n')
f.write('bool allow_damage = true;\n')
f.write('\n')
f.write('//Construct the file path\n')
f.write('\n')
f.write('std::string alpha_str = std::to_string(Python::alpha1);\n')
f.write('alpha_str.erase(alpha_str.find_last_not_of('0') + 1, std::string::npos);\n')
f.write('std::cout << "Alpha = " << Python::alpha1 << std::endl;\n')
f.write('\n')
f.write('std::string E_str = std::to_string(Youngs);\n')
f.write('E_str.erase(E_str.find_last_not_of('0') + 1, std::string::npos);\n')
f.write('std::cout << "Youngs = " << Youngs << std::endl;\n')
f.write('\n')
f.write('std::string percent_str = std::to_string(percentage);\n')
f.write('percent_str.erase(percent_str.find_last_not_of('0') + 1, std::string::npos);\n')
f.write('std::cout << "Percentage = " << percentage << std::endl;\n')
f.write('\n')
f.write('std::string eta_str = std::to_string(eta);\n')
f.write('eta_str.erase(eta_str.find_last_not_of('0') + 1, std::string::npos);\n')
f.write('std::cout << "Eta = " << eta << std::endl;\n')
f.write('\n')
f.write('std::string dx_str = std::to_string(sim.dx);\n')
f.write('dx_str.erase(dx_str.find_last_not_of('0') + 1, std::string::npos);\n')
f.write('std::cout << "SimDx = " << sim.dx << std::endl;\n')
f.write('\n')
f.write('std::string scale_str = std::to_string(Python::fiberScale);\n')
f.write('scale_str.erase(scale_str.find_last_not_of('0') + 1, std::string::npos);\n')
f.write('std::cout << "FiberScale = " << Python::fiberScale << std::endl;\n')
f.write('\n')
f.write('if (Python::isotropic) {\n')
f.write('    std::string path("output/3D_BoneTwist/3D_BoneTwist_Isotropic_Youngs" + E_str + "_percent" + percent_str + "_eta" + eta_str + "_dx" + dx_str + "_fiberScale" + scale_str);\n')
f.write('    sim.output_dir.path = path;\n')
f.write('}\n')
f.write('else {\n')
f.write('    std::string path("output/3D_BoneTwist/3D_BoneTwist_Youngs" + E_str + "_percent" + percent_str + "_eta" + eta_str + "_dx" + dx_str + "_fiberScale" + scale_str /*+ "computeSigmaCrit"*/);\n')
f.write('    sim.output_dir.path = path;\n')
f.write('    model.setExtraFiberStiffness(0, Python::fiberScale); //only scale elasticity if anisotropic!\n')
f.write('}\n')
f.write('\n')
f.write('particles_handle.addFBasedMpmForceWithAnisotropicPhaseField(a_0, alphas, percentage, l0, model, eta, zeta, allow_damage, Python::residual);\n')
f.write('\n')
f.write('init_helper.addAllWallsInDomain(4096 * sim.dx, 5 * sim.dx, AnalyticCollisionObject<T, dim>::STICKY); // add safety domain walls for SPGrid.\n')
f.write('\n')
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
f.write('if (fracture_type == 2) {\n')
f.write('    //Rotate F to match fiber direction\n')
f.write('    int i = 0;\n')
f.write('    for (auto iter = particles_handle.particles.subsetIter(DisjointRanges{ particles_handle.particle_range }, F_name<T, dim>()); iter; ++iter) {\n')
f.write('        auto& F = iter.template get<0>();\n')
f.write('        TV fiber = node_wise_fiber[i++];\n')
f.write('        StdVector<TV> a0;\n')
f.write('        a0.emplace_back(fiber);\n')
f.write('        F = particles_handle.initializeRotatedFHelper(a0);\n')
f.write('    }\n')
f.write('}\n')
f.write('\n')
f.write('//Setup boundary condition\n')
f.write('\n')
f.write('if (fracture_type == 0) //twist\n')
f.write('{\n')
f.write('    TV center(0, 0, 0);\n')
f.write('    T radius = 0.2;\n')
f.write('    auto topTransform = [](T time, AnalyticCollisionObject<T, dim>& object) {\n')
f.write('        T velocity = 0.02;\n')
f.write('        T theta = (T)-40.0 / 180 * M_PI;\n')
f.write('        T t = time;\n')
f.write('        Vector<T, 4> rotation(std::cos(theta * t / 2), 0, std::sin(theta * t / 2), 0);\n')
f.write('        object.setRotation(rotation);\n')
f.write('        TV omega(0, theta, 0);\n')
f.write('        object.setAngularVelocity(omega);\n')
f.write('        TV translation_velocity(0, velocity, 0);\n')
f.write('        TV translation(5.13, 5.83 + velocity * t, 5.18);\n')
f.write('        object.setTranslation(translation, translation_velocity);\n')
f.write('    };\n')
f.write('    auto bottomTransform = [](T time, AnalyticCollisionObject<T, dim>& object) {\n')
f.write('        T velocity = -0.02;\n')
f.write('        //T endTime = 1.2;\n')
f.write('        T theta = (T)40.0 / 180 * M_PI;\n')
f.write('        T t = time;\n')
f.write('        Vector<T, 4> rotation(std::cos(theta * t / 2), 0, std::sin(theta * t / 2), 0);\n')
f.write('        object.setRotation(rotation);\n')
f.write('        TV omega(0, theta, 0);\n')
f.write('        object.setAngularVelocity(omega);\n')
f.write('        TV translation_velocity(0, velocity, 0);\n')
f.write('        TV translation(5.16, 5.14 + velocity * t, 5.17);\n')
f.write('        object.setTranslation(translation, translation_velocity);\n')
f.write('    };\n')
f.write('\n')
f.write('    Sphere<T, dim> topLS(center, radius);\n')
f.write('    Sphere<T, dim> bottomLS(center, radius);\n')
f.write('    AnalyticCollisionObject<T, dim> topObject(topTransform, topLS, AnalyticCollisionObject<T, dim>::STICKY);\n')
f.write('    AnalyticCollisionObject<T, dim> bottomObject(bottomTransform, bottomLS, AnalyticCollisionObject<T, dim>::STICKY);\n')
f.write('    init_helper.addAnalyticCollisionObject(topObject);\n')
f.write('    init_helper.addAnalyticCollisionObject(bottomObject);\n')
f.write('}\n')
f.write('\n')
f.write('else if (fracture_type == 1) //bending\n')
f.write('{\n')
f.write('    TV center(0, 0, 0);\n')
f.write('    T radius = 0.3;\n')
f.write('    auto topTransform = [](T time, AnalyticCollisionObject<T, dim>& object) {\n')
f.write('        T theta = (T)40.0 / 180 * M_PI;\n')
f.write('        T t = time;\n')
f.write('        Vector<T, 4> rotation(std::cos(theta * t / 2), std::sin(theta * t / 2), 0, 0);\n')
f.write('        object.setRotation(rotation);\n')
f.write('        TV omega(theta, 0, 0);\n')
f.write('        object.setAngularVelocity(omega);\n')
f.write('        TV translation_velocity(0, 0, 0);\n')
f.write('        TV translation(5.13, 5.83, 5.18);\n')
f.write('        object.setTranslation(translation, translation_velocity);\n')
f.write('    };\n')
f.write('    auto bottomTransform = [](T time, AnalyticCollisionObject<T, dim>& object) {\n')
f.write('        T theta = (T)-40.0 / 180 * M_PI;\n')
f.write('        T t = time;\n')
f.write('        Vector<T, 4> rotation(std::cos(theta * t / 2), std::sin(theta * t / 2), 0, 0);\n')
f.write('        object.setRotation(rotation);\n')
f.write('        TV omega(theta, 0, 0);\n')
f.write('        object.setAngularVelocity(omega);\n')
f.write('        TV translation_velocity(0, 0, 0);\n')
f.write('        TV translation(5.16, 5.14, 5.17);\n')
f.write('        object.setTranslation(translation, translation_velocity);\n')
f.write('    };\n')
f.write('    Sphere<T, dim> topLS(center, radius);\n')
f.write('    Sphere<T, dim> bottomLS(center, radius);\n')
f.write('    AnalyticCollisionObject<T, dim> topObject(topTransform, topLS, AnalyticCollisionObject<T, dim>::STICKY);\n')
f.write('    AnalyticCollisionObject<T, dim> bottomObject(bottomTransform, bottomLS, AnalyticCollisionObject<T, dim>::STICKY);\n')
f.write('    init_helper.addAnalyticCollisionObject(topObject);\n')
f.write('    init_helper.addAnalyticCollisionObject(bottomObject);\n')
f.write('}\n')
f.write('else if (fracture_type == 2) //pulling\n')
f.write('{\n')
f.write('    TV center(0, 0, 0);\n')
f.write('    T radius = 0.3;\n')
f.write('    auto topTransform = [](T time, AnalyticCollisionObject<T, dim>& object) {\n')
f.write('        T velocity = 0.04; //0.02\n')
f.write('        T theta = (T)-0 / 180 * M_PI;\n')
f.write('        T t = time;\n')
f.write('        Vector<T, 4> rotation(std::cos(theta * t / 2), 0, std::sin(theta * t / 2), 0);\n')
f.write('        object.setRotation(rotation);\n')
f.write('        TV omega(0, theta, 0);\n')
f.write('        object.setAngularVelocity(omega);\n')
f.write('        TV translation_velocity(0, velocity, 0);\n')
f.write('        TV translation(5.13, 5.83 + velocity * t, 5.18);\n')
f.write('        object.setTranslation(translation, translation_velocity);\n')
f.write('    };\n')
f.write('    auto bottomTransform = [](T time, AnalyticCollisionObject<T, dim>& object) {\n')
f.write('        T velocity = -0.04; //-0.02\n')
f.write('        //T endTime = 1.2;\n')
f.write('        T theta = (T)0 / 180 * M_PI;\n')
f.write('        T t = time;\n')
f.write('        Vector<T, 4> rotation(std::cos(theta * t / 2), 0, std::sin(theta * t / 2), 0);\n')
f.write('        object.setRotation(rotation);\n')
f.write('        TV omega(0, theta, 0);\n')
f.write('        object.setAngularVelocity(omega);\n')
f.write('        TV translation_velocity(0, velocity, 0);\n')
f.write('        TV translation(5.16, 5.14 + velocity * t, 5.17);\n')
f.write('        object.setTranslation(translation, translation_velocity);\n')
f.write('    };\n')
f.write('    Sphere<T, dim> topLS(center, radius);\n')
f.write('    Sphere<T, dim> bottomLS(center, radius);\n')
f.write('    AnalyticCollisionObject<T, dim> topObject(topTransform, topLS, AnalyticCollisionObject<T, dim>::STICKY);\n')
f.write('    AnalyticCollisionObject<T, dim> bottomObject(bottomTransform, bottomLS, AnalyticCollisionObject<T, dim>::STICKY);\n')
f.write('    init_helper.addAnalyticCollisionObject(topObject);\n')
f.write('    init_helper.addAnalyticCollisionObject(bottomObject);\n')
f.write('\n')

f.close();