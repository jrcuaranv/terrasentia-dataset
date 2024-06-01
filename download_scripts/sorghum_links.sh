#!/bin/bash
mkdir sorghum
cd sorghum
mkdir 20220815_sorghum
cd 20220815_sorghum
wget -O ts_2022_08_15_12h06m26s_one_row.bag https://uofi.box.com/shared/static/k0kbp6jkirupdqmc0mu7p9v7zvxhe7mv.bag
wget -O ts_2022_08_15_12h06m26s_one_row.svo https://uofi.box.com/shared/static/s3d0b27q97lku2oc54rx5ck9faqwox2n.svo
cd ..
mkdir 20220906_sorghum
cd 20220906_sorghum
wget -O ts_2022_09_06_13h14m41s_one_random_sorghum.bag https://uofi.box.com/shared/static/y3u1l7mqj9irtlq9ll7c4jxhl4fpeeko.bag
wget -O ts_2022_09_06_13h14m41s_one_random_sorghum.svo https://uofi.box.com/shared/static/xymg6vukivq9xh44x1c26lqd3gw3twej.svo
cd ..
cd ..












