# SLAM-dataset
This dataset is intended for the evaluation of visual-based localization and mapping systems in agriculture. It includes stereo
images, IMU, GPS, and wheel encoder measurements. It was collected from a ground robot in the Illinois Autonomous Farm at the
University of Illinois at Urbana-Champaign. The collection campaign took place during the Summer of 2022. Different data sequences
were collected twice per week in corn fields, and less often in soybean and sorghum. This dataset exhibit high variability in terms of
weather conditions and growth stages. It contains challenging features like occlusions, illumination variations, weeds, dynamic objects, and rough terrain.

<div align="center">
  <a href="figures/robot.png">
    <img src="figures/robot.png" width="400" alt="Terrasentia-robot">
  </a>
</div>

![Alt Terrasentia Robot](figures/robot.png | width=500)

```
I0512 21:05:55.136549 21233 Pipeline.cpp:449] Statistics
-----------                                  #	Log Hz	{avg     +- std    }	[min,max]
Data Provider [ms]                      	    0	
Display [ms]                            	  146	36.5421	{8.28082 +- 2.40370}	[3,213]
VioBackend [ms]                         	   73	19.4868	{15.2192 +- 9.75712}	[0,39]
VioFrontend Frame Rate [ms]             	  222	59.3276	{5.77027 +- 1.51571}	[3,12]
VioFrontend Keyframe Rate [ms]          	   73	19.6235	{31.4110 +- 7.29504}	[24,62]
VioFrontend [ms]                        	  295	77.9727	{12.1593 +- 10.7279}	[3,62]
Visualizer [ms]                         	   73	19.4639	{3.82192 +- 0.805234}	[2,7]
backend_input_queue Size [#]            	   73	18.3878	{1.00000 +- 0.00000}	[1,1]
data_provider_left_frame_queue Size (#) 	  663	165.202	{182.265 +- 14.5110}	[1,359]
data_provider_right_frame_queue Size (#)	  663	165.084	{182.029 +- 14.5150}	[1,359]
display_input_queue Size [#]            	  146	36.5428	{1.68493 +- 0.00000}	[1,12]
stereo_frontend_input_queue Size [#]    	  301	75.3519	{4.84718 +- 0.219043}	[1,5]
visualizer_backend_queue Size [#]       	   73	18.3208	{1.00000 +- 0.00000}	[1,1]
visualizer_frontend_queue Size [#]      	  295	73.9984	{4.21695 +- 1.24381}	[1,7]
```

ZED SDK ([reference](https://www.stereolabs.com/docs/installation/))
