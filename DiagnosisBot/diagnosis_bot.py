
welcome_prompt = "Welcome doctor, what would you like to do today?\n - To list all patients, press 1\n - To run a new diagnosis, press 2\n - To quit, press q\n"

name_prompt = "What is the patients name?\n"

appearance_prompt = "How is the patient's general appearance?\n - 1: Normal appearance\n - 2: Irritable or lethargic\n"

eye_prompt = "How are the patients eyes?\n - 1: Normal/slightly sunken\n - 2: Eyes very sunken\n"

skin_prompt = "How is the patient's skin after pinching?\n - 1: Normal skin pinch\n - 2: Slow skin pinch\n"

def patient_list():
    print("Listing patientsw and diagnoses")

def assess_skin(skin):
    if skin == '1':
        return "Some dehydration"
    elif skin == '2':
        return "Severe dehydration"

def assess_eyes(eyes):
    if eyes == '1':
        return "No dehydration indicated"
    elif eyes == '2':
        return "Severe dehydration indicated"

def appearance_check():
    appearance = input(appearance_prompt)
    if appearance == '1':
        eyes = input(eye_prompt)
        return assess_eyes(eyes)
    elif appearance == '2':
        skin = input(skin_prompt)
        assess_skin(skin)


def start_new_diagnosis():
    name = input(name_prompt)
    dianosis = assess_appearance()
    print(name, diagnosis)


def main():
    while True:
        selection = input(welcome_prompt)
        if selection == "1":
            list_patients()
        elif selection == "2":
            start_new_diagnosis()
        elif selection == "q":
            return


main()
