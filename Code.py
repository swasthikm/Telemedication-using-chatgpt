import shutil
import os
import PyPDF2
import openai

from PyPDF2 import PdfReader

# Api Key
api_key="Your API"


#----------------------------------------------------------------------
print("Hello")
name = input("Please enter your name")
print("Welcome to Telemedication "+name)
source_folder = input("Enter the path of the source folder: ")
# Creating folder
# Input the location of the folder to be created
directory_path = r"Your path" #Path to create and save file

# Input the name of the folder
folder_name = name

try:
    # Creating path of new folder
    new_folder_path = os.path.join(directory_path, folder_name)

    # Checking for the folder already exists or not
    if os.path.exists(new_folder_path):
        print(f"The folder '{folder_name}' already exists in '{directory_path}'.")
    else:
        # Creating new folder with given name
        os.makedirs(new_folder_path)
        print(f"The folder '{folder_name}' has been created in '{directory_path}'.")
except Exception as e:
    print(f"An error occurred: {e}")
#-----------------------------------------------------------------------------------------------
#Copying file
destination_folder = new_folder_path
shutil.copy(source_folder,destination_folder)
#---------------------------------------------------------------------------------------------
#Entering the file name to be read
try:
    # Check if the folder path exists
    if os.path.exists(destination_folder) and os.path.isdir(destination_folder):
        # List the conetent in the folder
        files = os.listdir(destination_folder)

        if files:
            print("Files in the folder:")
            for file in files:
                print(file)
                file_name = file
        else:
            print("The folder is empty.")
    else:
        print(f"The folder at '{folder_path}' does not exist.")
except Exception as e:
    print(f"An error occurred: {e}")
read_file = input("enter the file to be read")
print(read_file)
#--------------------------------------------------------------------------------------------



# read_file is taken from previous section
pdf_path = os.path.join(destination_folder, read_file)

def search_terms_in_pdf(pdf_path, search_terms):
    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = PdfReader(pdf_file)
        lines_with_terms = []

        for page_number in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_number]
            page_text = page.extract_text()
            lines = page_text.split('\n')
            

            for line in lines:
                if any(term.lower() in line.lower() for term in search_terms):
                    lines_with_terms.append(line.strip())

        return lines_with_terms

# Key words to be searched in the PDF
terms_to_search = ['MUMPS ANTIBODY - IGG', 'MEASLES ANTIBODY - IGG', 'VARICELLA ZOSTER VIRUS ANTIBODY - IGG', 'RUBELLA - IGG']  # Add the terms you want to search for
lines_with_search_terms = search_terms_in_pdf(pdf_path, terms_to_search)

# Print the lines from PDF
print(f"Lines containing the search terms from the PDF '{pdf_path}':")
output = []
count = 0
for line in lines_with_search_terms:
    output.append(line)
    count = count +1
medical_terms = []
prefix = "A patient has conducted blood test and has "
suffix = " What does the value indicate and what are the precausionary measures to be taken? Explain in patient understandable form in 4-5 sentence"
for i in range(2, count, 3):
    print(output[i])
    medical_terms.append(prefix+output[i]+suffix)
print(" Input for Chatgpt")
for terms in medical_terms:
    print(terms)
#-----------------------------------------------------------------
#-----------------------------------------------------------------
for terms in medical_terms:
    user_prompt = terms
    #print(user_prompt)
    try:
        # Send the user's prompt to ChatGPT
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=user_prompt,
            max_tokens=50,  # Adjust this based on your desired response length
            api_key=api_key)

    # Extract and print the generated response
        generated_response = response.choices[0].text
        print("Generated Response:")
        print(generated_response)

    except Exception as e:
        print(f"An error occurred: {e}")

while True:
    user_input = input("Do you have any other questions? Type Yes to continue , Type No to Exit").lower()

    if user_input == 'yes':
        question = input("Type your question here")
        try:
        # Send the user's prompt to ChatGPT
            response = openai.Completion.create(
                engine="text-davinci-002",
                prompt=user_prompt,
                max_tokens=100,  
                api_key=api_key)

            generated_response = response.choices[0].text
            print("Generated Response:")
            print(generated_response)

        except Exception as e:
            print(f"An error occurred: {e}")
        

    elif user_input == 'no':
        print("Thank You. Bye Have a nice day!")
        break  # Exit the loop when the user enters 'no'

    else:
        print("Invalid input. Please enter 'yes' or 'no'.")
        
#---------------------------------------------------------------------------
#-----------------------------------------------------------------------------

    


