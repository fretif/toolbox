#!/bin/bash

cd ~
wd=`pwd`

# 3. Créer un répertoire dédié aux logiciels & librairies que nous allons installées manuellement. 
mkdir ~/softs
mkdir ~/softs/source

# 4. Installation de setuptools
cd ~/softs/source
wget https://pypi.python.org/packages/a4/c8/9a7a47f683d54d83f648d37c3e180317f80dc126a304c45dc6663246233a/setuptools-36.5.0.zip#md5=704f500dd55f4bd0be905444f3ba892c
unzip setuptools-36.5.0.zip
cd setuptools-36.5.0
python setup.py install --user || exit 1

# 5. Installation de numpy
cd ~/softs/source
wget https://pypi.python.org/packages/c0/3a/40967d9f5675fbb097ffec170f59c2ba19fc96373e73ad47c2cae9a30aed/numpy-1.13.1.zip#md5=2c3c0f4edf720c3a7b525dacc825b9ae
unzip numpy-1.13.1.zip
cd numpy-1.13.1
python setup.py install --user || exit 1

# 6. Installation de python-dateutil 
cd ~/softs/source
wget https://pypi.python.org/packages/b4/7c/df59c89a753eb33c7c44e1dd42de0e9bc2ccdd5a4d576e0bfad97cc280cb/python-dateutil-1.5.tar.gz#md5=0dcb1de5e5cad69490a3b6ab63f0cfa5
tar xvzf python-dateutil-1.5.tar.gz
cd python-dateutil-1.5
python setup.py install --user || exit 1

# 7. Installation de pandas
cd ~/softs/source
wget https://pypi.python.org/packages/ee/aa/90c06f249cf4408fa75135ad0df7d64c09cf74c9870733862491ed5f3a50/pandas-0.20.3.tar.gz#md5=4df858f28b4bf4fa07d9fbb7f2568173
tar xvzf pandas-0.20.3.tar.gz
cd pandas-0.20.3
python setup.py install --user || exit 1

# 8. Installation de scipy
cd ~/softs/source
wget https://pypi.python.org/packages/52/67/d9ef9b5058d4a9e3f0ae641ec151790622cbeb37f157de5773358e2bf3da/scipy-0.19.1.tar.gz#md5=6b4d91b62f1926282b127194a06b72b3
cd ~/softs/source
tar xvzf scipy-0.19.1.tar.gz
cd scipy-0.19.1
python setup.py install --user || exit 1

# 9. Installation de zlib
cd ~/softs/source
wget http://zlib.net/zlib-1.2.11.tar.gz
tar xvfz zlib-1.2.11.tar.gz
cd zlib-1.2.11
./configure --prefix=$wd/softs/zlib/zlib-1.2.11 --libdir=$wd/softs/zlib/zlib-1.2.11/lib
make || exit 1
make install || exit 1

# 10. Installation de HDF5
cd ~/softs/source
wget https://support.hdfgroup.org/ftp/HDF5/current/src/hdf5-1.10.1.tar.gz
tar xvfz hdf5-1.10.1.tar.gz
cd hdf5-1.10.1
./configure --prefix=$wd/softs/hdf5/hdf5-1.10.1 --libdir=$wd/softs/hdf5/hdf5-1.10.1/lib --with-zlib=$wd/softs/zlib/zlib-1.2.11
make || exit 1
make install || exit 1

# 11. Installation de NetCDF C
cd ~/softs/source
wget ftp://ftp.unidata.ucar.edu/pub/netcdf/netcdf-4.4.1.1.tar.gz
tar xvfz netcdf-4.4.1.1.tar.gz
cd netcdf-4.4.1.1
./configure --prefix=$wd/softs/netcdf/netcdf-4.4.1.1 --libdir=$wd/softs/netcdf/netcdf-4.4.1.1/lib CPPFLAGS="-I$wd/softs/zlib/zlib-1.2.11/include -I$wd/softs/hdf5/hdf5-1.10.1/include" LDFLAGS="-L$wd/softs/hdf5/hdf5-1.10.1/lib -L$wd/softs/zlib/zlib-1.2.11/lib"
make || exit 1
make install || exit 1

