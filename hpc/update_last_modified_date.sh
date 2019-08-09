#!/bin/bash

baseDir=$1
find $baseDir -type f -exec touch {} \;
