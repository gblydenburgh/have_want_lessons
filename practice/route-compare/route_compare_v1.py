#!/usr/bin/env python
'''
This script compares two text files containing the output from the pyats learn routing output or the output from
pyats parse "show ip routing".  It should work for Cisco IOS, IOS-XE, and NX-OS.
'''
__author__ = "Gary Blydenburgh"
__version__ = ": 1.0 $"
__date__ = "5/01/2021"
__copyright__ = "Copyright (c) What Really?!"
__license__ = "Python"
from argparse import ArgumentParser
import json
def quick_detect_changes(my_broutes, my_aroutes, my_missing_routes, my_new_routes):
    print("Changed Routes:")
    for i in my_broutes:
        #print(f"Subnet:  {i}")
        #Don't process routes that are in the delta missing_routes or new_routes lists; there is nothing to compare
        if i in my_missing_routes or i in my_new_routes:
            #print(f"Skip delta route: {i}")
            continue
        #Do not process connected routes
        elif my_broutes[i]['source_protocol'] == 'connected':
            #print(f"SKIP CONNECTED ROUTE: {broutes[i]}")
            continue
        #Do not process local routes
        elif my_broutes[i]['source_protocol'] == 'local':
            #print(f"SKIP LOCAL ROUTE: {broutes[i]}")
            continue
        #Do not process NULL0 static routes
        elif 'outgoing_interface' in my_broutes[i]['next_hop']:
            if 'Null0' in my_broutes[i]['next_hop']['outgoing_interface']:
                #print(f"SKIP NULL0 ROUTE: {broutes[i]}")
                continue
            #A catch all that should never match. If it does print the raw dictionary data.
            else:
                print(f"SKIP UNKNOWN REASON: {my_broutes[i]}")
                continue
        #Check to see if the the before and after route entry still share the same dictionary keys.
        if my_broutes[i].keys() != my_broutes[i].keys():
            print(f"\t{i:<18}:\tReason: Changed Dictionary Keys Unequal.")
            continue
        #Loop thorugh all the parent keys and compare them.
        for key in my_broutes[i]:
            #print(f"Evaluating key: {key}")
            #print(f"Before: {my_broutes[i][key]}\nAfter: {my_aroutes[i][key]}")
            if my_broutes[i][key] != my_aroutes[i][key] and key != "next_hop":
                print(f"\t{i:<18}:\tReason: Changed {key}")
                break
            elif len(my_broutes[i]['next_hop']['next_hop_list']) != len(my_aroutes[i]['next_hop']['next_hop_list']) and key == "next_hop":
                print(f"\t{i:<18}:\tReason: Changed Next-Hop")
                break
            elif len(my_broutes[i]['next_hop']['next_hop_list']) == len(my_aroutes[i]['next_hop']['next_hop_list']) and key == "next_hop":
                for j in my_broutes[i]['next_hop']['next_hop_list']:
                    if my_broutes[i]['next_hop']['next_hop_list'][j]['next_hop'] != my_aroutes[i]['next_hop']['next_hop_list'][j]['next_hop']:
                        print(f"\t{i:<18}:\tReason: Changed Next-Hop")
                        break
