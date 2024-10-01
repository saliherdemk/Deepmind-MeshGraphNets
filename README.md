# Learning Mesh-Based Simulation with Graph Networks

This repository provides a specialized version of Learning Mesh-Based Simulation with Graph Networks ([paper](https://arxiv.org/abs/2010.03409)-[code](https://github.com/google-deepmind/deepmind-research/tree/master/meshgraphnets)), adapted for a custom dataset in Blender. For additional details, a Turkish thesis on this project is also available [here](https://drive.google.com/file/d/1qjSybZ8LOF4OpcJJqkxDv0ttmlxmKuch/view?usp=sharing).

    @inproceedings{pfaff2021learning,
      title={Learning Mesh-Based Simulation with Graph Networks},
      author={Tobias Pfaff and
              Meire Fortunato and
              Alvaro Sanchez-Gonzalez and
              Peter W. Battaglia},
      booktitle={International Conference on Learning Representations},
      year={2021}
    }

## Setup

Some dependencies have been updated, requiring Python 3.7.10. Change the local Python version with [pyenv](https://github.com/pyenv/pyenv) to the value inside the .python-version file. Once you have done this, prepare the environment and install the dependencies.

```
python -m venv .venv
source .venv/bin/activate  # For Linux
pip install -r requirements.txt
```

If you have new generation card, you have to use [nvidia-tensorflow](https://github.com/NVIDIA/tensorflow) in order to train with gpu.

## Preparing Dataset
You can either download the dataset [here](https://www.kaggle.com/datasets/saliherdemkaymak/flag-dataset) or generate it using the provided scripts in the Blender folder.
Open the `Flag-sim.blend` file and generate data using the `Generate Data` script. Once you have created the JSON files, convert them to TFRecord format with `json_to_tfrecord.py`.
```
python -m json_to_tfrecord.py --data_dir=jsonDataTrain/ --output_dir=dataset/train.tfrecord
```

After this process, you should have `train.tfrecord` (or test.tfrecord-eval.tfrecord) and `meta.json` files.

## Running the model

May need `sudo` for creating files.

The samples are trivial; they are just meant to give an idea of the file structure and format.

Train a model:
```
python -m run_model --mode=train --checkpoint_dir=samples/sampleChk/ --dataset_dir=samples/sampleDataset/ --wind=true 
```

Generate some trajectory rollouts:

```
python -m run_model --mode=eval --checkpoint_dir=samples/sampleChk/ --dataset_dir=samples/sampleDataset/ --wind=true --rollout_path=rollouts/rollout.json --num_rollouts=2
```

After you have rollouts, you can either simulate with matplotlib or in a Blender scene.

Plot with `matplotlib`:

```
python -m plot_cloth --rollout_path=rollouts/rollout0.json
```
Simulate in `blender`: In the prediction script, change the directory and filename, then execute the script. This will create a new scene that contains a P-Flag. You can now play the animation. 

## CHECKPOINTS
You can access model weights from [here](https://drive.google.com/drive/u/0/folders/1eu2GXMEJ-R_ikhRkLZ436r-sHNfWUerV). Note that those were not trained using the dataset shared on Kaggle.


## TODOS
- Convert code to pytorch
- Translate thesis into English


