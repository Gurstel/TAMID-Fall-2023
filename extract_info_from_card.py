def extract_info_from_card(card_info: str):
    base = set(card_info.split("."))
    info = {}
    for s in base:
        if "My name" in s:
            info['name'] = s.split("name is")[1].strip()
            continue
        if "I am/was" in s:
            info['profession'] = s.split("am/was a")[1].strip()
            continue
        if "free time" in s:
            info['hobby'] = s.split("I like to")[1].strip()
            continue
        if "now hard" in s:
            info['difficulties'] = s.split("now hard for me to")[1].strip()
            if "it\'s" in s:
                info['situation'] = s.split("and it's now")[0][3:].strip()
            continue
        if "Please" in s:
            info['communication'] = s.split("help me by")[1].strip()
            continue
        if "Thank you" in s:
            l = s.split("!")[1:]
            if " ".join(l).strip():
                info['additional'] = " ".join(l).strip().strip()
    
    return info