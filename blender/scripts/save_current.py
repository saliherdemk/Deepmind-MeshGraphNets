import json
import os
import bmesh
import bpy


def get_vertices_and_cells_frame_by_frame(end_frame):
    data = {}
    cells = None
    flag_obj = bpy.data.objects.get("Flag")
    for frame in range(1, end_frame + 1):
        bpy.context.scene.frame_current = frame
        dg = bpy.context.evaluated_depsgraph_get()

        bm = bmesh.new()
        bm.from_object(flag_obj, dg)
        if frame == 1:
            cells = tuple(
                tuple(loop.vert.index for loop in face.loops) for face in bm.faces
            )

        vert_tuples = tuple((vert.co.x, vert.co.y, vert.co.z) for vert in bm.verts)

        data[f"Frame-{frame}"] = vert_tuples

        bm.free()

    return data, cells


def get_wind():
    wind = bpy.data.objects["Wind"]

    physics = wind.field

    wind_data = {
        "strength": physics.strength,
        "shape": physics.shape,
        "wind_factor": physics.wind_factor,
        "falloff_type": physics.falloff_type,
        "z_direction": physics.z_direction,
        "rotation_euler": tuple(wind.rotation_euler),
    }
    return wind_data


def play_and_combine_data(frame_count):
    data, cells = get_vertices_and_cells_frame_by_frame(frame_count)
    data = {"cells": cells, "mesh_pos": data, "wind": get_wind()}
    return data


def save_to_file(file, data):
    with open(file, "w+", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def main(file, frame_count):
    final_data = play_and_combine_data(frame_count)
    save_to_file(file, final_data)


file_path = os.path.expanduser("/L-HDD/")
filename = "current.json"
frame_count = 100

main(file_path + filename, frame_count)
