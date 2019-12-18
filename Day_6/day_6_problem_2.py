''' --- Part Two ---
Now, you just need to figure out how many orbital transfers you (YOU) need
to take to get to Santa (SAN).

You start at the object YOU are orbiting; your destination is the object SAN
is orbiting. An orbital transfer lets you move from any object to an object
orbiting or orbited by that object.

For example, suppose you have the following map:

    COM)B
    B)C
    C)D
    D)E
    E)F
    B)G
    G)H
    D)I
    E)J
    J)K
    K)L
    K)YOU
    I)SAN

Visually, the above map of orbits looks like this:

                            YOU
                            /
            G - H       J - K - L
        /           /
    COM - B - C - D - E - F
                \
                    I - SAN

In this example, YOU are in orbit around K, and SAN is in orbit around I. To
move from K to I, a minimum of 4 orbital transfers are required:

    K to J
    J to E
    E to D
    D to I

Afterward, the map of orbits looks like this:

            G - H       J - K - L
        /           /
    COM - B - C - D - E - F
                \
                    I - SAN
                    \
                    YOU

What is the minimum number of orbital transfers required to move from the
object YOU are orbiting to the object SAN is orbiting? (Between the objects
they are orbiting - not between YOU and SAN.)
'''

orbit_map = [
    'COM)WWS', 'BYZ)LMV', '2CT)GV2', '6RK)HK7', 'RJJ)MVV', 'YFQ)4LC', 'Q58)D46', 'D4T)3X8', '9GF)P89', 'TFP)9VJ', '5J9)YYK', 'WKB)6B4', 'PM4)3G9', 'NRG)QDB', 'Y2X)464', 'T1S)MJ1', 'RQ8)PD6', 'XP7)3F2', 'Y4Q)65H', 'KBG)ZMM', 'PCT)H5K', 'YPG)NZ6', '1KP)RFT', '3Y7)ZN5', 'BYH)RWH', '1BQ)X8J', '1VJ)MWT', 'GHH)7NX', 'CWZ)WC1', '5YB)3F5', 'YZG)NQJ', '18F)VZV', 'Z6Z)ZX9', 'PT3)KWY', 'QR2)5QK', 'HQL)6LJ', 'JMG)S4N', '4RL)PWG', 'G1H)J8W', 'WCX)RB3', 'CR4)GX5', '4YN)BDT', 'ZQY)C8H', 'JRF)Y62', 'GPY)4RN', '6TF)R8Y', 'JWD)L9L', 'QQ5)ZMX', 'YY5)JFY', 'F15)JCJ', 'J71)ZT8', '9KF)JR8', '82X)449', '544)WKB', 'QRN)MKW', 'Y57)1KV', '2C2)6C7', 'QNQ)MKH', 'X1H)XK6', 'QBH)GKH', 'FMY)9P9', '7DZ)Q9L', '8HP)F3V', 'XR9)4XS', '9CP)25Q', '4PC)92N', '87B)C3N', 'FFW)1CY', 'DFH)3VC', '4RS)PM4', 'LQF)J6P', 'ZXM)1K7', 'WYZ)C22', 'K1Y)YMZ', 'KXV)P93', 'K4G)MYZ', 'RWM)VC1', 'T8S)93S', '21J)MHY', 'MF7)N4L', '255)BDL', '1MG)M4B', 'KJL)K7J', 'MLX)ZR7', 'WPN)LRP', 'DQ6)9XW', 'DMF)RJ3', 'JNL)QMM', '68T)QLS', 'NQ1)RP3', '18C)7DC', 'KRH)2RT', 'KGT)DPL', '99Q)SWR', 'KRP)DCW', 'Y3P)PCT', 'PZJ)2RN', 'FTY)R6J', '7W2)T32', '6ZZ)VZ3', 'DPL)7KV', 'VX2)NH8', '2QF)GS5', 'Q8S)SZ4', 'VP4)8B8', 'S6X)BYZ', 'RKK)QQ5', 'LYN)S7C', 'ZZD)ZTP', '59C)25M', '3SD)KPS', 'GPY)5LY', 'B6Q)9M6', 'SDL)SGT', 'VY6)J47', 'KY6)WMB', 'M3Z)CWZ', '287)6FY', 'JR8)5LP', 'DXG)8GP', '5GV)Q15', 'WQ3)65V', 'MHY)ZTD', '2KN)1LQ', 'FPF)7W2', 'NPB)6NL', 'T32)9TC', 'JTZ)YHM', 'VNT)QWK', 'GNZ)VBD', 'JCW)JRR', 'N2B)TVX', 'VF2)P38', 'V5Z)3W5', 'SST)9LZ', 'TRC)PYG', '9VJ)SSX', '8BD)TXH', 'WVM)XRV', 'Z5B)T93', 'Z5L)T7K', 'H1V)YOU', 'NKX)54Z', '4XS)DZK', 'D3V)S4K', 'Q62)FWW', 'SWD)DJT', '2MJ)MXT', '98J)17N', 'GDZ)YN6', 'DRP)4PC', '4L3)VNG', 'R7G)7M9', 'WX5)MFM', '2S9)BK5', 'N9H)FDR', '22T)Y3Y', 'L65)XLK', '3DJ)S18', 'S18)WHR', 'S1Q)GYH', 'BF9)99R', 'CDW)MB6', 'FF7)44W', '5X7)XSL', 'QG3)WC8', '6Q4)83D', 'LP6)NTH', 'V84)X6W', 'SGR)FFW', 'CVX)54C', '6KD)RML', 'KZV)JRY', 'KY5)W9D', 'L4N)38R', 'GVD)KXQ', 'RCK)XNX', 'XRV)TKH', '5JZ)G19', 'Q5V)7VD', 'FYK)2MQ', 'VKV)8ZL', 'YQM)6XF', 'DKB)SND', 'HMZ)689', 'W2S)2YB', 'SWR)ZZD', 'MGQ)TW3', '3Y5)HHP', 'DJT)H7L', 'VNV)HMZ', 'C11)PWB', 'M3Z)SZ2', 'DHF)QG3', 'J9D)LQF', '3LC)5YB', 'XQQ)DRY', 'HWQ)27J', '4W8)FMF', 'TN1)VXT', '3GJ)FFB', 'LRP)NPB', 'LR2)5ZR', 'ZLJ)5V4', 'KXN)5QM', 'TXH)T4W', 'VNX)9ZB', 'J47)FPC', 'D9Y)9M7', 'MKB)5VF', 'RMC)VQ3', 'SVL)Z1C', 'RGC)S44', '8G4)MZ8', '6XK)3HJ', 'R3V)FLX', 'M6N)Y81', 'RP3)YVK', 'C3B)PFW', '4LK)GR1', '1QQ)6CC', '76J)1KP', 'DYY)QYR', 'PBQ)7X8', 'VZV)F15', '9F2)ZJN', 'VBD)6B2', '6X5)WXY', '23D)SP2', 'TQ1)TFW', 'WM1)G1Q', '5V4)9NS', '2WJ)QQF', 'ZV7)PYK', 'MP4)5DD', 'YC6)KW8', 'SQ9)XZX', 'X5Q)6NH', '54D)2LN', '9NS)X5J', '7T8)SRT', 'V45)7TG', 'CL7)QDF', 'XV4)9GF', 'ZYQ)H8P', '5GM)M5Z', 'QYG)XLH', 'QLS)29F', 'TTB)J6F', 'LGZ)9L7', 'HTD)C3B', '7VD)3Y7', 'FLQ)GWK', 'SY9)PN1', 'BHB)MLX', '3X4)G43', 'CV3)DHF', '7DM)HFB', 'YM9)8W7', '3D9)CMT', 'SKV)64Z', 'DTY)GGD', 'HLV)71T', 'Z6Y)N6H', 'JB2)73Y', 'MVG)LGZ', 'VYV)463', 'JCS)24L', 'MCX)5TY', 'RWQ)9BS', 'HVV)H4L', 'CN8)8FJ', 'YS5)NY2', '7CX)67Y', '5JY)LFV', '3GQ)2K4', '433)KY5', 'FLQ)MQ7', '3FR)CSB', 'TW8)V5Y', 'TY9)5CG', 'PWZ)86Z', 'XTT)3GJ', 'TM5)X18', 'NNT)KZV', 'RX9)DJY', 'RQS)TN1', 'S11)TJ4', 'FTV)KBG', '9YC)VCG', 'B8W)H29', '5ZH)2V1', 'MFH)3MG', '92Q)M6C', 'XSY)QT2', '347)614', 'DLP)BF9', 'B1L)KRP', 'NKF)88J', 'DDN)P4C', '2RG)JKJ', '5GZ)Q8S', 'WJK)GTB', 'RQC)21J', 'J56)3GZ', '25M)SGR', 'P29)M1W', '3FZ)PXR', 'LLQ)RRJ', 'NLD)PW6', '9R7)Y4X', 'JCC)6ZZ', '96D)1MF', 'TZV)JJ7', '2RN)Q48', 'Z7G)GD9', '85F)JWD', 'PFW)L9K', '6TF)S7G', 'DV4)9R7', 'Z9X)R9X', 'DXD)M6N', 'KWS)DPK', '1R6)Q58', '1B2)4LT', 'D9M)L4Z', 'JKJ)K4V', 'P36)V7J', 'GTZ)W24', 'GX5)MZ4', 'H73)QMT', 'VNG)4SZ', '9TV)BD2', 'CG6)SNS', 'WD1)HTT', '9R3)4L3', '7KV)96D', '8HW)QHV', '85K)HML', 'B77)BFL', 'RMB)3WP', 'MVC)B84', '6LJ)N3J', 'VPH)4NG', '14Q)23D', 'PCB)H1K', 'RRJ)9KY', 'W24)VHN', 'RDN)S54', '7ZS)C28', 'FWZ)FRW', '7JQ)NNY', '492)CG6', 'NWC)ZZW', 'JF2)YY5', '6B4)5KN', 'LZY)JTZ', 'P3V)4D7', 'NVT)1MG', 'SGT)P2M', '2NX)WJJ', 'K6L)64P', 'KXL)X7Z', 'R2D)NPQ', '33H)P62', '7SL)HF4', 'FYF)GKD', 'NT5)XN9', '6TL)BVZ', '5YK)K4B', 'XDG)347', 'B2P)8BF', 'B5Y)8NZ', 'DDC)TW6', 'GY6)XYL', 'T7D)D1Q', 'MXJ)6D6', '6NG)P3P', 'XSQ)D4T', 'HY9)RMB', 'K6L)ND1', 'RHL)MKB', 'KRH)QB7', 'SMS)BBM', 'DCW)GG2', 'SMZ)1SY', 'ZVP)C53', 'CJJ)ZRB', '3VC)RFC', 'F3V)713', '9KM)83Z', '18C)22W', '7R9)RCX', 'QMT)Q1R', '1VW)J8N', 'VSD)FWZ', 'W61)RMC', 'NQ4)Z61', 'LTN)KVP', 'YYK)V5S', '1GP)7W6', 'BJW)RQJ', 'FRW)5JZ', '1JF)KTT', 'ND1)N6L', '69L)R48', 'TW6)NZC', '6VG)RCM', 'FQR)5Z9', 'JTD)G9N', 'SDY)5T3', 'S33)925', '1SY)9SY', 'QF6)964', '2ZH)BTK', '1GC)22S', 'DJT)FCD', 'SKD)K79', 'VG1)QRQ', 'S7S)346', '8GP)YZG', '25R)1QQ', 'G4G)RWM', 'BHW)4JF', 'DHG)S1S', 'NJP)L5Z', 'ZTP)V5B', '2K4)8HK', 'RPQ)KRH', 'VXT)8TN', 'BVZ)P3T', 'HQ8)5GM', 'C22)PMP', '2B2)RH7', 'PWG)QWH', 'B45)VP4', 'RSR)WLL', '2RT)1D2', 'V5Y)ZGH', 'N3W)ZR9', 'N46)MD5', 'CMT)D19', 'YNF)7CZ', '294)ZV9', 'K4B)NPK', '5LP)CXN', 'BY9)6DF', 'NZ6)2QM', 'LRJ)Q25', '9ZL)G5B', '9VF)GLK', 'VH8)KJL', 'PWM)W5W', 'Z61)3SD', 'FWZ)1VX', 'YMZ)4V7', 'LP7)WZF', '3TC)BBV', '6QK)58C', 'W6T)ZCM', 'LMV)3SG', 'RXW)X9C', 'FB3)QXV', 'SFF)54D', '9V5)VDX', 'ZCX)HR1', 'J6F)9CT', 'S7C)FSD', '565)YTK', 'GW5)WSN', 'JMG)VKV', '83Z)MLH', 'FH1)HJ3', 'Y3Y)CDW', 'WJ8)Y4Q', '54C)GYZ', '46L)4F9', 'M9B)H6Y', 'C97)86G', 'T7D)BHW', 'SFQ)H2J', 'Y3W)M44', 'G1Q)MXZ', 'M6C)WWR', 'J76)4JB', 'H2D)85F', 'PT6)9VF', 'KK9)6K7', 'FM1)QVX', 'QX7)7X1', 'X5D)1J2', 'YXG)VMD', 'VHP)FTY', 'P62)X6M', 'XBT)V45', '2PP)GHP', 'BD2)8BD', 'HCS)59C', '38R)VF7', '7NX)SQJ', '9YX)1GX', 'W92)PDC', '3TH)WFL', '2P8)W6T', 'H85)693', '9NL)CJY', 'P2M)TRF', '35P)8VZ', 'R2G)2XZ', 'DRG)LGS', 'XBC)7JQ', 'LH1)QNQ', 'ZR7)ZXG', 'B5H)S1Q', 'YG1)LTN', 'LLY)74V', '4RN)Z6Y', 'P9R)17B', 'TFW)N4Y', 'HLS)JZL', 'XC8)R7L', 'Z4Q)B5H', '6NL)V63', 'Y5S)T9X', 'F72)JHN', 'PDC)DD5', 'XF4)RXW', 'QDF)2B2', '45M)4J1', 'WXY)YL8', '17N)DRL', 'L9K)TDM', '5NN)84K', 'J6P)SG1', '3L2)366', 'RVX)WD1', 'RML)TNL', 'WJC)7D7', '3Y5)DLP', '2XZ)9R3', 'YL8)H3V', 'WW7)NT5', 'WP9)9MZ', '5GQ)G1H', 'BR6)ZG6', 'F48)QF8', 'J8H)L57', '3HJ)6KD', 'S4M)J9H', 'P3T)DR2', '5BP)DYM', 'SHH)JTD', 'TKT)BJJ', '9KW)LRC', 'SGT)Y8D', 'ZXG)9CP', 'BSF)LD6', '86G)ZD4', 'NMS)H71', 'WFH)SP5', '5LY)3BB', 'XJT)51Q', 'P6P)SMS', 'WMB)L23', '1GX)C34', '2MQ)4R5', 'T66)FPF', 'ZZ8)6T8', 'Z88)PBQ', '2MS)X1H', 'MYZ)98J', 'Q48)JD3', 'CSN)8J5', 'XVZ)M6S', 'FHF)HTN', 'HCZ)D3V', '9JZ)SDL', '38P)HQL', '9J9)CJK', 'MPM)M92', 'N1X)B6Q', 'ZN5)JW8', 'JG6)3RK', 'R2G)TJ3', 'SKD)HLT', 'W8R)GBT', '58C)RGC', 'ZCM)26D', 'MKM)5BP', '71T)M1Z', 'C2M)KNC', 'SZ2)2YX', 'XJX)4B3', '2BK)76J', 'XQ6)FZV', 'VNK)4RS', '7MQ)RMS', 'FCD)34C', 'TF3)L4F', '23D)XJ2', 'W87)62T', '25M)QNS', 'DDS)VG1', 'F17)SH4', 'LL6)5T2', 'JYP)DFH', '5NN)V2X', '4R5)Q5V', 'Q25)Z8H', 'K6Q)BDR', 'R2K)PZJ', 'FP7)2S1', 'KMN)3VW', 'ZT8)H9X', 'W33)43Y', '758)R7G', '8QB)6LC', '6LC)MHQ', '88J)GLF', 'H1K)N12', 'BTK)DMF', 'ZG6)TFR', 'ZPZ)8TT', 'DJY)LSZ', 'S1Q)FY1', '74K)MVC', 'B34)9BH', '5BP)W1Z', 'N3W)TLS', '1J2)43R', '9PG)HLS', 'Q74)8M5', '2GH)6VG', 'Z5B)B45', 'L5Z)433', 'JFC)ZKY', 'VC1)HT7', '229)GW5', 'QF8)FTC', 'YB8)THG', '55B)27V', 'DF4)J9R', 'R7J)2FL', 'N15)H5C', 'RZN)5N3', 'B8C)WBW', '7M9)VN2', '8T1)7DM', 'VN9)5KR', 'FYJ)SKV', 'MVG)1VL', 'GRG)ZK2', '7HH)3S1', 'Q85)9PG', 'BGZ)MK7', 'H39)P3V', '6CF)FLQ', 'PK6)VYV', '9MN)6NP', 'FY4)PQJ', 'CR4)LH1', '7RL)RSR', 'JRY)1W6', '6RV)R11', 'MTV)VSD', 'N26)LWB', 'C4F)3X4', '9BK)LK2', 'PB3)WQB', 'JKJ)NWL', 'BDL)KBT', 'K35)9F2', 'WXN)1RD', 'FK9)XBT', 'FZT)34D', '5SL)B34', '6XK)CDV', '7XH)7PC', 'YHM)6VR', '7DC)X5D', 'FL1)3GQ', '7FM)67R', '6VG)XQQ', 'W1Z)2JK', 'Y1V)GZS', 'R5J)6JY', '4YL)ZW2', 'H2F)7CX', 'VXQ)HYQ', '65V)3CP', 'KTT)WW7', '6V7)T8S', 'LFR)LP7', '5CG)GFB', 'VCG)LCY', 'KWY)C48', '2YX)JG8', '73Y)6F1', 'QJT)DGK', 'VJB)Z7G', '8NZ)CDB', 'GXW)18C', 'WVM)JSX', 'XLK)9KF', 'JTD)PT6', '8G3)TJ9', '67R)YZH', 'J7G)5VG', '4JB)5GK', 'R6P)7HH', 'X7Z)N8X', 'LDL)294', 'H2J)T11', 'DZK)XTT', '8VZ)HWQ', 'DZ2)GKV', 'NTX)FP7', '2JK)TTB', 'FS9)22T', 'X6D)DC3', 'LK2)CS3', 'ZNQ)RPM', 'TW3)BK4', 'MLH)NWC', '2WN)RVX', 'M16)BJW', 'FDR)K6L', '7T8)ZWX', 'RPM)4LK', '3F5)BZT', 'TKK)KJ8', '6CR)C5V', 'XHY)X9T', 'ZG9)VFJ', 'D5Z)S82', 'HJ3)1GP', 'JD3)BB2', 'ZKY)6RK', '9M6)175', 'XM7)KSZ', 'ZZN)R2F', '5T2)VY6', '1NY)878', 'GS5)B61', 'MNS)N6Z', 'MVF)P74', 'LR9)PXG', '572)229', '9GD)HSL', 'S4N)XBC', '283)TRC', 'SC1)ZCX', 'HLT)MSD', '9M6)SFQ', 'SJD)RBR', '7F7)RPQ', 'PYG)BPR', 'X6M)RSH', '35P)VSJ', 'CXN)4QX', 'GWG)KZQ', 'SWL)DKK', 'QHV)1B2', 'BSC)H2D', '1K8)B3G', 'Z78)LPF', 'K5Z)7DZ', 'BXR)HBQ', 'T8T)LNW', 'Y2V)3Q9', 'BPR)HCS', 'TDM)DHS', 'MKH)1NJ', 'T3N)VF2', 'GNH)BKP', 'MQ7)74K', '4NL)YB8', '449)LV3', 'NXG)WD4', 'TXX)3L2', 'PMM)TD9', 'PYK)1NY', '9MZ)CHL', 'K79)RL1', 'F3V)XHY', 'MXM)FYF', 'V2X)SZR', 'ZZN)XBJ', '2P5)XH9', 'XYL)4XL', 'P61)MMF', 'NWL)P9R', '2DQ)1VJ', '2G6)2MS', 'B45)GRG', 'BB2)JC9', 'H3J)LLQ', 'TD9)NJP', 'PQJ)MT7', '5R9)2BM', 'RFD)WB8', '8SP)WGJ', 'SDC)RY4', 'ZTJ)PT3', '4PQ)VNX', '5ZH)BFW', '27J)Q62', 'SG1)XQ6', 'CHT)6NG', 'WYV)7FM', 'TF9)ZP4', 'K8C)L4N', '86G)VQD', 'GBG)FFH', '5N3)TF3', '5KR)WQQ', 'ZLY)KB8', 'CR2)TCV', 'ZWX)KMN', 'DL8)MGQ', 'PCL)L6H', 'B1Q)T2G', 'VNY)WTY', 'NGL)JBQ', 'HTN)YML', 'F8S)L4V', 'MWR)Z9H', 'ZGH)7ZS', 'RJG)QMB', '35R)CR2', '9PD)P6P', '9BH)J56', 'K9G)P41', 'K7F)WMP', 'SYM)K26', 'XF3)BQF', 'RY4)N75', 'XRQ)3NN', 'X8J)5SL', 'W6V)ZHV', 'Y3P)M14', 'CS3)JRF', 'LQJ)LYN', 'V5Y)BRW', '8J5)GHH', 'HFB)JF2', 'V63)3YQ', 'GPX)572', '6GD)7F7', '8HK)B8W', '68Y)QGR', 'ZK2)VL1', 'QMM)J7G', '198)38P', 'WTY)8RC', 'WFL)QV2', 'K6B)TXX', '3F2)QF6', 'QDF)TQL', '22T)3KS', '8BH)2P8', '7WP)VV3', '3TH)HM1', 'CDB)F8C', 'SMZ)M5J', 'MWJ)4FL', 'X4J)8SP', 'H71)WZC', '356)1HX', 'Y9Z)RLR', 'M1Z)SDC', 'L9L)RDN', '9PD)GNB', 'DGK)9TV', 'DD5)Q5F', 'XR5)6TF', '6NH)SF8', '8ZL)SQ9', 'FFH)K5L', '6D6)36R', 'N7P)5Z3', 'CDV)BPY', 'FKR)DTY', 'J8W)1S2', 'F7M)HLV', '17B)XVZ', '9CT)XHF', 'XL4)GNZ', 'XZX)M16', '1GB)MVG', 'C92)K5N', 'Q2W)VLT', '54N)S7S', 'GWK)T1D', '6VB)3V6', '24L)BMT', 'VN2)N2G', '9RX)SDY', '7ZC)4RL', 'LN5)PK7', 'BB9)TB5', 'W4Y)NC8', '3SG)PKC', 'SNS)Q9N', 'JK3)FB3', 'HK7)QWB', 'MJ4)TQ4', 'GWP)RQT', 'T4W)9RX', 'TD9)9ZL', 'XF3)FYT', '4LC)KLH', 'X6W)69V', 'WJJ)T52', 'QB7)G8R', '1W6)WQM', 'QW7)FMY', '6GR)1QM', 'ZMM)9GD', 'ZV9)9YX', '1NJ)HTK', 'XN9)P1R', 'G8R)D12', 'FPC)XSY', '6DF)WPZ', '87M)ZG9', 'QV2)DKB', 'H5C)GDZ', 'BDR)W2S', 'C53)3D9', 'L4F)VB5', 'V5B)3MR', 'PZJ)T99', 'FFB)LRJ', '9HZ)G1Z', 'BBV)2GH', '65H)Y9Z', 'X4J)CHT', '3X8)FLB', '3F3)T7D', 'W7Q)9M1', 'ZT4)FPP', 'Q5F)QYG', 'FTV)86Q', 'JQ5)L95', '53H)RH9', 'PN1)94Z', 'MT7)3NM', 'DKD)YRQ', 'DR5)CVK', 'LXT)T3N', '1D2)RQC', '1BK)G87', 'G95)JK3', 'P3P)4FP', '8DH)TKT', 'F2K)L1Z', 'KNC)N1P', 'PW6)RX9', '4SZ)GF8', 'YVK)2BK', 'WHR)6RV', '8PS)DZ2', 'KB8)Z3Y', '4FP)XP7', 'Z5Q)46L', '6C7)544', 'VJ6)SK8', 'VL5)L65', '8BF)VZX', 'S4K)QW4', 'M4B)G3W', 'X33)VVD', 'WSN)GBG', 'SP5)YXQ', '4XL)84M', 'W5W)Y1Q', 'S82)68S', 'HNN)GPY', '6LD)X5Q', 'FPF)JVL', '1CY)3Y5', 'D3F)S6X', 'WJ8)2WN', '26B)YL7', '4NF)NDC', 'Q15)PSF', '52T)FM1', 'VHN)9V5', 'MSD)TWC', '7D7)KYK', '175)J71', 'L4Z)HY9', '4HR)BSF', 'ZMY)TJC', 'RCM)QRN', 'HBQ)XJT', '64P)ZXS', 'QDJ)6GD', 'J71)NSN', '3WP)3TH', 'NPK)Y6M', '6XF)4ZL', 'QT2)MWR', 'N75)WYV', 'GFB)S29', '62Z)9NL', 'DXS)GWP', '71H)2CT', 'JWD)FWM', 'MK3)GVD', '9M1)442', 'SRT)D8M', 'BRW)P4H', 'M4H)9BV', 'ZVD)5GZ', 'WXP)X33', 'LPS)Y3P', 'R9D)RVH', 'NL6)Y1V', 'N53)WQ3', 'SK8)FS9', 'DY8)52Y', 'D75)CWF', 'Q9L)VJH', 'H4R)KXN', '4NG)P29', '74G)Z67', 'GX5)NVT', 'DHS)ZLY', 'LM3)ZYQ', '9P9)255', 'KBT)JCS', 'CVK)Z9X', 'TCW)F8N', 'HJY)LC8', 'KW8)K17', 'F82)WYZ', 'D3P)ZVP', 'SJX)NGL', '74V)R2K', 'LWB)R9D', '14J)71N', '9BS)43Z', '8GP)3F3', 'QMB)RDW', 'DR1)RWQ', 'GY7)BXR', '255)RHC', 'XLJ)3R3', 'P9C)NMS', 'KB8)5S5', 'KLZ)RMG', '1WZ)XLJ', 'W1Z)284', 'XJ2)DL1', 'N58)XDG', 'HYD)B5Y', 'NDC)RKK', '4FL)XSQ', 'CDL)Q85', 'C62)WF5', '94C)DVP', '84T)2YY', 'ZTD)PJP', 'S82)DKD', '6VR)CBC', 'M6S)W33', '949)MFH', '4R5)SWP', 'J98)XZ7', 'F8C)JCW', 'BHX)18F', 'WC1)KGT', '9XW)Z2L', 'TCW)84X', 'ZCV)5T7', 'K6Q)3NT', 'Q9N)FSS', '8TN)VKD', 'XF4)G56', 'J5C)LDL', 'D46)CGG', 'TJ3)96V', 'T5H)D8Y', 'YMN)QJT', '1QM)F2K', 'RWH)KXL', 'T52)79Y', 'FSD)KXV', 'XNX)6CR', '713)3TC', 'NLF)4LR', 'KY5)H4R', 'CWF)2CD', 'X9C)2S9', 'ZX9)ZQY', 'JFY)K7H', '5HT)Z1L', '9TV)HYD', '8RC)C77', '8MJ)3XG', '5L7)7RL', 'VB4)DV3', '3Y3)7WP', 'HHP)5GQ', 'XH9)2PP', 'VF7)GWG', 'BPY)7ZC', 'LHY)YNF', 'PPS)WVK', 'ZHV)JQF', 'TKH)B2P', 'QRN)3FZ', '8B8)S7K', 'T7K)SJD', 'S7K)YGQ', 'J8N)R7J', '4FL)7XD', '648)71B', 'G56)MPM', 'P38)68T', '5H7)5B9', 'TWC)PB3', 'XRV)FK9', 'WWR)KK9', 'XK6)F2Q', 'FYT)7T8', 'N85)54N', '8DZ)45M', 'G2F)92Q', 'LCY)ZZ8', 'PLD)LM3', 'RQJ)4WJ', 'J6L)315', 'Y6M)KY6', 'C53)3DB', 'MWT)Y8S', 'Q62)H2F', '6T8)B1J', '43Z)5P4', '1HX)M8B', 'TVX)84T', '2YB)Q68', '36R)V6Q', 'T9X)YG1', '2YY)NQ1', '5YP)GFM', 'QM9)J8H', 'JG8)16C', '5VG)N9H', 'M16)JST', 'RJ3)HR2', '29J)N6Y', '44W)VJ6', '9M7)F96', 'Z67)3RW', 'WLL)NTX', 'CSB)4CL', 'CWP)GGC', '84K)W7Q', 'QNQ)N25', 'NWR)CSN', 'J9H)PG5', 'DFW)K4G', 'FTC)68Y', 'VF7)4W8', 'VXT)2NX', 'G5B)FH1', 'DKK)DRG', 'C77)DJ1', 'VZ3)XD3', 'JVC)NRG', 'FLB)SHH', '71T)MP4', '9NL)VNV', 'RDQ)RJJ', 'GVN)ZT4', '84T)MF7', 'ZP4)4YN', 'WT2)3LC', '4D7)4NF', '5S5)9J9', 'MB6)N9N', 'MN3)B99', 'BFL)4XV', 'BN3)688', '5NJ)DPN', 'XK6)C92', 'D8M)KWS', 'RPV)W5S', 'GX8)FTH', 'VCT)6Q4', 'FWM)RDQ', '86Z)1M5', '46L)JNL', 'BX1)1R6', 'DV3)DXQ', 'JJ7)XFL', 'K5L)7MQ', 'X9J)SJX', 'NNY)MN3', 'RH9)3DJ', 'GG2)C2M', 'JR8)KLZ', '8M5)2SN', 'H9X)BYH', 'R48)ZZ2', 'YGQ)55P', 'BZT)MXJ', 'N2G)VQJ', 'VQD)NWR', '714)565', 'Q6W)27Y', '3NW)NL6', 'H6H)F5C', '4JF)YM9', 'D3L)T6S', '5QJ)QDJ', 'QYR)74G', 'HTT)VB4', '9L7)G2F', 'VVY)BR6', 'G43)BSC', 'M8R)S3F', 'QF6)DCN', '2C2)38G', 'BK4)VL5', '6K7)6H7', '5TY)96L', 'JF2)R2G', 'FLX)7R9', 'FFX)2MJ', 'M14)C97', '34C)Q6W', 'HF4)W8T', 'K7J)TF9', '464)4NX', 'MKW)6VB', '1S2)YPG', 'JK3)1JF', '6ZW)WJ8', '38G)XNL', '7F7)WXP', 'JST)2ZH', 'LNM)N26', '925)GC9', 'H29)LHG', '5B9)K1Y', 'ZD4)RH3', 'NY2)M1R', 'HF4)2G6', '4L6)FKR', 'H2D)2KN', '48L)7SQ', 'S1T)4YL', 'DJ1)XL4', 'B84)1RM', '92N)SY9', '7X1)MJ3', 'X32)WVM', 'TJC)Q1T', 'YTK)MWQ', 'WB8)ZV7', 'H5K)6LD', 'B66)1BQ', '4LB)D3F', 'Z3Y)SQB', '5Z3)2P5', 'X6L)BNH', '7DR)TQ1', 'SDC)JY4', 'RPC)SST', 'DXQ)WCX', 'WH3)YC6', 'JTZ)DYY', '9TL)QW7', 'LRP)758', 'TLS)Y2V', 'K5N)D75', 'MWQ)BX1', 'TRF)VLZ', 'DYM)PCL', 'JQF)9T7', 'D12)JG6', '3DB)NQ4', 'VKD)8BH', '7XD)WM1', 'T99)RKQ', '4LJ)RHL', 'P4C)K66', 'TWX)4TX', 'SY9)VJB', 'L6H)MVF', 'LV3)1FB', '71N)2PL', 'VFJ)F82', '116)95T', 'VSJ)LR2', '6CC)W8R', 'R84)HNK', '4TX)YWC', 'HTK)82X', 'P6P)B1G', 'Z4L)X9J', 'WVK)HNN', 'BQF)X6L', '734)6V7', 'LY2)HVV', 'Y8D)S1T', '1SN)4LJ', '3KS)6BX', '797)GY6', 'HR2)P6J', 'NQJ)C4F', '3NT)3FR', '2PP)Z5Q', 'F8N)8TY', '3GZ)4LB', 'BJJ)33H', 'LFV)QL2', 'TJ8)P9C', 'QWH)JQ5', 'KJ8)4KV', 'C7W)S33', 'Y4X)FTV', 'Z2L)JFC', 'B77)5QJ', 'N8X)CDL', 'RQT)HYC', '71B)D9M', '2LN)LGF', 'YKR)3MX', 'H6Y)116', 'X5J)LBS', '2BY)385', 'N6Z)C98', '5GN)9KW', '9TC)RQ8', 'LPS)RBD', 'T32)YMN', 'W3J)Z6Z', '7CZ)NRV', 'MGQ)DXS', 'HQK)2DV', 'HNW)8ZC', 'D3L)SYM', 'H3V)F84', 'VL1)BY9', 'LK9)HTD', 'VHQ)WX5', 'DR2)W6V', '3MX)2BY', '2PL)5GV', 'V5S)R5J', 'JLB)FL1', 'TQL)YQM', 'SWP)2DQ', '29F)8DH', 'W7W)H39', 'WGJ)5NJ', 'FQR)P36', 'PG5)DY8', 'WZC)F2V', 'ZJN)Y2X', 'P6J)N46', 'RSH)5X7', '7K2)PC9', '1WY)LDR', '3X8)H3J', 'R7T)LLY', 'Q1T)QRM', '9M7)K8C', 'R2P)V43', 'NRV)GKT', 'SQB)198', '2DK)Y5S', 'JVL)9BY', 'WPZ)LR9', 'ZXS)2VP', 'GY6)JJ6', 'XD3)3NW', 'XNL)4N5', '86Q)YKR', '2FL)1K8', 'F2D)PSP', '16C)LY2', 'TCV)TCW', 'JSX)71H', 'S29)W7W', '96L)VX2', 'YWC)C62', '68S)99Q', 'MZ4)2MX', 'WCX)9TL', 'D19)C11', '9SY)NNT', 'K26)RQS', 'YML)SMZ', 'K58)6X5', 'W1B)M4H', '3XG)J2R', 'PMP)V84', 'Q25)CN8', 'QWB)K58', '284)9BK', 'RCX)2C2', '1SQ)N3D', 'RFD)TWX', '5F6)VN9', '22W)WXN', 'QNS)JBB', 'GKT)TKK', '1WZ)DXG', 'QZL)VVY', '9BK)5YP', '1VX)X32', 'KZQ)5JY', 'DCN)F8X', 'Y6M)N58', 'ZP4)JLB', 'N9Q)8QB', 'VL1)QBH', 'LYN)8M7', 'V6Q)RZN', '2FL)DF4', 'F48)TNH', 'MXZ)GXW', 'M92)YLD', 'MSD)CWP', 'F9P)FQR', 'W8T)R7T', 'RDW)TY9', 'HNK)SVL', 'T3R)JWR', 'XLH)MBV', 'KLH)V5Z', 'WF5)Y3R', 'GR1)8RT', '132)DR1', 'HTT)4HR', '27V)8HW', 'FSH)WT2', 'X9J)5YK', '1RM)PTQ', 'DVP)F72', '5Z3)BB9', 'VQ3)WFH', 'QDB)X3S', 'F1C)S4M', 'MK7)PWZ', 'YL7)Y6R', '961)WQ4', 'GZS)1GC', 'ZRB)CR4', '62T)BGL', '4KV)XRQ', 'GNB)62Z', 'F9P)TJ8', 'T93)8DZ', '94G)5GN', 'ND1)NKX', '3NM)K6B', 'QRQ)MK3', 'GTB)DXD', '2CD)XC8', 'X6M)J9D', 'CBC)5MV', 'JCJ)VNT', 'XBC)RFD', 'GFM)HNW', 'DGK)8B5', '346)7XH', 'GF8)GD5', 'X53)85K', 'GD5)PMM', '83Y)JB2', '5Z9)ZXW', 'BJJ)H85', 'XR5)KGW', 'Z9H)YFQ', 'F58)HPW', '9M1)RCK', 'VV3)3YX', '36M)W61', 'KDR)1SQ', '3G9)D3P', 'CGG)FHB', 'PKC)3Y8', 'JJ6)VPH', 'FSS)ZCV', 'Z2L)3P9', 'XLJ)R3V', 'P93)KQQ', 'K17)JCC', '7DM)TZV', 'N12)XMC', 'V7J)MJ4', '64F)83Y', 'S7G)98Y', '84M)LSD', 'KWN)QR2', '3W5)F7M', 'ZW2)QPD', 'XFL)9MN', 'MW6)LK9', 'PMP)XF3', 'X9T)N9Q', 'CSN)14Q', '3Y8)GY7', 'DRP)GPJ', 'LGS)XM7', 'RBF)QZL', 'VLZ)Z88', '95T)P61', 'N6H)FHF', 'WMP)DFW', 'N6Y)87B', '27Y)F8S', 'QD6)WJC', 'WD4)J5C', 'PD6)WGH', '4LT)RJG', 'LPF)BHX', 'JBQ)D3G', 'THG)CVX', 'QWK)G1G', 'WWS)5HT', 'D3G)PCB', 'RMS)FSH', '689)69Y', 'LSZ)F1C', '315)FY4', 'HYC)N7P', 'G19)MW6', '6F1)QX7', '6JY)DHG', 'FWW)F9P', 'F2Q)7D5', '83X)LL6', 'NH8)WT9', 'XTG)WP9', '4B3)MKM', 'WQB)TW8', '169)R84', '4CL)M8R', 'ZRB)N2B', 'LD6)Y57', 'L57)B1Q', '8RT)LN5', 'MJ3)9DW', '5MV)55B', '3Q9)VHQ', 'R8Y)F2H', '614)734', '22S)FF7', 'W5S)4L6', 'JHN)6ZW', 'LDJ)VH8', 'T11)GVN', '2VP)FZT', '6H7)2QF', 'SDL)VCT', '94Z)5J9', 'TDH)FYJ', 'R6J)F2D', 'KPS)T8T', 'L6H)HQK', '5ZR)14J', 'HML)648', 'M1W)Q2W', 'MVV)169', 'QPD)CV3', 'QVX)LHY', 'WC8)RLH', '51Q)8T2', '8GF)J76', 'W92)PPS', '96V)R6P', 'ZZ2)WPN', '442)92Y', '2S1)K35', 'TB5)7TM', '43Y)949', 'F2H)JMG', 'K4V)DQ6', 'JY4)R3X', 'GD5)7KF', 'MZ8)DRP', 'BK5)KDR', 'CJK)HQ8', 'Y88)WJK', 'GLF)H73', 'PSF)94C', 'Y79)17K', 'LNW)LDJ', 'TNH)N15', 'MBV)K9G', 'VB5)SAN', '6X7)RPV', '54Z)SFF', '3P9)R2P', 'YLD)961', 'GPJ)PK6', 'M5J)BNZ', 'N3J)8CH', 'YXQ)PWM', 'TNL)KL2', 'JWR)D5Z', 'Z8B)N53', 'QRM)WH3', 'N1P)36M', '714)64F', '92Q)W49', 'GGD)8HP', 'PK7)FLN', 'K7H)CKT', '9V5)DDS', 'Y8S)R2D', 'F8X)N3W', 'S1S)DR5', '99R)4NL', 'R3X)5ZH', '79Y)8V7', 'V43)1B9', '2S1)H6H', '8TT)9PD', 'PXG)7SL', '9DW)DGZ', '7X1)F1F', '3V6)YXG', 'QKF)HJY', '2DK)2FC', 'SQJ)DDC', '4LR)S38', 'MJ1)KTK', 'J9R)F48', 'Q1R)F58', 'FTY)QKF', 'P1R)1WZ', '34D)XTG', 'QY8)LXT', 'MT7)Z4Q', 'SXQ)Q74', '8B5)BN3', 'HVV)XF4', 'TJ9)W1B', '64Z)NXG', 'BFW)9KM', '2QM)35H', 'NPQ)X53', 'NGL)VNY', 'F7M)J6L', 'M8B)W87', '3CP)LPS', '4QX)1RL', 'BKP)D9Y', '8W7)FYK', 'Y62)3Y3', 'Q68)6X7', 'CJY)35R', '8V7)ZPZ', 'L4V)B2T', 'FLN)1VW', 'S38)83X', 'RH7)9JZ', 'TQ4)6B3', 'P89)MCX', 'SP2)RBF', 'ZMX)DL8', 'BMT)6LB', 'PXR)1GB', '8ZC)B8C', '3BB)MXM', '43R)W92', 'Z8H)8GF', 'LSD)1KD', 'GD9)VHP', 'GHP)356', 'KZY)Y3W', 'GC9)JYP', 'FZV)5L7', '1RL)2DK', '35H)XJX', '5GM)C7W', '5DD)ZTJ', '6LB)SC1', '693)T3R', 'FY1)4PQ', 'QL2)TMP', 'DGZ)ZXM', '1B9)T96', '43Z)492', 'C98)Z5B', 'L95)K6Q', '3MG)YS5', '366)ZJJ', 'B6P)XV4', 'J6D)TM5', '6NP)Z8B', '4XV)53H', '4B3)SWL', '1VL)CJJ', 'F2V)5NN', 'XBJ)DDN', 'B3G)W3J', '7TG)KZY', '4V7)VNK', 'W9D)9YC', '4J1)VZ6', 'M5Z)94G', 'Y1Q)DV4', 'KZY)ZLJ', '7KF)TSB', 'GKH)JVC', 'FLB)1SN', 'DRY)8PS', 'WT9)T5H', '69Y)8G3', '7G4)S11', 'QQF)QM9', '8FJ)1BK', 'HSL)TFP', 'LHG)LZY', 'VJB)2WJ', 'XSL)GX8', 'P74)XR9', '2V1)52T', 'WGH)69L', 'L1Z)J98', 'VNV)HCZ', 'NG6)NLF', 'RBR)X4J', 'X18)35P', 'LBS)HK3', '7TM)NG6', '1RD)25R', '6BX)29J', 'BNH)VF1', 'QXV)797', 'M1R)X6D', '3R3)6CF', '7D5)1WY', 'MHQ)B6P', 'MW3)XZK', 'G3W)LP6', '16C)NLD', '9ZB)SXQ', '2MX)K5Z', '3Z2)7K2', 'JLP)CL7', '17K)VXQ', 'FFB)G91', 'RFC)48L', 'TMP)9HZ', 'T6S)Y79', 'DVP)283', 'CHL)QD6', 'ZJJ)LFR', 'R2F)N85', 'HT7)KWN', '3YX)W4Y', 'BGL)K74', '5T3)287', 'Z1L)ZNQ', 'C28)MW3', '385)MNS', 'GGC)6FJ', 'YRQ)8T1', '5F6)Z4L', '8TY)5R9', 'LC8)132', '688)BHB', '55P)TDH', 'K74)GTZ', 'VZX)714', 'N1X)2RG', 'MMF)26B', 'DV4)G4G', 'R9X)Z78', 'RVH)B66', 'LSZ)XR5', 'TC1)6XK', '98Y)LQJ', '83D)BWG', 'NC8)D3L', 'BDT)6GR', 'SH4)SKD', '7SQ)T1S', 'NKF)87M', '5KN)FFX', 'DFH)TC1', '8T2)F17', 'D8Y)5H7', 'C34)H1V', 'HM1)ZZN', 'N25)T66', '3VW)GNH', 'RL1)N1X', 'YN6)5F6', 'GKD)1JZ', '18F)JLP', 'PQJ)6TL', 'Z78)MTV', 'BBM)ZMY', 'B1G)Y88', 'JC9)NKF', 'QNS)7DR', '463)8MJ', '3MR)GPX', 'ZXW)PLD', 'BF9)7G4', 'ZKY)Z5L', 'QGR)MWJ', 'NSN)SWD', 'C5V)3Z2', 'VDX)M3Z', 'ZR9)K7F', '2BM)RPC', 'GYH)QY8', 'JBB)6QK', 'G9N)B77', 'RPC)M9B', 'F84)B1L', '1JZ)G95', 'SND)8G4', 'D1Q)J6D', 'N9N)LNM', 'YZH)V8R', 'TJ4)ZVD', '2V1)BGZ'
]

