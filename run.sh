python color_segment.py $1 && rm out.jpg.2.json; python get_ocr.py out.jpg && cat out.jpg.2.json| python -mjson.tool
