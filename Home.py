import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import datetime as dt
import pyodbc
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

st.set_page_config(layout='wide')

image = Image.open('wellness_image_1.png')
st.image(image, use_column_width=True)

server = os.environ.get('server_name')
database = os.environ.get('db_name')
username = os.environ.get('db_username')
password = os.environ.get('db_password')
login_username = os.environ.get('userlogin')
login_password = os.environ.get('login_password')


conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};SERVER='
        + server
        +';DATABASE='
        + database
        +';UID='
        + username
        +';PWD='
        + password
        )

# login_username = st.secrets['login_username']
# login_password = st.secrets['login_password']
# conn = pyodbc.connect(
#         'DRIVER={ODBC Driver 17 for SQL Server};SERVER='
#         +st.secrets['server']
#         +';DATABASE='
#         +st.secrets['database']
#         +';UID='
#         +st.secrets['username']
#         +';PWD='
#         +st.secrets['password']
#         )

query1 = "SELECT * from vw_wellness_enrollee_portal"
query2 = 'select MemberNo, MemberName, Client, email, state, selected_provider, Wellness_benefits, selected_date, selected_session, date_submitted\
            FROM enrollee_annual_wellness_reg_web_portal'
query3 = 'select * from updated_wellness_providers'
@st.cache_data(ttl = dt.timedelta(hours=4))
def get_data_from_sql():
    wellness_df = pd.read_sql(query1, conn)
    wellness_providers = pd.read_sql(query3, conn)
    # conn.close()
    return wellness_df, wellness_providers

wellness_df, wellness_providers = get_data_from_sql()

filled_wellness_df = pd.read_sql(query2, conn)

wellness_df['memberno'] = wellness_df['memberno'].astype(str)
filled_wellness_df['MemberNo'] = filled_wellness_df['MemberNo'].astype(str)

st.subheader('Welcome to AVON HMO Enrollee Annual Wellness Portal \nKindly note that you are only eligible to perform your Wellness check once in a policy year')

#initialize session state to store user input
if 'user_data' not in st.session_state:
    st.session_state.user_data = {
        'email': '',
        'mobile_num': '',
        'state': 'ABIA',
        'selected_provider': 'ROSEVINE HOSPITAL  - 73 ABA OWERRI ROAD, ABA',
        'job_type': 'Mainly Desk Work',
        'gender': 'Male',
        'resp_1_a': 'Grand Parent(s)',
        'resp_1_b': 'Grand Parent(s)',
        'resp_1_c': 'Grand Parent(s)',
        'resp_1_d': 'Grand Parent(s)',
        'resp_1_e': 'Grand Parent(s)',
        'resp_1_f': 'Grand Parent(s)',
        'resp_1_g': 'Grand Parent(s)',
        'resp_1_h': 'Grand Parent(s)',
        'resp_1_i': 'Grand Parent(s)',
        'resp_1_j': 'Grand Parent(s)',
        'resp_1_k': 'Grand Parent(s)',
        'resp_2_a': 'Yes',
        'resp_2_b': 'Yes',
        'resp_2_c': 'Yes',
        'resp_2_d': 'Yes',
        'resp_2_e': 'Yes',
        'resp_2_f': 'Yes',
        'resp_2_g': 'Yes',
        'resp_2_h': 'Yes',
        'resp_2_i': 'Yes',
        'resp_3_a': 'Yes',
        'resp_3_b': 'Yes',
        'resp_3_c': 'Yes',
        'resp_3_d': 'Yes',
        'resp_3_e': 'Yes',
        'resp_3_f': 'Yes',
        'resp_4_a': 'Never',
        'resp_4_b': 'Never',
        'resp_4_c': 'Never',
        'resp_4_d': 'Never',
        'resp_4_e': 'Never',
        'resp_4_f': 'Never',
        'resp_4_g': 'Never',
        'resp_4_h': 'Never',
        'resp_4_i': 'Never',
        'resp_4_j': 'Never',
        'resp_4_k': 'Never',
        'resp_4_l': 'Never',
        'resp_4_m': 'Never',
        'resp_4_n': 'Never',
        'resp_4_o': 'Never',
        'resp_4_p': 'Never',
        'resp_4_q': 'Never',
        'resp_4_r': 'Never',
        'resp_4_s': 'Never',
        'resp_4_t': 'Never',     
    }

# # Define radio options and their corresponding indices
# job_type_options = ['Office Work', 'Field Work', 'Both', 'None']
# job_type_indices = {option: index for index, option in enumerate(job_type_options)}

# # Define selectbox options and their corresponding indices
# state_options = ['ABIA', 'ABUJA', 'LAGOS', 'KANO', 'KADUNA', 'OGUN', 'OYO']

enrollee_id = st.text_input('Kindly input your Member ID to confirm your eligibility')
#add a submit button
st.button("Submit", key="button1", help="Click or Press Enter")
enrollee_id = str(enrollee_id)

