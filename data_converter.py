"""
Project Name: WDW-Transit-Optimizer
File Name: data_converter.py
Description: Data JSON generation and conversion utility.
Author: Joseph Lefkovitz (github.com/lefkovitzj)
Last Modified: 1/12/2026
"""

import json

monorails = [
    ("Ticket & Transportation Center - Resort Monorail", "Disney's Polynesian Village Resort - Resort Monorail", 4, "Resort Monorail", False),
    ("Disney's Polynesian Village Resort - Resort Monorail", "Disney's Grand Floridian Resort & Spa - Resort Monorail", 4, "Resort Monorail", False),
    ("Disney's Grand Floridian Resort & Spa - Resort Monorail", "Magic Kingdom - Resort Monorail", 4, "Resort Monorail", False),
    ("Magic Kingdom - Resort Monorail", "Disney's Contemporary Resort - Resort Monorail", 4, "Resort Monorail", False),
    ("Disney's Contemporary Resort - Resort Monorail", "Ticket & Transportation Center - Resort Monorail", 4, "Resort Monorail", False),
    ("Ticket & Transportation Center - Express Monorail", "Magic Kingdom - Express Monorail", 7, "Express Monorail", False),
    ("Magic Kingdom - Express Monorail", "Ticket & Transportation Center - Express Monorail", 5, "Express Monorail", False),
    ("Ticket & Transportation Center - Epcot Monorail", "Epcot - Epcot Monorail", 10, "Epcot Monorail", True),
]
boats = [
    ("Ticket & Transportation Center - Ferry", "Magic Kingdom", 11, "Ferry", True),
    ("Disney's Polynesian Village Resort - Gold Flag Launch", "Magic Kingdom - Gold Flag Launch", 7, "Gold Flag Launch", False),
    ("Disney's Grand Floridian Resort & Spa - Gold Flag Launch", "Disney's Polynesian Village Resort - Gold Flag Launch", 7, "Gold Flag Launch", False),
    ("Magic Kingdom - Gold Flag Launch", "Disney's Grand Floridian Resort & Spa - Gold Flag Launch", 7, "Gold Flag Launch", False),
    ("Magic Kingdom - Green Flag Launch", "Disney's Fort Wilderness Resort & Campground - Green Flag Launch", 15, "Green Flag Launch", True),
    ("Disney's Wilderness Lodge Resort - Red Flag Launch", "Magic Kingdom - Red Flag Launch", 7, "Red Flag Launch", True),
    ("Disney's Contemporary Resort - Blue Flag Launch", "Disney's Fort Wilderness Resort & Campground - Blue Flag Launch", 7, "Blue Flag Launch", True),
    ("Disney's Wilderness Lodge Resort - Blue Flag Launch", "Disney's Fort Wilderness Resort & Campground - Blue Flag Launch", 7, "Blue Flag Launch", True),
    ("Disney's Wilderness Lodge Resort - Blue Flag Launch", "Disney's Contemporary Resort - Blue Flag Launch", 7, "Blue Flag Launch", True),
    ("Hollywood Studios - Crescent Lake Friendship Boat to Epcot", "Swan and Dolphin Hotel - Crescent Lake Friendship Boat to Epcot", 8, "Crescent Lake Friendship Boat to Epcot", False),
    ("Swan and Dolphin Hotel - Crescent Lake Friendship Boat to Epcot", "Disney's Yacht and Beach Club Resorts - Crescent Lake Friendship Boat to Epcot", 8, "Crescent Lake Friendship Boat to Epcot", False),
    ("Disney's Yacht and Beach Club Resorts - Crescent Lake Friendship Boat to Epcot", "Disney's Boardwalk Inn - Crescent Lake Friendship Boat to Epcot", 8, "Crescent Lake Friendship Boat to Epcot", False),
    ("Disney's Boardwalk Inn - Crescent Lake Friendship Boat to Epcot", "Epcot International Gateway - Crescent Lake Friendship Boat to Epcot", 8, "Crescent Lake Friendship Boat to Epcot", False),
    ("Swan and Dolphin Hotel - Crescent Lake Friendship Boat to Hollywood Studios", "Hollywood Studios - Crescent Lake Friendship Boat to Hollywood Studios", 8, "Crescent Lake Friendship Boat to Hollywood Studios", False),
    ("Disney's Yacht and Beach Club Resorts - Crescent Lake Friendship Boat to Hollywood Studios", "Swan and Dolphin Hotel - Crescent Lake Friendship Boat to Hollywood Studios", 8, "Crescent Lake Friendship Boat to Hollywood Studios", False),
    ("Disney's Boardwalk Inn - Crescent Lake Friendship Boat to Hollywood Studios", "Disney's Yacht and Beach Club Resorts - Crescent Lake Friendship Boat to Hollywood Studios", 8, "Crescent Lake Friendship Boat to Hollywood Studios", False),
    ("Epcot International Gateway - Crescent Lake Friendship Boat to Hollywood Studios", "Disney's Boardwalk Inn - Crescent Lake Friendship Boat to Hollywood Studios", 8, "Crescent Lake Friendship Boat to Hollywood Studios", False),
    ("Disney's Port Orleans French Quarter Resort - Purple Flag Sassagoula River Ferry Boat", "Disney Springs Marketplace - Purple Flag Sassagoula River Ferry Boat", 20, "Purple Flag Sassagoula River Ferry Boat", True),
    ("Disney's Port Orleans Riverside Resort - Yellow Flag Sassagoula River Ferry Boat", "Disney Springs Marketplace - Yellow Flag Sassagoula River Ferry Boat", 17, "Yellow Flag Sassagoula River Ferry Boat", True),
    ("Disney's Saratogoa Springs Resort and Tree Houses - Blue Flag Sassagoula River Ferry Boat", "Disney Springs Landing - Blue Flag Sassagoula River Ferry Boat", 15, "Blue Flag Sassagoula River Ferry Boat", True),
    ("Disney's Old Key West Resort - Green Flag Sassagoula River Ferry Boat", "Disney Springs Landing - Green Flag Sassagoula River Ferry Boat", 10, "Green Flag Sassagoula River Ferry Boat", True),
]
skyliners = [
    ("Disney's Caribbean Beach Resort - Epcot Skyliner", "Disney Vacation Club Riviera Resort - Epcot Skyliner", 4, "Epcot Skyliner", True),
    ("Disney Vacation Club Riviera Resort - Epcot Skyliner", "Epcot International Gateway - Epcot Skyliner", 10, "Epcot Skyliner", True),
    ("Disney's Caribbean Beach Resort - Epcot Skyliner", "Hollywood Studios - Hollywood Studios Skyliner", 10, "Hollywood Studios Skyliner", True),
    ("Disney's Caribbean Beach Resort - Pop Century/Art of Animation Skyliner", "Generation Gap Bridge - Pop Century/Art of Animation Skyliner", 5, "Pop Century/Art of Animation Skyliner", True),
]
walks = [
    ("Magic Kingdom", "Magic Kingdom - Resort Monorail", 7, "Walk", False),
    ("Magic Kingdom - Resort Monorail", "Magic Kingdom", 1, "Walk", False),
    ("Magic Kingdom", "Magic Kingdom - Express Monorail", 7, "Walk", False),
    ("Magic Kingdom - Express Monorail", "Magic Kingdom", 1, "Walk", False),
    ("Magic Kingdom", "Magic Kingdom - Gold Flag Launch", 11, "Walk", False),
    ("Magic Kingdom - Gold Flag Launch", "Magic Kingdom", 1, "Walk", False),
    ("Magic Kingdom", "Magic Kingdom - Green Flag Launch", 15, "Walk", False),
    ("Magic Kingdom - Green Flag Launch", "Magic Kingdom", 1, "Walk", False),
    ("Magic Kingdom", "Magic Kingdom - Red Flag Launch", 20, "Walk", False),
    ("Magic Kingdom - Red Flag Launch", "Magic Kingdom", 1, "Walk", False),
    ("Ticket & Transportation Center", "Ticket & Transportation Center - Resort Monorail", 7, "Walk", False),
    ("Ticket & Transportation Center", "Ticket & Transportation Center - Express Monorail", 7, "Walk", False),
    ("Ticket & Transportation Center", "Ticket & Transportation Center - Epcot Monorail", 7, "Walk", False),
    ("Ticket & Transportation Center - Resort Monorail", "Ticket & Transportation Center", 1, "Walk", False),
    ("Ticket & Transportation Center - Express Monorail", "Ticket & Transportation Center", 1, "Walk", False),
    ("Ticket & Transportation Center - Epcot Monorail", "Ticket & Transportation Center", 1, "Walk", False),
    ("Ticket & Transportation Center", "Ticket & Transportation Center - Ferry", 11, "Walk", False),
    ("Ticket & Transportation Center - Ferry", "Ticket & Transportation Center", 1, "Walk", False),
    ("Disney's Polynesian Village Resort", "Disney's Polynesian Village Resort - Resort Monorail", 7, "Walk", False),
    ("Disney's Polynesian Village Resort - Resort Monorail", "Disney's Polynesian Village Resort", 1, "Walk", False),
    ("Disney's Polynesian Village Resort", "Disney's Polynesian Village Resort - Gold Flag Launch", 11, "Walk", False),
    ("Disney's Polynesian Village Resort - Gold Flag Launch", "Disney's Polynesian Village Resort", 1, "Walk", False),
    ("Disney's Grand Floridian Resort & Spa", "Disney's Grand Floridian Resort & Spa - Resort Monorail", 7, "Walk", False),
    ("Disney's Grand Floridian Resort & Spa - Resort Monorail", "Disney's Grand Floridian Resort & Spa", 1, "Walk", False),
    ("Disney's Grand Floridian Resort & Spa", "Disney's Grand Floridian Resort & Spa - Gold Flag Launch", 11, "Walk", False),
    ("Disney's Grand Floridian Resort & Spa - Gold Flag Launch", "Disney's Grand Floridian Resort & Spa", 1, "Walk", False),
    ("Disney's Contemporary Resort", "Disney's Contemporary Resort - Resort Monorail", 7, "Walk", False),
    ("Disney's Contemporary Resort - Resort Monorail", "Disney's Contemporary Resort", 1, "Walk", False),
    ("Disney's Contemporary Resort", "Disney's Contemporary Resort - Blue Flag Launch", 15, "Walk", False),
    ("Disney's Contemporary Resort - Blue Flag Launch", "Disney's Contemporary Resort", 1, "Walk", False),
    ("Disney's Fort Wilderness Resort & Campground", "Disney's Fort Wilderness Resort & Campground - Green Flag Launch", 15, "Walk", False),
    ("Disney's Fort Wilderness Resort & Campground - Green Flag Launch", "Disney's Fort Wilderness Resort & Campground", 1, "Walk", False),
    ("Disney's Fort Wilderness Resort & Campground", "Disney's Fort Wilderness Resort & Campground - Blue Flag Launch", 15, "Walk", False),
    ("Disney's Fort Wilderness Resort & Campground - Blue Flag Launch", "Disney's Fort Wilderness Resort & Campground", 1, "Walk", False),
    ("Disney's Wilderness Lodge Resort", "Disney's Wilderness Lodge Resort - Red Flag Launch", 20, "Walk", False),
    ("Disney's Wilderness Lodge Resort - Red Flag Launch", "Disney's Wilderness Lodge Resort", 1, "Walk", False),
    ("Disney's Wilderness Lodge Resort", "Disney's Wilderness Lodge Resort - Blue Flag Launch", 15, "Walk", False),
    ("Disney's Wilderness Lodge Resort - Blue Flag Launch", "Disney's Wilderness Lodge Resort", 1, "Walk", False),
    ("Generation Gap Bridge - Pop Century/Art of Animation Skyliner", "Disney's Pop Century Resort", 10, "Walk", True),
    ("Generation Gap Bridge - Pop Century/Art of Animation Skyliner", "Disney's Art of Animation Resort", 10, "Walk", True),
    ("Disney's Caribbean Beach Resort", "Disney's Caribbean Beach Resort - Epcot Skyliner", 1, "Walk", True),
    ("Disney's Caribbean Beach Resort", "Disney's Caribbean Beach Resort - Hollywood Studios Skyliner", 1, "Walk", True),
    ("Disney's Caribbean Beach Resort", "Disney's Caribbean Beach Resort - Pop Century/Art of Animation Skyliner", 1, "Walk", True),
    ("Disney Vacation Club Riviera Resort", "Disney Vacation Club Riviera Resort - Epcot Skyliner", 1, "Walk", True),
    ("Epcot International Gateway", "Epcot - Epcot Monorail", 25, "Walk", True),
    ("Epcot International Gateway", "Epcot International Gateway - Epcot Skyliner", 1, "Walk", True),
    ("Epcot International Gateway - Crescent Lake Friendship Boat to Epcot", "Epcot International Gateway", 1, "Walk", False),
    ("Epcot International Gateway", "Epcot International Gateway - Crescent Lake Friendship Boat to Hollywood Studios", 7, "Walk", False),
    ("Hollywood Studios", "Hollywood Studios - Crescent Lake Friendship Boat to Epcot", 7, "Walk", False),
    ("Hollywood Studios - Crescent Lake Friendship Boat to Hollywood Studios", "Hollywood Studios", 1, "Walk", False),
    ("Disney's Old Key West Resort", "Disney's Old Key West Resort - Green Flag Sassagoula River Ferry Boat", 10, "Walk", False),
    ("Disney's Old Key West Resort - Green Flag Sassagoula River Ferry Boat", "Disney's Old Key West Resort", 1, "Walk", False),
]

