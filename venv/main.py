import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty, ObjectProperty
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivymd.app import MDApp
from kivy.uix.image import Image
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.list import OneLineIconListItem
from kivy.metrics import dp
from kivymd.uix.picker import MDDatePicker
from kivy.uix.button import Button
import requests
import json
from firebase import firebase
from datetime import date
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

screen_helper = """
ScreenManager:
    LoginScreen:
        id: login
    MenuScreen:
        id: menu
    SignUpScreen:
        id: signup
    QuoteForm:
        id: quote_form
    QuoteScreen:
        id: quote_screen
    ClaimForm:
        id: claim_form
    PolicyScreen:
        id: policies
    ProfileScreen:
        id: profile
    SettingScreen:
        id: settings
    DisplayPolicy:
        id: display_policy
    ClaimScreen:
        id: claim_screen
    DisplayQuote:
        id: display_quote
    OwnershipDetailsScreen:
        id: ownership_details_screen
        

 
<LoginScreen>:
    name: 'login'
    MDCard:
        size_hint: None, None
        size: 300,500
        pos_hint:{"center_x":0.5, "center_y":0.5}
        elevation: 10
        padding: 25
        spacing: 25
        orientation: 'vertical'
        
        Image:
            source: "images/car-insurance.png"
            
        MDLabel:
            id: login_label
            text: "Vehicle Insurance App"
            font_size: 25
            halign: "center"
            size_hint_y: None
            height: self.texture_size[1]
            padding_y: 15

        MDTextFieldRound:
            id: user_field
            hint_text: "username"
            icon_right: "account"
            size_hint_x: None
            width: 200
            font_size: 20
            pos_hint:{"center_x":0.5}

        MDTextFieldRound:
            id: password_field
            hint_text: "password"
            icon_right: "eye-off"
            size_hint_x: None
            width: 200
            font_size: 20
            pos_hint:{"center_x":0.5}
            password: True

        MDRoundFlatButton:
            text: "LOG IN"
            font_size: 15
            pos_hint:{"center_x":0.5}
            on_press: root.logger(); root.update_profile(); root.update_policies()

        MDRoundFlatButton:
            text: "SIGN UP"
            font_size: 15
            pos_hint:{"center_x":0.5}
            on_press: app.root.current = 'signup'
            
        Widget:
            size_hint_y: None
            height: 10
        
<MenuScreen>:
    name: 'menu'
    
    MDCard:
        size_hint: None, None
        size: 300,500
        pos_hint:{"center_x":0.5, "center_y":0.5}
        elevation: 10
        padding: 25
        spacing: 25
        orientation: 'vertical'                   
                
        MDFloatLayout:
            MDGridLayout:
                size_hint: .9,.9
                pos_hint: {'center_x':0.5,'center_y':0.5}
                cols: 2
                rows: 3
                
                Button:
                    id: btn_quote
                    on_press: app.root.current = 'quote_form'
                    Label:
                        text_size: self.size
                        text: "Get Quote"
                        y: self.parent.y+ 15
                        x: self.parent.x+ 15
                    Image:
                        source: "images/quotation.png"
                        y: self.parent.y+ 35
                        x: self.parent.x
                
                Button:
                    id: btn_claim
                    on_press: app.root.current = 'claim_form'
                    Label:
                        text_size: self.size
                        text: "Register Claim"
                        y: self.parent.y+ 15
                        x: self.parent.x+ 15
                    Image:
                        source: "images/claim.png"
                        y: self.parent.y+ 35
                        x: self.parent.x
                
                Button:
                    id: btn_policies
                    on_press: app.root.current = 'policies'
                    Label:
                        text_size: self.size
                        text: "My Policies"
                        y: self.parent.y+ 15
                        x: self.parent.x+ 15
                    Image:
                        source: "images/insurance.png"
                        y: self.parent.y+ 35
                        x: self.parent.x
                
                Button:
                    id: btn_profile
                    on_press: app.root.current = 'profile'
                    Label:
                        text_size: self.size
                        text: "My Profile"
                        y: self.parent.y+ 15
                        x: self.parent.x+ 15
                    Image:
                        source: "images/profile.png"
                        y: self.parent.y+ 35
                        x: self.parent.x
                
                Button:
                    id: btn_settings
                    on_press: app.root.current = 'settings'
                    Label:
                        text_size: self.size
                        text: "Settings"
                        y: self.parent.y+ 15
                        x: self.parent.x+ 15
                    Image:
                        source: "images/settings.png"
                        y: self.parent.y + 35
                        x: self.parent.x
                
                Button:
                    id: btn_logout
                    on_press: app.root.current = 'login'
                    Label:
                        text_size: self.size
                        text: "Logout"
                        y: self.parent.y+ 15
                        x: self.parent.x+ 15
                    Image:
                        source: "images/logout.png"
                        y: self.parent.y+ 35
                        x: self.parent.x
            
<SignUpScreen>:
    name: 'signup'            
    MDCard:
        size_hint: None, None
        size: 300,500
        pos_hint:{"center_x":0.5, "center_y":0.5}
        elevation: 10
        padding: 25
        spacing: 25
        orientation: 'vertical'   
        
        MDLabel:
            id: signup_label
            text: "Sign Up"
            font_size: 30
            halign: "center"
            size_hint_y: None
            height: self.texture_size[1]
            padding_y: 15
        
        ScrollView:
            size_hint_y: .73
            do_scroll_x:False
            do_scroll_y:True
            
            GridLayout:
                size: (self.parent.width,self.parent.height)
                size_hint_x:None
                size_hint_y:None
                cols:1
                height:self.minimum_height
                
                Widget:
                    size_hint_y: None
                    height: 10
            
                Label:
                    text: 'Personal Info'
                    text_size: self.parent.width, None
                    size: self.texture_size
                    halign: 'right'
                    valign: 'middle'
    
                MDTextField:
                    id: name 
                    hint_text: "Name"
                    mode: "rectangle"
                    
                MDTextField:
                    id: surname 
                    hint_text: "Surname"
                    mode: "rectangle"
                    
                MDTextField:
                    id: dob
                    hint_text: "Date of Birth"
                    mode: "rectangle"
                    on_focus: if self.focus: root.date_picker()
                
                MDTextField:
                    id: gender
                    mode: "rectangle"
                    hint_text: "Gender"
                    on_focus: if self.focus: root.gender_picker()
                
                MDTextField:
                    id: address
                    hint_text: "Address"
                    mode: "rectangle"
                    
                MDTextField:
                    id: postal_code
                    hint_text: "Postal Code"
                    mode: "rectangle"
                    input_filter: 'int'
                    
                MDTextField:
                    id: phone_num
                    hint_text: "Phone Number"
                    mode: "rectangle"
                    input_filter: 'int'
                    
                MDTextField:
                    id: email 
                    hint_text: "Email"
                    mode: "rectangle"
                     
                    
                MDTextField:
                    id: edu
                    hint_text: "Education"
                    mode: "rectangle"
                    on_focus: if self.focus: root.edu_picker()
                    
                MDTextField:
                    id: income
                    hint_text: "Income per year (in USD)"
                    mode: "rectangle"
                    input_filter: 'float'
                    
                MDTextField:
                    id: credit_score
                    hint_text: "Credit Score (Between 0 and 1)"
                    mode: "rectangle"
                    input_filter: 'float'
                
                Widget:
                    size_hint_y: None
                    height: 50
                    
                Label:
                    text: 'Driving History'
                    text_size: self.parent.width, None
                    size: self.texture_size
                    halign: 'right'
                    valign: 'middle'
                    
                MDTextField:
                    id: driv_exp
                    hint_text: "Driving Experience (Number of Years)"
                    mode: "rectangle"
                    input_filter: 'int'
                    
                MDTextField:
                    id: veh_own
                    hint_text: "Number of Vehicles Owned"
                    mode: "rectangle"
                    input_filter: 'int'
                    
                MDTextField:
                    id: speeding
                    hint_text: "Number of Speeding Violations"
                    mode: "rectangle"
                    input_filter: 'int'
                    
                MDTextField:
                    id: duis
                    hint_text: "Number of DUIS"
                    mode: "rectangle"
                    input_filter: 'int'
                    
                MDTextField:
                    id: past_acc
                    hint_text: "Number of Past Accidents"
                    mode: "rectangle"
                    input_filter: 'int'
                
                Widget:
                    size_hint_y: None
                    height: 50
                    
                Label:
                    text: 'Account Info'
                    text_size: self.parent.width, None
                    size: self.texture_size
                    halign: 'right'
                    valign: 'middle'
                
                MDTextField:
                    id: user
                    hint_text: "username"
                    mode: "rectangle"
                    
                MDTextField:
                    id: passw
                    password: True
                    hint_text: "password"
                    mode: "rectangle"
                    
                Widget:
                    size_hint_y: None
                    height: 10
                    
                MDRoundFlatButton:
                    text: "SIGN UP"
                    font_size: 15
                    pos_hint:{"center_x":0.5}
                    on_press: root.create_post()
                
                Widget:
                    size_hint_y: None
                    height: 10
                    
                MDRoundFlatButton:
                    text: "CANCEL"
                    font_size: 15
                    pos_hint:{"center_x":0.5}
                    on_press: app.root.current = 'login'
            
<OwnershipDetailsScreen>:
    name: 'ownership_details_screen'            
    MDCard:
        size_hint: None, None
        size: 300,500
        pos_hint:{"center_x":0.5, "center_y":0.5}
        elevation: 10
        padding: 25
        spacing: 25
        orientation: 'vertical'   
        
        MDLabel:
            id: ownership_details_label
            text: "Please enter details below:"
            font_size: 20
            halign: "center"
            size_hint_y: None
            height: self.texture_size[1]
            padding_y: 15
        
        ScrollView:
            size_hint_y: .73
            do_scroll_x:False
            do_scroll_y:True
            
            GridLayout:
                size: (self.parent.width,self.parent.height)
                size_hint_x:None
                size_hint_y:None
                cols:1
                height:self.minimum_height
                
                Widget:
                    size_hint_y: None
                    height: 10
            
                Label:
                    text: 'Ownership Details'
                    text_size: self.parent.width, None
                    size: self.texture_size
                    halign: 'right'
                    valign: 'middle'
    
                MDTextField:
                    id: ownership
                    mode: "rectangle"
                    hint_text: "Gender"
                    on_focus: if self.focus: root.ownership_picker()
                    
                MDTextField:
                    id: licence_plate
                    hint_text: "Licence Plate Number"
                    mode: "rectangle"
                    input_filter: 'int'
                    
                Widget:
                    size_hint_y: None
                    height: 10
                    
                Label:
                    text: 'Payment Method'
                    text_size: self.parent.width, None
                    size: self.texture_size
                    halign: 'right'
                    valign: 'middle'
                    
                Label:
                    text: "Internet Banking"
                    font_size: 20
                    valign: 'middle'
                    halign: 'left'
                    size: self.size
                CheckBox:
                    id: chk_internet_banking
                    group: "payment_method"
                    halign: 'left'
                    
                Label:
                    text: "Card"
                    font_size: 20
                    valign: 'middle'
                    halign: 'left'
                    size: self.size
                CheckBox:
                    id: chk_card
                    group: "payment_method"
                    halign: 'left'
                
                    
                Widget:
                    size_hint_y: None
                    height: 10
                    
                MDRoundFlatButton:
                    text: "CONTINUE"
                    font_size: 15
                    pos_hint:{"center_x":0.5}
                    
                
                Widget:
                    size_hint_y: None
                    height: 10
                    
                MDRoundFlatButton:
                    text: "BACK"
                    font_size: 15
                    pos_hint:{"center_x":0.5}
                    on_press: app.root.current = 'display_quote'
            
<QuoteForm>:
    name: 'quote_form'            
    MDCard:
        size_hint: None, None
        size: 300,500
        pos_hint:{"center_x":0.5, "center_y":0.5}
        elevation: 10
        padding: 25
        spacing: 25
        orientation: 'vertical'    
        
        MDLabel:
            id: get_quote_label
            text: "Get Quotes"
            font_size: 30
            halign: "center"
            size_hint_y: None
            height: self.texture_size[1]
            padding_y: 15
    
        ScrollView:
            size_hint_y: .73
            do_scroll_x:False
            do_scroll_y:True
            
            GridLayout:
                size: (self.parent.width,self.parent.height)
                size_hint_x:None
                size_hint_y:None
                cols:1
                height:self.minimum_height
                
                Widget:
                    size_hint_y: None
                    height: 10
                
                MDTextField:
                    id: veh_make
                    hint_text: "Vehicle Make Year"
                    mode: "rectangle"
                    input_filter: 'int'
                    
                MDTextField:
                    id: veh_mileage 
                    hint_text: "Vehicle Annual Mileage"
                    mode: "rectangle"
                    input_filter: 'int'
                                         
                MDTextField:
                    id: veh_type
                    hint_text: "Vehicle Type"
                    mode: "rectangle"
                    on_focus: if self.focus: root.veh_type_picker()
                    
                MDTextField:
                    id: model
                    hint_text: "Model"
                    mode: "rectangle"
                    
                MDTextField:
                    id: fuel_type
                    hint_text: "Fuel Type"
                    mode: "rectangle"
                    on_focus: if self.focus: root.fuel_type_picker()
                    
                MDTextField:
                    id: vin
                    hint_text: "Vehicle Identification Number"
                    mode: "rectangle"
                    input_filter: 'int'
                    
                MDTextField:
                    id: reg_date
                    hint_text: "Registration Date"
                    mode: "rectangle"
                    on_focus: if self.focus: root.reg_date_picker()
                
                Widget:
                    size_hint_y: None
                    height: 20
                    
                GridLayout:
                    cols:2
                    row_default_height: '15dp'
                    row_force_default: True
                    spacing: 10, 10
                    padding: 5, 5
                    size_hint_y: None
                    height: self.minimum_height
                    
                    
                    Label:
                        text: "Used"
                        font_size: 20
                        valign: 'middle'
                        halign: 'left'
                        size: self.size
                    CheckBox:
                        id: chk_used
                        group: "vehicle_state"
                        halign: 'left'
                        
                    Label:
                        text: "New"
                        font_size: 20
                        valign: 'middle'
                        halign: 'left'
                        size: self.size
                    CheckBox:
                        id: chk_new
                        group: "vehicle_state"
                        halign: 'left'
                    
                Widget:
                    size_hint_y: None
                    height: 20
                    
                MDRoundFlatButton:
                    text: "FIND"
                    font_size: 15
                    pos_hint:{"center_x":0.5}
                    on_press: root.add_quote_request()
                    
                Widget:
                    size_hint_y: None
                    height: 10
                    
                MDRoundFlatButton:
                    text: "BACK"
                    font_size: 15
                    pos_hint:{"center_x":0.5}
                    on_press: app.root.current = 'menu'
                    
<QuoteScreen>:
    name: 'quote_screen'            
    MDCard:
        size_hint: None, None
        size: 300,500
        pos_hint:{"center_x":0.5, "center_y":0.5}
        elevation: 10
        padding: 25
        spacing: 25
        orientation: 'vertical'    
        
        MDLabel:
            id: quote_screen_label
            text: "Policy Recommendations"
            font_size: 25
            halign: "center"
            size_hint_y: None
            height: self.texture_size[1]
            padding_y: 15
    
        ScrollView:
            size_hint_y: .73
            do_scroll_x:False
            do_scroll_y:True
            
            GridLayout:
                id: quotes_grid
                size: (self.parent.width,self.parent.height)
                size_hint_x:None
                size_hint_y:None
                padding: 10,10
                spacing: 10,10
                cols:3
                height:self.minimum_height  
                                            
        MDRoundFlatButton:
            text: "BACK"
            font_size: 15
            pos_hint:{"center_x":0.5, "center_y":0.1}
            on_press: app.root.current = 'quote_form'
                    
<ClaimForm>:
    name: 'claim_form'            
    MDCard:
        size_hint: None, None
        size: 300,500
        pos_hint:{"center_x":0.5, "center_y":0.5}
        elevation: 10
        padding: 25
        spacing: 25
        orientation: 'vertical'   
        
        MDLabel:
            id: claim_form_label
            text: "Register a Claim"
            font_size: 30
            halign: "center"
            size_hint_y: None
            height: self.texture_size[1]
            padding_y: 15 
                
        ScrollView:
            size_hint_y: .73
            do_scroll_x:False
            do_scroll_y:True
            
            GridLayout:
                size: (self.parent.width,self.parent.height)
                size_hint_x:None
                size_hint_y:None
                cols:1
                height:self.minimum_height
                
                Widget:
                    size_hint_y: None
                    height: 10
            
                Label:
                    text: 'Incident Info'
                    text_size: self.parent.width, None
                    size: self.texture_size
                    halign: 'right'
                    valign: 'middle'
            
                MDTextField:
                    hint_text: "Policy Number"
                    mode: "rectangle"
                    input_filter: 'int'
                    id: policy_number
                     
                MDTextField:
                    hint_text: "Claim Amount"
                    mode: "rectangle"
                    input_filter: 'int'
                    id: claim_amount
                    
                MDTextField:
                    hint_text: "Incident Type"
                    mode: "rectangle"
                    id: incident_type
                    on_focus: if self.focus: root.incident_type_picker()
                    
                MDTextField:
                    hint_text: "Collision Type"
                    mode: "rectangle"
                    id: collision_type
                    on_focus: if self.focus: root.collision_type_picker()
                    
                MDTextField:
                    hint_text: "Incident Severity"
                    mode: "rectangle"
                    id: severity
                    on_focus: if self.focus: root.severity_picker()
                    
                MDTextField:
                    hint_text: "Authorities Contacted"
                    mode: "rectangle"
                    id: auth_contact
                    on_focus: if self.focus: root.auth_contact_picker()
                    
                MDTextField:
                    hint_text: "Police Report Available"
                    mode: "rectangle"
                    id: police_report
                    on_focus: if self.focus: root.police_report_picker()
                    
                MDTextField:
                    hint_text: "Location Address"
                    mode: "rectangle"
                    
                MDTextField:
                    hint_text: "Location Zipcode"
                    mode: "rectangle"
                    input_filter: 'int'
                
                MDTextField:
                    hint_text: "Incident Date"
                    mode: "rectangle"
                    id: incident_date
                    on_focus: if self.focus: root.incident_date_picker()
                
                MDTextField:
                    hint_text: "Number of Vehicles Involved"
                    mode: "rectangle"
                    input_filter: 'int'
                    id: num_vehicles
                
                Widget:
                    size_hint_y: None
                    height: 20
            
                Label:
                    text: 'Bank Details'
                    text_size: self.parent.width, None
                    size: self.texture_size
                    halign: 'right'
                    valign: 'middle'
                    
                MDTextField:
                    hint_text: "Account Holder Name"
                    mode: "rectangle"
                    id: account_holder_name
            
                MDTextField:
                    hint_text: "Account Number"
                    mode: "rectangle"
                    input_filter: 'int'
                    id: bank_account_number
                     
                MDTextField:
                    hint_text: "Routing Code"
                    mode: "rectangle"
                    input_filter: 'int'
                    id: routing_code
                    
                MDTextField:
                    hint_text: "Bank Name"
                    mode: "rectangle"
                    id: bank_name
                    
                MDTextField:
                    hint_text: "Branch Name"
                    mode: "rectangle"
                    id: bank_branch
                    
                MDTextField:
                    hint_text: "Taxpayer Identification Number"
                    mode: "rectangle"
                    input_filter: 'int'
                    id: taxpayer_number
                    
                Widget:
                    size_hint_y: None
                    height: 20                     
                    
                Label:
                    text: 'Upload registration Document'
                    text_size: self.parent.width, None
                    size: self.texture_size
                    halign: 'left'
                    
                Widget:
                    size_hint_y: None
                    height: 30
                    
                GridLayout:
                    cols:2
                    row_default_height: '15dp'
                    row_force_default: True
                    spacing: 10, 10
                    padding: 5, 5
                    size_hint_y: None
                    height: self.minimum_height
                    
                    MDRectangleFlatButton:
                        text: "Upload"
                        font_size: 10
                        pos_hint:{"center_x":0.5}
                        size: 15, 10
                        size_hint: None, None
                        
                    Label:
                        text: "No Document uploaded"
                        font_size: 10
                        valign: 'middle'
                        halign: 'left'
                        size: self.size
                    
                Widget:
                    size_hint_y: None
                    height: 10
                
                Label:
                    text: 'Add Photograph'
                    text_size: self.parent.width, None
                    size: self.texture_size
                    halign: 'left'
                    
                Widget:
                    size_hint_y: None
                    height: 30
                    
                GridLayout:
                    cols:2
                    row_default_height: '15dp'
                    row_force_default: True
                    spacing: 20, 20
                    padding: 5, 5
                    size_hint_y: None
                    height: self.minimum_height
                    
                    MDRectangleFlatButton:
                        text: "Front"
                        font_size: 10
                        pos_hint:{"center_x":0.5}
                        size: 15, 10
                        size_hint: None, None
                        
                    Label:
                        text: "No Photo"
                        font_size: 10
                        valign: 'middle'
                        halign: 'left'
                        size: self.size
                        
                    MDRectangleFlatButton:
                        text: "Back"
                        font_size: 10
                        pos_hint:{"center_x":0.5}
                        size: 15, 10
                        size_hint: None, None
                        
                    Label:
                        text: "No Photo"
                        font_size: 10
                        valign: 'middle'
                        halign: 'left'
                        size: self.size
                        
                    MDRectangleFlatButton:
                        text: "Left Side"
                        font_size: 10
                        pos_hint:{"center_x":0.5}
                        size: 15, 10
                        size_hint: None, None
                        
                    Label:
                        text: "No Photo"
                        font_size: 10
                        valign: 'middle'
                        halign: 'left'
                        size: self.size
                        
                    MDRectangleFlatButton:
                        text: "Right Side"
                        font_size: 10
                        pos_hint:{"center_x":0.5}
                        size: 15, 10
                        size_hint: None, None
                        
                    Label:
                        text: "No Photo"
                        font_size: 10
                        valign: 'middle'
                        halign: 'left'
                        size: self.size
                        
                Widget:
                    size_hint_y: None
                    height: 5             
                    
                Label:
                    text: "I confirm that all information is correct"
                    font_size: 12
                    valign: 'middle'
                    halign: 'left'
                    
                Widget:
                    size_hint_y: None
                    height: 20    
                     
                CheckBox:
                    halign: 'left'
                    
                Widget:
                    size_hint_y: None
                    height: 20 
                    
                Label:
                    text: "I will provide originals of all uploaded \\n documents within 30 days of filing this claim"
                    font_size: 10
                    valign: 'middle'
                    halign: 'left'
                    multiline : True
                    
                Widget:
                    size_hint_y: None
                    height: 20    
                     
                CheckBox:
                    halign: 'left'
                    
                Widget:
                    size_hint_y: None
                    height: 20 
                    
                MDRoundFlatButton:
                    text: "SUBMIT"
                    font_size: 15
                    pos_hint:{"center_x":0.5}
                    on_press: root.add_claim()
                
                Widget:
                    size_hint_y: None
                    height: 10
                    
                MDRoundFlatButton:
                    text: "BACK"
                    font_size: 15
                    pos_hint:{"center_x":0.5}
                    on_press: app.root.current = 'menu'

<PolicyScreen>:
    name: 'policies'            
    MDCard:
        size_hint: None, None
        size: 300,500
        pos_hint:{"center_x":0.5, "center_y":0.5}
        elevation: 10
        padding: 25
        spacing: 25
        orientation: 'vertical'   
        
        MDLabel:
            id: policies_label
            text: "Your Policies"
            font_size: 30
            halign: "center"
            size_hint_y: None
            height: self.texture_size[1]
            padding_y: 15 
                
        ScrollView:
            size_hint_y: .73
            do_scroll_x:False
            do_scroll_y:True
            
            GridLayout:
                id : fourwheel_grid
                size: (self.parent.width,self.parent.height)
                size_hint_x:None
                size_hint_y:None
                padding: 10,10
                spacing: 10,10
                cols:3
                height:self.minimum_height
                 

        MDRoundFlatButton:
            text: "BACK"
            font_size: 15
            pos_hint:{"center_x":0.5, "center_y":0.1}
            on_press: app.root.current = 'menu'
                         
<ProfileScreen>:
    name: 'profile'            
    MDCard:
        size_hint: None, None
        size: 300,500
        pos_hint:{"center_x":0.5, "center_y":0.5}
        elevation: 10
        padding: 25
        spacing: 25
        orientation: 'vertical'   
        
        MDLabel:
            id: policies_label
            text: "Profile"
            font_size: 30
            halign: "center"
            size_hint_y: None
            height: self.texture_size[1]
            padding_y: 15 
                
        ScrollView:
            size_hint_y: .73
            do_scroll_x:False
            do_scroll_y:True    
            
            GridLayout:
                size: (self.parent.width,self.parent.height)
                size_hint_x:None
                size_hint_y:None
                padding: 10,10
                spacing: 10,10
                cols:1
                height:400
                
                Image:
                    source: "images/user.png" 
                    halign: 'left'
                    
                MDRectangleFlatButton:
                    text: "Change Picture"
                    font_size: 10
                    pos_hint:{"center_x":0.5, "center_y":0.5}
                    
                GridLayout:
                    padding: 10,10
                    spacing: 10,10
                    cols:2
                    height:self.minimum_height
                    
                    MDLabel:
                        text: "Name"
                        font_size: 12
                    MDLabel:
                        id: profile_name 
                        text: ''
                        font_size: 10
                    MDLabel:
                        text: "username"
                        font_size: 12
                    MDLabel:
                        id: profile_user
                        text: ''
                        font_size: 10
                    MDLabel:
                        text: "Email"
                        font_size: 12
                    MDLabel:
                        id: profile_email
                        text: ''
                        font_size: 10
                        halign:'left'
                    MDLabel:
                        text: "Phone Number"
                        font_size: 12
                    MDLabel:
                        id:profile_phone
                        text: ''
                        font_size: 10
                
                MDRectangleFlatButton:
                    text: "Change Password"
                    font_size: 10
                    pos_hint:{"center_x":0.5, "center_y":0.5}
                
                MDRoundFlatButton:
                    text: "Edit Profile"
                    font_size: 15
                    pos_hint:{"center_x":0.5, "center_y":0.1}
                    
                MDRoundFlatButton:
                    text: "BACK"
                    font_size: 15
                    pos_hint:{"center_x":0.5, "center_y":0.1}
                    on_press: app.root.current = 'menu'
                    
                    
<SettingScreen>:
    name: 'settings'            
    MDCard:
        size_hint: None, None
        size: 300,500
        pos_hint:{"center_x":0.5, "center_y":0.5}
        elevation: 10
        padding: 25
        spacing: 25
        orientation: 'vertical'   
        
        MDLabel:
            id: settings_label
            text: "Settings"
            font_size: 30
            halign: "center"
            size_hint_y: None
            height: self.texture_size[1]
            padding_y: 15 
                
        ScrollView:
            size_hint_y: .73
            do_scroll_x:False
            do_scroll_y:True  
                            
            GridLayout:
                cols:2
                height:self.minimum_height
            
                Label:
                    text: "Preference 1"
                    valign: 'middle'
                    halign: 'left'
                CheckBox:
                    halign: 'left'
                    
                Label:
                    text: "Preference 2"
                    valign: 'middle'
                    halign: 'left'
                CheckBox:
                    halign: 'left'
                    
                Label:
                    text: "Preference 3"
                    valign: 'middle'
                    halign: 'left'
                CheckBox:
                    halign: 'left'
                    
                Label:
                    text: "Preference 4"
                    valign: 'middle'
                    halign: 'left'
                CheckBox:
                    halign: 'left'
                    
                Label:
                    text: "Preference 5"
                    valign: 'middle'
                    halign: 'left'
                CheckBox:
                    halign: 'left'
            
                        
        MDRoundFlatButton:
            text: "BACK"
            font_size: 15
            pos_hint:{"center_x":0.5, "center_y":0.1}
            on_press: app.root.current = 'menu'

<DisplayPolicy>:
    name: 'display_policy'            
    MDCard:
        size_hint: None, None
        size: 300,500
        pos_hint:{"center_x":0.5, "center_y":0.5}
        elevation: 10
        padding: 25
        spacing: 25
        orientation: 'vertical'  
        
        MDLabel:
            id: display_policies_label
            text: "Policy Details"
            font_size: 30
            halign: "center"
            size_hint_y: None
            height: self.texture_size[1]
            padding_y: 15 
                
        ScrollView:
            size_hint_y: .73
            do_scroll_x:False
            do_scroll_y:True  
                            
            GridLayout:
                id: policies_grid
                cols:2
                height:self.minimum_height   
                
        MDRoundFlatButton:
            text: "BACK"
            font_size: 15
            pos_hint:{"center_x":0.5, "center_y":0.1}
            on_press: app.root.current = 'policies' 
            
<DisplayQuote>:
    name: 'display_quote'            
    MDCard:
        size_hint: None, None
        size: 300,500
        pos_hint:{"center_x":0.5, "center_y":0.5}
        elevation: 10
        padding: 25
        spacing: 25
        orientation: 'vertical'  
        
        MDLabel:
            id: display_quote_label
            text: "Quote Details"
            font_size: 30
            halign: "center"
            size_hint_y: None
            height: self.texture_size[1]
            padding_y: 15 
                
        ScrollView:
            size_hint_y: .73
            do_scroll_x:False
            do_scroll_y:True  
                            
            GridLayout:
                id: quote_grid
                cols:2
                height:self.minimum_height   
                
        MDRoundFlatButton:
            text: "BACK"
            font_size: 15
            pos_hint:{"center_x":0.5, "center_y":0.1}
            on_press: app.root.current = 'quote_screen'  
            
<ClaimScreen>:
    name: 'claim_screen'
    MDCard:
        size_hint: None, None
        size: 300,500
        pos_hint:{"center_x":0.5, "center_y":0.5}
        elevation: 10
        padding: 25
        spacing: 25
        orientation: 'vertical'
        
        Image:
            source: "images/checked.png"
            
        MDLabel:
            text: "Claim Filed Successfully"
            font_size: 25
            halign: "center"
            size_hint_y: None
            height: self.texture_size[1]
            padding_y: 15     
            
        MDLabel:
            text: "Our agent will contact you shortly."
            font_size: 10
            halign: "center"
            size_hint_y: None
            height: self.texture_size[1]
            padding_y: 15 
            
        MDRoundFlatButton:
            text: "MENU"
            font_size: 15
            pos_hint:{"center_x":0.5, "center_y":0.1}
            on_press: app.root.current = 'menu'  
            

            
            
"""

