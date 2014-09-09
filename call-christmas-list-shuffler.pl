#!/usr/bin/perl

use strict;
use warnings;

system("python", "generate-christmas-list.py") == 0 or die "Python script returned error $?";
