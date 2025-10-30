import json

def generateArduinoCode(jsonFilePath):
    with open(jsonFilePath, 'r') as file: #load json data
        jsonData = json.load(file)
    
    player1inputs = [input_data for input_data in jsonData["inputs"] if not input_data["2p"]]
    
    player1inputs.sort(key=lambda x: x["frame"])  #Ensures inputs are stored in the correct time order
    
    #Arduino code, initialized as a string, and add onto the string to print out something that is Arduino code
    arduinoCode = """const int outputPin = 13;
const int startButton = 2;

void setup() {
    pinMode(outputPin, OUTPUT);
    pinMode(startButton, INPUT_PULLUP);
    digitalWrite(outputPin, LOW);
    while (digitalRead(startButton) == HIGH);
    delay(200);
}

void loop() {
"""

    previousFrame = 0
    frameDuration = 1000.0 / 60.0  #GD macro recorded at 60fps and GD runs 60 fps on laptop - change based on performance and macro
    
    for inputData in player1inputs:
        frameVal = inputData["frame"]
        down = inputData["down"]
        
        #Scale down delay time by 4  - determined through experimenting with Arduino code efficiency and how GD runs
        delayTime = ((frameVal - previousFrame) * frameDuration) / 4 
        previousFrame = frameVal

        arduinoCode += f"    delay({int(delayTime)});\n"
        arduinoCode += "    digitalWrite(outputPin, HIGH);\n" if down else "    digitalWrite(outputPin, LOW);\n"

    arduinoCode += "    while (true);\n}\n"

    return arduinoCode

jsonFilePath = r"C:\Users\ebabb\AppData\Local\GeometryDash\geode\mods\firee.prism\macros\fingerdash2.gdr.json" #Switch file path here
arduinoCode = generateArduinoCode(jsonFilePath)

#Output
print(arduinoCode)
