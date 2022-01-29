import xml.etree.ElementTree as ET

default_attributes = {
    'id': 'flow_0',
    'begin': '0.00',
    'from': '122227353',
    'to': '262572765',
    'end': '3600.00',
    'vehsPerHour': "1800.00",
    'departSpeed': 'max'}

bemowo_s = "178457350"
bemowo_n = "178457351"
lomianki_w = "29920364#0"
lomianki_e = "26020081"
centrum_e = "173870817"
centrum_w = "174153255"
zeran_e = "195100701"
zeran_w = "195104098"
bialoleka_ee = "86121808"
bialoleka_ew = "195626694"
bialoleka_w = "81254441"
marki_nn = "262947144"
marki_ns = "86122668"
marki_sn = "86121813"
marki_ss = "191570757"


def add_flow(xml_root, flow_id: str, _from: str, to: str):
    attributes = default_attributes
    attributes['id'] = flow_id
    attributes['from'] = _from
    attributes['to'] = to
    ET.SubElement(xml_root, 'flow', attrib=attributes)

def add_flows(xml_root):
    add_flow(root, 'flow_0', bemowo_s, marki_sn)
    add_flow(root, 'flow_1', bemowo_s, centrum_w)
    add_flow(root, 'flow_2', bemowo_s, lomianki_e)
    add_flow(root, 'flow_3', bemowo_s, zeran_w)
    add_flow(root, 'flow_4', bemowo_s, bialoleka_ee)

    add_flow(root, 'flow_5', marki_ns, bemowo_n)
    add_flow(root, 'flow_6', marki_nn, bialoleka_ee)
    add_flow(root, 'flow_7', marki_nn, zeran_w)
    add_flow(root, 'flow_8', marki_nn, lomianki_e)
    add_flow(root, 'flow_9', marki_nn, centrum_w)

    add_flow(root, 'flow_10', centrum_e, lomianki_e)
    add_flow(root, 'flow_11', centrum_e, bemowo_n)
    add_flow(root, 'flow_12', centrum_e, marki_ss)
    add_flow(root, 'flow_13', centrum_e, zeran_w)
    add_flow(root, 'flow_14', centrum_e, bialoleka_ee)

    add_flow(root, 'flow_15', lomianki_w, bemowo_n)
    add_flow(root, 'flow_16', lomianki_w, centrum_w)
    add_flow(root, 'flow_17', lomianki_w, marki_ss)
    add_flow(root, 'flow_18', lomianki_w, bialoleka_ee)
    add_flow(root, 'flow_19', lomianki_w, zeran_w)

    add_flow(root, 'flow_22', zeran_e, bemowo_n)
    add_flow(root, 'flow_23', zeran_e, lomianki_e)
    add_flow(root, 'flow_24', zeran_e, centrum_w)

    add_flow(root, 'flow_25', bialoleka_w, bemowo_n)
    add_flow(root, 'flow_26', bialoleka_w, lomianki_e)
    add_flow(root, 'flow_27', bialoleka_w, centrum_w)


root = ET.Element('routes')

add_flows(root)
tree = ET.ElementTree(root)
ET.indent(tree, space="\t", level=0)

with open('osm.rou.xml', 'wb') as f:
    tree.write(f, encoding='utf-8')