def clean_id(name):
    """Maps long strings to standardized Sub-node IDs."""
    mapping = {
        "Magic Kingdom": "MK_MAIN",
        "Epcot": "EP_MAIN",
        "Hollywood Studios": "HS_MAIN",
        "Ticket & Transportation Center": "TTC_MAIN",
        "Disney's Polynesian Village Resort": "POLY_MAIN",
        "Disney's Grand Floridian Resort & Spa": "GF_MAIN",
        "Disney's Contemporary Resort": "CONT_MAIN",
        "Disney's Fort Wilderness Resort & Campground": "FTW_MAIN",
        "Disney's Wilderness Lodge Resort": "WL_MAIN",
        "Disney's Pop Century Resort": "POP_MAIN",
        "Disney's Art of Animation Resort": "AOA_MAIN",
        "Disney's Caribbean Beach Resort": "CBR_MAIN",
        "Disney Vacation Club Riviera Resort": "RIV_MAIN",
        "Swan and Dolphin Hotel": "SND_MAIN",
        "Disney's Yacht and Beach Club Resorts": "YBC_MAIN",
        "Disney's Boardwalk Inn": "BWI_MAIN",
        "Epcot International Gateway": "EP_INTGATE",
        "Generation Gap Bridge": "GGB_MAIN",
        "Disney Springs Marketplace": "DS_MARKET",
        "Disney Springs Landing": "DS_LANDING",
        "Disney's Port Orleans French Quarter Resort": "POFQ_MAIN",
        "Disney's Port Orleans Riverside Resort": "POR_MAIN",
        "Disney's Saratogoa Springs Resort and Tree Houses": "SSR_MAIN",
        "Disney's Old Key West Resort": "OKW_MAIN"
    }

    # Check for direct matches first
    if name in mapping: return mapping[name]

    # Process suffixes for transit sub-nodes
    base = name.split(" - ")[0]
    base_id = mapping.get(base, base.replace(" ", "_").upper())

    if "Resort Monorail" in name: return f"{base_id}_MONO_R"
    if "Express Monorail" in name: return f"{base_id}_MONO_E"
    if "Epcot Monorail" in name: return f"{base_id}_MONO_EP"
    if "Skyliner" in name: return f"{base_id}_SKY"
    boat_colors = ["Gold", "Green", "Red", "Blue", "Purple", "Yellow"]
    if "Launch" in name or "Boat" in name or "Ferry" in name: 
        boat_ext = ""
        for boat_color in boat_colors:
            if boat_color in name:
                boat_ext = f"_{boat_color.upper()}"
        return f"{base_id}_BOAT{boat_ext}"

    return base_id