class LoginScreen(Screen):
    def create_get(self):
         firebase_url = "https://fypvehicleappusers-default-rtdb.firebaseio.com/.json"
         res=requests.get(url = firebase_url)
         user_dict = res.json().get("Users")
         auth_list = []
         for key,value in user_dict.items():
             temp = [0, 0]
             for key1, value1 in value.items():
                 if key1=="Username":
                     temp[0]=value1
                 elif key1 == "Password":
                     temp[1]=value1
             auth_list.append(temp)
         return auth_list, user_dict

    def logger(self):
        auth_list,user_dict = self.create_get()
        user = self.ids.user_field.text
        passw = self.ids.password_field.text
        for item in auth_list:
            if item[0]==user and item[1]==passw:
                app = App.get_running_app()
                app.root.current = 'menu'

    def clear(self):
        self.ids.user_field.text = ""
        self.ids.password_field.text = ""

    def update_profile(self):
        auth_list, user_dict = self.create_get()
        name = ""
        user = ""
        email = ""
        phone = ""

        for key, value in user_dict.items():
            if value['Username'] == self.ids.user_field.text:
                for key1, value1 in value.items():
                    if key1 == "Name":
                        name = value1
                    elif key1 == "Surname":
                        name += " "+value1
                    elif key1 == "Username":
                        user = value1
                    elif key1 == "Email":
                        email = value1
                    elif key1 == "Phone Number":
                        phone = value1


        app = App.get_running_app()
        app.root.ids.profile.ids.profile_name.text = name
        app.root.ids.profile.ids.profile_user.text = user
        app.root.ids.profile.ids.profile_email.text = email
        app.root.ids.profile.ids.profile_phone.text = phone


    def update_policies(self):
        firebase_url = "https://fypvehicleapppolicies-default-rtdb.firebaseio.com/.json"
        res = requests.get(url=firebase_url)
        user_dict = res.json().get("Policies")
        for key, value in user_dict.items():
            for key1, value1 in value.items():
                if key1 == "Username" and value1==self.ids.user_field.text:
                    for key1, value1 in value.items():
                        if key1 == "Type":
                            typ = value1
                        if key1 == "Make":
                            make = value1
                        if key1 == "Policy Number":
                            pol_num = value1
                        if key1 == "Expiration Date":
                            exp_date = value1
                        if key1 == "VIN":
                            vin = value1

                    image_name = "images/sedan.png"
                    if make == 'sports car':
                        image_name = "images/sport-car.png"

                    new_img = Image(source = image_name, size_hint_x=None, width=40,size_hint_y=None)
                    new_label = Label(font_size="8sp",text="Type: "+str(typ)+"\nPolicy Number: "+str(pol_num)+"\nExpiration Date: "+str(exp_date)+"\nVIN: "+str(vin), valign="middle",
                                      size_hint_y=None)
                    new_button = Button(font_size="10sp", text="VIEW",size_hint_x=None, size_hint_y=None, width=40)
                    self.ids[str(pol_num)] = new_button


                    app = App.get_running_app()
                    app.root.ids.policies.ids.fourwheel_grid.add_widget(new_img)
                    app.root.ids.policies.ids.fourwheel_grid.add_widget(new_label)
                    app.root.ids.policies.ids.fourwheel_grid.add_widget(new_button)
                    new_button.bind(on_press = self.update_policy_display)


    def update_policy_display(self,instance):
        firebase_url = "https://fypvehicleapppolicies-default-rtdb.firebaseio.com/.json"
        res = requests.get(url=firebase_url)
        policy_dict = res.json().get("Policies")
        app = App.get_running_app()
        app.root.ids.display_policy.ids.policies_grid.clear_widgets()
        policy_num = QuoteForm.get_instance_id(self,instance)
        for key, value in policy_dict.items():
            for key1, value1 in value.items():
                if  key1 == "Policy Number" and value1 == int(policy_num):
                    for key1, value1 in value.items():
                        field = Label(text=str(key1), valign="middle")
                        val = Label(text=str(value1), valign="middle")
                        app.root.ids.display_policy.ids.policies_grid.add_widget(field)
                        app.root.ids.display_policy.ids.policies_grid.add_widget(val)
        app.root.current = 'display_policy'