def normal_detect_changes(my_broutes, my_aroutes, my_missing_routes, my_new_routes):
    for i in my_broutes:
        detected_changes={}
        #print(f"Subnet:  {i}")
        #Don't process routes that are in the delta missing_routes or new_routes lists; there is nothing to compare
        if i in my_missing_routes or i in my_new_routes:
            #print(f"Skip delta route: {i}")
            continue
        #Do not process connected routes
        elif my_broutes[i]['source_protocol'] == 'connected':
            #print(f"SKIP CONNECTED ROUTE: {broutes[i]}")
            continue
        elif my_broutes[i]['source_protocol'] == 'local':
            #print(f"SKIP LOCAL ROUTE: {broutes[i]}")
            continue
        #Do not process NULL0 static routes
        elif 'outgoing_interface' in my_broutes[i]['next_hop']:
            if 'Null0' in my_broutes[i]['next_hop']['outgoing_interface']:
                #print(f"SKIP NULL0 ROUTE: {broutes[i]}")
                continue
            #A catch all that should never match. If it does print the raw dictionary data.
            else:
                print(f"SKIP UNKNOWN REASON: {my_broutes[i]}")
                continue
        #Check to see if the the before and after route entry still share the same dictionary keys.
        if my_broutes[i].keys() != my_broutes[i].keys():
            print(f"\t{i:<18}:\tReason: Changed Dictionary Keys Unequal.")
            continue
        #Loop thorugh all the parent keys and compare them.
        for key in my_broutes[i]:
            #print(f"Evaluating key: {key}")
            #print(f"Before: {my_broutes[i][key]}\nAfter: {my_aroutes[i][key]}")
            if my_broutes[i][key] != my_aroutes[i][key] and key != "next_hop":
                detected_changes[key]={'name': key + " Changed"}
                detected_changes[key]['before']=my_broutes[i][key]
                detected_changes[key]['after']=my_aroutes[i][key]
                #print(f"{detected_changes['source_protocol']}")
            if len(my_broutes[i]['next_hop']['next_hop_list']) != len(my_aroutes[i]['next_hop']['next_hop_list']) and key == "next_hop":
                #print("Fuckery")
                detected_changes['next_hop_len']={'name': 'Num of Next-Hops Changed'}
                detected_changes['next_hop_len']['before']=len(my_broutes[i]['next_hop']['next_hop_list'])
                detected_changes['next_hop_len']['after']=len(my_aroutes[i]['next_hop']['next_hop_list'])
                #print(f"{detected_changes['next_hop_len']}")
                detected_changes['next_hop_unequal']={'name': 'Next-Hops Changed'}
                detected_changes['next_hop_unequal']['before']=[]
                detected_changes['next_hop_unequal']['after']=[]
                for j in my_broutes[i]['next_hop']['next_hop_list']:
                    detected_changes['next_hop_unequal']['before'].append(my_broutes[i]['next_hop']['next_hop_list'][j]['next_hop'])
                for j in my_aroutes[i]['next_hop']['next_hop_list']:
                    detected_changes['next_hop_unequal']['after'].append(my_aroutes[i]['next_hop']['next_hop_list'][j]['next_hop'])
            elif len(my_broutes[i]['next_hop']['next_hop_list']) == len(my_aroutes[i]['next_hop']['next_hop_list']) and key == "next_hop":
                temp_detected_changes={}
                temp_detected_changes['next_hop_equal']={'name': 'Next-Hops Changed'}
                temp_detected_changes['next_hop_equal']['next_hops']={}
                #detected_changes['next_hop']['before']=[]
                #detected_changes['next_hop']['after']=[]
                for j in my_broutes[i]['next_hop']['next_hop_list']:
                    if my_broutes[i]['next_hop']['next_hop_list'][j]['next_hop'] != my_aroutes[i]['next_hop']['next_hop_list'][j]['next_hop']:
                        #print(f"INDEX: {broutes[i]['next_hop']['next_hop_list'][j]['index']}")
                        jindex=my_broutes[i]['next_hop']['next_hop_list'][j]['index']
                        temp_detected_changes['next_hop_equal']['next_hops'][jindex]={'index':jindex,
                                                                                      'before':my_broutes[i]['next_hop']['next_hop_list'][j]['next_hop'],
                                                                                      'after':my_aroutes[i]['next_hop']['next_hop_list'][j]['next_hop']
                                                                                  }
        if temp_detected_changes:
            if 1 in temp_detected_changes['next_hop_equal']['next_hops']:
                detected_changes['next_hop_equal']=temp_detected_changes['next_hop_equal']
        if detected_changes:
            print(f"Route {i} Changed:")
            print(f"\tReasons:")
            for k in detected_changes:
                #print(f"K - {k}")
                if k == "next_hop_equal":
                    print(f"\t\t{detected_changes[k]['name']:<25}:")
                    for l in detected_changes[k]['next_hops']:
                        print(f"\t\t{detected_changes[k]['next_hops'][l]['index']:>25}: before: {detected_changes[k]['next_hops'][l]['before']:>16} after: {detected_changes[k]['next_hops'][l]['after']:>16}")
                elif k == "next_hop_unequal":
                    print(f"\t\t{detected_changes[k]['name']:<25}: before: {str(detected_changes[k]['before'])}")
                    print(f"\t\t{' ':>25}: after: {str(detected_changes[k]['after'])}")
                else:
                    print(f"\t\t{detected_changes[k]['name']:<25}: before: {detected_changes[k]['before']:<20}after: {detected_changes[k]['after']:<20}")
            if args.raw:
                print("\n\tRAW DATA:")
                print("\tBEFORE:")
                print(f"\t\t{my_broutes[i]}")
                print("\tAFTER:")
                print(f"\t\t{my_aroutes[i]}\n\n")
