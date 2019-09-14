python color_segment.py images/IMG_20190914_181527.jpg && rm out.jpg.2.json; python get_ocr.py out.jpg && cat out.jpg.2.json| python -mjson.tool
