
welcome_prompt = "Welcome doctor, what would you like to do today?\n - To list all patients, press 1\n - To run a new diagnosis, press 2\n - To quit, press q\n"

name_prompt = "What is the patients name?\n"

appearance_prompt = "How is the patient's general appearance?\n - 1: Normal appearance\n - 2: Irritable or lethargic\n"

eye_prompt = "How are the patients eyes?\n - 1: Normal/slightly sunken\n - 2: Eyes very sunken\n"

skin_prompt = "How is the patient's skin after pinching?\n - 1: Normal skin pinch\n - 2: Slow skin pinch\n"

severe_dehydration = "Severe dehydration indicated"
some_dehydration = "Some dehydration indicated"
no_dehydration = "No dehydration indicated"


patients_and_diagnoses = []




def patient_list():
    print("Listing patients and diagnoses")
    for patient in patients_and_diagnoses:
        print(patient)

def save_new_diagnosis(name, diagnosis):
    if name == "" or diagnosis == "":
        print("Could not save patient and diagnosis due to invalid input")
        return
    final_diagnosis = name + " - " + diagnosis
    patients_and_diagnoses.append(final_diagnosis)
    print("Final diagnosis:", final_diagnosis, "\n")

def assess_skin(skin):
    if skin == '1':
        return some_dehydration
    elif skin == '2':
        return severe_dehydration
    else:
        return ""

def assess_eyes(eyes):
    if eyes == '1':
        return no_dehydration
    elif eyes == '2':
        return severe_dehydration
    else:
        return ""

def appearance_check():
    appearance = input(appearance_prompt)
    if appearance == '1':
        eyes = input(eye_prompt)
        return assess_eyes(eyes)
    elif appearance == '2':
        skin = input(skin_prompt)
        assess_skin(skin)
    else:
        return ""


def start_new_diagnosis():
    name = input(name_prompt)
    diagnosis = appearance_check()
    save_new_diagnosis(name, diagnosis)


def main():
    while True:
        selection = input(welcome_prompt)
        if selection == "1":
            patient_list()
        elif selection == "2":
            start_new_diagnosis()
        elif selection == "q":
            return


main()
