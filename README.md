# Documentation
This is the documentation that will help others to run our software on their own machine.
1. The first step is to make sure that you have Python 3.10 installed. The version of Python must be 3.10 since the Pytorch version used in our system is compatible with Python 3.10.
2. The next step is to download all of the python libraries that are being used by the project. To install all the libraries please run
```pip install -r requirements.txt```
3. After that to start the desktop application please run the following command in the terminal.
```python3 liveVideoAppV2.py```
4. This will take a few minutes and if it does not open just press Ctrl + c and then run the above command again.
5. The Start Capture button will start capturing the video feed and send it to the AI processing pipeline.
6. The Pause Capture button will pause the video capture process but still continue the AI processing.
7. Now the Dehazing model is very heavy so if you only want to test or use the Detection Processing just click on the Only Detection button. This will make it so that the video feed is only processed by the Detection model and the Dehazing model will be skipped.
8. Now if you have low-end hardware you can lower the resolution by clicking on the values in the Select Resolution dropdown. Also you can change the downscaling option to performance or balanced to make the Dehazing process faster. 
9. Note by doing step 9 there will be a drop in quality but not that much.
10. The following image is a path structure of the system. The Dehazing_Models folder contains all the code related to the Dehazing model and the Detection_Models folder contains everything related to the Detection model. The Image_Processing folder contains everything related to the Pre and Post Processing Code. The liveVideoPipeline file contains the code for the pipeline. 

