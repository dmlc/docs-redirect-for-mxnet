# docs-redirect-for-mxnet

Collection of rst files to re-direct all webpages from mxnet.readthedocs.io to mxnet.io.

## Running for MXNet

```
python builder/generaterst.py
```

## How to run generally

First, generate your filelist.  Which involves building the docs for 
your project, and then going into `_build/html` directory and
getting the file list.

```
cd _build/html
find . -type f > /tmp/filelist.txt
python builder/generaterst.py --filelist /tmp/filelist.txt
```

## Resetting the git repo

```
rm -rf docs
git checkout docs
```
# Credits

Idea in this repo is mainly borrowed from https://github.com/leopd/rtdtest