import textwrap


def parse_log_file(log_file):
    with open(log_file, "r", encoding="utf-8") as file:

        sensor_dict = {}

        for line in file:
             if "BIG" in line:
                orig_line_parts = line.split("> ", 1)
                if len(orig_line_parts) > 1:
                    clean_line = orig_line_parts[1].replace("'", "").strip()[0:-1]

                    clean_line_parts = clean_line.split(";")

                    sensor_id = clean_line_parts[2]
                    # list with S_P_1, S_P_2 and STATE
                    sensor_data = [clean_line_parts[6], clean_line_parts[13], clean_line_parts[17]] 

                    # for each sensor id - list of signals data
                    if sensor_id not in sensor_dict.keys():
                        sensor_dict[sensor_id] = [sensor_data] 
                    else:
                        sensor_dict[sensor_id].append(sensor_data)

        messages_count = {}
        failed_sensors = {}
        
        for key, value in sensor_dict.items():
            success_messages_for_current_key = 0
            for data in value:
                if data[2] == 'DD':
                    success_messages_for_current_key = 0
                    failed_sensors[key] = data
                    break
                elif data[2] == '02': 
                    success_messages_for_current_key += 1   

            messages_count[key] = success_messages_for_current_key

        all_big_messages = 0
        success_big_messages = 0
        failed_big_messages = 0

        for key, value in messages_count.items():
            all_big_messages += 1
            if value > 0:
                success_big_messages += 1
            else:
                failed_big_messages += 1

        print(f"All BIG sensore: {all_big_messages}")
        print(f"Succesful BIG sensors: {success_big_messages} ")
        print(f"Failed BIG sensors: {failed_big_messages} \n ")

        for key, value in failed_sensors.items():
            flags = parse_failed_logs(value[0],value[1])
            error_message = check_device_error(flags)
            print(f"{key} : {error_message}")
        

        print("\nSuccess messages count:")

        for key, value in messages_count.items():
            if value > 0:
                print(f"{key}: {value}")


def parse_failed_logs(sp1:str, sp2:str) -> str:

    control_data = sp1[:-1]+sp2 

    pairs_to_bin = textwrap.wrap(control_data, 2)

    num_pairs = [int(pair) for pair in pairs_to_bin]
    flags = []

    for num in num_pairs:
        binary_num = str(bin(num)[2:])
        while len(binary_num) != 8:
            binary_num = '0' + binary_num
        flags.append(binary_num[4])

    return "".join(flags)
    
# task did not provide clear instructions regarding the mapping between results and specific errors, so I developed my own error-handling system 
def check_device_error(flags: str) -> str:

    error_dict = {
        "100": "Battery device error",
        "010": "Temperature device error",
        "001": "Threshold central error",
        "110": "Battery and Threshold error",
        "101": "Battery and Temperature error",
        "011": "Temperature and Threshold error",
        "111": "Threshold central error"
    }
    
    return error_dict.get(flags, "Unknown device error")


parse_log_file("app_2.log")
        
