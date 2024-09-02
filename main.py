# CS2500 Programming Assignment #1 - Wade Bradford

CT_precip_file = "CT Precip.csv"
CT_tmin_file = "CT Min Temp.csv"
CT_tmax_file = "CT Max Temp.csv"
CT_tavg_file = "CT Avg Temp.csv"
ME_precip_file = "ME Precip.csv"
ME_tmin_file = "ME Min Temp.csv"
ME_tmax_file = "ME Max Temp.csv"
ME_tavg_file = "ME Avg Temp.csv"


def most_annual_precip(dict):
    """ Given a dictionary with weather data, return the month that had
    the most precipitation across all years and the average precip in that month
    Arguments:
    dict: the dictionary for a single region
    Return:
    a tuple of (month_number, avg precip for that month across all years)
    for the month with highest precip
    """
    monthly_precip = {}

    for date, precip in dict['PRECIP']:
        # last two digits in yyyymm format
        month = date[-2:]

        # skip "date" header and skip any other non-dates
        try:
            precip_value = float(precip)
        except ValueError:
            continue

        if month not in monthly_precip:
            monthly_precip[month] = []

        monthly_precip[month].append(float(precip_value))

    # calculate avg precip for each month
    monthly_avg_precip = {}
    for month, precip_list in monthly_precip.items():
        if precip_list:
            monthly_avg_precip[month] = sum(precip_list) / len(precip_list)

    # find month with most precip
    max_month = max(monthly_avg_precip, key=monthly_avg_precip.get)
    # get average in month with most precip
    max_avg_precip = monthly_avg_precip[max_month]

    return max_month, max_avg_precip


def create_merged_csv(region1_dict, region2_dict, filename):
    """
    Merge the data from both regions into a single .csv file
    with format
    date region1_tmin, region2_tmin, region1_tmax, region2_tmax,
    region1_tavg, region2_tavg, region1_precip, region2_precip
    Arguments: region1_dict: dictionary for first region
    region2_dict: dictionary for second region
    filename: name of csv file to be created
    """
    # get all dates from both dictionaries
    all_dates = set()
    for records in region1_dict.values():
        for date, _ in records:
            all_dates.add(date)
    for records in region2_dict.values():
        for date, _ in records:
            all_dates.add(date)

    # put dates in order
    sorted_dates = sorted(all_dates)

    with open(filename, 'w') as file:
        file.write(
            "date,region1_tmin,region2_tmin,region1_tmax,region2_tmax,"
            "region1_tavg,region2_tavg,region1_precip,region2_precip\n")

        # go through dates and get data from each dictionary
        for date in sorted_dates:

            region1_tmin = region2_tmin = 0
            region1_tmax = region2_tmax = 0
            region1_tavg = region2_tavg = 0
            region1_precip = region2_precip = 0

            # get data from region 1
            if 'TMIN' in region1_dict:
                for d, temp in region1_dict['TMIN']:
                    if d == date:
                        region1_tmin = temp

            if 'TMAX' in region1_dict:
                for d, temp in region1_dict['TMAX']:
                    if d == date:
                        region1_tmax = temp

            if 'TAVG' in region1_dict:
                for d, temp in region1_dict['TAVG']:
                    if d == date:
                        region1_tavg = temp

            if 'PRECIP' in region1_dict:
                for d, precip in region1_dict['PRECIP']:
                    if d == date:
                        region1_precip = precip

            # get data from region 2
            if 'TMIN' in region2_dict:
                for d, temp in region2_dict['TMIN']:
                    if d == date:
                        region2_tmin = temp

            if 'TMAX' in region2_dict:
                for d, temp in region2_dict['TMAX']:
                    if d == date:
                        region2_tmax = temp

            if 'TAVG' in region2_dict:
                for d, temp in region2_dict['TAVG']:
                    if d == date:
                        region2_tavg = temp

            if 'PRECIP' in region2_dict:
                for d, precip in region2_dict['PRECIP']:
                    if d == date:
                        region2_precip = precip

            file.write(
                f"{date},{region1_tmin},{region2_tmin},"
                f"{region1_tmax},{region2_tmax},"
                f"{region1_tavg},{region2_tavg},"
                f"{region1_precip},{region2_precip}\n")


