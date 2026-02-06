import pandas as pd


def find_number(df, lookup_value, genre):
    lobe_values = []
    for _, row in df.iterrows():
        mbon_values = [x.strip() for x in row['MBON names'].split(',')]
        if lookup_value in mbon_values:
            lobe_values.append(row[genre])
    lobelobe = list(set(lobe_values))
    return ', '.join(lobelobe)


def generate_lobelocation(mbon_list, csv_path):
    csvfile = pd.read_csv(csv_path).astype('string')

    lobelocation = pd.DataFrame()
    for m in mbon_list:
        row = {
            'MBON': m,
            'Lobe_location': find_number(csvfile, m, "Lobe"),
            'MBON number': find_number(csvfile, m, "MBON number").strip(),
            'Neurotransmitter': find_number(csvfile, m, "Neurotransmitter"),
        }
        lobelocation = pd.concat([lobelocation, pd.DataFrame([row])])

    lobelocation = lobelocation.reset_index(drop=True)
    return lobelocation
