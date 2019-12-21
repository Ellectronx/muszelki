import sys
import urllib.request
from urllib.request import urlopen
from string import ascii_lowercase
import os
import glob
import re 


filename = ""
#url = urlopen("https://s3.zylowski.net/public/input/3.txt")
#urllib.request.urlretrieve("https://s3.zylowski.net/public/input/3.txt", filename)


def download_file(address):
	global filename
	filename = "netfile.txt"
	#urllib.request.urlretrieve("https://s3.zylowski.net/public/input/3.txt", filename)
	try:
		urllib.request.urlretrieve(address, filename)
		print("Plik został pobrany")
	except Exception:
		print("Wystąpił problem podczas pobierania pliku")
	
def open_file_try(_filename):
	global filename
	try:
		with open(_filename, 'r') as myfile:
			data = myfile.read()
			filename = _filename
			print("Plik instnieje")
	except Exception:
		print("Problem z otwarciem pliku lokalnego")

def print_menu():
    print(5 * "\n")
    print(25 * "-", "ANALIZATOR TEKSTÓW", 25 * "-")
    print("1. Wybierz plik wejściowy ")
    print("2. Zlicz liczbę liter w pobranym pliku ")
    print("3. Zlicz liczbę wyrazów w pliku ")
    print("4. Zlicz liczbę znaków interpunkcyjnych w pliku ")        
    print("5. Zlicz liczbę zdań w pliku ")
    print("6. Wygeneruj raport o użyciu liter (A-Z) ")
    print("7. Zapisz statystyki z punktów 2-5 do pliku statystyki.txt ")
    print("8. Wyjście z programu ")
    print(70 * "-")


def download_file_choice():
	#global filename
	while True:
		user_input = input ("Czy wczytać plik z internetu [T/N]")
		if user_input == 'T':
			file_address = input ("Podaj prawidłowy adres pliku z internetu:")
			while re.match("'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+'", file_address) == False:
				file_address = input ("Podaj prawidłowy adres pliku z internetu:")
			download_file(file_address)
			return
		elif user_input == 'N':
			filename = input ("Podaj nazwę pliku lokalnego *.txt:")
			while re.match('.+\.txt$', filename) == False:
				filename = input ("Podaj nazwę pliku lokalnego:")
			open_file_try(filename)
			return


def count_letters():
        global letters
        global letters2
        letters = 0
        letters2 = 0
        try:
                with open(filename, 'r') as myfile:
                        data = myfile.read()
                
                
                for x in data:
                        y = x.lower()
                        if y == "a" or y == "e" or y == "i" or y == "o" or y == "u" or y == "y":
                                letters+=1
                        else:
                                letters2+=1

                print(" Ilość samogłosek w pliku ",filename," to ", str(letters))
                print(" Ilość spółgłosek w pliku ",filename," to ", str(letters2))
        except FileNotFoundError:
                print(" ** Brak pliku ",filename, " **")
        except Exception:
                print(" ** Nie mogę otworzyć pliku ",filename)

                
def count_words():
        try:
                with open(filename, 'r') as myfile:
                        data = myfile.read()

                array = []
                array = data.split()
                global words
                words = 0
                global x
                x = 0
                for y in array:    
                        if len(array[x]) > 1:
                                words+=1
                        x+=1

                print("Ilość wyrazów w pliku " ,filename, " to ", str(words))
        except FileNotFoundError:
                print(" ** Nie mogę znaleść pliku ", filename)
        except Exception:
                print(" ** Nie mogę otworzyć pliku ",filename)


def count_punctation():
        try:
                with open(filename, 'r') as myfile:
                        data = myfile.read()

                global punctation        
                punctation = 0
                punctation = data.count(".") + data.count("?")
                print("Ilość znaków interpunkcyjnych w pliku " ,filename, " to ", str(punctation))
        except FileNotFoundError:
                print(" ** Nie mogę znaleść pliku ", filename)
        except Exception:
                print(" ** Nie mogę otworzyć pliku ",filename)


def count_sentences():
        try:
                with open(filename, 'r') as myfile:
                        data = myfile.read()

                global sentences 
                #sentences = 0
                #sentences = data.count(".") + data.count("?")
                r1 = re.findall('[^.]{1}\.',data)
                r2 = re.findall('[^?]{1}\?',data)
                sentences = len(r1) + len(r2)
                print("Ilość zdań w pliku " ,filename, " to ", str(sentences))
        except FileNotFoundError:
                print(" ** Nie mogę znaleść pliku ", filename)
        except Exception:
                print(" ** Nie mogę otworzyć pliku ",filename) 


def generate_report():
	try:
		with open(filename, 'r') as myfile:
			data = myfile.read()
		
		for char in ascii_lowercase:
			x = data.count(char) + data.count(char.upper())
			print( char.upper(),": ",x)
	except FileNotFoundError:
		print(" ** Brak pliku ",filename, " **")
	except Exception:
		print(" ** Nie mogę otworzyć pliku ",filename)
def exit():
    fileList = glob.glob('*.txt')
    if len(fileList) is not 0 :
       for filePath in fileList:
            try:
                os.remove(filePath)
                print("Usunieto: ", filePath)
            except:
                print("Nie mozna usunac pliku : ", filePath)

    else:
        print("Pliki nie istnieja")
    sys.exit()

def save_stats():

    path="statystyki.txt"
    if os.path.isfile(path):
        os.unlink(path)

    count_letters()
    count_punctation()
    count_sentences()
    count_words()
    myfile = open('statystyki.txt','a')
    myfile.write("Ilość liter: ")
    myfile.write(str(letters))
    myfile.write("\n")
    myfile.write("Ilość słów: ")
    myfile.write(str(words))
    myfile.write("\n")
    myfile.write("Ilość znaków interpunkcyjnych: ")
    myfile.write(str(punctation))
    myfile.write("\n")
    myfile.write("Ilość zdań: ")
    myfile.write(str(sentences))
    myfile.write("\n")
    myfile.close()


#download_file()

while True:
	print_menu()
	
	
	#get user input and convert to int
	while True:
		user_input = input ("Dokonaj wyboru [1-8]: ")
		try:
			choice = int(user_input)
			if choice>=1 and choice <=8:
				break
		except ValueError:
			choice = -1

		print("!! DOKONANO NIEPRAWIDŁOWEGO WYBORU !!\n")

	#print(choice)

	if choice == 1:
		#print(" Pobieranie plik z internetu...")
		download_file_choice()
	elif choice == 2:
		count_letters()
	elif choice == 3:
		count_words()
	elif choice == 4:
		count_punctation()
	elif choice == 5:
		count_sentences()
	elif choice == 6:
		generate_report()
	elif choice == 7:
		print(" Zapisywanie statystyki z punktów 2-5 do pliku statystyki.txt...")
		save_stats()
	elif choice == 8:
		exit()
	else:
		print("!! DOKONANO NIEPRAWIDŁOWEGO WYBORU !!\n")