def compare_monthly_avg_temps(region1_dict, region2_dict, month, filename):
    """Create a file of average monthly temperature (avg of avg) across all years
    Comparing two regions
    if day does not exist in both dictionaries, it is ommitted
    make no assumption about order of data
    Arguments: region1_dict: dictionary for first region
    region2_dict: dictionary for second region
    month: specified month to avg
    filename: name of file to write monthly avgs to
    """
    results = {}

    # get region 1 temps
    for key, entries in region1_dict.items():
        for date, temp in entriess:
            if date.endswith(month):
                if date not in results:
                    results[date] = {'Region1': [], 'Region2': []}
                results[date]['Region1'].append(float(temp))

    # get region 2 temps
    for key, entries in region2_dict.items():
        for date, temp in entries:
            if date.endswith(month):
                if date not in results:
                    results[date] = {'Region1': [], 'Region2': []}
                results[date]['Region2'].append(float(temp))

    with open(filename, 'w') as file:
        file.write("Date,Region1,Region2,Difference\n")

        # calculate differences
        for date in sorted(results.keys()):
            region1_avg = sum(results[date]['Region1']) / len(results[date]['Region1'])
            region2_avg = sum(results[date]['Region2']) / len(results[date]['Region2'])

            difference = region1_avg - region2_avg

            # one decimal point
            file.write(
                f"{date},{region1_avg:.1f},{region2_avg:.1f},{difference:.1f}\n")


def month_int_to_name(num):
    """Convert month number to name
    Arguments: month number (1-January, etc)
    Return: Month name
    """

    if num == "01":
        return "January"
    if num == "02":
        return "February"
    if num == "03":
        return "March"
    if num == "04":
        return "April"
    if num == "05":
        return "May"
    if num == "06":
        return "June"
    if num == "07":
        return "July"
    if num == "08":
        return "August"
    if num == "09":
        return "September"
    if num == "10":
        return "October"
    if num == "11":
        return "November"
    if num == "12":
        return "December"
    else:
        return "Error, not a valid month number"


def load_file_into_dict(dict, filename, key):
    """
    Given a CSV file that has year, data as first 2 items on a line
    load them into provided dictionary
    Arguments: dict - dictionary to be loaded
    filename - file that contains data
    key - key value in dictionary
    """

    with open(filename, 'r') as file:
        for line in file:
            # remove whitespace, split by comma
            parts = line.strip().split(',')
            if len(parts) >= 2:
                date, data = parts[0], parts[1]

                # use key to add year and data to dict
                if key not in dict:
                    dict[key] = []
                dict[key].append((date, data))


def main():
    region1_dict = {}
    load_file_into_dict(region1_dict, CT_precip_file, "PRECIP")
    load_file_into_dict(region1_dict, CT_tmin_file, "TMIN")
    load_file_into_dict(region1_dict, CT_tmax_file, "TMAX")
    load_file_into_dict(region1_dict, CT_tavg_file, "TAVG")
    region2_dict = {}
    load_file_into_dict(region2_dict, ME_precip_file, "PRECIP")
    load_file_into_dict(region2_dict, ME_tmin_file, "TMIN")
    load_file_into_dict(region2_dict, ME_tmax_file, "TMAX")
    load_file_into_dict(region2_dict, ME_tavg_file, "TAVG")
    compare_monthly_avg_temps(region1_dict, region2_dict, '01',
"Monthly data comp.txt")
    create_merged_csv(region1_dict,region2_dict, "Connecticut Maine Weather Data.csv")
    month, precip = most_annual_precip(region1_dict)
    print(f'In Region1, historically {month_int_to_name(month)} ' +
    f'has had the most precipation with avg of {precip:.2f} inches')
    month, precip = most_annual_precip(region2_dict)
    print(f'In Region2, historically {month_int_to_name(month)} ' +
    f'has had the most precipation with avg of {precip:.2f} inches')


if __name__ == '__main__':
    main()
