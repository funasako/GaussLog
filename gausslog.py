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
    Maximum_Force = "Null"
    RMS_Force = "Null"
    Maximum_Displacement = "Null"
    RMS_Displacement = "Null"
    Firstfreq = "Null"
    Secondfreq = "Null"
    OptChk = True
    FreqChk = True
    OptFlag = False
    PrintFlag = False
    PrintedFlag = False

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
            st.write(f"\nNumber of imaginary frequency = {imaginary_count}")
            FreqChk = False
        elif Linedata[1:3] == ["Optimized", "Parameters"]:
            OptFlag = True
            if OptChk:
                st.write(f"Maximum_Force        {Maximum_Force}")
                st.write(f"RMS_Force            {RMS_Force}")
                st.write(f"Maximum_Displacement {Maximum_Displacement}")
                st.write(f"RMS_Displacement     {RMS_Displacement}")         
                st.write("\n---Optimized Geometry---")
                OptChk = False
        elif Linedata[:2] == ["Standard", "orientation:"]:
            PrintFlag = OptFlag
        elif Linedata[0] == "Rotational":
            if PrintFlag:
                PrintedFlag = True
            PrintFlag = False
        elif PrintFlag and Linedata[0].isdigit() and not PrintedFlag:
            atom_info = number_atom.get(Linedata[1], "Unknown")
            st.text(f"{atom_info} {Linedata[3]} {Linedata[4]} {Linedata[5]}")

    # 熱力学的諸量
    PrintFlag = False
    EE = None
    for line in lines:
        Linedata = line.split()
        if len(Linedata) < 2:
            continue
        if Linedata[:2] == ["Zero-point", "correction="]:
            PrintFlag = True
        if PrintFlag:
            st.text(line)
        if len(Linedata) > 5 and Linedata[4:6] == ["thermal", "Free"]:
            PrintFlag = False
        if Linedata[:2] == ["SCF", "Done:"]:
            EE = Linedata[4]
        if line == lines[-1] and EE is not None:
            st.write(f"Electronic Energy = {EE}")