class MenuScreen(Screen):
    pass

class SignUpScreen(Screen):

    def date_picker(self):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_save)
        date_dialog.open()

    def on_save(self, instance, value, date_range):
        self.ids.dob.text = str(value)

    def gender_picker(self):
        genders = ['Male', 'Female']
        gender_items = [
            {
                "viewclass": "OneLineListItem",
                "text": i,
                "height": dp(40),
                "on_release": lambda x=i: self.set_gender(x),
            } for i in genders
        ]
        self.gender_menu = MDDropdownMenu(
            caller=self.ids.gender,
            items=gender_items,
            position="center",
            width_mult=2,
        )
        self.gender_menu.open()

    def edu_picker(self):
        quals = ['none', 'highschool', 'university']
        qual_items = [
            {
                "viewclass": "OneLineListItem",
                "text": i,
                "height": dp(40),
                "on_release": lambda x=i: self.set_edu(x),
            } for i in quals
        ]
        self.qual_menu = MDDropdownMenu(
            caller=self.ids.edu,
            items=qual_items,
            position="center",
            width_mult=2,
        )
        self.qual_menu.open()

    def set_gender(self, text_item):
        self.ids.gender.text = text_item
        self.gender_menu.dismiss()

    def set_edu(self, text_item):
        self.ids.edu.text = text_item
        self.qual_menu.dismiss()

    def create_post(self):
        firebase_url = "https://fypvehicleappusers-default-rtdb.firebaseio.com/"

        name = self.ids.name.text
        surname = self.ids.surname.text
        dob = self.ids.dob.text
        gender = self.ids.gender.text
        address = self.ids.address.text
        postal_code = self.ids.postal_code.text
        phone_num = self.ids.phone_num.text
        email = self.ids.email.text
        edu = self.ids.edu.text
        income = self.ids.income.text
        credit_score = self.ids.credit_score.text

        driv_exp = self.ids.driv_exp.text
        veh_own = self.ids.veh_own.text
        speeding = self.ids.speeding.text
        duis = self.ids.duis.text
        past_acc = self.ids.past_acc.text

        user = self.ids.user.text
        passw = self.ids.passw.text

        fb = firebase.FirebaseApplication(firebase_url, None)
        data = {'Name': name,
                'Surname': surname,
                'Date of Birth': dob,
                'Gender': gender,
                'Address':address,
                'Postal Code': postal_code,
                'Phone Number': phone_num,
                'Email': email,
                'Education':edu,
                'Income': income,
                'Credit Score': credit_score,
                'Driving Experience': driv_exp,
                'Number of Vehicles Owned': veh_own,
                'Times Speeding': speeding,
                'DUIS': duis,
                'Number of Past Accidents': past_acc,
                'Username':user,
                'Password':passw
                }
        result = fb.post('/Users/', data)
        app = App.get_running_app()
        app.root.current = 'menu'


