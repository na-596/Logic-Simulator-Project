device_property = ('0201110')

if str(device_property) >= '1'*len(str(device_property)):
    print ('This is not a valid binary waveform')
else: 
    print ('11111111'<='1'*len(str(device_property)))

print (str(device_property)[0].isdigit())