'''
orbit_map = [
   'COM)B',
   'B)C',
   'C)D',
   'D)E',
   'E)F',
   'B)G',
   'G)H',
   'D)I',
   'E)J',
   'J)K',
   'K)L',
   'K)YOU',
   'I)SAN'
]'''


class CelestialBody:
    def __init__(self, name, orbiters):
        self.name = name
        self.orbiters = orbiters
        self.num_oribters = len(self.orbiters)
        # self.tab = ''

    def add_orbiters(self, orbiter):
        self.orbiters.append(orbiter)
        # print(f"{self.name} gained a new orbiter {orbiter.name}")

    '''
    def show_orbiters_recursive(self, tab):
        self.tab = tab + ' '
        if(self.num_oribters > 0):
            print(f"{self.tab}{self.name} has {len(self.orbiters)} orbiters")
            for i in range(len(self.orbiters)):
                self.orbiters[i].to_string(
                                    self.name,
                                    self.orbiters[i].name,
                                    self.tab)
                self.orbiters[i].show_orbiters(self.tab)
        else:
            print(f"{self.tab}{self.name} has NO orbiters!")
            print("\n")

    def show_orbiters(self, tab):
        self.tab = tab + ' '
        if(len(self.orbiters) > 0):
            print(f"{self.tab}{self.name} has {len(self.orbiters)} orbiters")
            for i in range(len(self.orbiters)):
                self.to_string(self.name, self.orbiters[i].name, self.tab)
        else:
            print(f"{self.tab}{self.name} has NO orbiters!")
            print("\n")

    def to_string(self, orbited_name, orbiter_name, tab):
        print(f"{tab}{orbited_name} has {orbiter_name} as an orbiter!")
    '''


