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




f.write('std::string helper_output;\n')
f.write('helper_output = "output/orange";\n')
f.write('\n')
f.write('sim.output_dir.path = helper_output;\n')
f.write('sim.end_frame = ' + endFrame + ';\n')
f.write('T frameRate = ' + frameRate + ';\n')
f.write('sim.step.frame_dt = (T)1 / frameRate;\n')
f.write('sim.gravity = ' + gravity + ' * TV::Unit(1);\n')
f.write('sim.step.max_dt = 1e-3;\n')
f.write('sim.symplectic = true;\n')
f.write('sim.verbose = false;\n')
f.write('sim.cfl = 0.4;\n')
f.write('sim.transfer_scheme = MpmSimulationBase<T, dim>::FLIP_blend_PIC;\n')
f.write('sim.flip_pic_ratio = 0; // FULL PIC for damping\n')
f.write('sim.dump_F_for_meshing = true;\n')
f.write('T particle_per_cell = 20;\n')
f.write('sim.rpic_damping_iteration = 0;\n')
f.write('\n')
f.write('// ****************************************************************************\n')
f.write('// Interior\n')
f.write('// ****************************************************************************\n')
f.write('if (1) {\n')
f.write('    T Youngs = 10000;\n')
f.write('    T nu = 0.4;\n')
f.write('    T rho = 500;\n')
f.write('    T helper_isotropic = false;\n')
f.write('    TV helper_fiber = TV(1, 1, 1); // will overwrite with radial fiber\n')
f.write('    T helper_alpha = -1;\n')
f.write('\n')
f.write('    std::string filename = "' + mesh + '";\n')
f.write('    MpmParticleHandleBase<T, dim> particles_handle = init_helper.sampleFromTetWildFile(filename, rho);\n')
f.write('    T total_volume = particles_handle.total_volume;\n')
f.write('    T particle_count = particles_handle.particle_range.length();\n')
f.write('    T per_particle_volume = total_volume / particle_count;\n')
f.write('    sim.dx = std::pow(particle_per_cell * per_particle_volume, (T)1 / (T)3);\n')
f.write('    if (1) {\n')
f.write('        StdVector<TV> samples;\n')
f.write('        StdVector<Vector<int, 4>> indices;\n')
f.write('        std::string absolute_path = DataDir().absolutePath(filename);\n')
f.write('        readTetMeshTetWild(absolute_path, samples, indices);\n')
f.write('        sim.output_dir.createPath();\n')
f.write('        std::string vtk_path = DataDir().path + "/../Projects/anisofracture/" + sim.output_dir.path + "/tet1.vtk";\n')
f.write('        writeTetmeshVtk(vtk_path, samples, indices);\n')
f.write('    }\n')
f.write('\n')
f.write('    QRAnisotropic<T, dim> model(Youngs, nu, helper_isotropic);\n')
f.write('    StdVector<TV> a_0;\n')
f.write('    StdVector<T> alphas;\n')
f.write('    TV a_1, a_2;\n')
f.write('    a_1 = helper_fiber;\n')
f.write('    a_1.normalize();\n')
f.write('    a_0.push_back(a_1);\n')
f.write('    alphas.push_back(helper_alpha);\n')
f.write('    T theta2 = std::atan2(a_1[1], a_1[2]) * (180 / M_PI);\n')
f.write('    T percentage = 0.15;\n')
f.write('    T l0 = 0.5 * sim.dx;\n')
f.write('    T eta = 0.01;\n')
f.write('    T zeta = 1;\n')
f.write('    bool allow_damage = true;\n')
f.write('    T residual_stress = 0.001;\n')
f.write('    // model.scaleFiberStiffness(0, 2);\n')
f.write('    particles_handle.transform([&](int index, Ref<T> mass, TV& X, TV& V) { X += TV(2, 2, 2); });\n')
f.write('    particles_handle.addFBasedMpmForceWithAnisotropicPhaseField(a_0, alphas, percentage, l0, model, eta, zeta, allow_damage, residual_stress);\n')
f.write('\n')
f.write('    TV center(2, 2, 2);\n')
f.write('    int zeroDim = 1;\n')
f.write('    particles_handle.radialFibers(center, zeroDim);\n')
f.write('\n')
f.write('    // SnowPlasticity<T> p(0, 1, 0.5);\n')
f.write('    //particles_handle.addPlasticity(model, p, "F");\n')
f.write('    std::cout << "Particle count: " << sim.particles.count << std::endl;\n')
f.write('}\n')
f.write('\n')
f.write('// ****************************************************************************\n')
f.write('// Peel\n')
f.write('// ****************************************************************************\n')
f.write('if (1) {\n')
f.write('    T Youngs = 50000;\n')
f.write('    T nu = 0.4;\n')
f.write('    T rho = 500;\n')
f.write('    T helper_isotropic = true;\n')
f.write('    TV helper_fiber = TV(1, 1, 1);\n')
f.write('    T helper_alpha = 0;\n')
f.write('\n')
f.write('    std::string filename = "' + mesh + '";\n')
f.write('    MpmParticleHandleBase<T, dim> particles_handle = init_helper.sampleFromTetWildFile(filename, rho);\n')
f.write('    T total_volume = particles_handle.total_volume;\n')
f.write('    T particle_count = particles_handle.particle_range.length();\n')
f.write('    T per_particle_volume = total_volume / particle_count;\n')
f.write('    sim.dx = std::pow(particle_per_cell * per_particle_volume, (T)1 / (T)3);\n')
f.write('    if (1) {\n')
f.write('        StdVector<TV> samples;\n')
f.write('        StdVector<Vector<int, 4>> indices;\n')
f.write('        std::string absolute_path = DataDir().absolutePath(filename);\n')
f.write('        readTetMeshTetWild(absolute_path, samples, indices);\n')
f.write('        sim.output_dir.createPath();\n')
f.write('        std::string vtk_path = DataDir().path + "/../Projects/anisofracture/" + sim.output_dir.path + "/tet2.vtk";\n')
f.write('        writeTetmeshVtk(vtk_path, samples, indices);\n')
f.write('    }\n')
f.write('\n')
f.write('    QRAnisotropic<T, dim> model(Youngs, nu, helper_isotropic);\n')
f.write('    StdVector<TV> a_0;\n')
f.write('    StdVector<T> alphas;\n')
f.write('    TV a_1, a_2;\n')
f.write('    a_1 = helper_fiber;\n')
f.write('    a_1.normalize();\n')
f.write('    a_0.push_back(a_1);\n')
f.write('    alphas.push_back(helper_alpha);\n')
f.write('    T theta2 = std::atan2(a_1[1], a_1[2]) * (180 / M_PI);\n')
f.write('    T percentage = 999;\n')
f.write('    T l0 = 0.5 * sim.dx;\n')
f.write('    T eta = 0.1;\n')
f.write('    T zeta = 1;\n')
f.write('    bool allow_damage = true;\n')
f.write('    T residual_stress = 0.005;\n')
f.write('    // model.scaleFiberStiffness(0, 2);\n')
f.write('    particles_handle.transform([&](int index, Ref<T> mass, TV& X, TV& V) { X += TV(2, 2, 2); });\n')
f.write('    particles_handle.addFBasedMpmForceWithAnisotropicPhaseField(a_0, alphas, percentage, l0, model, eta, zeta, allow_damage, residual_stress);\n')
f.write('}\n')
f.write('\n')
f.write('// ****************************************************************************\n')
f.write('// Collision objects\n')
f.write('// ****************************************************************************\n')
f.write('TV ground_origin = TV(0, 1.984, 0);\n')
f.write('TV ground_normal(0, 1, 0);\n')
f.write('HalfSpace<T, dim> ground_ls(ground_origin, ground_normal);\n')
f.write('AnalyticCollisionObject<T, dim> ground_object(ground_ls, AnalyticCollisionObject<T, dim>::SLIP);\n')
f.write('ground_object.setFriction(1);\n')
f.write('init_helper.addAnalyticCollisionObject(ground_object);\n')
f.write('\n')
f.write('{\n')
f.write('    auto leftTransform = [](T time, AnalyticCollisionObject<T, dim>& object) {\n')
f.write('        T t = time;\n')
f.write('        TV translation = TV(-0.1 * time, 0, 0) + TV(2, 2, 2);\n')
f.write('        TV translation_velocity(-0.1, 0, 0);\n')
f.write('        object.setTranslation(translation, translation_velocity);\n')
f.write('    };\n')
f.write('    Sphere<T, dim> leftLS(TV(-0.08, 0, -0.2), 0.05);\n')
f.write('    AnalyticCollisionObject<T, dim> leftObject(leftTransform, leftLS, AnalyticCollisionObject<T, dim>::STICKY);\n')
f.write('    init_helper.addAnalyticCollisionObject(leftObject);\n')
f.write('}\n')
f.write('\n')
f.write('{\n')
f.write('    auto leftTransform = [](T time, AnalyticCollisionObject<T, dim>& object) {\n')
f.write('        T t = time;\n')
f.write('        TV translation = TV(-0.1 * time, 0, 0) + TV(2, 2, 2);\n')
f.write('        TV translation_velocity(-0.1, 0, 0);\n')
f.write('        object.setTranslation(translation, translation_velocity);\n')
f.write('    };\n')
f.write('    Sphere<T, dim> leftLS(TV(-0.19, 0, -0.12), 0.05);\n')
f.write('    AnalyticCollisionObject<T, dim> leftObject(leftTransform, leftLS, AnalyticCollisionObject<T, dim>::STICKY);\n')
f.write('    init_helper.addAnalyticCollisionObject(leftObject);\n')
f.write('}\n')
f.write('{\n')
f.write('    auto leftTransform = [](T time, AnalyticCollisionObject<T, dim>& object) {\n')
f.write('        T t = time;\n')
f.write('        TV translation = TV(-0.1 * time, 0, 0) + TV(2, 2, 2);\n')
f.write('        TV translation_velocity(-0.1, 0, 0);\n')
f.write('        object.setTranslation(translation, translation_velocity);\n')
f.write('    };\n')
f.write('    Sphere<T, dim> leftLS(TV(-0.22, 0, 0.01), 0.05);\n')
f.write('    AnalyticCollisionObject<T, dim> leftObject(leftTransform, leftLS, AnalyticCollisionObject<T, dim>::STICKY);\n')
f.write('    init_helper.addAnalyticCollisionObject(leftObject);\n')
f.write('}\n')
f.write('\n')
f.write('{\n')
f.write('    auto rightTransform = [](T time, AnalyticCollisionObject<T, dim>& object) {\n')
f.write('        TV translation = TV(0 * time, 0, 0) + TV(2, 2, 2);\n')
f.write('        TV translation_velocity(0, 0, 0);\n')
f.write('        object.setTranslation(translation, translation_velocity);\n')
f.write('    };\n')
f.write('    Sphere<T, dim> sphere2(TV(0.12, 0, 0), 0.05);\n')
f.write('    AnalyticCollisionObject<T, dim> rightObject(rightTransform, sphere2, AnalyticCollisionObject<T, dim>::STICKY);\n')
f.write('    init_helper.addAnalyticCollisionObject(rightObject);\n')
f.write('}\n')
f.write('\n')
f.write('{\n')
f.write('    auto rightTransform = [](T time, AnalyticCollisionObject<T, dim>& object) {\n')
f.write('        TV translation = TV(0 * time, 0, 0) + TV(2, 2, 2);\n')
f.write('        TV translation_velocity(0, 0, 0);\n')
f.write('        object.setTranslation(translation, translation_velocity);\n')
f.write('    };\n')
f.write('    Sphere<T, dim> sphere2(TV(-0.12, 0, 0.19), 0.05);\n')
f.write('    AnalyticCollisionObject<T, dim> rightObject(rightTransform, sphere2, AnalyticCollisionObject<T, dim>::STICKY);\n')
f.write('    init_helper.addAnalyticCollisionObject(rightObject);\n')
f.write('}\n')
f.write('\n')
f.write('init_helper.addAllWallsInDomain(4096 * sim.dx, 5 * sim.dx, AnalyticCollisionObject<T, dim>::STICKY); // add safety domain walls for SPGrid\n')

f.close();