if enrollee_id:
    if enrollee_id in filled_wellness_df['MemberNo'].values:
        member_name = filled_wellness_df.loc[filled_wellness_df['MemberNo'] == enrollee_id, 'MemberName'].values[0]
        clientname = filled_wellness_df.loc[filled_wellness_df['MemberNo'] == enrollee_id, 'Client'].values[0]
        package = filled_wellness_df.loc[filled_wellness_df['MemberNo'] == enrollee_id, 'Wellness_benefits'].values[0]
        member_email = filled_wellness_df.loc[filled_wellness_df['MemberNo'] == enrollee_id, 'email'].values[0]
        provider = filled_wellness_df.loc[filled_wellness_df['MemberNo'] == enrollee_id, 'selected_provider'].values[0]
        app_date = filled_wellness_df.loc[filled_wellness_df['MemberNo'] == enrollee_id, 'selected_date'].values[0]
        app_session = filled_wellness_df.loc[filled_wellness_df['MemberNo'] == enrollee_id, 'selected_session'].values[0]
        submitted_date = np.datetime_as_string(filled_wellness_df.loc[filled_wellness_df['MemberNo'] == enrollee_id, 'date_submitted'].values[0], unit='D')
        #change the submitted_date to date format, add 6 weeks and return the date in this format e.g Wednesday, 31st December 2021
        six_weeks = dt.datetime.strptime(submitted_date, "%Y-%m-%d").date() + dt.timedelta(weeks=6)
        six_weeks = six_weeks.strftime('%A, %d %B %Y')
        # .strftime('%A, %d %B %Y')
               

        filled_message = f'Dear {member_name}.\n \n Please note that you have already booked your wellness appointment on {submitted_date}\
              and your booking confirmation has been sent to {member_email} as provided.\n\n Find your booking information below:\n\n Wellness\
                  Facility: {provider}.\n\n Wellness Benefits: {package}.\n\n Appointment Date: {app_date} - {app_session}.\n\n Kindly contact your\
                    Client Manager if you wish change your booking appointment.\n\n Note that your annual wellness is only valid till {six_weeks}.\n\n Thank you for choosing AVON HMO.'
        st.info(f'Dear {member_name}.\n\n'
                f'Please note that you have already booked your wellness appointment on {submitted_date} and your booking confirmation has been sent to {member_email} as provided\n\n'
                f'Wellness Facility: {provider}.\n\n'
                f'Wellness Benefits: {package}.\n\n'
                f'Appointment Date: {app_date} - {app_session}.\n\n'
                f'Kindly contact your Client Manager if you wish change your booking appointment.\n\n'
                f'###Note that your annual wellness is only valid till {six_weeks}.\n\n'
                ,icon="✅")
        
        #check if the user is logged in
        if 'logged_in' not in st.session_state:
            st.session_state.logged_in = False

        #Initialise form state
        if 'pacode' not in st.session_state:
            st.session_state.pacode = ''
        if 'pa_tests' not in st.session_state:
            st.session_state.pa_tests = []
        if 'pa_provider' not in st.session_state:
            st.session_state.pa_provider = ''
        if 'pa_issue_date' not in st.session_state:
            st.session_state.pa_issue_date = dt.date.today()

        #Login form in the sidebar
        if not st.session_state.logged_in:
            #create a button to enable contact center agent fill in the details of the generated PA code
            st.subheader('For Internal Use Only. Kindly Login to Access the PA Authorisation Page')
            st.sidebar.title("PA Authorisation Page")
            # st.sidebar.write("Login with your username and password to access the portal.")
            username = st.sidebar.text_input("Username")
            password = st.sidebar.text_input("Password", type="password")

        if st.sidebar.button("LOGIN"):
            if username == login_username and password == login_password:
                st.sidebar.success("Login Successful")
                st.session_state.logged_in = True
                st.experimental_rerun()
            else:
                st.error("Username/password is incorrect")

        #add a logout button
        else:
            if st.sidebar.button("LOGOUT", help="Click to logout"):
                st.session_state.logged_in = False
                st.experimental_rerun()

        if st.session_state.logged_in:
            st.write('Fill the details of the PA issued to Enrollee below to complete the wellness booking for the enrollee')

            with st.form(key='my_form',clear_on_submit=True):
                pacode = st.text_input('Input the Generated PA Code', value=st.session_state.pacode)
                pa_tests = st.multiselect('Select the Tests Conducted', options=['Physical Exam', 'Urinalysis', 'PCV', 'Blood Sugar', 'BP', 'Genotype', 'BMI',
                                                                                    'Chest X-Ray', 'Cholesterol', 'Liver Function Test', 'Electrolyte, Urea and Creatinine Test(E/U/Cr)',
                                                                                    'Stool Microscopy', 'Mammogram', 'Prostrate Specific Antigen(PSA)', 'Cervical Smear'],
                                                                                    default=st.session_state.pa_tests)
                # Convert pa_tests list to a comma-separated string
                pa_tests_str = ','.join(pa_tests)
                pa_provider = st.selectbox('Select the Wellness Provider', placeholder='Select Provider', options=['Select Provider'] + list(wellness_providers['PROVIDER'].unique()),
                                           index=0 if st.session_state.pa_provider == '' else wellness_providers['PROVIDER'].unique().tolist().index(st.session_state.pa_provider) + 1)
                pa_issue_date = st.date_input('Select the Date the PA was Issued',value=st.session_state.pa_issue_date)

                #add a submit button
                proceed = st.form_submit_button("PROCEED", help="Click to proceed")
            if proceed:
                #insert the generated PA code into the enrollee_annual_wellness_reg_web_portal on the database
                cursor = conn.cursor()
                query = """
                UPDATE enrollee_annual_wellness_reg_web_portal
                SET IssuedPACode = ?, PA_Tests = ?, PA_Provider = ?, PAIssueDate = ?
                WHERE MemberNo = ?
                """
                cursor.execute(query, pacode, pa_tests_str, pa_provider, pa_issue_date, enrollee_id)
                conn.commit()
                st.success('PA Code has been successfully updated for the enrollee')

                #clear the form fields
                st.session_state.form_submitted = True
                st.session_state.pacode = ''
                st.session_state.pa_tests = []
                st.session_state.pa_provider = ''
                st.session_state.pa_issue_date = dt.date.today()
                st.experimental_rerun()

        if 'form_submitted' in st.session_state:
            if st.session_state.form_submitted:
                st.session_state.form_submitted = False

    elif (enrollee_id not in filled_wellness_df['MemberNo'].values) & (enrollee_id in wellness_df['memberno'].values):
        enrollee_name = wellness_df.loc[wellness_df['memberno'] == enrollee_id, 'membername'].values[0]
        client = wellness_df.loc[wellness_df['memberno'] == enrollee_id, 'Client'].values[0]
        policy = wellness_df.loc[wellness_df['memberno'] == enrollee_id, 'PolicyName'].values[0]
        package = wellness_df.loc[wellness_df['memberno'] == enrollee_id, 'WellnessPackage'].values[0]
        age = int(wellness_df.loc[wellness_df['memberno'] == enrollee_id, 'Age'].values[0])

        #write a code to assign 6weeks from the current date to a variable
        six_week_dt = dt.date.today() + dt.timedelta(weeks=6)
        #convert six_weeks to this date format e.g Wednesday, 31st December 2021
        six_weeks = six_week_dt.strftime('%A, %d %B %Y')
        
        st.info(f'Dear {enrollee_name}.\n\n'
                f'Kindly confirm that your enrollment details matches with the info displayed below.\n\n'
                f'By proceeding to fill the form below, I understand and hereby acknowledge that my data would be collected and processed only for the performance of this wellness screening exercise.\n\n'
                f'### Please note that once you complete this form, you only have till {six_weeks} to complete your wellness check.',icon="✅")
        st.info(f'Company: {client}.\n\n Policy: {policy}.\n\n Please contact your Client Manager if this information does not match with your enrollment details')

        # #add a submit button
        # proceed = st.button("PROCEED", help="Click to proceed")
        # if proceed:
        st.subheader('Kindly fill all the fields below to proceed')

        email = st.text_input('Input a Valid Email Address', st.session_state.user_data['email'])
        mobile_num = st.text_input('Input a Valid Mobile Number', st.session_state.user_data['mobile_num'])
        gender = st.radio('Sex', options=['Male', 'Female'], index=['Male', 'Female'].index(st.session_state.user_data['gender']))
        job_type = st.selectbox('Occupation', options=['Mainly Desk Work', 'Mainly Field Work', 'Desk and Field Work', 'Physical Outdoor Work', 'Physical Indoor Work'], index=['Mainly Desk Work', 'Mainly Field Work', 'Desk and Field Work', 'Physical Outdoor Work', 'Physical Indoor Work'].index(st.session_state.user_data['job_type']))
        # age = st.number_input('Your Current Age', value=st.session_state.user_data['age'])
        state = st.selectbox('Your Current Location', options=wellness_providers['STATE'].unique())
        if client == 'UNITED BANK FOR AFRICA' and state == 'LAGOS':
            selected_provider = st.selectbox('Pick your Preferred Wellness Facility', options=['CERBA LANCET NIGERIA - Ikeja - Aviation Plaza, Ground Floor,31 Kodesoh Street, Ikeja',
                                                                                               'CERBA LANCET NIGERIA - Victoria Island - 3 Babatunde Jose Street Off Ademola Adetokunbo street, V/I',
                                                                                               'UBA Head Office - Marina, Lagos Island.'])
        elif client == 'STANDARD CHARTERED BANK NIGERIA LIMITED' and state == 'LAGOS':
            available_provider = wellness_providers.loc[wellness_providers['STATE'] == state, 'PROVIDER'].unique()
            additional_provider = 'Onsite - SCB Head Office - 142, Ahmadu Bello Way, Victoria Island'
            available_provider = list(available_provider) + [additional_provider]
            selected_provider = st.selectbox('Pick your Preferred Wellness Facility', options=available_provider)
        
        elif client == 'STANDARD CHARTERED BANK NIGERIA LIMITED' and state == 'RIVERS ':
            available_provider = wellness_providers.loc[wellness_providers['STATE'] == state, 'PROVIDER'].unique()
            additional_provider = 'Onsite - SCB Office, 143, Port Harcourt Aba Express Road (F-0)'
            available_provider = list(available_provider) + [additional_provider]
            selected_provider = st.selectbox('Pick your Preferred Wellness Facility', options=available_provider)

        elif client == 'STANDARD CHARTERED BANK NIGERIA LIMITED' and state == 'FCT ':
            available_provider = wellness_providers.loc[wellness_providers['STATE'] == state, 'PROVIDER'].unique()
            additional_provider = 'Onsite - SCB Office, 374 Ademola Adetokunbo Crescent Wuse II, Beside Visa/Airtel Building'
            available_provider = list(available_provider) + [additional_provider]
            selected_provider = st.selectbox('Pick your Preferred Wellness Facility', options=available_provider)
            
        else:
            available_provider = wellness_providers.loc[wellness_providers['STATE'] == state, 'PROVIDER'].unique()
            selected_provider = st.selectbox('Pick your Preferred Wellness Facility', options=available_provider)
        
        if client == 'UNITED BANK FOR AFRICA' and age >= 40 and gender == 'Female':
            benefits = 'Physical Exam, Urinalysis, PCV, Blood Sugar, BP, Genotype, BMI, Chest X-Ray, Cholesterol, Liver Function Test, Electrolyte,Urea and Creatinine Test, Cervical Smear'
        elif client == 'UNITED BANK FOR AFRICA' and age >= 40 and gender == 'Male':
            benefits = 'Physical Exam, Urinalysis, PCV, Blood Sugar, BP, Genotype, BMI, Chest X-Ray, Cholesterol, Liver Function Test, Electrolyte,Urea and Creatinine Test, Prostrate Specific Antigen'
        elif client == 'UNITED BANK FOR AFRICA' and age < 40:
            benefits = 'Physical Exam, Urinalysis, PCV, Blood Sugar, BP, Genotype, BMI, Chest X-Rray, Cholesterol, Liver Function Test, Electrolyte,Urea and Creatinine Test'
        else:
            benefits = package

        if client == 'PIVOT   GIS LIMITED':
            current_date = dt.date.today()
            # Define the maximum date as '2023-12-18' as a datetime.date object
            max_date = dt.date(2023, 12, 31)
            # Display a date picker
            selected_date = st.date_input("Select Your Preferred Appointment Date", min_value=current_date,max_value=max_date)
        elif client == 'UNITED BANK FOR AFRICA':
            current_date = dt.date.today()
            # Define the maximum date as '2023-12-18' as a datetime.date object
            max_date = dt.date(2023, 12, 31)
            # Display a date picker
            selected_date = st.date_input("Select Your Preferred Appointment Date", min_value=current_date,max_value=max_date)
        else:
            max_date = dt.date(2024, 12, 31)
            selected_date = st.date_input('Pick Your Preferred Appointment Date',max_value=max_date)


        if state == 'LAGOS':
            if selected_provider == 'UBA Head Office - Marina, Lagos Island.':
                st.info('Fill the questionaire below to complete your wellness booking')
                selected_date_str = 'To be Communicated by the HR'
                session = ''
                
            elif (selected_provider == 'CERBA LANCET NIGERIA - Ikeja - Aviation Plaza, Ground Floor, 31 Kodesoh Street, Ikeja') or (selected_provider == 'CERBA LANCET NIGERIA - Victoria Island - 3 Babatunde Jose Street Off Ademola Adetokunbo street, V/I'):        
                selected_date_str = selected_date.strftime('%Y-%m-%d')

                booked_sessions_from_db = filled_wellness_df.loc[(filled_wellness_df['selected_date'] == selected_date_str) &
                                                                (filled_wellness_df['selected_provider'] == selected_provider),
                                                                'selected_session'].values.tolist()

                available_sessions = ['08:00 AM - 09:00 AM', '09:00 AM - 10:00 AM', '10:00 AM - 11:00 AM', '11:00 AM - 12:00 PM',
                                        '12:00 PM - 01:00 PM', '01:00 PM - 02:00 PM', '02:00 PM - 03:00 PM', '03:00 PM - 04:00 PM']
                # Create a dictionary to keep track of the number of bookings for each session
                session_bookings_count = {session: booked_sessions_from_db.count(session) for session in available_sessions}

                # Filter available sessions to only include those with less than 3 bookings
                available_sessions = [session for session in available_sessions if session_bookings_count[session] < 3]
                st.info('Please note that the Facilities are opened between the 8:00 am and 5:00 pm, Monday - Friday and 8:00 am - 2:00 pm on \
                        Saturdays.\n\n If you notice any missing session between their opening hours, this implies that the missing session has been\
                        fully booked and no longer available for the selected date')
                
                if not available_sessions:
                    st.warning("All sessions for the selected date at this facility are fully booked. Please select another date or facility.")
                else:
                    session = st.radio('Select your preferred time from the list of available sessions below', options=available_sessions)
                    st.info('Fill the questionaire below to complete your wellness booking')
            else:
                selected_date_str = selected_date.strftime('%Y-%m-%d')
                session = ''
                st.info('Fill the questionaire below to complete your wellness booking')

        else:
            selected_date_str = selected_date.strftime('%Y-%m-%d')
            session = ''
            st.info('Fill the questionaire below to complete your wellness booking')

        # Define a list of Family Medical History Conditions
        questions1 = [
            'a. HYPERTENSION (HIGH BLOOD PRESSURE)',
            'b. DIABETES',
            'c. CANCER (ANY TYPE)',
            'd. ASTHMA',
            'e. ARTHRITIS',
            'f. HIGH CHOLESTEROL',
            'g. HEART ATTACK',
            'h. EPILEPSY',
            'i. TUBERCLOSIS',
            'j. SUBSTANCE DEPENDENCY',
            'k. MENTAL ILLNESS',
        ]

        # Define the generic options
        options1 = ["Grand Parent(s)", "Parent(s)", "Uncle/Aunty", "Nobody"]

        # Label the section accordingly
        st.title("1. Family Medical History")
        st.subheader('Have any of your family members experienced any of the following conditions?')


        # Create a dictionary to store user responses
        user_responses1 = {}

        for question1 in questions1:
            st.markdown(f"**{question1}**")  # Display the question in bold

            # Use radio buttons for these set of questions with a unique key
            unique_key1 = f"{question1}_response"
            response1 = st.radio(f'Response to {question1}', options1, key=unique_key1, label_visibility='collapsed')

            # Store the response in the dictionary
            user_responses1[question1] = response1

        # Assign the user's responses to a variable
        resp_1_a = user_responses1['a. HYPERTENSION (HIGH BLOOD PRESSURE)']
        resp_1_b = user_responses1['b. DIABETES']
        resp_1_c = user_responses1['c. CANCER (ANY TYPE)']
        resp_1_d = user_responses1['d. ASTHMA']
        resp_1_e = user_responses1['e. ARTHRITIS']
        resp_1_f = user_responses1['f. HIGH CHOLESTEROL']
        resp_1_g = user_responses1['g. HEART ATTACK']
        resp_1_h = user_responses1['h. EPILEPSY']
        resp_1_i = user_responses1['i. TUBERCLOSIS']
        resp_1_j = user_responses1['j. SUBSTANCE DEPENDENCY']
        resp_1_k = user_responses1['k. MENTAL ILLNESS']
        


        # Define a list of personal medical history questions
        questions2 = [
            'i. HYPERTENSION (HIGH BLOOD PRESSURE)',
            'ii. DIABETES',
            'iii. CANCER (ANY TYPE)',
            'iv. ASTHMA',
            'v. ULCER',
            'vi. POOR VISION',
            'vii. ALLERGY',
            'viii. ARTHRITIS/LOW BACK PAIN',
            'ix. ANXIETY/DEPRESSION',
        ]

        # Define the generic responses for these set of questions
        options2 = ['Yes', 'No', 'Yes, but not on Medication']

        # Label the section accordingly
        st.title("2. Personal Medical History")
        st.subheader('Do you have any of the following condition(s) that you are managing?')

        # Create a dictionary to store user responses
        user_responses2 = {}

        for question2 in questions2:
            st.markdown(f"**{question2}**")  # Display the question in bold

            # Use radio buttons for these set of questions with a unique key
            unique_key2 = f"{question2}_response"
            response2 = st.radio(f'Response to {question2}', options2, key=unique_key2, label_visibility='collapsed')

            # Store the response in the dictionary
            user_responses2[question2] = response2

        # Assign the user's responses to a variable
        resp_2_a = user_responses2['i. HYPERTENSION (HIGH BLOOD PRESSURE)']
        resp_2_b = user_responses2['ii. DIABETES']
        resp_2_c = user_responses2['iii. CANCER (ANY TYPE)']
        resp_2_d = user_responses2['iv. ASTHMA']
        resp_2_e = user_responses2['v. ULCER']
        resp_2_f = user_responses2['vi. POOR VISION']
        resp_2_g = user_responses2['vii. ALLERGY']
        resp_2_h = user_responses2['viii. ARTHRITIS/LOW BACK PAIN']
        resp_2_i = user_responses2['ix. ANXIETY/DEPRESSION']
        
        # Define a list of surgery related survey questions
        questions3 = [
            'i. CEASAREAN SECTION',
            'ii. FRACTURE REPAIR',
            'iii. HERNIA',
            'iv. LUMP REMOVAL',
            'v. APPENDICETOMY',
            'vi. SPINE SURGERY',
        ]

        # Define the generic options for these set of questions
        options3 = ['Yes', 'No']

        # Create a Streamlit app
        st.title("3. Personal Surgical History")
        st.subheader('Have you ever had surgery for any of the following?')

        # Create a dictionary to store user responses
        user_responses3 = {}

        for question3 in questions3:
            st.markdown(f"**{question3}**")  # Display the question in bold

            # Use radio buttons for these set of questions with a unique key
            unique_key3 = f"{question3}_response"
            response3 = st.radio(f'Response to {question2}', options3, key=unique_key3, label_visibility='collapsed')

            # Store the response in the dictionary
            user_responses3[question3] = response3

        # Assign the user's responses to a variable
        resp_3_a = user_responses3['i. CEASAREAN SECTION']
        resp_3_b = user_responses3['ii. FRACTURE REPAIR']
        resp_3_c = user_responses3['iii. HERNIA']
        resp_3_d = user_responses3['iv. LUMP REMOVAL']
        resp_3_e = user_responses3['v. APPENDICETOMY']
        resp_3_f = user_responses3['vi. SPINE SURGERY']

        
        # Define a list of emotional wellness related survey questions
        questions4 = [
            'a. I avoid eating foods that are high in fat',
            'b. I have been avoiding the use or minimise my exposure to alcohol',
            'c. I have been avoiding the use of tobacco products',
            'd. I am physically fit and exercise at least 30 minutes every day',
            'e. I have been eating vegetables and fruits at least 3 times weekly',
            'f. I drink 6-8 glasses of water a day',
            'g. I maintain my weight within the recommendation for my weight, age and height',
            'h. My blood pressure is within normal range without the use of drugs',
            'i. My cholesterol level is within the normal range',
            'j. I easily make decisions without worry',
            'k. I enjoy more than 5 hours of sleep at night',
            'l. I enjoy my work and life',
            'm. I enjoy the support from friends and family',
            'n. I feel bad about myself or that I am a failure or have let myself or my family down',
            'o. I have poor appetite or I am over-eating',
            'p. I feel down, depressed, hopeless, tired or have little energy',
            'q. I have trouble falling asleep, staying asleep, or sleeping too much',
            'r. I have no interest or pleasure in doing things',
            's. I have trouble concentrating on things, such as reading the newspaper, or watching TV',
            't. I think I would be better off dead or better off hurting myself in some way',
        ]

        # Define the generic options for these set of questions
        options4 = ['Never', 'Occasional', 'Always', 'I Do Not Know']

        # Create a Streamlit app
        st.title("4. Health Survey Questionnaire")
        st.subheader('Kindly provide valid responses to the following questions')

        # Create a dictionary to store user responses
        user_responses4 = {}

        for question4 in questions4:
            st.markdown(f"**{question4}**")  # Display the question in bold

            # Use radio buttons for Likert scale with a unique key
            unique_key4 = f"{question4}_response"
            response4 = st.radio(f'Response to {question4}', options4, key=unique_key4, label_visibility='collapsed')

            # Store the response in the dictionary
            user_responses4[question4] = response4

        # Assign the user's responses to a variable
        resp_4_a = user_responses4['a. I avoid eating foods that are high in fat']
        resp_4_b = user_responses4['b. I have been avoiding the use or minimise my exposure to alcohol']
        resp_4_c = user_responses4['c. I have been avoiding the use of tobacco products']
        resp_4_d = user_responses4['d. I am physically fit and exercise at least 30 minutes every day']
        resp_4_e = user_responses4['e. I have been eating vegetables and fruits at least 3 times weekly']
        resp_4_f = user_responses4['f. I drink 6-8 glasses of water a day']
        resp_4_g = user_responses4['g. I maintain my weight within the recommendation for my weight, age and height']
        resp_4_h = user_responses4['h. My blood pressure is within normal range without the use of drugs']
        resp_4_i = user_responses4['i. My cholesterol level is within the normal range']
        resp_4_j = user_responses4['j. I easily make decisions without worry']
        resp_4_k = user_responses4['k. I enjoy more than 5 hours of sleep at night']
        resp_4_l = user_responses4['l. I enjoy my work and life']
        resp_4_m = user_responses4['m. I enjoy the support from friends and family']
        resp_4_n = user_responses4['n. I feel bad about myself or that I am a failure or have let myself or my family down']
        resp_4_o = user_responses4['o. I have poor appetite or I am over-eating']
        resp_4_p = user_responses4['p. I feel down, depressed, hopeless, tired or have little energy']
        resp_4_q = user_responses4['q. I have trouble falling asleep, staying asleep, or sleeping too much']
        resp_4_r = user_responses4['r. I have no interest or pleasure in doing things']
        resp_4_s = user_responses4['s. I have trouble concentrating on things, such as reading the newspaper, or watching TV']
        resp_4_t = user_responses4['t. I think I would be better off dead or better off hurting myself in some way']
        

        # Submit button
        if st.button("Submit", help="Click to submit"):
            st.session_state.user_data['member_number'] = enrollee_id
            st.session_state.user_data['EnrolleeName'] = enrollee_name
            st.session_state.user_data['client'] = client
            st.session_state.user_data['policy'] = policy
            st.session_state.user_data['email'] = email
            st.session_state.user_data['mobile_num'] = mobile_num
            st.session_state.user_data['age'] = age
            st.session_state.user_data['state'] = state
            st.session_state.user_data['selected_provider'] = selected_provider
            st.session_state.user_data['job_type'] = job_type
            st.session_state.user_data['gender'] = gender
            st.session_state.user_data['wellness_benefit'] = benefits
            st.session_state.user_data['selected_date_str'] = selected_date_str
            st.session_state.user_data['session'] = session
            st.session_state.user_data['resp_1_a'] = resp_1_a
            st.session_state.user_data['resp_1_b'] = resp_1_b
            st.session_state.user_data['resp_1_c'] = resp_1_c
            st.session_state.user_data['resp_1_d'] = resp_1_d
            st.session_state.user_data['resp_1_e'] = resp_1_e
            st.session_state.user_data['resp_1_f'] = resp_1_f
            st.session_state.user_data['resp_1_g'] = resp_1_g
            st.session_state.user_data['resp_1_h'] = resp_1_h
            st.session_state.user_data['resp_1_i'] = resp_1_i
            st.session_state.user_data['resp_1_j'] = resp_1_j
            st.session_state.user_data['resp_1_k'] = resp_1_k
            st.session_state.user_data['resp_2_a'] = resp_2_a
            st.session_state.user_data['resp_2_b'] = resp_2_b
            st.session_state.user_data['resp_2_c'] = resp_2_c
            st.session_state.user_data['resp_2_d'] = resp_2_d
            st.session_state.user_data['resp_2_e'] = resp_2_e
            st.session_state.user_data['resp_2_f'] = resp_2_f
            st.session_state.user_data['resp_2_g'] = resp_2_g
            st.session_state.user_data['resp_2_h'] = resp_2_h
            st.session_state.user_data['resp_2_i'] = resp_2_i
            st.session_state.user_data['resp_3_a'] = resp_3_a
            st.session_state.user_data['resp_3_b'] = resp_3_b
            st.session_state.user_data['resp_3_c'] = resp_3_c
            st.session_state.user_data['resp_3_d'] = resp_3_d
            st.session_state.user_data['resp_3_e'] = resp_3_e
            st.session_state.user_data['resp_3_f'] = resp_3_f
            st.session_state.user_data['resp_4_a'] = resp_4_a
            st.session_state.user_data['resp_4_b'] = resp_4_b
            st.session_state.user_data['resp_4_c'] = resp_4_c
            st.session_state.user_data['resp_4_d'] = resp_4_d
            st.session_state.user_data['resp_4_e'] = resp_4_e
            st.session_state.user_data['resp_4_f'] = resp_4_f
            st.session_state.user_data['resp_4_g'] = resp_4_g
            st.session_state.user_data['resp_4_h'] = resp_4_h
            st.session_state.user_data['resp_4_i'] = resp_4_i
            st.session_state.user_data['resp_4_j'] = resp_4_j
            st.session_state.user_data['resp_4_k'] = resp_4_k
            st.session_state.user_data['resp_4_l'] = resp_4_l
            st.session_state.user_data['resp_4_m'] = resp_4_m
            st.session_state.user_data['resp_4_n'] = resp_4_n
            st.session_state.user_data['resp_4_o'] = resp_4_o
            st.session_state.user_data['resp_4_p'] = resp_4_p
            st.session_state.user_data['resp_4_q'] = resp_4_q
            st.session_state.user_data['resp_4_r'] = resp_4_r
            st.session_state.user_data['resp_4_s'] = resp_4_s
            st.session_state.user_data['resp_4_t'] = resp_4_t

            cursor = conn.cursor()
            try:
                # Define an SQL INSERT statement to add data to your database table
                insert_query = """
                INSERT INTO [dbo].[enrollee_annual_wellness_reg_web_portal] (MemberNo, MemberName, client, policy, email, mobile_num, job_type, age, state, selected_provider,
                sex, wellness_benefits, selected_date, selected_session,
                [HIGH BLOOD PRESSURE - Family],[Diabetes - Family],[Cancer - Family],[Asthma - Family],[Arthritis - Family]
                ,[High Cholesterol],[Heart Attack - Family],[Epilepsy - Family],[Tuberclosis - Family],[Substance Dependency - Family]
                ,[Mental Illness - Family],[HIGH BLOOD PRESSURE - Personal],[Diabetes - Personal],[Cancer - Personal],[Asthma - Personal]
                ,[Ulcer - Personal],[Poor Vision - Personal],[Allergy - Personal],[Arthritis/Low Back Pain - Personal],[Anxiety/Depression - Personal]
                ,[CEASAREAN SECTION],[FRACTURE REPAIR],[HERNIA],[LUMP REMOVAL] ,[APPENDICETOMY],[SPINE SURGERY],[I AVOID EATING FOODS THAT ARE HIGH IN FAT]
                ,[I AVOID THE USE OR MINIMISE MY EXPOSURE TO ALCOHOL],[I AVOID THE USE OF TOBACCO PRODUCTS],[I AM PHYSICALLY FIT AND EXERCISE AT LEAST 30 MINUTES EVERY DAY]
                ,[I EAT VEGETABLES AND FRUITS AT LEAST 3 TIMES WEEKLY],[I DRINK 6-8 GLASSES OF WATER A DAY],[I MAINTAIN MY WEIGHT WITHIN THE RECOMMENDATION FOR MY WEIGHT, AGE AND HEIGHT]
                ,[MY BLOOD PRESSURE IS WITHIN NORMAL RANGE WITHOUT THE USE OF DRUGS],[MY CHOLESTEROL LEVEL IS WITHIN THE NORMAL RANGE]
                ,[I EASILY MAKE DECISIONS WITHOUT WORRY],[I ENJOY MORE THAN 5 HOURS OF SLEEP AT NIGHT],[I ENJOY MY WORK AND LIFE]
                ,[I ENJOY THE SUPPORT FROM FRIENDS AND FAMILY],[I FEEL BAD ABOUT MYSELF OR THAT I AM A FAILURE OR HAVE LET MYSELF OR MY FAMILY DOWN]
                ,[I HAVE POOR APPETITE OR I AM OVER-EATING],[I FEEL DOWN, DEPRESSED, HOPELESS, TIRED OR HAVE LITTLE ENERGY]
                ,[I HAVE TROUBLE FALLING ASLEEP, STAYING ASLEEP, OR SLEEPING TOO MUCH],[I HAVE NO INTEREST OR PLEASURE IN DOING THINGS]
                ,[I HAVE TROUBLE CONCENTRATING ON THINGS, SUCH AS READING THE NEWSPAPER, OR WATCHING TV]
                ,[THOUGHT THAT I WOULD BE BETTER OFF DEAD OR BETTER OFF HURTING MYSELF IN SOME WAY],
                date_submitted)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                """

                # Execute the INSERT statement with the user's data
                cursor.execute(insert_query, (
                    st.session_state.user_data['member_number'],
                    st.session_state.user_data['EnrolleeName'],
                    st.session_state.user_data['client'],
                    st.session_state.user_data['policy'],
                    st.session_state.user_data['email'],
                    st.session_state.user_data['mobile_num'],
                    st.session_state.user_data['job_type'],
                    st.session_state.user_data['age'],
                    st.session_state.user_data['state'],
                    st.session_state.user_data['selected_provider'],
                    st.session_state.user_data['gender'],
                    st.session_state.user_data['wellness_benefit'],
                    st.session_state.user_data['selected_date_str'],
                    st.session_state.user_data['session'],
                    st.session_state.user_data['resp_1_a'],
                    st.session_state.user_data['resp_1_b'],
                    st.session_state.user_data['resp_1_c'],
                    st.session_state.user_data['resp_1_d'],
                    st.session_state.user_data['resp_1_e'],
                    st.session_state.user_data['resp_1_f'],
                    st.session_state.user_data['resp_1_g'],
                    st.session_state.user_data['resp_1_h'],
                    st.session_state.user_data['resp_1_i'],
                    st.session_state.user_data['resp_1_j'],
                    st.session_state.user_data['resp_1_k'],
                    st.session_state.user_data['resp_2_a'],
                    st.session_state.user_data['resp_2_b'],
                    st.session_state.user_data['resp_2_c'],
                    st.session_state.user_data['resp_2_d'],
                    st.session_state.user_data['resp_2_e'],
                    st.session_state.user_data['resp_2_f'],
                    st.session_state.user_data['resp_2_g'],
                    st.session_state.user_data['resp_2_h'],
                    st.session_state.user_data['resp_2_i'],
                    st.session_state.user_data['resp_3_a'],
                    st.session_state.user_data['resp_3_b'],
                    st.session_state.user_data['resp_3_c'],
                    st.session_state.user_data['resp_3_d'],
                    st.session_state.user_data['resp_3_e'],
                    st.session_state.user_data['resp_3_f'],
                    st.session_state.user_data['resp_4_a'],
                    st.session_state.user_data['resp_4_b'],
                    st.session_state.user_data['resp_4_c'],
                    st.session_state.user_data['resp_4_d'],
                    st.session_state.user_data['resp_4_e'],
                    st.session_state.user_data['resp_4_f'],
                    st.session_state.user_data['resp_4_g'],
                    st.session_state.user_data['resp_4_h'],
                    st.session_state.user_data['resp_4_i'],
                    st.session_state.user_data['resp_4_j'],
                    st.session_state.user_data['resp_4_k'],
                    st.session_state.user_data['resp_4_l'],
                    st.session_state.user_data['resp_4_m'],
                    st.session_state.user_data['resp_4_n'],
                    st.session_state.user_data['resp_4_o'],
                    st.session_state.user_data['resp_4_p'],
                    st.session_state.user_data['resp_4_q'],
                    st.session_state.user_data['resp_4_r'],
                    st.session_state.user_data['resp_4_s'],
                    st.session_state.user_data['resp_4_t'],
                    dt.datetime.now()
                ))

                # Commit the transaction to save the data to the database
                conn.commit()

                # Provide feedback to the user
                st.info(f'Thank you {enrollee_name}.\n\n'
                    f'Your annual wellness has been successfully booked.\n\n'
                    f'###Please note that you have from now till {six_weeks} to complete your annual wellness exercise.')

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

            finally:
                # Close the cursor and the database connection
                cursor.close()
                conn.close()

                recipient_email = email
                subject = 'AVON ENROLLEE WELLNESS APPOINTMENT CONFIRMATION'
                # Create a table (HTML format) with some sample data
                msg_befor_table = f'''
                Dear {enrollee_name},<br><br>
                We hope you are staying safe.<br><br>
                You have been scheduled for a wellness screening at your selected provider, see the below table for details.<br><br>
                '''
                #create a table with the booking information
                wellness_table = {
                    "Appointment Date": [selected_date_str + ' - ' + session],
                    "Wellness Facility": [selected_provider],
                    "Wellness Benefits": [benefits]
                }

                #convert the wellness_table to a html table
                wellness_table_html = pd.DataFrame(wellness_table).to_html(index=False, escape=False, justify='center')

                #initialise an empty table
                table_html = f"""
                <style>
                table {{
                        border: 1px solid #1C6EA4;
                        background-color: #EEEEEE;
                        width: 100%;
                        text-align: left;
                        border-collapse: collapse;
                        }}
                        table td, table th {{
                        border: 1px solid #AAAAAA;
                        padding: 3px 2px;
                        }}
                        table tbody td {{
                        font-size: 13px;
                        }}
                        table thead {{
                        background: #59058D;
                        border-bottom: 2px solid #444444;
                        }}
                        table thead th {{
                        font-size: 15px;
                        font-weight: bold;
                        color: #FFFFFF;
                        border-left: 2px solid #D0E4F5;
                        }}
                        table thead th:first-child {{
                        border-left: none;
                        }}
                </style>
                <table>
                {wellness_table_html}
                </table>
                """

                # table_html += f"""
                # <tr>
                #     <td>{selected_date_str} - {session}</td>
                #     <td>{selected_provider}</td>
                #     <td>{benefits}</td>
                # </tr>
                # """

                # table_html += "</table>" #close the table

                #customised text for upcountry
                text_after_table = f'''
                <br>Kindly note the following requirements for your wellness exercise:<br><br>

                -Present at the hospital with your Avon member ID number ({enrollee_id})/ Ecard.<br>
                -Provide the facility with your valid email address to mail your result.<br>
                -Visit your designated centers between the hours of 8 am - 11 am any day of the week from the scheduled date communicated.<br>
                -Arrive at the facility fasting i.e. last meals should be before 9 pm the previous night and nothing should be eaten that morning before the test.
                You are allowed to drink up to two cups of water.<br><br>

                For the best results of your screening, it is advisable for blood tests to be done on or before 10 am.<br><br>
                Your results will be strictly confidential and will be sent to you directly via your email. You are advised to review
                your results with your primary care provider for relevant medical advice.<br><br>

                Should you require assistance at any time or wish to make any complaint about the service at any of the facilities, 
                please contact our Call-Center at 0700-277-9800  or send us a chat on WhatsApp at 0912-603-9532. 
                You can also send us an email at callcentre@avonhealthcare.com. Please be assured that an agent would always be on standby to assist you.<br><br>

                Thank you for choosing Avon HMO,<br><br>

                Medical Services.<br>

                '''

                #customised text for Lagos enrollees
                text_after_table1 = f'''
                <br>Kindly note that wellness exercise at your selected facility is strictly by appointment and
                and you are expected to be available at the facility on the appointment date as selected by you.<br><br>
                Also, note that you will be required to:<br><br>

                -Present at the facility with your Avon member ID number ({enrollee_id})/ Ecard.<br>
                -Provide the facility with your valid email address to mail your result.<br>
                -You are advised to be present at your selected facility 15 mins before your scheduled time.<br><br>
                
                Your results will be strictly confidential and will be sent to you directly via your email. You are advised to review
                your results with your primary care provider for relevant medical advice.<br><br>

                Should you require assistance at any time or wish to make any complaint about the service at any of the facilities, 
                please contact our Call-Center at 0700-277-9800  or send us a chat on WhatsApp at 0912-603-9532. 
                You can also send us an email at callcentre@avonhealthcare.com. Please be assured that an agent would always be on standby to assist you.<br><br>

                Thank you for choosing Avon HMO,<br><br>

                Medical Services.<br>

                '''
                head_office_msg = f'''
                Dear {enrollee_name},<br><br>
                We hope you are staying safe.<br><br>
                You have been scheduled for a wellness screening at {selected_provider}.<br><br>
                Find listed below your wellness benefits:<br><br><b>{benefits}</b>.<br><br>
                Kindly note the following regarding your wellness appointment:<br><br>
                - HR will reach out to you with a scheduled date and time for your annual wellness.<br><br>
                - Once scheduled, you are to present your Avon HMO ID card or member ID - {enrollee_id} at the point of accessing your annual wellness check.<br><br>
                - The wellness exercise will take place at the designated floor which will be communicated to you by the HR between 9 am and 4 pm from Monday – Friday. <br><br>
                - For the most accurate fasting blood sugar test results, it is advisable for blood tests to be done before 10am. <br><br>
                - Staff results will be sent to the email addresses provided by them to the wellness providers.<br><br>
                - There will be consultation with a physician to review immediate test results on-site while other test results that are not readily available will be reviewed by a physician at your Primary Care Provider.<br><br>
                
                Should you require assistance at any time or wish to make any complaint about the service rendered during this wellness exercise,
                please contact our Call-Center at 0700-277-9800 or send us a chat on WhatsApp at 0912-603-9532.
                You can also send us an email at callcentre@avonhealthcare.com. Please be assured that an agent would always be on standby to assist you.<br><br>
                Thank you for choosing Avon HMO.<br><br>
                Medical Services.<br>
                '''

                pivotgis_msg = f'''
                <br>Kindly note that this wellness activation is only valid till the 31st of December, 2023.<br><br>
                Also, note that you will be required to:<br><br>

                -Present at the hospital with your Avon member ID number ({enrollee_id})/ Ecard.<br>
                -Provide the facility with your valid email address to mail your result.<br>
                -You are advised to be present at your selected facility 15 mins before your scheduled time.<br><br>
                
                Your results will be strictly confidential and will be sent to you directly via your email. You are advised to review
                your results with your primary care provider for relevant medical advice.<br><br>

                Should you require assistance at any time or wish to make any complaint about the service at any of the facilities, 
                please contact our Call-Center at 0700-277-9800  or send us a chat on WhatsApp at 0912-603-9532. 
                You can also send us an email at callcentre@avonhealthcare.com. Please be assured that an agent would always be on standby to assist you.<br><br>

                Thank you for choosing Avon HMO,<br><br>

                Medical Services.<br>
                '''

                # html_string = f'''<!DOCTYPE html>
                #     <html lang="en">
                #     <head>
                #         <meta charset="UTF-8">
                #         <meta name="viewport" content="width=device-width, initial-scale=1.0">
                #         <title>Email Message</title>
                #         <style>
                #             /* Define your styles here */

                #             .email-container {{
                #                 max-width: 600px;
                #                 margin: 0 auto;
                #                 padding: 20px;
                #                 border: 1px solid #ccc;
                #                 border-radius: 10px;
                #             }}
                #             .company-logo {{
                #                 max-width: 150px;
                #                 height: auto;
                #                 margin-bottom: 20px;
                #             }}
                #             .table-container {{
                #                 border: 1px solid #1C6EA4;
                #                 background-color: #EEEEEE;
                #                 width: 100%;
                #                 text-align: left;
                #                 border-collapse: collapse;
                #                 margin-bottom: 20px;
                #             }}
                #             .table-container td, .table-container th {{
                #                 border: 1px solid #AAAAAA;
                #                 padding: 3px 2px;
                #             }}
                #             .table-container tbody td {{
                #                 font-size: 13px;
                #             }}
                #             .table-container thead {{
                #                 background: #59058D;
                #                 border-bottom: 2px solid #444444;
                #             }}
                #             .table-container thead th {{
                #                 font-size: 15px;
                #                 font-weight: bold;
                #                 color: #FFFFFF;
                #                 border-left: 2px solid #D0E4F5;
                #             }}
                #             .table-container thead th:first-child {{
                #                 border-left: none;
                #             }}
                #         </style>
                #     </head>
                #     <body>
                #         <div class="email-container">
                #             <img src="wellness_image.png" alt="Company Logo" class="company-logo">
                #             <div class="table-container">
                #                 <!-- Your table HTML goes here -->
                #                 <table>
                #                     {wellness_table_html}
                #                 </table>
                #             </div>
                #             <!-- Additional text after the table -->
                #             <p>{text_after_table}</p>
                #         </div>
                #     </body>
                #     </html>
                #     '''

                #put the table and text together in a text border with an image added

                upcountry_message = msg_befor_table + table_html + text_after_table
                cerba_message = msg_befor_table + table_html + text_after_table1
                pivot_msg = msg_befor_table + table_html + pivotgis_msg
            
                myemail = 'noreply@avonhealthcare.com'
                password = os.environ.get('emailpassword')
                # password = st.secrets["emailpassword"]
                #add a condition to use the citron_bcc_list whenever any of the CITRON wellness providers is selected by the enrollee
                if (selected_provider == 'ECHOLAB - Opposite mararaba medical centre, Tipper Garage, Mararaba') or (selected_provider == 'TOBIS CLINIC - Chief Melford Okilo Road Opposite Sobaz Filling Station, Akenfa –Epie') or (selected_provider == 'ECHOLAB - 375B Nnebisi Road, Umuagu, Asaba'):
                    bcc_email_list = ['ademola.atolagbe@avonhealthcare.com', 'client.services@avonhealthcare.com',
                                'callcentre@avonhealthcare.com','medicalservicesdepartment@avonhealthcare.com', 
                                'adeoluwa@citron-health.com', 'hello@citron-health.com']
                else:
                    bcc_email_list = ['ademola.atolagbe@avonhealthcare.com', 'client.services@avonhealthcare.com',
                                 'callcentre@avonhealthcare.com','medicalservicesdepartment@avonhealthcare.com']
                    
                to_email_list =[recipient_email]

                try:
                    server = smtplib.SMTP('smtp.office365.com', 587)
                    server.starttls()

                    #login to outlook account
                    server.login(myemail, password)

                    #create a MIMETesxt object for the email message
                    msg = MIMEMultipart()
                    msg['From'] = 'AVON HMO Client Services'
                    msg['To'] = recipient_email
                    msg['Bcc'] = ', '.join(bcc_email_list)
                    msg['Subject'] = subject
                    if client == 'UNITED BANK FOR AFRICA':
                        if selected_provider == 'UBA Head Office - Marina, Lagos Island.':
                            msg.attach(MIMEText(head_office_msg, 'html'))
                        # elif selected_provider == 'UBA FESTAC Branch.':
                        #     msg.attach(MIMEText(festac_office_msg, 'html'))
                        elif (selected_provider == 'CERBA LANCET NIGERIA - Ikeja - Aviation Plaza, Ground Floor, 31 Kodesoh Street, Ikeja') or (selected_provider == 'CERBA LANCET NIGERIA - Victoria Island - 3 Babatunde Jose Street Off Ademola Adetokunbo street, V/I'):
                            msg.attach(MIMEText(cerba_message, 'html'))
                        else:
                            msg.attach(MIMEText(upcountry_message, 'html'))
                    else:
                        msg.attach(MIMEText(upcountry_message, 'html'))


                    all_recipients = to_email_list + bcc_email_list
                    #send the email
                    server.sendmail(myemail, all_recipients, msg.as_string())
                    server.quit()

                    st.success('A confirmation Email has been sent to your provided email')
                except Exception as e:
                    st.error(f'An error occurred: {e}')
       
    elif enrollee_id not in wellness_df['memberno'].values:
        st.info('You are not eligible to participate, please contact your HR or Client Manager')
else:
    st.write('You must input your Member number to continue')