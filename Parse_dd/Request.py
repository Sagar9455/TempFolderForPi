import xml.etree.ElementTree as ET

def parse_positve():
    file_path = 'diag.xml' 
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    positive_responses = {}
    responses_root=root.find('Responses')
    if responses_root is not None:
         positive_root=responses_root.find('Positive')
         if positive_root is not None:
             for response in positive_root:
                 resp_id = response.attrib.get('id')
                 resp_desc = response.attrib.get('description')
        
                 positive_responses[ resp_id] =resp_desc

    return positive_responses
def parse_nrcs():
    file_path = 'diag.xml' 
    tree = ET.parse(file_path)
    root = tree.getroot()  
    
    nrcs = {}
    nrcs_root=root.find('NRCs')
    if nrcs_root is not None:
        for nrc in nrcs_root:
            nrc_id = nrc.attrib.get('id')
            nrc_desc = nrc.attrib.get('description')
            nrcs[ nrc_id] =nrc_desc
    return nrcs


positve_data = parse_positve()
nrcs_data = parse_nrcs()

print("\nNRCS:")
for nrc,nrc_id in nrcs_data.items():
    print(f"{nrc}:{nrc_id}")



print("\nPositiveResponses:")
for resp,resp_id in positve_data.items():
    print(f"{resp}:{resp_id}")

