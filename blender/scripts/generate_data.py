import json
import math
import os
import random
import pandas as pd
import bmesh
import bpy
import pyarrow as pa
import pyarrow.parquet as pq
import csv

wind = bpy.data.objects["Wind"]


def set_wind(strength, rotation_euler):
    wind.field.strength = strength
    wind.rotation_euler = rotation_euler


def generate_random_wind():
    random.seed(random.uniform(0, 100))
    random_strength = random.uniform(5000, 100000)
    random_rotation = [random.uniform(0, 2 * math.pi) for _ in range(3)]

    return random_strength, random_rotation


def get_vertices_and_cells_frame_by_frame(end_frame):
    data = {}
    cells = None
    node_type = []
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

            most_left_vertex_index = min(bm.verts, key=lambda vert: vert.co.x).index

            for vert in bm.verts:
                node_type.append([1] if vert.index == most_left_vertex_index else [0])

        vert_tuples = tuple((vert.co.x, vert.co.y, vert.co.z) for vert in bm.verts)

        data[f"Frame-{frame}"] = vert_tuples

        bm.free()

    return data, cells, node_type


def get_wind():
    physics = wind.field

    wind_data = {
        "strength": physics.strength,
        "rotation_euler": tuple(wind.rotation_euler),
    }
    return wind_data


def play_and_combine_data(frame_count):
    random_s, random_r = generate_random_wind()
    set_wind(random_s, random_r)
    data, cells, node_type = get_vertices_and_cells_frame_by_frame(frame_count)
    data = {
        "cells": cells,
        "world_pos": data,
        "mesh_pos": [[pos[0], pos[1]] for pos in data["Frame-1"]],
        "node_type": node_type,
        "wind": get_wind(),
    }
    return data


def save_to_file(save_directory, filename, data, type):
    if type == "json":
        with open(
            os.path.join(save_directory, filename + ".json"), "w+", encoding="utf-8"
        ) as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    elif type == "csv":
        flat_data = pd.json_normalize(data)
        flat_data.to_csv(os.path.join(save_directory, filename + ".csv"), index=False)
    elif type == "parquet":
        flat_data = pd.json_normalize(data)
        flat_data.to_parquet(os.path.join(save_directory, filename + ".parquet"))


def generate_n_file(save_path, n, frame_count):
    for i in range(n):
        final_data = play_and_combine_data(frame_count)
        save_to_file(save_path, str(i), final_data, type="json")


def main(scene_name, save_directory, file_count, frame_count):
    bpy.context.window.scene = bpy.data.scenes[scene_name]
    generate_n_file(save_directory, file_count, frame_count)


scene_name = "Main"  # Must be initialized first with initialize.py
save_directory = os.path.expanduser("/L-HDD/jsonData")
file_count = 1000
frame_count = 250

main(scene_name, save_directory, file_count, frame_count)