class QuoteForm(Screen):

    def reg_date_picker(self):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_save)
        date_dialog.open()

    def on_save(self, instance, value, date_range):
        self.ids.reg_date.text = str(value)

    def veh_type_picker(self):
        types = ['sedan', 'sports car']
        type_items = [
            {
                "viewclass": "OneLineListItem",
                "text": i,
                "height": dp(40),
                "on_release": lambda x=i: self.set_veh_type(x),
            } for i in types
        ]
        self.type_menu = MDDropdownMenu(
            caller=self.ids.veh_type,
            items=type_items,
            position="center",
            width_mult=2,
        )
        self.type_menu.open()

    def set_veh_type(self, text_item):
        self.ids.veh_type.text = text_item
        self.type_menu.dismiss()

    def fuel_type_picker(self):
        types = ['petrol', 'diesel']
        type_items = [
            {
                "viewclass": "OneLineListItem",
                "text": i,
                "height": dp(40),
                "on_release": lambda x=i: self.set_fuel_type(x),
            } for i in types
        ]
        self.type_menu = MDDropdownMenu(
            caller=self.ids.fuel_type,
            items=type_items,
            position="center",
            width_mult=2,
        )
        self.type_menu.open()

    def set_fuel_type(self, text_item):
        self.ids.fuel_type.text = text_item
        self.type_menu.dismiss()

    def post_quote_request(self, veh_make, veh_mileage, veh_type, model,fuel_type,vin,reg_date,condition):
        firebase_url = "https://fypvehicleappquoterequests-default-rtdb.firebaseio.com/"
        fb = firebase.FirebaseApplication(firebase_url, None)
        data = {'Vehicle Make': veh_make,
                'Vehicle Mileage': veh_mileage,
                'Vehicle Type': veh_type,
                'Model': model,
                'Fuel Type': fuel_type,
                'Vehicle Identification Number': vin,
                'Registration Date': reg_date,
                'Condition': condition
                }
        result = fb.post('/Quote Requests/', data)

    def get_income_level(self, income):
        income_level = ''
        income = int(income)
        if income>200000:
            income_level = 'upper class'
        elif income>=100000 and income<=200000:
            income_level = 'middle class'
        elif income>=50000 and income<100000:
            income_level = 'working class'
        else:
            income_level = 'poverty'

        return income_level


    def apply_multipliers(self,base_premium,multipliers):
        if multipliers==[]:
            return base_premium
        else:
            base_premium = base_premium+multipliers[0]*base_premium
            return(self.apply_multipliers(base_premium,multipliers[1:]))


    def find_recommendations(self, age, veh_mileage, credit_score, duis, driving_exp, education, gender, income, past_acc, speeding, veh_type):
        firebase_url = "https://fypvehicleappbasepremiums-default-rtdb.firebaseio.com/.json"
        res = requests.get(url=firebase_url)
        bases_dict = res.json().get("Bases per Annum")
        mult_dict = res.json().get("Multipliers")

        effects = []
        causes = []
        for key, value in mult_dict.items():
            if isinstance(value,dict):
                for key1, value1 in value.items():
                    if value1 != 0:
                        causes.append([key,key1])
                        effects.append(value1)
            else:
                causes.append(key)
                effects.append(value)

        multipliers = []
        for i in causes:
            if isinstance(i, list):
                if i[0] == 'Age':
                    bounds = i[1].split("-")
                    lower = bounds[0]
                    upper = bounds[1]
                    if int(age) >= int(lower) and int(age) <= int(upper):
                        multipliers.append(effects[causes.index(i)])
                if i[0] == 'Driving Exp':
                    bounds = i[1].split("-")
                    lower = bounds[0]
                    upper = bounds[1]
                    if int(driving_exp) >= int(lower) and int(driving_exp) <= int(upper):
                        multipliers.append(effects[causes.index(i)])
                if i[0] == 'Education':
                    if education == i[1].lower():
                        multipliers.append(effects[causes.index(i)])
                if i[0] == 'Income':
                    income_level = self.get_income_level(income)
                    if income_level == i[1].lower():
                        multipliers.append(effects[causes.index(i)])
                if i[0] == 'Vehicle Type':
                    if veh_type == i[1].lower():
                        multipliers.append(effects[causes.index(i)])
                if i[0] == 'Gender':
                    if gender == i[1]:
                        multipliers.append(effects[causes.index(i)])

            if i=='Annual Mileage':
                if int(veh_mileage) > 0:
                    multipliers.append(effects[causes.index(i)])
            if i=='Credit Score':
                if float(credit_score) > 0:
                    multipliers.append(effects[causes.index(i)])
            if i=='DUIS':
                if int(duis) > 0:
                    multipliers.append(effects[causes.index(i)])
            if i=='Past Accidents':
                if int(past_acc) > 0:
                    multipliers.append(effects[causes.index(i)])
            if i=='Speeding Violations':
                if int(speeding) > 0:
                    multipliers.append(effects[causes.index(i)])
            if i=='Vehicle Owned':
                multipliers.append(effects[causes.index(i)])

        multipliers[:] = [x / 100 for x in multipliers]

        recommendations_dict = {}
        for key, value in bases_dict.items():
            for key1 in value:
                if key1 == "Vehicle Type" and value[key1] == veh_type:
                    basic = value["Basic Premium"]
                    cng_lpg_cover = value["CNG-LPG"]
                    duration = value["Duration"]
                    passenger_cover = value["Passenger Cover"]
                    tppd = value["TPPD"]
                    total = value["Total Premium"]
                    vat = value["VAT"]
                    policy_name = key
                    new_basic = self.apply_multipliers(basic, multipliers)
                    total = int(total-(basic-new_basic))
                    basic = int(new_basic)
                    recommendations_dict[policy_name] = {'Basic Premium':basic,  'CNG-LPG Cover':cng_lpg_cover,
                                            'Duration':duration,'Passenger Cover':passenger_cover,'TPPD':tppd,
                                            'VAT':vat,'Total Premium':total}
        return recommendations_dict




    def add_quote_request(self):
        veh_make = self.ids.veh_make.text
        veh_mileage = self.ids.veh_mileage.text
        veh_type = self.ids.veh_type.text
        model = self.ids.model.text
        fuel_type = self.ids.fuel_type.text
        vin = self.ids.vin.text
        reg_date = self.ids.reg_date.text
        chk_used = self.ids.chk_used.active
        chk_new =self.ids.chk_new.active
        condition = ''

        if chk_used==False:
            condition = 'New'
        else:
            condition = 'Used'


        self.post_quote_request(veh_make,veh_mileage,veh_type,model,fuel_type,vin,reg_date,condition)

        app = App.get_running_app()
        username = app.root.ids.profile.ids.profile_user.text



        dob, gender, education, credit_score, duis, driving_exp, income, past_acc, speeding = ClaimForm().get_user_info(username, claim=False)
        dob = dob.split("-")
        age = ClaimForm().calculate_age(date(int(dob[0]), int(dob[1]), int(dob[2])))

        self.recommendations = self.find_recommendations(age, veh_mileage, credit_score, duis, driving_exp, education, gender, income, past_acc, speeding, veh_type)

        image_name = "images/sedan.png"
        if veh_type == 'sports car':
            image_name = "images/sport-car.png"

        for key, value in self.recommendations.items():
            for key1 in value:
                if key1=='Basic Premium':
                    basic = value["Basic Premium"]
                if key1=='Duration':
                    duration = value["Duration"]
                if key1=='Total Premium':
                    total = value["Total Premium"]
                if key1=='VAT':
                    vat = value["VAT"]


            slug = key.replace(" ", "_")
            new_img = Image(source=image_name, size_hint_x=None, width=40,size_hint_y=None)
            new_label = Label(font_size="8sp",
                          text="Policy Name: " + str(key) + "\nTotal Premium: " + str(total) + "\nBasic Premium: " + str(
                              basic) + "\nVAT: " + str(vat)+ "\nDuration: " + str(duration), valign="middle", size_hint_y=None)
            new_button = Button(font_size="10sp", text="VIEW", size_hint_x=None, width=40,size_hint_y=None)
            self.ids[str(key)] = new_button
            new_button.bind(on_press=self.update_quote_display)
            app.root.ids.quote_screen.ids.quotes_grid.add_widget(new_img)
            app.root.ids.quote_screen.ids.quotes_grid.add_widget(new_label)
            app.root.ids.quote_screen.ids.quotes_grid.add_widget(new_button)

        app.root.current = 'quote_screen'

    def get_instance_id(self, instance):
        if instance in self.ids.values():
            return (list(self.ids.keys())[list(self.ids.values()).index(instance)])

    def update_quote_display(self, instance):
        recommendations  = self.recommendations
        policy_name = str(self.get_instance_id(instance))

        firebase_url = "https://fypvehicleapppolicies-default-rtdb.firebaseio.com/.json"
        res = requests.get(url=firebase_url)
        policies_dict = res.json().get("Policies")
        app = App.get_running_app()
        app.root.ids.display_quote.ids.quote_grid.clear_widgets()

        display_recommendation = recommendations[policy_name]
        for key1, value1 in display_recommendation.items():
            field = Label(text=str(key1), valign="middle")
            val = Label(text=str(value1), valign="middle")
            app.root.ids.display_quote.ids.quote_grid.add_widget(field)
            app.root.ids.display_quote.ids.quote_grid.add_widget(val)

        app.root.current = 'display_quote'

