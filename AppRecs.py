from csv import reader

### The Google Play data set ### 1
opened_file = open('googleplaystore.csv')
read_file = reader(opened_file)
android = list(read_file)
android_header = android[0]
android = android[1:]

### The App Store data set ### 1.1
opened_file = open('AppleStore.csv')
read_file = reader(opened_file)
ios = list(read_file)
ios_header = ios[0]
ios = ios[1:]

### A Function to view the dataset ### 1.2
def explore_data(dataset, start, end, rows_and_columns=False):
    dataset_slice = dataset[start:end]    
for row in dataset_slice:
        print(row)
        print('\n') # adds a new (empty) line between rows
        
    if rows_and_columns:
        print('Number of rows:', len(dataset))
        print('Number of columns:', len(dataset[0]))

### Sorting duplicate apps ### 2
dapps = []
uapps = []
for app in android:
    name = app[0]
    if name in uapps:
        dapps.append(name)
    else:
        uapps.append(name)

### Sorting duplicates by amount of reviews to find the latest duplicate version, and re-entering it into the dataset as a unique value. The app version with the most reviews will be the most recent ### 2.1
reviews_max = {}
for row in android:
    name = row[0]
    n_reviews = float(row[3])
    if name not in reviews_max:
        reviews_max[name] = n_reviews
    if name in reviews_max and reviews_max[name] < n_reviews:
        name = n_reviews
android_clean = []
already_added = []
for row in android:
    name = row[0]
    n_reviews = float(row[3])
    if n_reviews == reviews_max[name] and name not in already_added:
        android_clean.append(row)
        already_added.append(name)

### Ord Function to remove no english characters, as most common english characters have a unicode value below 127. Required 4 values above 127 to trigger a false to account for uncommon characters (i.e. emojis) 2.2
def engcheck(string):
    count = 0
    for char in string:
        if ord(char) > 127:
            count += 1
    if count > 3:
        return False
    return True
### Building lists with cleaned, english apps (Such that market analysis will be conducted on English apps) ### 2.3
engand = []
engios = []
for row in android_clean:
    name = row[0]
    if engcheck(name) == True:
        engand.append(row)
for row in ios:
    name = row[1]
    if engcheck(name) == True:
        engios.append(row)

### Further refining the analysis, removing all paid apps from previous lists, such that analysis is conducted on free, english apps ### 2.4
android_final = []
ios_final = []
for app in engand:
    price = app[7]
    if price == '0':
        android_final.append(app)
for app in engios:
    price = app[4]
    if price =='0.0':
        ios_final.append(app)

### Function to create a dataset frequency table ### 3
def freq_table(dataset, index):
    d = {}
    total = 0
    for app in dataset:
        total += 1
        val = app[index]
        if val not in d:
            d[val] = 1
        elif val in d:
            d[val] += 1

    table_percentages = {}
    for key in d:
        percentage = (d[key] / total) * 100
        table_percentages[key] = percentage 
    
    return table_percentages

### Function to display the created frequency table as a list of sorted tuples ###
def display_table(dataset, index):
    table = freq_table(dataset, index)
    table_display = []
    for key in table:
        key_val_as_tuple = (table[key], key)
        table_display.append(key_val_as_tuple)
        
    table_sorted = sorted(table_display, reverse = True)
    for entry in table_sorted:
        print(entry[1], ':', entry[0])

### IOS Frequency table, which can be modified for increased specifity, by a range of factors (i.e. the unique column headers: genre, rating count etc) ###
fi = freq_table(ios_final, 11)
for genre in fi:
     total = 0
    len_genre = 0
    for app in ios_final:
        genre_app = app[11]
        if genre_app == genre:
            n_ratings = float(app[5])
            total += n_ratings
            len_genre += 1
    av = total / len_genre
    print(genre, av)

### Android Frequency table, which can be modified for increased specifity, by a range of factors (i.e. the unique column headers: genre, rating count etc) ###
fa = freq_table(android_final, 1)
for app in fa:
    total = 0
    len_category = 0
    for cat in android_final:
        category_app = cat[1]
        if category_app == app:
            a = cat[5]
            x = a.replace('+', '')
            y = x.replace(',', '')
            z = float(y)
            total += z
            len_category += 1
    av = total / len_category
    print(genre, av)
