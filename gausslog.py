import streamlit as st

# ファイルをアップロードする
uploaded_file = st.file_uploader("LOGファイルをアップロードしてください。", type=["log", "txt"])

if uploaded_file is not None:
    # ファイルの内容を読み込む
    content = uploaded_file.read().decode("utf-8")
    lines = content.splitlines()
    
    # パラメーター
    number_atom = {
        '1': 'H', '2': 'He', '3': 'Li', '4': 'Be', '5': 'B', '6': 'C', '7': 'N', '8': 'O', '9': 'F', '10': 'Ne',
        '11': 'Na', '12': 'Mg', '13': 'Al', '14': 'Si', '15': 'P', '16': 'S', '17': 'Cl', '18': 'Ar', '19': 'K', '20': 'Ca',
        '21': 'Sc', '22': 'Ti', '23': 'V', '24': 'Cr', '25': 'Mn', '26': 'Fe', '27': 'Co', '28': 'Ni', '29': 'Cu', '30': 'Zn',
        '31': 'Ga', '32': 'Ge', '33': 'As', '34': 'Se', '35': 'Br', '36': 'Kr', '37': 'Rb', '38': 'Sr', '39': 'Y', '40': 'Zr',
        '41': 'Nb', '42': 'Mo', '43': 'Tc', '44': 'Ru', '45': 'Rh', '46': 'Pd', '47': 'Ag', '48': 'Cd', '49': 'In', '50': 'Sn',
        '51': 'Sb', '52': 'Te', '53': 'I', '54': 'Xe', '55': 'Cs', '56': 'Ba'
    }

    # 初期値設定
    Maximum_Force = RMS_Force = Maximum_Displacement = RMS_Displacement = "Null"
    Firstfreq = Secondfreq = "Null"
    OptChk = FreqChk = True
    OptFlag = PrintFlag = PrintedFlag = False
    geometry_data = []
    energy_data = []
    imaginary_count = 0
    EE = None

    # 構造最適化の処理
    for line in lines:
        Linedata = line.split()
        if len(Linedata) < 2:
            continue
        if Linedata[:2] == ["Maximum", "Force"] and Linedata[4] == 'YES':
            Maximum_Force = "YES"
        elif Linedata[:2] == ["RMS", "Force"] and Linedata[4] == 'YES':
            RMS_Force = "YES"
        elif Linedata[:2] == ["Maximum", "Displacement"] and Linedata[4] == 'YES':
            Maximum_Displacement = "YES"
        elif Linedata[:2] == ["RMS", "Displacement"] and Linedata[4] == 'YES':
            RMS_Displacement = "YES"
        elif Linedata[:2] == ["Input", "orientation:"]:
            Maximum_Force = "NO"
            RMS_Force = "NO"
            Maximum_Displacement = "NO"
            RMS_Displacement = "NO"
        elif Linedata[:2] == ["Frequencies", "--"] and FreqChk:
            Firstfreq, Secondfreq = Linedata[2], Linedata[3]
            imaginary_count = sum(float(freq) < 0 for freq in [Firstfreq, Secondfreq])
            # st.text(f"Number of imaginary frequency = {imaginary_count}")
            FreqChk = False
        elif Linedata[1:3] == ["Optimized", "Parameters"]:
            OptFlag = True
            if OptChk:
                st.text("--- Optimization Results ---")
                # st.text(f"Maximum_Force {Maximum_Force}")
                # st.text(f"RMS_Force {RMS_Force}")
                # st.text(f"Maximum_Displacement {Maximum_Displacement}")
                # st.text(f"RMS_Displacement {RMS_Displacement}")
                # st.text(f"Number of imaginary frequency 1 = {imaginary_count}")
                optimization_results = [
                    f"Maximum_Force {Maximum_Force}",
                    f"RMS_Force {RMS_Force}",
                    f"Maximum_Displacement {Maximum_Displacement}",
                    f"RMS_Displacement {RMS_Displacement}",
                    f"Number of imaginary frequency = {imaginary_count}"
                ]
                st.text("\n".join(optimization_results))  # 結果を1行ごとに表示し、余分な改行を削除
                OptChk = False
        elif Linedata[:2] == ["Standard", "orientation:"]:
            PrintFlag = OptFlag
        elif Linedata[0] == "Rotational":
            if PrintFlag:
                PrintedFlag = True
            PrintFlag = False
        elif PrintFlag and Linedata[0].isdigit() and not PrintedFlag:
            atom_info = number_atom.get(Linedata[1], "Unknown")
            geometry_data.append(f"{atom_info} {Linedata[3]} {Linedata[4]} {Linedata[5]}")
    
    # 熱力学的諸量の処理
    PrintFlag = False
    for line in lines:
        Linedata = line.split()
        if len(Linedata) < 2:
            continue
        if Linedata[:2] == ["Zero-point", "correction="]:
            PrintFlag = True
        if PrintFlag:
            energy_data.append(line.strip())
        if len(Linedata) > 5 and Linedata[4:6] == ["thermal", "Free"]:
            PrintFlag = False
        if Linedata[:2] == ["SCF", "Done:"]:
            EE = Linedata[4]
       
    # 熱力学的諸量の結果を表示    
    if energy_data:
        energy_output = "\n".join(energy_data)  # energy_dataを1つの文字列にまとめる
        if EE:
            energy_output += f"\nElectronic Energy = {EE}"  # EEを最後に追加
        st.text("\n\n--- Energies ---")
        st.text(energy_output)  # 結果をまとめて表示


    # 最適化構造の座標を表示
    if geometry_data:
        st.text("\n\n---Optimized Geometry ---")
        st.text("\n".join(geometry_data))  # 余分な改行を削除するため、joinを使用
    


