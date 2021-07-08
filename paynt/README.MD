
# paynt

paynt draw the image specified from the command line in paint, note that the colors is limited to the color palette in paint desktop app. RGBA and transaparancy is ignored. This is just a FUN project to kill boredom, and a mini proof of concept for a bigger project in mind 😉. 

## Setup

The project uses Pillow to read the image array, pywin32 to send windows native events such as click, mouse move and 
numpy for.... nothing I guess, 

```
pip install -r requirements.txt
```

## Running 

Ensure python and the dependencies are installed, also ensure mspaint (paint) desktop app is opened

```
python paynt.py "/path/to/image"
```