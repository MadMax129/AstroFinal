# ASTO170 Final Project
> Simulate and observe orbital machenics

# Run
> Once followed steps in build
```
cd src
python main.py
```

| Key | Function |
|-----|----------|
| a   | zoom out |
| d   | zoom in  |
| o   | slow down time |
| p   | speed up time |

Drag and click to move camera view.

Click on preset buttons to view simuation.

## Adding more
To simualate something new go into "presets.py"

In the function "get_presets()" add a Preset() into the list, it will automatically be update on the screen. Following the documentation notes in class Preset to understand units and strucutre.

## Build
```bash
# Used Python3.12
python -m venv ./env
source ./env/bin/activate
pip install -r requirements.txt
```
