def group_by_owners(files):
    if not files:
        return
    res = {}
    for key, val in files.items():
        if val not in res:
            res[val] = [key]
        else:
            res[val] += [key]
    return res

if __name__ == "__main__":    
    files = {
        'Input.txt': 'Randy',
        'Code.py': 'Stan',
        'Output.txt': 'Randy'
    }   
    print(group_by_owners(files))