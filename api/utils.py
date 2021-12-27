from csv_ical import Convert
from datetime import datetime
import pandas as pd
pd.options.mode.chained_assignment = None


def convert_to_csv(calendar_ics,csv_location):
    convert = Convert()
    convert.CSV_FILE_LOCATION = csv_location
    convert.SAVE_LOCATION = calendar_ics

    
    
    convert.read_ical(convert.SAVE_LOCATION)
    convert.make_csv()
    convert.save_csv(convert.CSV_FILE_LOCATION)

    with open(csv_location, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write('zajęcia,rozpoczęcie,zakończenie,zajęcia2,sala'.rstrip('\r\n') + '\n' + content)

    df = pd.read_csv(csv_location)
    return df


def df_preparation(df):
    current_time=str(datetime.now())
    filt=(df['rozpoczęcie'] >= current_time)
    df=df[filt]

    df['przedmiot']=df['zajęcia']
    df['rodzaj zajęć']=df['zajęcia']
    df['nauczyciel']=df['zajęcia']

    def getSubject(subject):
        x=subject.split('-')
        subject=x[0]
        return subject
    df['przedmiot']=df['przedmiot'].apply(getSubject)

    def getPlace(subject):
        try:
            x=subject.split("-")
            place=x[1].split(" ")[1]
            return place
        except:
            return subject
    df['rodzaj zajęć']=df['rodzaj zajęć'].apply(getPlace)

    def getTeacher(teacher):
        try:
            row_value=teacher.split('-')
            middle_data=row_value[1]
            data=middle_data.split(" ")
            data=data[3:]
            if len(data)>2:  
                if "_" in data[-1]:
                    data.pop()
                
                for i in data:
                    if i == "zaliczeniem" or i == "egzaminem":
                        data.remove(i)
                        
                data[:] = [x for x in data if x]
                data=" ".join(data)
                if data != "brak nauczyciela":
                    return data
            return False
        except:
            return teacher
    df['nauczyciel']=df['nauczyciel'].apply(getTeacher)


    def place(sala):
        if sala == "brak lokalizacji brak sali":
            return "Zdalne"
        return sala
    df['sala']=df['sala'].apply(place)


    df=df[df['nauczyciel']!=False]
    df=df[['przedmiot','rodzaj zajęć','rozpoczęcie','zakończenie','nauczyciel']]
    df.reset_index(drop=True, inplace=True)
    df.index+=1

    filt=df['przedmiot'].str.contains('_',"+")
    df=df[~filt]
    return df

def subjectsCount(df):
    an=df[['przedmiot','rodzaj zajęć']].value_counts(sort=True)
    an=an.to_frame()
    an.reset_index(inplace = True)  
    an.columns=['przedmiot', 'rodzaj zajęć', 'powtórzenia']
    an.sort_values(by=['przedmiot'],inplace=True)
    return an

def classTypeCount(df):
    df=df['rodzaj zajęć'].value_counts()
    df=df.to_frame()
    df=df.reset_index()
    return df

def first_last_class(df):
    an={
    "najbliższe zajęcia" : [df['rozpoczęcie'].min()],
    "ostatnie zajęcia" :[df['rozpoczęcie'].max()],
    }
    df=pd.DataFrame(an)

    return df



def df_records(df):
    df['przedmiot']=df['zajęcia']
    df['rodzaj zajęć']=df['zajęcia']
    df['nauczyciel']=df['zajęcia']

    def getSubject(subject):
        x=subject.split('-')
        subject=x[0]
        return subject
    df['przedmiot']=df['przedmiot'].apply(getSubject)

    def getPlace(subject):
        try:
            x=subject.split("-")
            place=x[1].split(" ")[1]
            return place
        except:
            return subject
    df['rodzaj zajęć']=df['rodzaj zajęć'].apply(getPlace)

    def getTeacher(teacher):
        try:
            row_value=teacher.split('-')
            middle_data=row_value[1]
            data=middle_data.split(" ")
            data=data[3:]
            if len(data)>2:  
                if "_" in data[-1]:
                    data.pop()
                
                for i in data:
                    if i == "zaliczeniem" or i == "egzaminem":
                        data.remove(i)
                        
                data[:] = [x for x in data if x]
                data=" ".join(data)
                if data != "brak nauczyciela":
                    return data
            return False
        except:
            return teacher
    df['nauczyciel']=df['nauczyciel'].apply(getTeacher)


    def place(sala):
        if sala == "brak lokalizacji brak sali":
            return "Zdalne"
        return sala
    df['sala']=df['sala'].apply(place)


    df=df[df['nauczyciel']!=False]
    df=df[['przedmiot','rodzaj zajęć','rozpoczęcie','zakończenie','nauczyciel']]
    df.reset_index(drop=True, inplace=True)
    df.index+=1

    filt=df['przedmiot'].str.contains('_',"+")
    df=df[~filt]
    return df
