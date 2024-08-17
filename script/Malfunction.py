from wave import open as openw
from struct import pack
from operator import xor
from optparse import OptionParser

bits = 7
base = 32
maximum = 63
reversem = padding = frequency = card = card2 = filen = trackp = None

def main():
    global bits, base, maximum, padding, frequency, card, filen, listOuti, reversem, card2
    parser = OptionParser('Usage: \n\t'+ __file__ + ' <parameters>:' +\
        '\n\n\tTo encode mag-stripe:\n\t\t-t [Track #[1-3]] | default:1>' +\
        '\n\t\t-c <data>\n\t\t-z [# of zeros | default:20] '+\
        '\n\t\t-s [samples per bit | default:15]'+\
        '\n\t\t-f [wav filename | if not specified, only shows binary encode]\n\n' +\
        '\n\t\t-r [reverse magstripe | default:0]'+\
        '\n\tTo decode Magstripe binary:\n\t\t-d [data]\n')
    parser.add_option('-t', dest='tr', type='string',\
        help='specify track number')
    parser.add_option('-c', dest='da1', type='string',\
        help='data for the track')
    parser.add_option('-b', dest='da2', type='string',\
        help='data for the track 2')
    parser.add_option('-z', dest='ze', type='string',\
        help='specify number of leading zeros')
    parser.add_option('-s', dest='sa', type='string',\
        help='Samples per bit, recommended [5-45]')
    parser.add_option('-f', dest='fi', type='string',\
        help='File name')
    parser.add_option('-d', dest='mb', type='string',\
        help='MagStripe Binary')
    parser.add_option('-r', dest='re', type='string',\
        help='Reverse MagStripe')
    (options, args) = parser.parse_args()
    
    trackp = options.tr
    card = options.da1
    card2 = options.da2

    padding = options.ze
    frequency = options.sa
    filen = options.fi
    reversem = options.re
    
    if options.mb != None:
        decodeMagbinary(options.mb)
    else:
        if card == None:
            print(parser.usage)
            exit(0)

        padding = int(padding) if padding != None else 25
        frequency = int(frequency) if frequency != None else 15
        reversem = int(reversem) if reversem != None else 0
        card2 = card2 if card2 != None else ''

        if trackp != None:
            if trackp == '2' or trackp == '3':
                changeTrack(2)
        GenerateWav()
        
def changeTrack(num):
    global bits, base, maximum
    bits = 7
    base = 32
    maximum = 63
    if num == 2 or num == 3:
        bits = 5
        base = 48
        maximum = 15
    
def decodeMagbinary(data):
    # check for IATA data - find start sentinel
    start_decode = data.find("1010001")
    if start_decode < 0:
        print("No start sentinel found!")
        exit(-1)
        
    end_sentinel = data.find("1111100")
    # check end sentinel is on 7 bit boundary
    while (end_sentinel - start_decode) % 7:
        newpos = data[end_sentinel + 1:].find("1111100")
        if newpos >= 0:
            end_sentinel += newpos + 1
        else:
            print("No end sentinel found!")
            exit(-1)
            
    # LRC comes immediately after end sentinel
    actual_lrc = end_sentinel + 7
    # initialise rolling LRC
    rolling_lrc = [0, 0, 0, 0, 0, 0, 0]
    decoded_string = ''
    # do the decode
    while start_decode <= end_sentinel:
        asciichr = 32
        parity = int(data[start_decode + 6])
        
        for x in range(6):
            asciichr += int(data[start_decode + x]) << x
            parity += int(data[start_decode + x])
            rolling_lrc[x] = xor(rolling_lrc[x], int(data[start_decode + x]))
            
        # check parity
        if not parity % 2:
            print("parity error!")
            exit(-1)
            
        decoded_string += chr(asciichr)
        start_decode += 7
        
    # check LRC
    parity = 1
    for x in range(6):
        parity += rolling_lrc[x]
        
    rolling_lrc[6] = parity % 2
    for x in range(7):
        if not rolling_lrc[x] == int(data[actual_lrc + x]):
            print("LRC/CRC check failed!")
            exit(-1)
    print("result:")
    print(decoded_string)
    
def encodeMag(d1):
    data = d1
    lrc = []
    output = ''
    # Check what track
    if data[:1] == '%':
        changeTrack(1)
    else:
        changeTrack(2)
        
    for x in range(bits):
        # zero += "0"
        lrc.append(0)
    
    for x in range(padding):
        output += '0'
    
    for x in range(len(data)):
        raw = ord(data[x]) - base
        if raw < 0 or raw > maximum:
            print('Illegal character:' , chr(raw + base))
            exit(0)
            
        parity = 1
        for y in range(bits - 1): 
            # raw >> y & 1 : (raw >> y) shift the x bits to the right by 'y' places
            #  & 1 : each bit of the output is 1 if the corresponding bit is 1, otherwise it's 0.
            output += str(raw >> y & 1)
            parity += raw >> y & 1
            lrc[y] = xor(lrc[y], raw >> y & 1)
            
        output += chr((parity % 2) + ord('0'))

    parity = 1
    for x in range(bits - 1):
        output += chr(lrc[x] + ord('0'))
        parity += lrc[x]
        
    output += chr((parity % 2) + ord('0'))
    for x in range(padding):
        output += '0'
    # Finishing the first part of the code:
    return output

def GenerateWav():
    data = encodeMag(card)
    # Second part:
    if filen == None:
        exit(0)
    else:
        print("Creating wav file: " + filen)
        newtrack = openw(filen, "w")
        params = (1, 2, 22050, 0, 'NONE', 'not compressed')
        newtrack.setparams(params)
        tmp = ''
        peak = 32767

        # write the actual data
        # square wave for now
        for x in range(2):
            n = 0
            writedata = peak
            while n < len(data):
                if data[n] == '1':
                    for x in range(2):
                        writedata = -writedata
                        for y in range(int(frequency / 4)):
                            newtrack.writeframes(pack("h", writedata))

                if data[n] == '0':
                    writedata = -writedata
                    for y in range(int(frequency / 2)):
                        newtrack.writeframes(pack("h", writedata))
                n = n + 1
            tmp = tmp + data

            if card2 != '':
                if card2[:1] == ';':
                    data = encodeMag(card2)
            else:
                if reversem == 0 or card[:1] != ';':
                    break
            data = data[::-1]
        print(tmp)        
        newtrack.close()
        print("Done")
        
if __name__ == '__main__':
    main()
