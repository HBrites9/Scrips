#!/usr/bin/python3

import arrow
# arrow.Arrow implements the datetime interface
from arrow import Arrow as datetime

from argparse import ArgumentParser as argparser

if __name__ == "__main__":
    
    # Define command arguments
    parser = argparser()
    
    #Cli Arguments for Host
    parser.add_argument('-d', '--downtime-name', type=str, help='Downtime name:')
    parser.add_argument('-a', '--author', type=str, help='Downtime author:')
    parser.add_argument('-m', '--comment', type=str, required=True, help='Add a Comment')
    parser.add_argument('-f', '--fixed', type=str, choices=['true', 'false'], required=True, help='Fixed: True or False')
    parser.add_argument('-n', '--display-name', type=str, help='Display name \n ')
    parser.add_argument('-t', '--timezone', type=str, required=True, help='Timezone')
    parser.add_argument('-s', '--start-time', type=str, required=True, help='Start time in format YYYY-MM-DDTHH:mm')
    parser.add_argument('-e', '--end-time', type=str, required=True, help='End time in format YYYY-MM-DDTHH:mm')
    parser.add_argument('-se', '--with-services', type= str,required=True, help='Apply to Hosts: 0 \n  Hosts and Services: 1 \n Services: 3 ')
    
    args = parser.parse_args()

    start_range = arrow.get(args.start_time, 'YYYY-MM-DDTHH:mm',tzinfo=args.timezone)
    end_range = arrow.get(args.end_time, 'YYYY-MM-DDTHH:mm',tzinfo=args.timezone)
    
    if(end_range < start_range):
        change = None
        change = end_range
        end_range = start_range
        start_range = change

    format_date="YYYY-MM-DD"
    format_hours="HH:mm"

    downtime_name = args.downtime_name
    author        = args.author
    comment       = args.comment
    fixed         = args.fixed
    display_name  = args.display_name
    with_services = args.with_services
    
    output        = ""
    start_tz      = None
    end_tz        = None
    prev_start    = None
    prev_end      = None
    printed       = False
    timezone      = "UTC"


    for timestamp in arrow.Arrow.span_range('day', start_range, end_range):
        start=timestamp[0].replace(
            hour=start_range.hour,
            minute=start_range.minute
        )
        end=timestamp[1].replace(
            hour=end_range.hour,
            minute=end_range.minute
        )
        
        # Handle start range
        start_tz=start.to(timezone)
            
        # Handle end range
        end_tz=end.to(timezone)
            
        if None in [prev_start,prev_end]:
            prev_start=start
            prev_end=end
            
        if prev_start.dst() != start.dst() or prev_end.dst() != end.dst():
            #Daylight Savings in effect
            printed = True
            
            output += "\t \t \"{} - {}\" = \"{}-{}\" \n".format(
            prev_start.to(timezone).format(format_date),
            end_tz.format(format_date),
            prev_start.to(timezone).format(format_hours),
            prev_end.to(timezone).format(format_hours)
        )
        
            
            if prev_start.dst() != start.dst():
                    prev_start = start
                    
                    
            if prev_end.dst() != end.dst():
                    prev_end = end
                   
        else:
            printed = False
    
    if(with_services == "0"):
        
        print("apply ScheduleDowntime \"{}\" to Host  \n".format(downtime_name)) 
        print(" \t author = \"{}\" \n".format(author))
        print(" \t comment = \"{}\" \n".format(comment))
        print(" \t fixed = {} \n".format(fixed))
        print(" \t assign where host.display_name == \"{}\"\n".format(display_name))
        print(" \t ranges = {")
        print(output)
        

    if(with_services == "1"):
        print("apply ScheduleDowntime \"{}\" to Host \n".format(downtime_name)) 
        print(" \t author = \"{}\" \n".format(author))
        print(" \t comment = \"{}\" \n".format(comment))
        print(" \t fixed = {} \n".format(fixed))
        print(" \t assign where host.display_name == \"{}\"\n".format(display_name))
        print(" \t ranges = {")
        print(output)
        

        print("apply ScheduleDowntime \"{}\" to Service  \n".format(downtime_name)) 
        print(" \t author = \"{}\" \n".format(author))
        print(" \t comment = \"{}\" \n".format(comment))
        print(" \t fixed = {} \n".format(fixed))
        print(" \t assign where host.display_name == \"{}\"\n".format(display_name))
        print(" \t ranges = {")
        print(output)
        

    if(with_services == "2"):    
        print("apply ScheduleDowntime \"{}\" to Service  \n".format(downtime_name)) 
        print(" \t author = \"{}\" \n".format(author))
        print(" \t comment = \"{}\" \n".format(comment))
        print(" \t fixed = {} \n".format(fixed))
        print(" \t assign where host.display_name == \"{}\"\n".format(display_name))
        print(" \t ranges = {")
        print(output)
        

    if printed is False:
        print("\t \t \"{} - {}\" = \"{}-{}\"".format(
            prev_start.to(timezone).format(format_date),
            end_tz.format(format_date),
            prev_start.to(timezone).format(format_hours),
            end_tz.format(format_hours)
            
            )
        )

    print("    }")
    print("}")