import math
import bpy


def create_scene(scene_name):
    return bpy.data.scenes.new(scene_name)


def create_flag():
    bpy.ops.mesh.primitive_plane_add(
        size=2, enter_editmode=False, align="WORLD", location=(0, 0, 0), scale=(1, 1, 1)
    )
    flag = bpy.context.object
    flag.location = (0.0, 0.0, 0.0)

    flag.rotation_euler[1] = math.radians(90)

    flag.scale[2] = 4
    flag.scale[1] = 1.8

    bpy.ops.object.mode_set(mode="EDIT")

    bpy.ops.mesh.subdivide(number_cuts=40)

    bpy.ops.mesh.quads_convert_to_tris(quad_method="BEAUTY", ngon_method="BEAUTY")

    bpy.ops.object.mode_set(mode="OBJECT")

    flag.name = "Flag"
    cloth_mod = flag.modifiers.new("ClothMod", "CLOTH")

    bpy.context.view_layer.objects.active = flag
    bpy.ops.object.mode_set(mode="EDIT")

    bpy.ops.mesh.select_all(action="DESELECT")

    bpy.ops.object.mode_set(mode="OBJECT")
    for vertex in flag.data.vertices:
        if vertex.co.y == 1 and vertex.co.z == 0:
            vertex.select = True

    bpy.ops.object.mode_set(mode="EDIT")
    group = flag.vertex_groups.new(name="PinGroup")
    bpy.ops.object.vertex_group_assign()

    cloth_mod.settings.vertex_group_mass = "PinGroup"
    cloth_mod.point_cache.frame_end = 400

    bpy.ops.object.mode_set(mode="OBJECT")

    #    cloth_mod.settings.quality = 5
    #    cloth_mod.settings.mass = 0.3

    return flag


def create_wind():
    bpy.ops.object.effector_add(type="WIND")
    wind = bpy.context.object
    wind.name = "Wind"
    wind = set_wind(wind)
    return wind


def set_wind(wind):
    default_wind = {
        "shape": "PLANE",
        "strength": 40000,
        "wind_factor": 1,
        "falloff_type": "SPHERE",
        "z_direction": "BOTH",
        "rotation_euler": [0, math.radians(90), 0],
    }
    for attr, value in default_wind.items():
        w = wind
        if attr not in ["location", "rotation_euler"]:
            w = wind.field
        setattr(w, attr, value)
    return wind


def adjust_scene(scene):
    # Set the frame rate to 5 fps (0.2 seconds per frame)
    scene.render.fps = 60
    scene.frame_end = 400
    scene.simulation_frame_end = 400
    bpy.ops.ptcache.free_bake_all()


def main():
    bpy.ops.outliner.orphans_purge()
    scene = create_scene("Main")
    bpy.context.window.scene = scene

    flag = create_flag()
    wind = create_wind()

    adjust_scene(scene)


main()
