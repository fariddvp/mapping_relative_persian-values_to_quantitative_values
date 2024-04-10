import pandas as pd
# from num2words import num2words

features = ['یک', 'چهار', 'هجده', 'بیست و یک', 'منفی سه'
            , 'شش', 'هفتصد و چهل و دو', 'دو درصد' ,'سی','شصت'
            ,'صد','منفی بیست','ششصد و هجده', 'منفی هشتاد و چهار'
            , 'پانزده صدم', 'هفت دهم', 'صد و چهل و دو هزارم'
            , 'منفی دوازده صدم', 'یک و نیم'
            , 'هفت و ربع','یک و نیم درصد'
            ,'منفی هشتاد و چهار درصد','بیست و پنج درصد']


df = pd.DataFrame(features, columns=['letter Numbers'])
print(df)


# Function to convert Farsi numbers to digits
def calc_zarib(farsi_zarib_parts):
    
    farsi_num_parts = farsi_num.split()
    
    global totals
    for part in farsi_num_parts:
        if part == 'میلیارد':
            index_milliyard = index_start
            index_milliyard = farsi_num_parts.index(part)
            zarib_milliyard_parts = ' '.join(farsi_num_parts[0:index_milliyard])
            zarib_milliyard = farsi_to_digits(zarib_milliyard_parts)
            totals += zarib_milliyard * digits_mapping['میلیارد']   

        if part == 'میلیون':
            index_million = farsi_num_parts.index(part)
            zarib_million_parts = ' '.join(farsi_num_parts[index_milliyard + 1:index_million])
            zarib_million = farsi_to_digits(zarib_million_parts)
            totals += zarib_million * digits_mapping['میلیون']

        if part == 'هزار':
            index_thousand = farsi_num_parts.index(part)
            zarib_thousand_parts = ' '.join(farsi_num_parts[index_million + 1:index_thousand])
            zarib_thousand = farsi_to_digits(zarib_thousand_parts)
            totals += zarib_thousand * digits_mapping['هزار']

    return totals



def farsi_to_digits(farsi_num):    
    global farsi_num_parts
    global digits_mapping    
    total = 0
    is_negative = False
    is_percent = False
    is_10th = False
    is_100th = False
    is_1000th = False
    reminder = 0  
    
    farsi_num_parts = farsi_num.split() 

        
    
    for part in farsi_num_parts:
        
        if part == 'منفی':
            is_negative = True
        elif part == 'درصد':
            is_percent = True
        elif part == 'دهم':
            is_10th = True
            pass
        elif part == 'صدم':
            is_100th = True
            pass
        elif part == 'هزارم':
            is_1000th = True
            pass
        elif part == 'نیم':
            reminder = 0.5
        elif part == 'ربع':
            reminder = 0.25
        elif any(item in ['میلیارد', 'میلیون', 'هزار'] for item in farsi_num_parts):    
            if part == 'میلیارد' or part == 'میلیون' or part == 'هزار':
                total += calc_zarib(part)
                part = ' '.join(farsi_num_parts[farsi_num_parts.index(part) + 1:])
                total += farsi_to_digits(part)
            else:
                pass
        elif part in digits_mapping:
            if is_negative:
                total -= digits_mapping[part]
                total -= reminder
            else:
                total += digits_mapping[part]
                total += reminder
        else:
            try:
                if is_negative:
                    total -= int(part)
                    total -= reminder
                    is_negative = False
                else:
                    total += int(part)
                    total += reminder
            except ValueError:
                pass  # Ignore non-numeric and non-Persian numeric parts
    
    if is_percent:
        return str(total+reminder) + '%'
    if is_10th:
        return float(total/10)
    if is_100th:
        return float(total/100)
    if is_1000th:
        return float(total/1000)
    else:
        return total + reminder

digits_mapping = {
        'یک': 1,
        'دو': 2,
        'سه': 3,
        'چهار': 4,
        'پنج': 5,
        'شش': 6,
        'هفت': 7,
        'هشت': 8,
        'نه': 9,
        'ده': 10,
        'یازده': 11,
        'دوازده': 12,
        'سیزده': 13,
        'چهارده': 14,
        'پانزده': 15,
        'شانزده': 16,
        'هفده': 17,
        'هجده': 18,
        'نوزده': 19,
        'بیست': 20,
        'سی': 30,
        'چهل': 40,
        'پنجاه': 50,
        'شصت': 60,
        'هفتاد': 70,
        'هشتاد': 80,
        'نود': 90,
        'صد': 100,
        'دویست': 200,
        'سیصد': 300,
        'چهارصد': 400,
        'پانصد': 500,
        'ششصد': 600,
        'هفتصد': 700,
        'هشتصد': 800,
        'نهصد': 900,
        'هزار': 1000,
        'میلیون': 1000000,
        'میلیارد': 1000000000,
        'صفر': 0,
        'منفی': '-',
        'درصد': '%'
    }    

index_start = 0
totals = 0


# farsi_num_parts = farsi_num.split()
# Convert Farsi numbers to digits
# features_digits = [farsi_to_digits(farsi_num_parts) for farsi_num in df['letter Numbers']]



features_digits=[]
for farsi_num in df['letter Numbers']:
    result = farsi_to_digits(farsi_num)
    features_digits.append(result)

df['Numbers'] = features_digits

print(df)

PATH_csv = '/home/farid/Documents/TAAV_vscode_prj/mapping_relative_persian-values_to_quantitative_values/src/Output.csv'
# Export dataset to csv
df.to_csv(PATH_csv, index=False)


