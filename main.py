import serial

def main():
    try:
        # 打开两个串口
        ser_recv = serial.Serial(port='COM10', baudrate=115200, timeout=1)  # 接收端
        ser_send = serial.Serial(port='COM7', baudrate=921600, timeout=1)  # 发送端

        print("串口已打开：")
        print("  COM10（接收端）")
        print("  COM21（发送端）")

        while True:
            # 检查接收串口是否有数据
            if ser_recv.in_waiting > 0:
                # 从COM10读取数据
                data = ser_recv.read(ser_recv.in_waiting)
                print("接收到的数据:", data.hex(' ').upper())

                # 判断是否为有效数据包（以A5开头，长度为39字节）
                if data.startswith(b'\xA5') and len(data) == 39:
                    print("有效数据包，发送至COM21")
                    ser_send.write(data)  # 通过COM21发送数据
                else:
                    print("无效数据包，丢弃")

    except serial.SerialException as e:
        print(f"串口打开失败: {e}")
    except KeyboardInterrupt:
        print("程序被用户中断")
    finally:
        # 关闭串口
        if 'ser_recv' in locals() and ser_recv.is_open:
            ser_recv.close()
        if 'ser_send' in locals() and ser_send.is_open:
            ser_send.close()
        print("串口已关闭")

if __name__ == "__main__":
    main()
