# This script was used to check if the occasionally appearing seventh channel (Ch. 6)
# contains any useful data. Turns out no.

from utils import zoll

def get_max_ch(filename):
    j = zoll.LoadJSON(filename)
    #zoll.LoadWaveform(j)

    data = j['ZOLL']['FullDisclosure'][0]['FullDisclosureRecord']
    wave_records = []
    for item in data:
        for key in item:
            if key == "ContinWaveRec":
                wave_records.append(item['ContinWaveRec'])

    l = 0
    for wave_rec in wave_records:
        if len(wave_rec['Waveform']) > l:
            if len(wave_rec['Waveform']) == 7:
                print(wave_rec['Waveform'][6])
            l = len(wave_rec['Waveform'])
            t = type(wave_rec['Waveform'])

    print(f'{filename}: {str(l)}')
    print(f'Type: {t}')

get_max_ch("data\\zoll00001.json")
get_max_ch("data\\zoll00002.json")
get_max_ch("data\\zoll00003.json")
get_max_ch("data\\zoll00004.json")
get_max_ch("data\\zoll00005.json")
get_max_ch("data\\zoll00006.json")
get_max_ch("data\\zoll00007.json")
get_max_ch("data\\zoll00008.json")
get_max_ch("data\\zoll00009.json")
get_max_ch("data\\zoll00010.json")
get_max_ch("data\\zoll00011.json")
get_max_ch("data\\zoll00012.json")
get_max_ch("data\\zoll00013.json")
get_max_ch("data\\zoll00014.json")
get_max_ch("data\\zoll00015.json")
get_max_ch("data\\zoll00016.json")
get_max_ch("data\\zoll00017.json")
get_max_ch("data\\zoll00018.json")
get_max_ch("data\\zoll00019.json")
get_max_ch("data\\zoll00020.json")
get_max_ch("data\\zoll00021.json")
get_max_ch("data\\zoll00022.json")
get_max_ch("data\\zoll00023.json")
get_max_ch("data\\zoll00024.json")
get_max_ch("data\\zoll00025.json")
get_max_ch("data\\zoll00026.json")
get_max_ch("data\\zoll00027.json")
get_max_ch("data\\zoll00028.json")
get_max_ch("data\\zoll00029.json")
get_max_ch("data\\zoll00031.json")
get_max_ch("data\\zoll00032.json")
get_max_ch("data\\zoll00033.json")
get_max_ch("data\\zoll00034.json")
get_max_ch("data\\zoll00035.json")
get_max_ch("data\\zoll00036.json")
get_max_ch("data\\zoll00037.json")
get_max_ch("data\\zoll00038.json")
get_max_ch("data\\zoll00039.json")
get_max_ch("data\\zoll00040.json")
get_max_ch("data\\zoll00041.json")
get_max_ch("data\\zoll00042.json")
get_max_ch("data\\zoll00043.json")
get_max_ch("data\\zoll00044.json")
get_max_ch("data\\zoll00045.json")
get_max_ch("data\\zoll00046.json")
get_max_ch("data\\zoll00047.json")
get_max_ch("data\\zoll00048.json")
get_max_ch("data\\zoll00049.json")
get_max_ch("data\\zoll00050.json")
get_max_ch("data\\zoll00051.json")
get_max_ch("data\\zoll00052.json")
get_max_ch("data\\zoll00053.json")
get_max_ch("data\\zoll00054.json")
get_max_ch("data\\zoll00055.json")
get_max_ch("data\\zoll00056.json")
get_max_ch("data\\zoll00057.json")
get_max_ch("data\\zoll00058.json")
