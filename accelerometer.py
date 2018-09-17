import smbus

DEVICE_BUS = 1
DEVICE_ADDR = 0x18
LIS3DH_REG_CTRL1 = 0x20
LIS3DH_REG_CTRL2 = 0x21
LIS3DH_REG_CTRL3 = 0x22
LIS3DH_REG_CTRL4 = 0x23
LIS3DH_REG_TEMPCFG = 0x1F
LIS3DH_DATARATE_400_HZ = 0x0b0111


bus = smbus.SMBus(DEVICE_BUS)


def twos_comp(val, bits):
    if (val & (1 << (bits - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
        val = val - (1 << bits)        # compute negative value
    return val                         # return positive value as is

# setup 
# enable all axes, normal mode, set to 400hz
bus.write_byte_data(DEVICE_ADDR, LIS3DH_REG_CTRL1, 0x77)

#High res & BDU enabled
bus.write_byte_data(DEVICE_ADDR, LIS3DH_REG_CTRL4, 0x88)

#DRDY on INT1
bus.write_byte_data(DEVICE_ADDR, LIS3DH_REG_CTRL3, 0x10)

#enable adcs
bus.write_byte_data(DEVICE_ADDR, LIS3DH_REG_TEMPCFG, 0x80)


#bus.write_byte_data(DEVICE_ADDR, 0x31, 0x30)
while True:
  raw_values = []
  for i in range(0x28, 0x2E):
    byte = bus.read_byte_data(DEVICE_ADDR, i)
    raw_values.append(byte)
  x_result = (raw_values[1] << 4) + raw_values[0]
  x_result_8 = (raw_values[1] << 8) + raw_values[0]
  x_two_comp = twos_comp(int(x_result_8), 16)
  y_result = (raw_values[3] << 4) + raw_values[2]
  z_result = (raw_values[5] << 4) + raw_values[4]
  print x_result, "  ", x_two_comp, "   ",  y_result, "  ", z_result
