
## Structure of the web app

#### 1. Home page
Simple landing page with description of the project and how to use it, who should use it. 

NavBar: 
1. *Register as Traveler or Organization* 
2. *Login* (or *Logout* and *Profile Update* for logged-in users)
3. Links to  *Traveler* and *Organization* info
4. Links to *Trip* and *Availability*
5. Link to Visa/Destination *Info* page
6. Link to *Contact* & *Search* Page

Content:
1. Overview of the webapp
2. How does the webapp work
3. FAQs

#### 2. Register Page
Register Form
0. account type
1. username
2. email
3. password

Or Social Authentication (v2)
1. Google (not tried yet)
2. Facebook ( not working yet)
3. LinkedIn (no API key)
4. Twitter (working)
5. Github (not working yet)

#### 3. Update Profile (@login_required @type_required)

##### Travelers
**Page 1** (with progress bar)

Basic Info:
- first name* (default: username)
- last name*
- gender* (f/m/o)
- birthdate* (datepicker)
- nationality* (country list)
- phone number 
- languages* (multiple choices)
- profile photo

**Page 2** (with progress bar)

Professional Info:
- bio (Tell us more about your)
- area of expertise (multiple choice with tag) 
- experiences

**Page 3** (with progress bar)

Add social links:
- Social links (e.g. facebook, linkedin, etc)
- Personal Website
- Other channels


**Page 4** (with progress bar)

Traveler offer (more than one topic - allowed):

- Subject* (list)
- Type* (Event Type List)
- Frequency*
  - One time 
  - Multiple (x times)
  - Flexi 
- Duration* per section(<=2h, 2-4h, 4-8h, >8h)
- Title*
- Description*
- Requirement* (projector, internet, equipments etc)


##### Local Hosts
**Page 1** (with progress bar)

Basic Info:
- profile photo
- org name*
- org type* (list)
- phone number
- description of the org
- address* (google autocomplete)
(google map and geolocation auto)


**Page 2** (with progress bar)

More about the org:

- area of interests (multiple choices) 
- more about what we want (text area)
- languages (multiple choices)

**Page 3** (with progress bar)

Add social links:
- Social links (e.g. facebook, linkedin, etc)
- Personal Website
- Other channels
  
**Page 4** (with progress bar)

Add local host's offer: 
- title
- details(text area)
    - physical space
    - equipments
    - others 
- photo

#### 4. Update Trips/Availability (@login_required @type_required)

##### Travelers Calendar Update
- Previous/Next month
- New Trip
    - start date
    - end date
    - destination (country list)
    - details
- Links to Trip Details
    - Update Trip
        - start date
        - end date
        - destination (country list)
        - details
    - Delete Trip

##### Local Host Availability Calendar

- Previous/Next month
- New Trip
    - start date
    - end date
    - title
    - details
- Links to Trip Details
    - Update Trip
        - start date
        - end date
        - title
        - details
    - Delete Trip

#### 5. List of Travelers 
- Total number of travelers
- List of results per traveler

#### 6. List of Local Hosts
- Total number of localhost
- List of results per host

#### 7. Profile page - per Traveler 
- detailed traveler profile
- travel offers
- coming trips

#### 8. Profile page - per Local host 
- detailed organization profile
- local host offers

#### 9. List of Trips
- sorting based on start-date, end-date,
destination, traveler
- Number of trips
- List of results per trip

#### 10. List of Availables
- sorting based on start-date, end-date,
localhost, summary
- Number of available space
- List of results per availables

#### 11. Contact
title, content, email

#### 12. Info

- Choose Destination and Nationality
- Display Visa Requirements & Destination Info

#### 13. Search

- checkbox of Traveler and Host (default: both checked)
- search fields
  - traveler: Language, bio, expertise, trip destination
  - host: Language, description, interests, address

