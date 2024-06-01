#!/bin/bash
mkdir cornfield3
cd cornfield3
mkdir 20220711_cornfield3
cd 20220711_cornfield3
wget -O ts_2022_07_11_12h23m16s_field3_three_rows.bag https://uofi.box.com/shared/static/z11w4qr5bpt49xjguahwftardcb59blm.bag
wget -O ts_2022_07_11_12h23m16s_field3_three_rows.svo https://uofi.box.com/shared/static/vn4xsx7zmjebxf00nhgwo8ynbzcxjom9.svo
cd ..
mkdir 20220714_cornfield3
cd 20220714_cornfield3
wget -O ts_2022_07_14_12h01m08s_three_rows.bag https://uofi.box.com/shared/static/2kul7w6uqyrkevn9o9puvo36itjy6aco.bag
wget -O ts_2022_07_14_12h01m08s_three_rows.svo https://uofi.box.com/shared/static/a27nlvg7qjc4b5nj1rxjaca9zzqt99ob.svo

cd ..
cd ..
