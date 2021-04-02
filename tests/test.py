from alvadescpy import smiles_to_descriptors


if __name__ == '__main__':

    print(smiles_to_descriptors('CCCOC', descriptors=['MW', 'AMW'], labels=True))
    res = smiles_to_descriptors(['CCCC', 'CCOCC', 'CCCCC'], descriptors='ALL', labels=True)
    print(len(res))
    print(len(res[0]))
