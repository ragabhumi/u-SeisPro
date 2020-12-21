import os

os.chdir('../hypodd')
os.system('../aux/HypoDD/ph2dt ph2dt.inp')
os.system('../aux/HypoDD/hypoDD hypoDD.inp')