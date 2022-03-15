
def delete_invalid_contracts(r_root,contracts_codes):
    for code in contracts_codes:
        for one in r_root[2:]:
            if code == one[0].text:
                print("Match found at "+one[0].text)
                r_root.remove(one)
                print("Match removed from tree")

def find_invalid_entity_code(f_root):
    contracts_codes = []
    
    for item in f_root:
        if item.get('Severity') == 'Error':
            bc = item.get('EntityCode')    
            
            contracts_codes.append(bc)
            
    return contracts_codes