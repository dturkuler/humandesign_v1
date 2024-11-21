import json
import hd_constants
def general(data):
    output = {
        "birth_date": data['birth_date'],
        "create_date": data['create_date'],
        "energie_type": data['energie_type'],
        "inner_authority": data['inner_authority'],
        "inc_cross": data['inc_cross'],
        "profile": data['profile'],
        "defined_centers": list(data['active_chakras']), 
        "undefined_centers": list(set(hd_constants.CHAKRA_LIST) - set(data['active_chakras'])), 
        "split": data['split'],
        "variables": data['variables']
  }
  
    return json.dumps(output, indent=2)

def gatesJSON(data):
    # Initialize the structure for 'prs' and 'des'
    output = {
        "prs": {
            "Planets": []
        },
        "des": {
            "Planets": []
        }
    }

    # Loop through the data and populate 'prs' and 'des'
    for i in range(len(data['label'])):
        planet_data = {
            "Planet": data['planets'][i],
            "Lon": data['lon'][i],
            "Gate": data['gate'][i],
            "Line": data['line'][i],
            "Color": data['color'][i],
            "Tone": data['tone'][i],
            "Base": data['base'][i],
            "Ch_Gate": data['ch_gate'][i]
        }
        
        # Add planet data to the appropriate label ('prs' or 'des')
        if data['label'][i] == 'prs':
            output['prs']['Planets'].append(planet_data)
        else:
            output['des']['Planets'].append(planet_data)

    # Convert the result to JSON string (optional, for display purposes)
    return json.dumps(output, indent=2)

def channelsJSON(data, details=False):
    # details: get all details or only channels numbers
    result = []
    
    # Extracting the arrays from the input data
    labels = data['label']
    planets = data['planets']
    gates = data['gate']
    ch_gates = data['ch_gate']
    gate_chakras = data['gate_chakra']
    ch_gate_chakras = data['ch_gate_chakra']
    ch_gate_labels = data['ch_gate_label']
    gate_labels = data['gate_label']

    # Creating the JSON structure based on the details flag
    for i in range(len(labels)):
        if details:
            channel_data = {
                "channel": f"{gates[i]}/{ch_gates[i]}",  # Format channel as "gate/ch_gate"
                "label": str(labels[i]),
                "planets": str(planets[i]),
                "gate": str(gates[i]),
                "ch_gate": str(ch_gates[i]),
                "ch_gate_chakra": str(ch_gate_chakras[i]),
                "ch_gate_chakra_label": [str(label) for label in ch_gate_labels[i]],
                "gate_label": [str(label) for label in gate_labels[i]],
                "gate_label_detail": str(gate_chakras[i])
            }
        else:
            channel_data = {
                "channel": f"{gates[i]}/{ch_gates[i]}"  # Only include channel
            }
        result.append(channel_data)
    
    # Convert the result to a JSON string
    return json.dumps({"Channels": result}, indent=4)

