"""
F1 Lap time visualiser

The script below uses the FastF1 API to load Formula 1 lap data, which is then plotted onto scatter plots for any selected driver,
of any year between 2018 and 2024. It also color codes the lap times with the specific tyre compound that is used.

Features:
- Can choose to look at one race, or plot two different races
- User can choose the year, track, and driver
- The tyre compound colors match the official Pirelli colors
- Can compare two drivers lap times side-by-side using the two races mode

Requirements:
- FastF1
- Matplotlib
- Pandas

Usage:
- install dependencies: pip install -r
- Run script and follow prompts provided in terminal

Notes:
- For venue, requires the full name of the race, will not accept if there is a minor mistake,
  (e.g., "Abu Dhabi Grand Prix" will be accepted, partial names will not).
"""
import matplotlib.pyplot as plt
import fastf1
import fastf1.plotting




fastf1.plotting.setup_mpl(mpl_timedelta_support=True, color_scheme='fastf1')

Pirelli_compound_colors = {
    'HYPERSOFT':'#F596C8',
    'ULTRASOFT':'#A020F0',
    'SUPERSOFT':'#FF0000',
    'SOFT': '#FF3333',
    'MEDIUM': '#FFCC33',
    'HARD': '#FFFFFF',
    'INTERMEDIATE': '#39B54A',
    'WET': '#0090FF'
}


mode = input('Do you want to compare one race or two? ')
#one race
if mode.lower() in ['one', '1']:
    year = int(input('Pick a Year: '))
    while year < 2018 or year > 2024:
        print('Sorry out of range, try again.')
        year = int(input('Pick a Year: '))

    schedule = fastf1.get_event_schedule(year)
    valid_venues = schedule['EventName'].tolist()
    print(f"Venues in {year}:")
    count = 1
    for venue_name in valid_venues:
        print(f"{count}. {venue_name}")
        count += 1

#venue details
    venue = input('Which venue would you like to pick? ').strip()#removes uneaded spaces, when there is input
    while venue.lower() not in [v.lower() for v in valid_venues]:
        print('That venue is not a valid venue in the provided year.')
        venue = input('Which venue would you like to pick? ').strip()
    venue_exact = next(v for v in valid_venues if v.lower() == venue.lower())

   #collects race info  
    race = fastf1.get_session(year, venue_exact, "R")
    race.load()

    # Driver codes
    valid_driver_codes = [race.get_driver(r)['Abbreviation'] for r in race.drivers]
    print(f"Driver codes in {venue_exact} {year}: {', '.join(valid_driver_codes)}")

    driver = input('Pick a driver code: ').upper()
    while driver not in valid_driver_codes:
        print("Invalid driver code. Try again.")
        driver = input('Pick a driver code: ').upper()
    driverinfo = race.get_driver(driver)
    Lastname = driverinfo.get('LastName')

    # Laps
    laps = race.laps.pick_driver(driver)
    laps_final = laps.pick_quicklaps().reset_index()
    valid_laps = laps_final[laps_final['LapTime'].notnull()]

    # Plot
    for tyre in valid_laps['Compound'].unique():
        laps_and_tyres = valid_laps[valid_laps['Compound'] == tyre]
        plt.scatter(
            laps_and_tyres['LapNumber'],
            laps_and_tyres['LapTime'].dt.total_seconds(),
            color=Pirelli_compound_colors.get(tyre, 'purple'),
            label=tyre, s=15
        )

    plt.title(f"{driver}({Lastname}) - {venue_exact} {year}")
    plt.xlabel('Lap Number')
    plt.ylabel('Lap Time (seconds)')
    plt.legend(title='Compound')
    plt.show()
