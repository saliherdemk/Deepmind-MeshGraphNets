# Learning Mesh-Based Simulation with Graph Networks

This repository provides a specialized version of Learning Mesh-Based Simulation with Graph Networks ([paper](https://arxiv.org/abs/2010.03409),[code](https://github.com/google-deepmind/deepmind-research/tree/master/meshgraphnets)), adapted for a custom dataset in Blender. You can either download the dataset [here](https://www.kaggle.com/datasets/saliherdemkaymak/flagdata) or generate it using the provided scripts in the Blender folder. For additional details, a Turkish thesis on this project is also available [here](https://drive.google.com/drive/u/0/starred).

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

## Running the model

May need `sudo` for creating files.
Train a model:
```
   python -m run_model --mode=train --checkpoint_dir=samples/sampleChk/ --dataset_dir=samples/sampleDataset/ --wind=true 
```

Generate some trajectory rollouts:

    
    python -m run_model --mode=eval --checkpoint_dir=samples/sampleChk/ --dataset_dir=samples/sampleDataset/ --wind=true --rollout_path=rollouts/rollout.json --num_rollouts=2


Plot a trajectory:

    python -m plot_cloth --rollout_path=rollouts/rollout0.json