def map_orbits(orbit_map):
    map = {}

    # Direct orbits
    for orbit in orbit_map:
        data = orbit.split(')')
        orbited_name = data[0]
        orbiter_name = data[1]
        orbiter = CelestialBody(orbiter_name, [])

        if orbited_name in map:
            map[orbited_name].add_orbiters(orbiter)
        else:
            orbited = CelestialBody(orbited_name, [])
            map[orbited_name] = orbited
            map[orbited_name].add_orbiters(orbiter)

        if orbiter_name not in map:
            orbiter = CelestialBody(orbiter_name, [])
            map[orbiter_name] = orbiter

    # Indirect Orbits
    for celestial_body in map.values():
        for i in range(len(celestial_body.orbiters)):
            if celestial_body.orbiters[i].name in map:
                cb = celestial_body.orbiters[i]
                cb = map[cb.name]

    return map


def calculate_distance(move_from, move_to, map):
    from_map = []
    to_map = []
    closest_neighbor = ''

    from_map = look_for_name(map, move_from, from_map)
    to_map = look_for_name(map, move_to, to_map)

    for orb in from_map:
        if orb in to_map:
            closest_neighbor = orb
            break

    from_distance = from_map.index(closest_neighbor)
    to_distance = to_map.index(closest_neighbor)

    print(f"Distance 1 = {from_distance}, Distance 2 = {to_distance}")
    print(f"Total distance = {from_distance + to_distance}")


def look_for_name(map, name, orbits):
    for celestial_body in map.values():
        for i in range(len(celestial_body.orbiters)):
            if celestial_body.orbiters[i].name == name:
                orbits.append(celestial_body.name)
                look_for_name(map, celestial_body.name, orbits)
                return orbits


def start():
    map = map_orbits(orbit_map)
    calculate_distance("YOU", "SAN", map)


if __name__ == "__main__":
    start()
    # Your puzzle answer was 466.