#two races
elif mode.lower() in ['two', '2']:
    # Year 1
    year1 = int(input('Enter the first year: '))
    while year1 < 2018 or year1 > 2024:
        print('Sorry out of range, try again.')
        year1 = int(input('Enter the first year: '))

    # Year 2
    year2 = int(input('Enter the second year: '))
    while year2 < 2018 or year2 > 2024:
        print('Sorry out of range, try again.')
        year2 = int(input('Enter the second year: '))

    # Venue 1
    schedule1 = fastf1.get_event_schedule(year1)
    valid_venues1 = schedule1['EventName'].tolist()
    print(f"Venues in {year1}:")
    count1 = 1
    for venue_name1 in valid_venues1:
        print(f'{count1}. {venue_name1}')
        count1 += 1
    venue1 = input('Pick the first venue: ').strip()
    while venue1.lower() not in [v.lower() for v in valid_venues1]:
        print('Sorry, this venue is not valid for the selected year.')
        venue1 = input('Pick the first venue: ').strip()
    venue1_exact = next(v for v in valid_venues1 if v.lower() == venue1.lower())

    # Venue 2
    schedule2 = fastf1.get_event_schedule(year2)
    valid_venues2 = schedule2['EventName'].tolist()
    print(f"Venues in {year2}:")
    count2 = 1
    for venue_name2 in valid_venues2:
        print(f"{count2}. {venue_name2}")
        count2 += 1
    venue2 = input('Pick the second venue: ').strip()
    while venue2.lower() not in [v.lower() for v in valid_venues2]:
        print('Sorry, this venue is not valid for the selected year.')
        venue2 = input('Pick the second venue: ').strip()
    venue2_exact = next(v for v in valid_venues2 if v.lower() == venue2.lower())

    # Race 1
    race1 = fastf1.get_session(year1, venue1_exact, "R")
    race1.load()
    valid_driver_codes1 = [race1.get_driver(r)['Abbreviation'] for r in race1.drivers]
    print(f"Driver codes in {venue1_exact} {year1}: {', '.join(valid_driver_codes1)}")
    driver1 = input('Pick a driver code: ').upper()
    while driver1 not in valid_driver_codes1:
        print("Invalid driver code. Try again.")
        driver1 = input('Pick a driver code: ').upper()
    driverinfo1 = race1.get_driver(driver1)
    Lastname1 = driverinfo1.get('LastName')
    # Race 2
    race2 = fastf1.get_session(year2, venue2_exact, "R")
    race2.load()
    valid_driver_codes2 = [race2.get_driver(r)['Abbreviation'] for r in race2.drivers]
    print(f"Driver codes in {venue2_exact} {year2}: {', '.join(valid_driver_codes2)}")
    driver2 = input('Pick a driver code: ').upper()
    while driver2 not in valid_driver_codes2:
        print("Invalid driver code. Try again.")
        driver2 = input('Pick a driver code: ').upper()
    driverinfo2 = race2.get_driver(driver2)
    Lastname2 = driverinfo2.get('LastName')
    # Laps Race 1
    laps1 = race1.laps.pick_driver(driver1)
    laps_final1 = laps1.pick_quicklaps().reset_index()
    valid_laps1 = laps_final1[laps_final1['LapTime'].notnull()]

    # Laps Race 2
    laps2 = race2.laps.pick_driver(driver2)
    laps_final2 = laps2.pick_quicklaps().reset_index()
    valid_laps2 = laps_final2[laps_final2['LapTime'].notnull()]

    # Plot1
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    for tyre in valid_laps1['Compound'].unique():
        laps_and_tyres = valid_laps1[valid_laps1['Compound'] == tyre]
        axes[0].scatter(
            laps_and_tyres['LapNumber'],
            laps_and_tyres['LapTime'].dt.total_seconds(),
            color=Pirelli_compound_colors.get(tyre, 'purple'),
            label=tyre, s=15
        )
    axes[0].set_xlabel('Lap Number')
    axes[0].set_ylabel('Lap Time (seconds)')
    axes[0].legend(title='Compound')
    axes[0].set_title(f"{driver1} ({Lastname1}) - {venue1_exact} {year1}")
    #plot2
    for tyre in valid_laps2['Compound'].unique():
        laps_and_tyres = valid_laps2[valid_laps2['Compound'] == tyre]
        axes[1].scatter(laps_and_tyres['LapNumber'],laps_and_tyres['LapTime'].dt.total_seconds(),
        color=Pirelli_compound_colors.get(tyre, 'purple'),
        label=tyre, s=15
        )
    axes[1].set_xlabel('Lap Number')
    axes[1].set_ylabel('Lap Time (seconds)')
    axes[1].legend(title='Compound')
    axes[1].set_title(f"{driver2}({Lastname2}) - {venue2_exact} {year2}")

    plt.show()