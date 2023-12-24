#!/bin/bash
cut -f4 -d" " temp-history | sort -n | head -1