# 12. Installation de NetCDF Python
cd ~/softs/source
wget https://pypi.python.org/packages/6a/37/49fd7cc21af0fb173e40de5e15f7fdd48d521429922a90347219c77b0c36/netCDF4-1.2.9.tar.gz#md5=e320491d52c42e937e6df47b56a2579c
tar xvzf netCDF4-1.2.9.tar.gz
cd  netCDF4-1.2.9
rm -f setup.cfg
cat >> setup.cfg << EOF
# Rename this file to setup.cfg to set build options.
# Follow instructions below for editing.
[options]
use_ncconfig=True
use_cython=True
[directories]
netCDF4_dir = $wd/softs/netcdf/netcdf-4.4.1.1/
HDF5_dir = $wd/softs/hdf5/hdf5-1.10.1
HDF5_libdir = $wd/softs/hdf5/hdf5-1.10.1/lib
HDF5_incdir = $wd/softs/hdf5/hdf5-1.10.1/include
szip_libdir = $wd/softs/zlib/zlib-1.2.11/lib
EOF

cat >> setup.patch << EOF
--- setup.py	2017-06-18 22:38:30.000000000 +0200
+++ ../setup_fixed.py	2017-09-12 18:46:19.821782818 +0200
@@ -271,11 +271,7 @@
     else:
         if HDF5_incdir is None:
             HDF5_incdir = os.path.join(HDF5_dir, 'include')
-        hdf5_version = check_hdf5version(HDF5_incdir)
-        if hdf5_version is None:
-            raise ValueError('did not find HDF5 headers in %s' % HDF5_incdir)
-        elif hdf5_version[1:6] < '1.8.0':
-            raise ValueError('HDF5 version >= 1.8.0 is required')
+        hdf5_version = check_hdf5version(HDF5_incdir)       
 
     if netCDF4_incdir is None and netCDF4_dir is None:
         sys.stdout.write( """
@@ -314,6 +310,7 @@
     if HDF5_libdir is not None: lib_dirs.append(HDF5_libdir)
     if netCDF4_incdir is not None: inc_dirs = [netCDF4_incdir]
     if HDF5_incdir is not None: inc_dirs.append(HDF5_incdir)
+    lib_dirs.append(szip_libdir)
 
     # add szip to link if desired.
     if szip_libdir is None and szip_dir is not None:

EOF

patch -i setup.patch setup.py
python setup.py install --user || exit 1

# 15. Installation de udunits
cd ~/softs/source
wget ftp://ftp.unidata.ucar.edu/pub/udunits/udunits-2.2.25.tar.gz
tar xvfz udunits-2.2.25.tar.gz
cd  udunits-2.2.25
./configure --prefix=$wd/softs/udunits/udunits-2.2.25 --libdir=$wd/softs/udunits/udunits-2.2.25/lib
make || exit 1
make install || exit 1

# 16. Installation de ncview
cd ~/softs/source
wget ftp://cirrus.ucsd.edu/pub/ncview/ncview-2.1.7.tar.gz
tar xvfz ncview-2.1.7.tar.gz
cd ncview-2.1.7
./configure --prefix=$wd/softs/ncview/ncview-2.1.7 -with-udunits2_incdir=$wd/softs/udunits/udunits-2.2.25/include -with-udunits2_libdir=$wd/softs/udunits/udunits-2.2.25/lib --with-nc-config=$wd/softs/netcdf/netcdf-4.4.1.1/bin/nc-config
make || exit 1
make install || exit 1

# 17. Éditer le fichier ~/.bashrc et insérer ces lignes à la fin du fichier
var=$(echo "$wd" | sed 's/\//\\\//g')
cat >> ~/.bashrc << \EOF
#netcdf-4.4.1.1
export PATH=myVarToReplace/softs/netcdf/netcdf-4.4.1.1/bin:$PATH
export LD_LIBRARY_PATH=myVarToReplace/softs/netcdf/netcdf-4.4.1.1/lib:$LD_LIBRARY_PATH

#hdf5-1.10.1
export PATH=myVarToReplace/softs/hdf5/hdf5-1.10.1/bin:$PATH
export LD_LIBRARY_PATH=myVarToReplaced/softs/hdf5/hdf5-1.10.1/lib:$LD_LIBRARY_PATH

#ncview-2.1.7
export PATH=myVarToReplace/softs/ncview/ncview-2.1.7/bin:$PATH
EOF

sed -i -e "s/myVarToReplace/$var/g" ~/.bashrc

# 18. Installation de ‘Pycharm’ version Community
cd ~/softs/source
wget https://download.jetbrains.com/python/pycharm-community-2017.2.3.tar.gz
tar xvzf pycharm-community-2017.2.3.tar.gz -C../
cd ../pycharm-community-2017.2.3/bin
./pycharm.sh

