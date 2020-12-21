#!/bin/bash

eq_data=../hypodd/hypoDD.reloc
sta=../hypodd/station.dat
topo=../gmt/songa.grd
lon1=127.4985
lon2=127.7549
lat1=-0.8319
lat2=-0.5565
R=$lon1/$lon2/$lat1/$lat2
J=M17

gmt begin ../map/plot png
    gmt grdimage -R$R -J$J $topo -Cetopo1 -I+d -Ba0.1 -BWeSn
    awk '{print $3,$2,$4}' $eq_data | gmt plot -Sc0.2 -Gred -W0.4
    awk '{print $3,$2}' $sta | gmt plot -Si0.4 -Gyellow -W0.3
    awk '{print $3,$2,$1}' $sta | gmt text -F+f10,black -D0.3/0.3
gmt end

gmt begin ../map/side_ns png
    gmt project -C"$(awk "BEGIN {print ($lon1+$lon2)/2}")"/$lat1 -E"$(awk "BEGIN {print ($lon1+$lon2)/2}")"/$lat2 -Q -G0.01 > ../map/track_ns
    gmt grdtrack ../map/track_ns -G$topo > ../map/tracked_ns
    awk '{gsub(/\NaN/,"0",$4)} 1' ../map/tracked_ns | awk '{print $3, $4/1000}' | gmt plot -JX19/17 -R0/24.32/-25/3 -W1 -Bx5+l"Range (Km)" -By5+l"Depth (Km)" -BWeSn+t"Relocated"
    awk '{print $3, $2, $4*-1}' $eq_data| gmt project -Q -C"$(awk "BEGIN {print ($lon1+$lon2)/2}")"/$lat1 -E"$(awk "BEGIN {print ($lon1+$lon2)/2}")"/$lat2 -Fpz | gmt plot -Sc0.2 -W0.3 -Gred

    rm ../map/track_ns ../map/tracked_ns
gmt end

gmt begin ../map/side_ew png
    gmt project -C$lon1/"$(awk "BEGIN {print ($lat1+$lat2)/2}")" -E$lon2/"$(awk "BEGIN {print ($lat1+$lat2)/2}")" -Q -G0.01 > ../map/track_ew
    gmt grdtrack ../map/track_ew -G$topo > ../map/tracked_ew
    awk '{gsub(/\NaN/,"0",$4)} 1' ../map/tracked_ns | awk '{print $3, $4/1000}' | gmt plot -JX19/17 -R0/24.32/-25/3 -W1 -Bx5+l"Range (Km)" -By5+l"Depth (Km)" -BWeSn+t"Relocated"
    awk '{print $3, $2, $4*-1}' $eq_data| gmt project -Q -C$lon1/"$(awk "BEGIN {print ($lat1+$lat2)/2}")" -E$lon2/"$(awk "BEGIN {print ($lat1+$lat2)/2}")" -Fpz | gmt plot -Sc0.2 -W0.3 -Gred

    rm ../map/track_ew ../map/tracked_ew
gmt end