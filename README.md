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
Description
Folder          Number of           Time           Occlusions          Presence of           Weather         Growth-stage            Rough      Folder
                sequences           span                               Weeds                 variability     variability             terrain    size (GB)
Cornfield1      80                  4 months       ✓                   ✓                     ✓               ✓                       ✓          584
Cornfield2      17                  3 months       ✓                   ✓                     ✓               ✓                       ✓          171
Cornfield3      2                   1 week         x                   x                     x               x                       ✓          28
Cornfield4      4                   1 months       ✓                   x                     x               ✓                       ✓          37
Sorghum         2                   3 weeks        ✓                   ✓                     x               x                       ✓          9
Soybean         12                  2 weeks        ✓                   ✓                     ✓               x                       ✓          79
Sweet Corn      4                   1 weeks        ✓                   ✓                     x               x                       ✓          49
Others          14                  3 months       x                   x                     ✓               ✓                       ✓          103
```

ZED SDK ([reference](https://www.stereolabs.com/docs/installation/))