def routetotals (mydata, title):
    bgp_cnt = 0
    ospf_cnt = 0
    eigrp_cnt = 0
    static_cnt = 0
    connected_cnt = 0
    rip_cnt = 0
    local_cnt=0
    direct_cnt=0
    hsrp_cnt=0
    glbp_cnt=0
    unknown_cnt = 0
    for i in mydata:
        if 'bgp' in mydata[i]['source_protocol']:
            bgp_cnt += 1
        elif 'ospf' in mydata[i]['source_protocol']:
            ospf_cnt += 1
        elif 'eigrp' in mydata[i]['source_protocol']:
            eigrp_cnt += 1
        elif 'static' in mydata[i]['source_protocol']:
            static_cnt += 1
        elif 'connected' in mydata[i]['source_protocol']:
            connected_cnt += 1
        elif 'rip' in mydata[i]['source_protocol']:
            rip_cnt += 1
        elif 'local' in mydata[i]['source_protocol']:
            local_cnt += 1
        elif 'direct' in mydata[i]['source_protocol']:
            direct_cnt += 1
        elif 'hsrp' in mydata[i]['source_protocol']:
            hsrp_cnt += 1
        elif 'glbp' in mydata[i]['source_protocol']:
            glbp_cnt += 1
        else:
            unknown_cnt += 1
    total = bgp_cnt + ospf_cnt + eigrp_cnt + static_cnt + connected_cnt + rip_cnt + unknown_cnt
    print(f"* * {title} Route Totals. * *")
    print(f"{'BGP':<9}: {bgp_cnt}\t{'OSPF':<9}: {ospf_cnt}\t{'EIGRP':<9}: {eigrp_cnt}")
    print(f"{'STATIC':<9}: {static_cnt}\t{'CONNECTED':<9}: {connected_cnt}\t{'RIP':<9}: {rip_cnt}")
    print(f"{'Local':<9}: {local_cnt}\t{'Direct':<9}: {direct_cnt}")
    print(f"{'HSRP':<9}: {hsrp_cnt}\t{'GLB':<9}: {glbp_cnt}")
    print(f"{'UNKNOWN':<9}: {unknown_cnt}")
    print(f"--------------------------------")
    print(f"TOTAL ROUTES: {total}\n")
def gen_route_count_summary(my_before_network_list, my_after_network_list):
    '''Compare before and after sets of network subnets to determine subnets missing from the after set, and new subnets
    in the after set that are not in the before set. The result of the compares will be printed to STDOUT, and returned
    to the original caller.'''
    #Subtract the before set from the after set to produce a new set containing a list of subnets that are were listed
    #in the before set but are missing from the after set.
    my_missing_routes = my_before_network_list - my_after_network_list
    my_new_routes = my_after_network_list - my_before_network_list
    print(f"\nMissing routes: {my_missing_routes}")
    print(f"New routes: {my_new_routes}\n")
    return my_missing_routes, my_new_routes
def custom_attributes():
    '''Not working yet.'''
    print("\tCompared Attributes:")
    if my_source_protocol_flag:
        print(f"\t\tSOURCE_PROTOCOL:  was: {broutes[i]['source_protocol']:<16}<-- now: {aroutes[i]['source_protocol']:<16}<--")
    else:
        print(f"\t\tSOURCE_PROTOCOL:  was: {broutes[i]['source_protocol']:<19} now: {aroutes[i]['source_protocol']:<19}")
    if my_source_protocol_code_flag:
        print(f"\t\tROUTE_CODES:      was: {broutes[i]['source_protocol_codes']:<16}<-- now: {aroutes[i]['source_protocol_codes']:<16}<--")
    else:
        print(f"\t\tROUTE_CODES:      was: {broutes[i]['source_protocol_codes']:<19} now: {aroutes[i]['source_protocol_codes']:<19}")
    if my_metric_flag:
        print(f"\t\tMETRIC:           was: {broutes[i]['metric']:<16}<-- now: {aroutes[i]['metric']:<16}<--")
    else:
        print(f"\t\tMETRIC:           was: {broutes[i]['metric']:<19} now: {aroutes[i]['metric']:<19}")
    if my_route_preference_flag:
        print(f"\t\tAdmin Distance:   was: {broutes[i]['route_preference']:<16}<-- now: {aroutes[i]['route_preference']:<16}<--")
    else:
        print(f"\t\tROUTE_PREF:       was: {broutes[i]['route_preference']:<19} now: {aroutes[i]['route_preference']:<19}")
    if my_active_flag:
        print(f"\t\tACTIVE:           was: {broutes[i]['active']:<16}<-- now -> {aroutes[i]['active']:<16}<--")
    else:
        print(f"\t\tACTIVE:           was: {broutes[i]['active']:<19} now: {aroutes[i]['active']:<19}")
    if my_next_hop_len_flag:
        print(f"\t\tNUM_OF_NEXT_HOPS: was: {len(broutes[i]['next_hop']['next_hop_list']):<16}<-- now: {len(aroutes[i]['next_hop']['next_hop_list']):<16}<--")
    else:
        print(f"\t\tNUM_OF_NEXT_HOPS: was: {len(broutes[i]['next_hop']['next_hop_list']):<19} now: {len(aroutes[i]['next_hop']['next_hop_list']):<19}")
    '''
    for j in broutes[i]['next_hop']['next_hop_list']:
        if broutes[i]['next_hop']['next_hop_list'][j]['next_hop'] != aroutes[i]['next_hop']['next_hop_list'][j]['next_hop']:
            print(f"\t\tNEXT-HOP({broutes[i]['next_hop']['next_hop_list'][j]['index']})     : was: {broutes[i]['next_hop']['next_hop_list'][j]['next_hop']:<16}<-- now: {aroutes[i]['next_hop']['next_hop_list'][j]['next_hop']:<16}<--")
        else:
            print(f"\t\tNEXT-HOP({broutes[i]['next_hop']['next_hop_list'][j]['index']})     : was: {broutes[i]['next_hop']['next_hop_list'][j]['next_hop']:<19} now: {aroutes[i]['next_hop']['next_hop_list'][j]['next_hop']:<19}")
    '''
