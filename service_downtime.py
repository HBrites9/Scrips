#!/usr/bin/python3

import arrow
# arrow.Arrow implements the datetime interface
from arrow import Arrow as datetime

from argparse import ArgumentParser as argparser

if __name__ == "__main__":
    
    # Define command arguments
    parser = argparser()
    
    #Cli Arguments
    parser.add_argument('-ty', '--type', type=str, choices=['fixed', 'flexible'], default='fixed', help='Type or Downtime: fixed or flexible \n Default: fixed')
    parser.add_argument('-fh', '--hour', type=str, help='Hour (for flexible downtime only)')
    parser.add_argument('-fm', '--minute', type=str, help='Minute (for flexible downtime only)')
    parser.add_argument('-m', '--comment', type=str, required=True, help='Add a Comment')
    parser.add_argument('-t', '--timezone', type=str, required=True, help='Timezone')
    parser.add_argument('-s', '--start-time', type=str, required=True, help='Start time in format YYYY-MM-DDTHH:MM')
    parser.add_argument('-e', '--end-time', type=str, required=True, help='End time in format YYYY-MM-DDTHH:MM')
    args = parser.parse_args()

    start_range = arrow.get(args.start_time, 'YYYY-MM-DDTHH:mm').replace(tzinfo=args.timezone)
    end_range = arrow.get(args.end_time, 'YYYY-MM-DDTHH:mm').replace(tzinfo=args.timezone)

    format_date="YYYY-MM-DD"
    format_hours="HH:mm"

    type1       = args.type
    comment     = args.comment
    
    print("    ranges = {")
    start_tz      = None
    end_tz        = None
    prev_tz_start = start_range
    prev_tz_end   = end_range
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
            
        if None in [prev_tz_start,prev_tz_end]:
            prev_tz_start=start
            prev_tz_end=end
            
        if prev_tz_start.dst() != start.dst() or prev_tz_end.dst() != end.dst():
            #Daylight Savings in effect
            printed = True

            print("comment={},  \"{} - {}\" = \"{}-{}\", type1={}".format(
            comment,
            prev_tz_start.to(timezone).format(format_date),
            end_tz.format(format_date),
            prev_tz_start.to(timezone).format(format_hours),
            end_tz.to(timezone).format(format_hours),
            type1,
                    )
                )
            
            if prev_tz_start.dst() != start.dst():
                    prev_tz_start = start
                    
                    
            if prev_tz_end.dst() != end.dst():
                    prev_tz_end = end
                   
        else:
            printed = False

    if printed is False:
        print("comment={},  \"{} - {}\" = \"{}-{}\", type1={} ".format(
            comment,
            prev_tz_start.format(format_date),
            end_tz.format(format_date),
            start_tz.format(format_hours),
            end_tz.format(format_hours),
            type1,
            )
        )

    print("    }")
    
