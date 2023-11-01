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

query1 = 'SELECT * from vw_wellness_enrollee_portal'
query2 = 'select MemberNo, MemberName, Client, email, state, selected_provider, Wellness_benefits, selected_date, selected_session, date_submitted\
            FROM [dbo].[enrollee_test_data_from_portal]'
query3 = 'select * from wellness_providers'
@st.cache_data(ttl = dt.timedelta(hours=24))
def get_data_from_sql():
    wellness_df = pd.read_sql(query1, conn)
    wellness_providers = pd.read_sql(query3, conn)
    conn.close()
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
        'selected_provider': 'LIVING WORD HOSPITAL ABA - 5/7 Umuocham road off Aba- Owerri road Aba.',
        'job_type': 'Office Work',
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

enrollee_id = st.text_input('Kindly input your member number to confirm your eligibility')
#add a submit button
st.button("Submit", key="button1", help="Click or press Enter")
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

        filled_message = f'Dear {member_name}.\n \n Please note that you have already booked your wellness appointment on {submitted_date}\
              and your booking confirmation has been sent to {member_email} as provided.\n\n Find your booking information below:\n\n Wellness\
                  Facility: {provider}.\n\n Wellness Benefits: {package}.\n\n Appointment Date: {app_date} - {app_session}.\n\n Kindly contact your\
                      Client Manager if you wish change your booking appointment.\n\n Thank you for choosing AVON HMO'
        st.info(filled_message,icon="✅")
        

    elif (enrollee_id not in filled_wellness_df['MemberNo'].values) & (enrollee_id in wellness_df['memberno'].values):
        enrollee_name = wellness_df.loc[wellness_df['memberno'] == enrollee_id, 'membername'].values[0]
        client = wellness_df.loc[wellness_df['memberno'] == enrollee_id, 'Client'].values[0]
        policy = wellness_df.loc[wellness_df['memberno'] == enrollee_id, 'PolicyName'].values[0]
        # benefits = wellness_df.loc[wellness_df['memberno'] == enrollee_id, 'WellnessPackage'].values[0]
        age = int(wellness_df.loc[wellness_df['memberno'] == enrollee_id, 'Age'].values[0])
        
        st.info(f"Dear {enrollee_name}.\n \n Kindly confirm that your enrollment details matches with the info displayed below.\
                  \n By proceeding to fill the form below, I understand and hereby acknowledge that my data would be collected\
                 and processed only for the performance of this wellness screening exercise.",icon="✅")
        st.info(f'Company: {client}.\n\n Policy: {policy}.\n\n Please contact your Client Manager if this information does not match with your enrollment details')

        # #add a submit button
        # proceed = st.button("PROCEED", help="Click to proceed")
        # if proceed:
        st.subheader('Kindly fill all the fields below to proceed')

        email = st.text_input('Input a Valid Email Address', st.session_state.user_data['email'])
        mobile_num = st.text_input('Input a Valid Mobile Number', st.session_state.user_data['mobile_num'])
        job_type = st.selectbox('Job Type', options=['Office Work', 'Field Work', 'Both', 'None'], index=['Office Work', 'Field Work', 'Both', 'None'].index(st.session_state.user_data['job_type']))
        # age = st.number_input('Your Current Age', value=st.session_state.user_data['age'])
        state = st.selectbox('Your Current Location', options=wellness_providers['STATE'].unique())
        available_provider = wellness_providers.loc[wellness_providers['STATE'] == state, 'Provider'].unique()
        selected_provider = st.selectbox('Pick your Preferred Wellness Facility', options=available_provider)
        gender = st.radio('Sex', options=['Male', 'Female'], index=['Male', 'Female'].index(st.session_state.user_data['gender']))

        if age >= 30 and gender == 'Female':
            benefits = 'Physical Exam, Urinalysis, PCV, Blood Sugar, BP, Genotype, BMI, Chest X-Ray, Cholesterol, Liver Function Test, Electrolyte,Urea and Creatinine Test, Cervical Smear'
        elif age >= 40 and gender == 'Male':
            benefits = 'Physical Exam, Urinalysis, PCV, Blood Sugar, BP, Genotype, BMI, Chest X-Ray, Cholesterol, Liver Function Test, Electrolyte,Urea and Creatinine Test, Prostrate Specific Antigen'
        else:
            benefits = 'Physical Exam, Urinalysis, PCV, Blood Sugar, BP, Genotype, BMI, Chest X-Rray, Cholesterol, Liver Function Test, Electrolyte,Urea and Creatinine Test'
            
        if state == 'LAGOS':
            current_date = dt.date.today()
            # Define the maximum date as '2023-12-18' as a datetime.date object
            max_date = dt.date(2023, 12, 18)
            # Display a date picker
            selected_date = st.date_input("Select Your Preferred Appointment Date", min_value=current_date,max_value=max_date)
            selected_date_str = selected_date.strftime('%Y-%m-%d')

            booked_sessions_from_db = filled_wellness_df.loc[(filled_wellness_df['selected_date'] == selected_date_str) &
                                                             (filled_wellness_df['selected_provider'] == selected_provider),
                                                               'selected_session'].values.tolist()

            available_sessions = ['08:00 AM', '09:00 AM', '10:00 AM', '11:00 AM', '12:00 PM', '01:00 PM', '02:00 PM', '03:00 PM', '04:00 PM']
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

        else:
            current_date = dt.date.today()
            max_date = dt.date(2023, 12, 18)
            selected_date = st.date_input("Select Your Preferred Appointment Date", min_value=current_date,max_value=max_date)
            selected_date_str = selected_date.strftime('%Y-%m-%d')
            session = ''

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
            'l. I enjoyed my work and life',
            'm. I enjoyed the support from friends and family',
            'n. I feel bad about myself or that I am a failure or have let myself or my family down',
            'o. I have poor appetite or I am over-eating',
            'p. I feel down, depressed, hopeless, tired or have little energy',
            'q. I have trouble falling asleep, staying asleep, or sleeping too much',
            'r. I have no interest or pleasure in doing things',
            's. I have trouble concentrating on things, such as reading the newspaper, or watching TV',
            't. Thought that I would be better off dead or better off hurting myself in some way',
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
        resp_4_l = user_responses4['l. I enjoyed my work and life']
        resp_4_m = user_responses4['m. I enjoyed the support from friends and family']
        resp_4_n = user_responses4['n. I feel bad about myself or that I am a failure or have let myself or my family down']
        resp_4_o = user_responses4['o. I have poor appetite or I am over-eating']
        resp_4_p = user_responses4['p. I feel down, depressed, hopeless, tired or have little energy']
        resp_4_q = user_responses4['q. I have trouble falling asleep, staying asleep, or sleeping too much']
        resp_4_r = user_responses4['r. I have no interest or pleasure in doing things']
        resp_4_s = user_responses4['s. I have trouble concentrating on things, such as reading the newspaper, or watching TV']
        resp_4_t = user_responses4['t. Thought that I would be better off dead or better off hurting myself in some way']
        

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
                INSERT INTO enrollee_test_data_from_portal (MemberNo, MemberName, client, policy, email, mobile_num, job_type, age, state, selected_provider,
                sex, wellness_benefits, selected_date, selected_session,
                [resp_1_a],[resp_1_b],[resp_1_c],[resp_1_d],[resp_1_e],[resp_1_f],[resp_1_g],[resp_1_h],[resp_1_i],[resp_1_j],[resp_1_k],[resp_2_a],
                [resp_2_b],[resp_2_c],[resp_2_d],[resp_2_e],[resp_2_f],[resp_2_g],[resp_2_h],[resp_2_i],[resp_3_a],[resp_3_b],[resp_3_c],[resp_3_d],
                [resp_3_e],[resp_3_f],[resp_4_a],[resp_4_b],[resp_4_c],[resp_4_d],[resp_4_e],[resp_4_f],[resp_4_g],[resp_4_h],[resp_4_i],[resp_4_j],
                [resp_4_k],[resp_4_l],[resp_4_m],[resp_4_n],[resp_4_o],[resp_4_p],[resp_4_q],[resp_4_r],[resp_4_s],[resp_4_t], date_submitted)
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
                st.success("Thank you, your annual wellness has been successfully booked")

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

            finally:
                # Close the cursor and the database connection
                cursor.close()
                conn.close()

                recipient_email = email
                subject = 'AVON ENROLLEE WELLNESS APPOINTMENT CONFIRMATION'
                # Create a table (HTML format) with some sample data
                # date = dt.datetime.now()
                msg_befor_table = f'''
                Dear {enrollee_name},<br><br>
                We hope you are staying safe.<br><br>
                You have been scheduled for a wellness screening at your selected provider, see the below table for details.<br><br>
                '''

                #initialise an empty table
                table_html = """
                <table border="1">
                <tr>
                    <th>Appointment Date</th>
                    <th>Wellness Facility</th>
                    <th>Wellness Benefits</th>
                </tr>
                """

                table_html += f"""
                <tr>
                    <td>{selected_date_str} - {session}</td>
                    <td>{selected_provider}</td>
                    <td>{benefits}</td>
                </tr>
                """

                table_html += "</table>" #close the table

                #customised text for 
                text_after_table = f'''
                <br>Kindly note that this wellness activation is only valid till the 18th of December, 2023.<br><br>
                Also, note that you will be required to:<br><br>

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
                <br>Kindly note that this wellness activation is only valid till the end of the year 2023.<br><br>
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

                message = msg_befor_table + table_html + text_after_table
                message1 = msg_befor_table + table_html + text_after_table1
                myemail = 'noreply@avonhealthcare.com'
                password = os.environ.get('emailpassword')
                cc_email_list = ['ademola.atolagbe@avonhealthcare.com', 'adebola.adesoyin@avonhealthcare.com']
                to_email_list =[recipient_email]
                # myemail = 'ademola.atolagbe@avonhealthcare.com'
                # password = 'ndbxxttqzvrrpywq'

                try:
                    server = smtplib.SMTP('smtp.office365.com', 587)
                    server.starttls()

                    #login to outlook account
                    server.login(myemail, password)

                    #create a MIMETesxt object for the email message
                    msg = MIMEMultipart()
                    msg['From'] = 'AVON HMO Client Services'
                    msg['To'] = recipient_email
                    msg['Cc'] = ', '.join(cc_email_list)
                    msg['Subject'] = subject
                    if state == 'LAGOS':
                        msg.attach(MIMEText(message1, 'html'))
                    else:
                        msg.attach(MIMEText(message, 'html'))

                    all_recipients = to_email_list + cc_email_list
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