def has_premium_transit(resort_id, park_id, connections):
    """Checks if a non-bus connection exists between a resort and park area."""
    r_pref = resort_id.split('_')[0]
    p_pref = park_id.split('_')[0]

    # Define common gateway nodes for parks
    park_gateways = {
        "MK": ["MK_MONO_R", "MK_MONO_E", "MK_BOAT"],
        "EP": ["EP_MONO_EP", "EP_IG", "EP_SKY"],
        "HS": ["HS_SKY", "HS_BOAT"]
    }

    targets = park_gateways.get(p_pref, [f"{p_pref}_MAIN"])

    for conn in connections:
        f, t = conn['from'], conn['to']
        if r_pref in f or r_pref in t:
            if any(gate in f or gate in t for gate in targets):
                if conn['mode'] in [
                        "Resort Monorail",
                        "Epcot Monorail",
                        "Skyliner",
                        "Boat",
                        "Ferry"]:
                    print(f"{resort_id} has premium transit to {park_id}")
                    return True
    return False

def generate_busses(final_data):
    """ Dynamically create bus routes based on existing data. """
    bus_connections = []
    display_names = final_data['display_names']
    hubs = {"MK_MAIN":20, "EP_MAIN":20, "HS_MAIN":20, "AK_MAIN":20, "DS_MAIN":25, "TTC_MAIN":None}
    
    # Select resort MAIN nodes only.
    resorts = [node_id for node_id in display_names.values() if node_id.endswith("_MAIN") and node_id not in hubs]
    for resort in resorts:
        resort_bus = resort.replace("_MAIN", "_BUS")
        bus_connections.append({
            "from": resort, "to": resort_bus, "weight": 20, "mode": "Walk & Wait", "bidirectional": False
        })
        bus_connections.append({
            "from": resort_bus, "to": resort, "weight": 5, "mode": "Walk", "bidirectional": False
        })

        for hub, weight in hubs.items():
            # No busses offered from resorts to this hub (TTC).
            if not weight:
                pass
            elif not has_premium_transit(resort, hub, final_data["connections"]):
                hub_bus = hub.replace("_MAIN", "_BUS")
                bus_connections.append({
                    "from": resort_bus, "to": hub_bus, "weight": 20, "mode": "Bus", "bidirectional": True
                })

    # One-time creation of busses at hubs.
    for hub, weight in hubs.items():
        # No Disney busses offered to/from TTC hub.
        if weight:
            hub_bus = hub.replace("_MAIN", "_BUS")
            bus_connections.append({
                "from": hub_bus, "to": hub, "weight": 5, "mode": "Walk", "bidirectional": False
            })
            bus_connections.append({
                "from": hub, "to": hub_bus, "weight": 20, "mode": "Walk & Wait", "bidirectional": False
            })
    
    # Park hopper busses.
    parks = ["MK_MAIN", "EP_MAIN", "HS_MAIN", "AK_MAIN"]
    for i, park_a in enumerate(parks):
        for park_b in parks[i+1:]:
            # Parks are always connected to each other by bus (or other modes handled elsewhere)
            if not has_premium_transit(park_a, park_b, final_data["connections"]):
                bus_connections.append({
                    "from": park_a.replace("_MAIN", "_BUS"), 
                    "to": park_b.replace("_MAIN", "_BUS"), 
                    "weight": 15, "mode": "Bus", "bidirectional": True
                })

    return bus_connections

def convert_to_json(all_raw_data):
    """ Convert existing data and generate busses into one dictionary. """
    connections = []
    display_names = {}

    for data_list in all_raw_data:
        for u_raw, v_raw, weight, mode, bidirectional in data_list:
            u_id = clean_id(u_raw)
            v_id = clean_id(v_raw)
            
            # Populate display names for _MAIN nodes
            if "_MAIN" in u_id: display_names[u_raw] = u_id
            if "_MAIN" in v_id: display_names[v_raw] = v_id
            
            connections.append({
                "from": u_id,
                "to": v_id,
                "weight": weight,
                "mode": mode,
                "bidirectional": bidirectional
            })

    all_transport = {"display_names": display_names, "connections": connections}
    all_transport["connections"].extend(generate_busses(all_transport))
    return all_transport

if __name__ == "__main__":
    # Run the script
    final_data = convert_to_json([monorails, boats, skyliners, walks])

    # Output to file
    with open('wdw_graph.json', 'w') as f:
        json.dump(final_data, f, indent=2)

    print(f"Successfully converted {len(final_data['connections'])} connections.")
