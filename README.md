# Zone Counting by Class Names
This is an attempt to enhance current PeekingDuck's (v1.2.0) zone counting capabilities by introducing a breakdown of the counts of detected objects by their class names. 

Since PeekingDuck's Object Detection tools leverage on open-source models trained on MS COCO dataset containing over 80 classes including common objects like vehicles, animals, food, etc, this enhancement has a huge potential in a wide range of use cases - from traffic flow monitoring to tracking wildlife migration patterns! By segregating the number of detected objects in different zones by their class names, this detailed count allows for more targeted downstream data analysis.

Other interesting use cases like blood flow monitoring or smart refrigerators can also be explored if such models are being sufficiently trained on custom datasets, to be included into the current pool of models and class names.

Let's start counting!

## Setup project directory
This section explains the setup for a default run of the submitted solution.

1. Create and navigate to root project directory:
```
$ mkdir pd_custom_zone_count
$ cd pd_custom_zone_count
```

2. Clone repository as a sub-project directory: 
```
$ git clone https://github.com/JoyLinWQ/vehicle_zone_count
$ cd vehicle_zone_count
```

3. Create a virtual environment (python 3.6 to 3.9) and install PeekingDuck:
```
$ conda create --name my_pd python=3.9
$ conda activate my_pd
$ pip install -U peekingduck 
```
For Apple Silicon Mac users, follow Custom Install [here](https://peekingduck.readthedocs.io/en/latest/getting_started/03_custom_install.html#apple-silicon-mac-installation).

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


https://user-images.githubusercontent.com/69743962/163529401-f8dfe64b-165f-46c4-bf15-6b2bd41eca3f.mp4







## Customize to your desired use case
This section guides more adventurous users to add your own video data source with simple changes to the configuration file.

### A. Get data
You can source for your own video containing any of the class names in this [list](https://peekingduck.readthedocs.io/en/latest/resources/01a_object_detection.html?highlight=coco#object-detection-ids).

For videos obtained from YouTube, you may refer to Step 1 below.
1. Convert YouTube video to MP4 using [Online Video Converter](https://onlinevideoconverter.pro/en28/youtube-downloader-mp4).
2. Trim video to desired frames of interest.
3. Store trimmed videos in `data` folder.

Sample video:
A 10-second trimmed video is available in `vehicle_zone_count/data/sample.mp4` (Credits: 4K camera example for Traffic Monitoring (Road).mp4 - https://www.youtube.com/watch?v=jjlBnrzSGjc).

### B. Configure script
Before running, you may wish to copy and rename the folder contents in `vehicle_zone_count` to your specific use case, eg. `animal_zone_count`. Next, perform 3 simple configurations for your custom data sources in `pd_custom_zone_count/animal_zone_count/custom_config.yml`.

1. Input source:
Update the path to your input video source, relative to the sub-project folder `amimal_zone_count`.
Example:
```
- input.visual:
    source: data/animal_sample.mp4
```

2. Detect IDs:
Update `detect_ids` to include the classes you wish to 
detect.
Example:
```
- model.efficientdet:
    detect_ids: ["bird", "cat", "dog", "horse", "sheep"]
```
Refer to full list of class names and IDs provided [here](https://peekingduck.readthedocs.io/en/latest/resources/01a_object_detection.html?highlight=coco#object-detection-ids).

Also, based on <u>selected model, class names, and IDs</u> above, update your `custom_class_names` dictionary inside `src/custom_nodes/configs/draw/legend.yml`.

Example for EfficientDet model:
```
custom_class_names: {"bird": 15, "cat": 16, "dog": 17, "horse"" 18, "sheep": 19}
```

3. Zone division:
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
