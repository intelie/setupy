#!/bin/bash

covered_files="test_setupy.py setupy.py setupy"

rm -rf coverage_html
coverage run $covered_files
coverage report $covered_files
coverage html -d coverage_html $covered_files
