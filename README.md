# Zone Counting by Class Names
This is an attempt to enhance current [PeekingDuck's (v1.2.0)](https://github.com/aimakerspace/PeekingDuck) [zone counting](https://peekingduck.readthedocs.io/en/latest/use_cases/zone_counting.html) and [object detection (over time)](https://peekingduck.readthedocs.io/en/latest/use_cases/object_counting_over_time.html) capabilities by introducing a breakdown of the counts per frame of detected objects by their class names. 

Since PeekingDuck's Object Detection tools leverage on open-source models trained on MS COCO dataset containing over 80 classes including common objects like vehicles, animals, food, etc, this enhancement has a huge potential in a wide range of use cases - from traffic flow monitoring to tracking wildlife migration patterns! By segregating the number of detected objects in different zones by their class names, this detailed near real-time (30 FPS) count allows for more targeted downstream data analysis.

Other interesting use cases like blood flow monitoring or smart refrigerators can also be explored if such models are being sufficiently trained on custom datasets, to be included into the current pool of models and class names.

Let's start counting!

## Setup project directory
This section explains the setup for a default run of the submitted solution detecting traffic vehicles (eg. car, motorcycle, truck, bus). A 10-second trimmed sample video is available in `vehicle_zone_count/data/sample_traffic.mp4` (Credits: 4K camera example for Traffic Monitoring (Road).mp4 - https://www.youtube.com/watch?v=jjlBnrzSGjc).

1. Create and navigate to root project directory:
```
$ mkdir pd_custom_zone_count
$ cd pd_custom_zone_count
```

2. Clone repository as a sub-project directory: 
```
$ git clone https://github.com/JoyLinWQ/vehicle_zone_count.git
$ cd vehicle_zone_count
```

3. Create a virtual environment (python 3.6 to 3.9) and install PeekingDuck. For Apple Silicon Mac users, follow Custom Install [here](https://peekingduck.readthedocs.io/en/latest/getting_started/03_custom_install.html#apple-silicon-mac-installation).
```
$ conda create --name my_pd python=3.9
$ conda activate my_pd
$ pip install -U peekingduck 
```

4. Locate the original file and replace with custom file below:
    - Original file:
        ```
        "C:\Users\<your_name>\anaconda3\envs\my_pd\Lib\site-packages\peekingduck\pipeline\nodes\draw\utils\legend.py"
        ```

    - Custom file:
        ```
        "...\pd_custom_zone_count\vehicle_zone_count\custom_env\legend.py"
        ```

5. Navigate to project directory and run:
```
$ cd vehicle_zone_count
$ peekingduck run --config_path="custom_config.yml"
```

6. Watch the zone counting proceed in a new popup window with output below, which will be automatically saved to `"...\pd_custom_zone_count\vehicle_zone_count\PeekingDuck\data\output\XXX.mp4"` when the run is completed.


![sample_output](https://github.com/JoyLinWQ/vehicle_zone_count/blob/main/PeekingDuck/data/output/sample/sample_vehicle.gif)

Each detected object is shown in a bounding box with its class name. The number above each box represents a unique instance of a detected object.

The counts of detected objects by their class names in each zone per video frame is reflected in the legend.





## Customize to your desired use case
This section guides more adventurous users to add your own video data source with simple changes to the configuration file.

### A. Get data
You can source for your own video containing any of the class names in this [list](https://peekingduck.readthedocs.io/en/latest/resources/01a_object_detection.html?highlight=coco#object-detection-ids).

For videos obtained from YouTube, you may refer to Step 1 below.
1. Convert YouTube video to MP4 using [Online Video Converter](https://onlinevideoconverter.pro/en28/youtube-downloader-mp4).
2. Trim video to desired frames of interest.
3. Store trimmed videos in `data` folder.

Sample video:
A 13-second trimmed video is available in 
`vehicle_zone_count/data/sample_animal.mp4` (Credits: Wildlife Video 2021 | Best Wildlife Compilation With Natural Sound | Wild Animals Collections Video -
https://www.youtube.com/watch?v=G2usoiFYlho).

### B. Configure script
Before running, you may wish to copy and rename the folder contents in `vehicle_zone_count` to your specific use case, eg. `animal_zone_count`.

Next, perform 3 simple configurations for your custom data sources in `pd_custom_zone_count/animal_zone_count/custom_config.yml`.

1. **Input source**:
Update the path to your input video source, relative to the sub-project folder `amimal_zone_count`.
Example:
```
- input.visual:
    source: data/sample_animal.mp4
```

2. **Detect IDs**:
Update `detect_ids` to include the classes you wish to 
detect.
Example:
```
- model.efficientdet:
    detect_ids: ["bird", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe"]
```
Refer to full list of class names and IDs provided [here](https://peekingduck.readthedocs.io/en/latest/resources/01a_object_detection.html?highlight=coco#object-detection-ids).

Also, based on <u>selected model, class names, and IDs</u> above, update your `custom_class_names` dictionary inside `src/custom_nodes/configs/draw/legend.yml`.

Example for EfficientDet model:
```
custom_class_names: {"bird": 15, "horse": 18, "sheep": 19, "cow": 20, "elephant": 21, "bear": 22, "zebra": 23, "giraffe": 24}
```

3. **Zone division**:
Update the scaled coordinates of bounding boxes to cover the static zone areas you are interested in. Details can be found [here](https://peekingduck.readthedocs.io/en/latest/use_cases/zone_counting.html).
Example:
```
- dabble.zone_count:
    zones: [
        [[0, 0], [0.55, 0], [0.55, 1], [0, 1]],
        [[0.55, 0], [1, 0], [1, 1], [0.55, 1]]
    ]
```

4. Navigate to custom project directory and run:
```
$ cd animal_zone_count
$ peekingduck run --config_path="custom_config.yml"
```

# Author
Joy Lin [Email](jlwq07@hotmail.com) | [GitHub Repository Link](https://github.com/JoyLinWQ/vehicle_zone_count)

Submitted: April 2022

# Acknowledgements
PeekingDuck (v1.2.0) developed by AI Singapore Computer Vision Hub

[GitHub](https://github.com/aimakerspace/PeekingDuck) | [Documentation](https://peekingduck.readthedocs.io/en/latest/)