def main( ):
    print(f"*************************")
    print(f"* ROUTE COMPARE STARTED *")
    print(f"*************************")
    print(f"VRF: {args.vrf.strip()}\v")
    print(f"BEFORE File: {args.before}")
    print(f"AFTER  File: {args.after}")
    with open(args.before) as f:
        bdata = json.load(f)
    with open(args.after) as f:
        adata = json.load(f)
    if args.parsed:
        try:
            broutes = bdata['info']['vrf'][args.vrf]['address_family']['ipv4']['routes']
        except KeyError:
            print("\n* * ERROR * *: The file is in the wrong format. Try using learned mode.\n")
            exit(1)
        aroutes = adata['info']['vrf'][args.vrf]['address_family']['ipv4']['routes']
        before_networks = bdata['info']['vrf'][args.vrf]['address_family']['ipv4']['routes'].keys()
        after_networks = adata['info']['vrf'][args.vrf]['address_family']['ipv4']['routes'].keys()
    elif args.learned:
        try:
            broutes = bdata['vrf'][args.vrf]['address_family']['ipv4']['routes']
        except KeyError:
            print("\n* * ERROR * *: The file is in the wrong format. Try using parsed mode.\n")
            exit(1)
        aroutes = adata['vrf'][args.vrf]['address_family']['ipv4']['routes']
        before_networks = bdata['vrf'][args.vrf]['address_family']['ipv4']['routes'].keys()
        after_networks = adata['vrf'][args.vrf]['address_family']['ipv4']['routes'].keys()
    before_network_list = set(before_networks)
    after_network_list = set(after_networks)
    missing_routes, new_routes = gen_route_count_summary( before_network_list, after_network_list )
    # Output: {'name': 'Bob', 'languages': ['English', 'Fench']}
    #pprint(broutes)
    routetotals(broutes,"BEFORE")
    routetotals(aroutes,"AFTER")
    if args.quick:
        quick_detect_changes(broutes, aroutes, missing_routes, new_routes)
    else:
        normal_detect_changes(broutes, aroutes, missing_routes, new_routes)
# Standard call to the main() function.
if __name__ == '__main__':
    parser = ArgumentParser(description="Compare two formatted/parsed routing tables captured with pyATS.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-p", "--parsed", action="store_true", help="Use if ouptut was gathered using pyats parsed mode. Example: pyats parse 'show ip route summary'... ")
    group.add_argument("-l", "--learned", action="store_true", help="Use if ouptut was gathered using pyats learned mode. Example: pyats parse learn routing ... ")
    parser.add_argument('-b', '--before', required=True, metavar='{{ PATH TO BEFORE FILE }}',
                    help='PyATS before route file.')
    parser.add_argument('-a', '--after', required=True, metavar='{{ PATH TO AFTER FILE }}',
                    help='PyATS after route file.')
    parser.add_argument('-v', '--vrf', metavar='{{ VRF }}', default='default',
                        help='Specify the VRF. default is assumed.')
    parser.add_argument('-t', '--attributes', action='store_true',
                        help='Print all attributes of changed routes. -NOT READY YET-')
    parser.add_argument('-r', '--raw', action='store_true',
                        help='Print raw dictionary of changed routes.')
    parser.add_argument('-q', '--quick', action='store_true',
                        help='Print a shorter report. Will list subnets that changed but will only report the first \
                        changed attribute.')
    args = parser.parse_args()
    main()
