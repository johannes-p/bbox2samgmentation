<a name="readme-top"></a>

<br />
<div align="center">
  <a href="https://github.com/johannes-p/bbox2samgmentation">
    <img src="logo.png" alt="Logo" width="160" height="160">
  </a>

<h3 align="center">bbox2SAMgmentation</h3>

  <p align="center">
    Convert your boundingbox annotations to instance segmentation annotations.
    <br />
    <br />
    <a href="https://github.com/johannes-p/bbox2samgmentation/issues">Report Bug</a>
    ·
    <a href="https://github.com/johannes-p/bbox2samgmentation/issues">Request Feature</a>
  </p>
</div>



<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
  </ol>
</details>




## Getting Started

### Prerequisites

* [Python](https://www.python.org/downloads/)
* [Segment Anything Model](https://github.com/facebookresearch/segment-anything#model-checkpoints)
    * the program defaults to "vit_b", if you would prefer to use a different model size that works as well

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/johannes-p/bbox2samgmentation.git
   ```
2. Setup the virtual environment
   ```sh
   cd bbox2samgmentation
   python -m venv venv
   ```
3. Activate the virtual environment
    - on Windows:
        ```sh
        .\venv\Scripts\activate
        ```
    - on Linux/macOS:
        ```sh
        source venv/bin/activate
        ```
4. Install [Pytorch](https://pytorch.org/get-started/locally/) following the instructions on the page

5. Install the remaining dependencies
   ```sh
   pip install -r requirements.txt
   ```
6. Put the Segment Anything Model into the models folder.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



## Usage

> Make sure that the venv is active. If it isn't, activate it as described in the installation instructions.

After putting the images and annotations in the corresponding folders you can run the program in the default configuration using:
```sh
python main.py --class_name <name_of_the_annotated_object>
```

After completion, an ``annotations.json`` file is located in the root directory, and the generated mask images are located in the ``masks`` folder as well, should they be needed.
<br>
<br>
⚠ Make sure to try out the ```--use_bbox``` flag in case only parts of an object are detected. ⚠
<br>
<br>

If you want to use a model different from vit_b just specify the path when calling the program:
```sh
python main.py -m <path/to/the/pth-file> ...
```

To further change the default behaviour checkout the options using:
    ```python main.py --help```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



## Roadmap

- [ ] Input annotation format support
    - [X] PascalVOC
    - [ ] COCO
    - [ ] CSV
    - [ ] ... ?
- [ ] Multiclass support



<p align="right">(<a href="#readme-top">back to top</a>)</p>
