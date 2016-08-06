from os import listdir, getcwd
from os.path import isfile, join
from math import sin, cos
files = [f for f in listdir(getcwd()+'\uploads') if isfile(join(getcwd()+'\uploads', f))]
files = [f for f in files if f.endswith(".txt")]

czml =(
    'var accRate_time_data = {\n'
    'data: [\n'
)

fileIndex = 0;

for file in files :
    czml += ('[');

    FILE_PATH = getcwd()+'\uploads'+'\%s' % file

    data = []
    with open(FILE_PATH, 'r') as input_stream :

        lines = input_stream.readlines()

        words = lines[4].split(' ')
        words = [x for x in words if len(x) > 0]
        front_height = int(words[3])

        words = lines[5].split(' ')
        words = [x for x in words if len(x) > 0]
        back_height = int(words[3])
        front_vel = back_height-front_height
        front_height = back_height


        for i in range( 6, len(lines)) : #avoid head text
            words = lines[i].split(' ')
            words = [x for x in words if len(x) > 0]
            if (len(words)>15) : #avoid crash data
                back_height = int(words[3])
                back_vel = back_height-front_height
                acc = back_vel - front_vel
                minutes = float(words[0]) + float(words[1])/60
                data.append([ minutes, acc])
                front_height = back_height
                front_vel = back_vel

    input_stream.close()

    for j in range(0, len(data)) :
        czml += ('[ %f, %d], ' %(data[j][0],data[j][1]))

        fileIndex += 1

    czml += ('], \n')

czml += (
    '],\n'
    'filename: ['
)

for file in files:
    czml += ('"%s",' %(file))

czml += (
    '],\n'
    'xAxisName: "minute(s)",\n'
    "yAxisName: 'm/s^2',\n"
    'xMax: 0,\n'
    'yMax: 0,\n'
    'xMin: 1000,\n'
    'yMin: 1000,\n'
    'target: "accRate_time",\n'
    'W: 800,\n'
    'H: 400\n'
    '}\n'
)

fout = open(getcwd()+'\\balloon\data'+'\\accRate_time_data.js', 'w')
fout.write(czml)
fout.close()