class QuoteScreen(Screen):
    pass

class ClaimForm(Screen):

    def send_email(self, fromaddr, toaddr, subject, message):

        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = subject
        body = message

        msg.attach(MIMEText(body, 'plain'))

        s = smtplib.SMTP('smtp.gmail.com', 587)

        s.starttls()

        try:
            s.login(fromaddr, "FYPinsuranceapp2022")

            text = msg.as_string()

            s.sendmail(fromaddr, toaddr, text)
        except:
            print("An Error occured while sending email.")
        finally:
            s.quit()

        return []

    def incident_type_picker(self):
        incident_types = ['Multi Vehicle Collision', 'Single Vehicle Collision']
        incident_types_items = [
            {
                "viewclass": "OneLineListItem",
                "text": i,
                "height": dp(40),
                "on_release": lambda x=i: self.set_incident_type(x),
            } for i in incident_types
        ]
        self.incident_types_menu = MDDropdownMenu(
            caller=self.ids.incident_type,
            items=incident_types_items,
            position="center",
            width_mult=4,
        )
        self.incident_types_menu.open()

    def set_incident_type(self, text_item):
        self.ids.incident_type.text = text_item
        self.incident_types_menu.dismiss()

    def collision_type_picker(self):
        collision_types = ['Front Collision', 'Rear Collision', 'Side Collision']
        collision_types_items = [
            {
                "viewclass": "OneLineListItem",
                "text": i,
                "height": dp(40),
                "on_release": lambda x=i: self.set_collision_type(x),
            } for i in collision_types
        ]
        self.collision_types_menu = MDDropdownMenu(
            caller=self.ids.collision_type,
            items=collision_types_items,
            position="center",
            width_mult=4,
        )
        self.collision_types_menu.open()

    def set_collision_type(self, text_item):
        self.ids.collision_type.text = text_item
        self.collision_types_menu.dismiss()

    def severity_picker(self):
        severity_types = ['Major Damage', 'Minor Damage', 'Total Loss']
        severity_types_items = [
            {
                "viewclass": "OneLineListItem",
                "text": i,
                "height": dp(40),
                "on_release": lambda x=i: self.set_severity_type(x),
            } for i in severity_types
        ]
        self.severity_types_menu = MDDropdownMenu(
            caller=self.ids.severity,
            items=severity_types_items,
            position="center",
            width_mult=4,
        )
        self.severity_types_menu.open()

    def set_severity_type(self, text_item):
        self.ids.severity.text = text_item
        self.severity_types_menu.dismiss()

    def auth_contact_picker(self):
        auth_contact_types = ['Ambulance', 'Fire', 'Police', 'Other']
        auth_contact_types_items = [
            {
                "viewclass": "OneLineListItem",
                "text": i,
                "height": dp(40),
                "on_release": lambda x=i: self.set_auth_contact_type(x),
            } for i in auth_contact_types
        ]
        self.auth_contact_types_menu = MDDropdownMenu(
            caller=self.ids.severity,
            items=auth_contact_types_items,
            position="center",
            width_mult=4,
        )
        self.auth_contact_types_menu.open()

    def set_auth_contact_type(self, text_item):
        self.ids.auth_contact.text = text_item
        self.auth_contact_types_menu.dismiss()

    def incident_date_picker(self):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_save)
        date_dialog.open()

    def on_save(self, instance, value, date_range):
        self.ids.incident_date.text = str(value)

    def police_report_picker(self):
        police_report_status = ['Yes', 'No']
        police_report_status_items = [
            {
                "viewclass": "OneLineListItem",
                "text": i,
                "height": dp(40),
                "on_release": lambda x=i: self.set_police_report_type(x),
            } for i in police_report_status
        ]
        self.police_report_types_menu = MDDropdownMenu(
            caller=self.ids.police_report,
            items=police_report_status_items,
            position="center",
            width_mult=2,
        )
        self.police_report_types_menu.open()

    def set_police_report_type(self, text_item):
        self.ids.police_report.text = text_item
        self.police_report_types_menu.dismiss()

    def calculate_age(self, birthDate):
        today = date.today()
        age = today.year - birthDate.year - ((today.month, today.day) < (birthDate.month, birthDate.day))
        return age

    def get_user_info(self, username, claim=True):
        users_url = "https://fypvehicleappusers-default-rtdb.firebaseio.com/.json"
        res_users = requests.get(url=users_url)
        users_dict = res_users.json().get("Users")

        for key, value in users_dict.items():
            for key1 in value:
                if key1 == "Username" and value[key1] == username:
                    dob = value["Date of Birth"]
                    gender = value["Gender"]
                    education = value["Education"]
                    credit_score = value["Credit Score"]
                    duis = value["DUIS"]
                    driving_exp = value["Driving Experience"]
                    income = value["Income"]
                    past_acc = value["Number of Past Accidents"]
                    speeding = value["Times Speeding"]

                    if claim:
                        return dob, gender, education
                    else:
                        return dob, gender, education, credit_score, duis, driving_exp, income, past_acc, speeding


    def get_policy_info(self, policy_number):
        policies_url = "https://fypvehicleapppolicies-default-rtdb.firebaseio.com/.json"
        res_policies = requests.get(url=policies_url)
        policies_dict = res_policies.json().get("Policies")

        for key, value in policies_dict.items():
            for key1 in value:
                if key1 == "Policy Number" and value["Policy Number"] == int(policy_number):
                    policy_deductible = value["Deductible"]
                    policy_annual_premium = value["Premium per Annum"]
                    auto_year = value["Vehicle Year"]

                    return policy_deductible, policy_annual_premium, auto_year

    def post_claim(self, policy_number, incident_type, total_claim_amount, collision_type, severity,
                   incident_date, auth_contact, police_report, number_of_vehicles_involved, account_holder_name,
                   bank_account_number, routing_code, bank_name, bank_branch, taxpayer_number, fraud):
        firebase_url = "https://fypvehicleappclaims-default-rtdb.firebaseio.com/"
        fb = firebase.FirebaseApplication(firebase_url, None)
        data = {'Policy Number': policy_number,
                'Incident Type': incident_type,
                'Total Claim Amount': total_claim_amount,
                'Collision Type': collision_type,
                'Severity': severity,
                'Incident Date': incident_date,
                'Authorities Contacted': auth_contact,
                'Police Report Available': police_report,
                'Number of Vehicles Involved': number_of_vehicles_involved,
                'Account Holder Name': account_holder_name,
                'Bank Account Number': bank_account_number,
                'Routing Code': routing_code,
                'Bank Name': bank_name,
                'Bank Branch Name': bank_branch,
                'Taxpayer Identification Number': taxpayer_number,
                'Fraud Suspect':fraud
                }
        result = fb.post('/Claims/', data)



    def add_claim(self):
        policy_number = self.ids.policy_number.text
        incident_type = self.ids.incident_type.text
        total_claim_amount = self.ids.claim_amount.text
        collision_type = self.ids.collision_type.text
        severity = self.ids.severity.text
        incident_date = self.ids.incident_date.text
        auth_contact = self.ids.auth_contact.text
        police_report = self.ids.police_report.text
        number_of_vehicles_involved = self.ids.num_vehicles.text
        account_holder_name = self.ids.account_holder_name.text
        bank_account_number= self.ids.bank_account_number.text
        routing_code= self.ids.routing_code.text
        bank_name= self.ids.bank_name.text
        bank_branch= self.ids.bank_branch.text
        taxpayer_number= self.ids.taxpayer_number.text

        app = App.get_running_app()
        username = app.root.ids.profile.ids.profile_user.text
        email = app.root.ids.profile.ids.profile_email.text

        if incident_type == "Multi Vehicle Collision":
            incident_type_Multi_Vehicle_Collision = 1
            incident_type_Single_Vehicle_Collision = 0
        else:
            incident_type_Multi_Vehicle_Collision = 0
            incident_type_Single_Vehicle_Collision = 1

        if collision_type == "Front Collision":
            collision_type_Front_Collision = 1
            collision_type_Rear_Collision = 0
            collision_type_Side_Collision = 0
        elif collision_type == "Rear Collision":
            collision_type_Front_Collision = 0
            collision_type_Rear_Collision = 1
            collision_type_Side_Collision = 0
        else:
            collision_type_Front_Collision = 0
            collision_type_Rear_Collision = 0
            collision_type_Side_Collision = 1

        if severity == "Major Damage":
            incident_severity_Major_Damage = 1
            incident_severity_Minor_Damage = 0
            incident_severity_Total_Loss = 0
        elif severity == "Minor Damage":
            incident_severity_Major_Damage = 0
            incident_severity_Minor_Damage = 1
            incident_severity_Total_Loss = 0
        else:
            incident_severity_Major_Damage = 0
            incident_severity_Minor_Damage = 0
            incident_severity_Total_Loss = 1

        if auth_contact == "Ambulance":
            authorities_contacted_Ambulance = 1
            authorities_contacted_Fire = 0
            authorities_contacted_Other = 0
            authorities_contacted_Police = 0
        elif auth_contact == "Fire":
            authorities_contacted_Ambulance = 0
            authorities_contacted_Fire = 1
            authorities_contacted_Other = 0
            authorities_contacted_Police = 0
        elif auth_contact == "Other":
            authorities_contacted_Ambulance = 0
            authorities_contacted_Fire = 0
            authorities_contacted_Other = 1
            authorities_contacted_Police = 0
        else:
            authorities_contacted_Ambulance = 0
            authorities_contacted_Fire = 0
            authorities_contacted_Other = 0
            authorities_contacted_Police = 1

        if police_report=="Yes":
            police_report_available_NO = 0
            police_report_available_YES = 1
        else:
            police_report_available_NO = 1
            police_report_available_YES = 0

        dob, gender, education = self.get_user_info(username)
        dob = dob.split("-")
        age = self.calculate_age(date(int(dob[0]), int(dob[1]), int(dob[2])))

        policy_deductible, policy_annual_premium, auto_year = self.get_policy_info(policy_number)



        if gender == "Male":
            insured_sex_FEMALE = 0
            insured_sex_MALE = 1
        else:
            insured_sex_FEMALE = 1
            insured_sex_MALE = 0

        if education == "highschool":
            insured_education_level_Associate = 0
            insured_education_level_College = 0
            insured_education_level_High_School = 1
            insured_education_level_JD = 0
            insured_education_level_MD = 0
            insured_education_level_Masters = 0
            insured_education_level_PhD = 0
        elif education == "university":
            insured_education_level_Associate = 0
            insured_education_level_College = 1
            insured_education_level_High_School = 0
            insured_education_level_JD = 0
            insured_education_level_MD = 0
            insured_education_level_Masters = 0
            insured_education_level_PhD = 0
        else:
            insured_education_level_Associate = 0
            insured_education_level_College = 0
            insured_education_level_High_School = 0
            insured_education_level_JD = 0
            insured_education_level_MD = 0
            insured_education_level_Masters = 0
            insured_education_level_PhD = 0

        with open('classifiers/random_forest_classifier_pkl', 'rb') as f:
            clf = pickle.load(f)
        prediction = clf.predict([[
            insured_sex_FEMALE,
            insured_sex_MALE,
            incident_type_Multi_Vehicle_Collision,
            incident_type_Single_Vehicle_Collision,
            insured_education_level_Associate,
            insured_education_level_College,
            insured_education_level_High_School,
            insured_education_level_JD,
            insured_education_level_MD,
            insured_education_level_Masters,
            insured_education_level_PhD,
            collision_type_Front_Collision,
            collision_type_Rear_Collision,
            collision_type_Side_Collision,
            incident_severity_Major_Damage,
            incident_severity_Minor_Damage,
            incident_severity_Total_Loss,
            authorities_contacted_Ambulance,
            authorities_contacted_Fire,
            authorities_contacted_Other,
            authorities_contacted_Police,
            police_report_available_NO,
            police_report_available_YES,
            age,
            policy_deductible,
            policy_annual_premium,
            number_of_vehicles_involved,
            total_claim_amount,
            auto_year
        ]])

        print("prediction = "+str(prediction))


        prediction = re.sub('\D', '', str(prediction))
        fraud = ""
        if prediction == "1":
            fraud = "True"
        else:
            fraud = "False"



        self.post_claim(policy_number, incident_type, total_claim_amount, collision_type, severity,
                        incident_date, auth_contact, police_report, number_of_vehicles_involved, account_holder_name,
                        bank_account_number, routing_code, bank_name, bank_branch, taxpayer_number, fraud)

        fromaddr = 'fypcarinsuranceapp@gmail.com'
        toaddr = email
        subject = 'Claim Filed'
        message = 'claim filed successfully'

        self.send_email(fromaddr, toaddr, subject, message)
        app.root.current = 'claim_screen'