---
## Folder structure of the project
github repository: finalproject

            -| env (virtual environment)
            -| proj_travelshare
                -| app_search
                    -| templatetags
                        -| class_name
                            -| class_name
                            -| param_replace(for pagination)
                    -| views
                        -| search_view
                            -| def get_context_data
                            -| def get_queryset
                -| app_user
                    -| forms.py
                        -| FormRegister
                            -| Type
                            -| Username
                            -| Email
                            -| Password
                        -| FormLogin
                            -| Username
                            -| Password
                        -| FormLogout
                        -| FormUserUpdate
                        -| FormProfileTravelerUpdate
                        -| FormProfileTravelerUpdate2
                        -| FormProgram
                        -| DeleteProgramForm                     
                        -| FormProfileHostUpdate
                        -| FormProfileHostUpdate2
                        -| FormSpace
                        -| DeleteSpaceForm
                        -| LinkForm
                        -| DeleteLinkForm

                    -| models.py
                        -| User (AbstractUser)
                            -| type
                        -| ProfileTraveler (extension of User)
                            -| user (one to one)
                            -| gender (Choice)
                            -| nationality (Choice)
                            -| birthdate
                            -| phone (PhoneNumberField)
                            -| photo (image)
                            -| bio (Text)
                            -| experience (Text)
                            -| expertise (ManyToMany: Expertise) 
                            -| language (ManyToMany: Language)
                        -| ProfileHost (extension of User)
                            -| User (one to one)
                            -| Name (Char)
                            -| Type (choice)
                            -| Description (Text)
                            -| phone (PhoneNumberField)
                            -| photo (image)
                            -| address (Google API)
                            -| geolocation (Google API)
                            -| language (ManyToMany: Language)
                            -| interests (ManyToMany: Expertise)
                            -| interest_details (Text)
                          
                        -| Program 
                            -| owner (foreign key)
                            -| subject (choice)
                            -| type (choice)
                            -| title (Char)
                            -| frequency ()
                            -| duration (Choice)
                            -| description (Text)   
                            -| requirements (Text)
                            
                        -| Space 
                            -| owner (foreign key)
                            -| title (char)
                            -| details (text) 
                            -| photo (image)
                            
                        -| Language
                            -| language      
                        -| Topics - tag
                            -| topic                   
                        -| Links
                            -| user (foreign key)
                            -| Name 
                            -| Url                                                                           
                    -| urls.py
                        -| password_reset_complete
                        -| password_reset_confirm
                        -| password_reset
                        -| password_reset_done
                    -| views.py
                        -| viewregister
                        -| viewindex
                        -| UserLogin
                        -| UserLogout
                        -| profile_update_traveler
                        -| profile_update_traveler2
                        -| profile_update_traveler3
                        -| program_add
                        -| program_update
                        -| program_delete
                        -| program_detail
                        -| program_list
                        -| profile_update_host
                        -| profile_update_host2
                        -| profile_update_host3 
                        -| space_add
                        -| space_update
                        -| space_delete
                        -| space_detail
                        -| space_list
                        -| link_add
                        -| link_delete
                        -| link_update
                        -| link_detail  
                        -| link_list                  
                        -| profile_traveler
                        -| profile_host
                -| app_main
                    -| forms.py
                        -| TripForm(ModelForm)
                        -| TripDeleteForm (Form)
                        -| AvailableForm (ModelForm)
                        -| AvailableDeleteForm (Form)
                        -| EntryRequirementForm (Form)
                        
                    -| models.py
                        -| Trip 
                            -| user (foreign key)
                            -| destination (Char)
                            -| Details (Text)
                            -| Start_Time (DateTime)
                            -| End_Time (DateTime)
                        -| Available 
                            -| user (foreign key)
                            -| summary (Text)
                            -| Extra_info (Text)
                            -| Start_Time (DateTime)
                            -| End_Time (DateTime)
                    -| urls.py
                        -| home
                        -| info
                        -| travelers
                        -| hosts
                        -| trip_list
                        -| available_list
                        -| calendar_trip
                        -| calendar_available
                        -| calendar_trip_traveler
                        -| calendar_available_host
                        -| calendar_trip_private
                        -| calendar_available_private
                        -| trip_edit
                        -| trip_detail                       
                        -| trip_new
                        -| available_edit   
                        -| available_detail
                        -| available_new                                                                                              
                    -| views.py
                        -| home
                        -| travelers
                        -| hosts
                        -| CalendarView (ListView)
                        -| CalendarViewTripPrivate (ListView)
                        -| CalendarViewAvailablePrivate (ListView)
                        -| CalendarViewTripTraveler (ListView)
                        -| CalendarViewAvailableHost (ListView)
                        -| CalendarViewTrip (ListView)
                        -| CalendarViewAvailable (ListView)
                        -| trip
                        -| trip_list 
                        -| available_new
                        -| available
                        -| available_list
                        -| trip_view
                        -| available_view
                        -| get_info
                    
                -| app_info
                    - forms.py
                    - views.py

                -| proj_travelshare
                    -| settings.py
                    -| urls.py
                        -| register
                        -| login
                        -| logout
                        -| profile_update_person
                        -| profile_view_person
                        -| profile_update_org
                        -| profile_view_org

                -| media
                    -|profile_traveler
                    -|profile_host
                -| static
                    -| css
                    -| js
                    -| pic
                -| templates
                    -| app_user
                    -| app_main
                    -| app_info
            -| .gitignore
            -| .env (for decouple)
            -| README.md

