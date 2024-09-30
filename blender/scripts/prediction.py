import json
import math
import os
import bpy


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

    flag.name = "P-Flag"

    return flag


def prepare_scene(scene_name):
    new_scene = bpy.data.scenes.new(scene_name)
    bpy.context.window.scene = new_scene
    flag = create_flag()

    return flag, new_scene


def add_keyframes(scene, flag, anim_data):
    vertex_data_by_frame = anim_data

    frame_end = 1

    for frame_num, vertices in enumerate(vertex_data_by_frame):
        for i, v in enumerate(vertices):
            vertex = flag.data.vertices[i]
            vertex.co = v
            vertex.keyframe_insert(data_path="co", frame=frame_num + 1)
        frame_end = frame_num

    scene.simulation_frame_start = 1
    scene.frame_start = 1
    scene.simulation_frame_end = frame_end
    scene.frame_end = frame_end


def load_data(directory, filename):
    with open(os.path.join(directory, filename), "r") as f:
        data = json.load(f)
    return data


def main(directory, filename, scene_name):
    bpy.ops.outliner.orphans_purge()
    data = load_data(directory, filename)
    flag, scene = prepare_scene(scene_name)
    add_keyframes(scene, flag, data["pred_pos"])


directory = os.path.expanduser("/L-HDD/rollouts/")
filename = "rollout0.json"
scene_name = "Pred-Scene"

main(directory, filename, scene_name)