class DisplayQuote(Screen):
    pass

class ClaimScreen(Screen):
    pass

class PolicyScreen(Screen):
    pass

class DisplayPolicy(Screen):
    pass

class ProfileScreen(Screen):
    pass

class OwnershipDetailsScreen(Screen):
    pass

class SettingScreen(Screen):
    pass


# Create the screen manager
sm = ScreenManager()
sm.add_widget(LoginScreen(name='login'))
sm.add_widget(MenuScreen(name='menu'))
sm.add_widget(MenuScreen(name='signup'))
sm.add_widget(MenuScreen(name='quote_form'))
sm.add_widget(MenuScreen(name='quote_screen'))
sm.add_widget(MenuScreen(name='claim_form'))
sm.add_widget(MenuScreen(name='claim_screen'))
sm.add_widget(MenuScreen(name='policies'))
sm.add_widget(MenuScreen(name='profile'))
sm.add_widget(MenuScreen(name='settings'))
sm.add_widget(MenuScreen(name='display_policy'))
sm.add_widget(MenuScreen(name='display_quote'))
sm.add_widget(MenuScreen(name='ownership_details_screen'))

class MainApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"
        screen = Builder.load_string(screen_helper)
        self.title = "Vehicle Insurance Application"
        return screen


if __name__ == '__main__':
    MainApp().run()