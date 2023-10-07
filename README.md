# python_diploma_generator
Generate PDF diplomas using images and a CSV file


## Install
```
pip install diploma_generator
```

# Usage as module
Params:
- background_image_path: path to the background image
- x: x position of the name in cm
- y: y position of the name in cm
- w: width of the name in cm
- h: height of the name in cm
- font_size: font size of the name
- font_path: path to the font
```
from diploma_generator import DiplomaGenerator
diploma_generator = DiplomaGenerator(
        background_image_path,
        x, y,
        w, h,
        font_size, font_path
    )
diploma_generator.add_diploma_page(person_name, Optional[qr_code_text])

diploma_generator.save("output.pdf")
```

# Usage as CLI single diploma
```
diploma_generator \
    --background_image_path <path> \
    -n <name> \
    -xy "1,11" \
    -wh  "24,1" \
    -o "output.pdf" 
```

# Usage as CLI multiple diplomas
```
diploma_generator \
    --background_image_path <path> \
    --csv <path> \
    -xy "1,11" \
    -wh  "24,1" \
    -o "output.pdf" 
```

Example CSV (name, qr, output)
```
Nombre 1,Para el QR,diploma1
Nombre 2,,diploma.pdf
Nombre 3,,
```