import argparse
from pathlib import Path
import tensorflow as tf
from multiprocessing import Process, Queue, cpu_count
import numpy as np
import json


def process_json_data(path):
    with open(path, "r") as fp:
        json_data = json.load(fp)

    wind_strength = json_data["wind"]["strength"]
    wind_strength = (wind_strength - 5000) / (100000 - 5000)
    wind_direction = json_data["wind"]["rotation_euler"]
    wind_direction = wind_direction / np.linalg.norm(wind_direction)
    wind_velocity = (wind_strength * wind_direction).tolist()

    wind_data = [json_data["wind"]["strength"]] + json_data["wind"]["rotation_euler"]

    world_pos = []
    for frame in json_data["world_pos"]:
        frame_pos = [pos for pos in json_data["world_pos"][frame]]
        world_pos.append(frame_pos)

    cells = [json_data["cells"]]
    mesh_pos = [json_data["mesh_pos"]]
    node_type = [json_data["node_type"]]
    wind_training = [wind_velocity for _ in range(len(world_pos))]
    wind = [wind_data for _ in range(len(world_pos))]

    return (
        tf.constant(cells),
        tf.constant(mesh_pos),
        tf.constant(node_type),
        tf.constant(world_pos),
        tf.constant(wind_training),
        tf.constant(wind),
    )


def byte_feature(value):
    value = (
        value.numpy() if tf.executing_eagerly() else value.eval(session=tf.Session())
    )
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value.tobytes()]))


def worker(data_queue, result_queue, worker_id):
    while not data_queue.empty():
        path = data_queue.get(block=True)
        print(f"Worker {worker_id}: Processing {path}")
        try:
            cells, mesh_pos, node_type, world_pos, wind_training, wind = (
                process_json_data(path)
            )
            shapes = {
                "cells": cells.shape.as_list(),
                "mesh_pos": mesh_pos.shape.as_list(),
                "node_type": node_type.shape.as_list(),
                "world_pos": world_pos.shape.as_list(),
                "wind_training": wind_training.shape.as_list(),
                "wind": wind.shape.as_list(),
            }

            features = {
                "cells": byte_feature(tf.reshape(cells, [-1])),
                "mesh_pos": byte_feature(tf.reshape(mesh_pos, [-1])),
                "node_type": byte_feature(tf.reshape(node_type, [-1])),
                "world_pos": byte_feature(tf.reshape(world_pos, [-1])),
                "wind_training": byte_feature(tf.reshape(wind_training, [-1])),
                "wind": byte_feature(tf.reshape(wind, [-1])),
            }

            proto = tf.train.Example(features=tf.train.Features(feature=features))
            tf_data = proto.SerializeToString()
            result_queue.put((tf_data, shapes, path))
        except Exception as e:
            print(f"Worker {worker_id}: Error processing {path}: {e}")


def tfrecord_write(result_queue, output_file, length):
    processed = 0
    shapes_prev = {}

    with tf.io.TFRecordWriter(str(output_file)) as writer:
        while processed < length:
            tf_data, shapes, path = result_queue.get(block=True)
            writer.write(tf_data)

            if processed == 0:
                shapes_prev = shapes
            else:
                assert (
                    shapes_prev == shapes
                ), f"Error: tensor shapes from data file {path} don't match."

            processed += 1
            print(f"Processed {processed}/{length} data files.")

    features = {
        "cells": {
            "type": "static",
            "shape": shapes_prev["cells"],
            "dtype": "int32",
            "for_sim": False,
        },
        "mesh_pos": {
            "type": "static",
            "shape": shapes_prev["mesh_pos"],
            "dtype": "float32",
            "for_sim": False,
        },
        "node_type": {
            "type": "static",
            "shape": shapes_prev["node_type"],
            "dtype": "int32",
            "for_sim": False,
        },
        "world_pos": {
            "type": "dynamic",
            "shape": shapes_prev["world_pos"],
            "dtype": "float32",
            "for_sim": False,
        },
        "wind_training": {
            "type": "dynamic",
            "shape": shapes_prev["wind_training"],
            "dtype": "float32",
            "for_sim": False,
        },
        "wind": {
            "type": "dynamic",
            "shape": shapes_prev["wind"],
            "dtype": "float32",
            "for_sim": True,
        },
    }

    meta = {
        "simulator": "blender",
        "features": features,
        "field_names": list(features.keys()),
        "trajectory_length": shapes_prev["world_pos"][0],
    }

    parent_folder = Path(output_file).parent
    with open(parent_folder / "meta.json", "w") as fp:
        json.dump(meta, fp, indent=4)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Process JSON data and write to TFRecord."
    )
    parser.add_argument(
        "--data_dir",
        type=str,
        required=True,
        help="Path to the data directory containing JSON files.",
    )
    parser.add_argument(
        "--output_file",
        type=str,
        required=True,
        help="Path to the output TFRecord file.",
    )

    args = parser.parse_args()

    data_path = Path(args.data_dir)
    output_path = Path(args.output_file)
    data_files = list(data_path.glob("*.json"))

    data_queue = Queue()
    for path in data_files:
        data_queue.put(path)

    result_queue = Queue()

    num_workers = max(1, cpu_count() // 2)
    processes = [
        Process(target=worker, args=(data_queue, result_queue, i))
        for i in range(num_workers)
    ]
    writer_process = Process(
        target=tfrecord_write, args=(result_queue, output_path, len(data_files))
    )

    writer_process.start()
    for p in processes:
        p.start()

    for p in processes:
        p.join()
    writer_process.join()
