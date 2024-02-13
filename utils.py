import json
import openai
from collections import defaultdict

Accounts_file = 'Accounts.json'
types_file = 'types.json'

delimiter = "####"
step_2_system_message_content = f"""
You will be provided with customer service queries. \
The customer service query will be delimited with \
{delimiter} characters.
Output a python list of accounts, where each account has \
the following format:
    'type': <Savings Account (Gold Saver), \
     Savings Account(Youth Saver), \,
     Savings Account (Smart Saver), \, 
     Savings Account (Premium Plus) \, 
     Current Account(Business Pro)\,  
     Fixed Deposit Account (Senior Citizens FD)>,
OR
    'Accounts': <a list of account type that must \
    be found in the allowed accounts below>

Where the account type and account must be identified in \
the customer service query.
If a account type is mentioned, it should be matched with \
the correct account from the allowed account type below.
If no account type or account are identified, output an \
empty list.

Allowed Accounts: 
 
Savings Account (Gold Saver)type:
Premium Savings Account
VIP Savings Account
Gold Priority Savings Account
Platinum Savings Account
Premium Wealth Savings Account
Exclusive Savings Account

Savings Account (Smart Saver)type:
Digital or Online Savings Account
High-Interest Savings Account
Cashback Savings Account
Health Savings Account 
Green Savings Account
Goal-Based Savings Account

Savings Account(Youth Saver)type:
Government-sponsored Youth Savings
Student Savings Account
Children's Savings Account
Charitable or Community-focused Youth 
Savings Account
Custodial Savings Account
Educational Savings Account
Incentivized Savings Account

Savings Account (Premium Plus)type:
Premium Customer Service
Exclusive Access to Financial Products
Fee Waivers
Complimentary Services
Travel Benefits
Cashback Rewards

Current Account(Business Pro)type:
Standard Current Account
Student Current Account
Premium Current Account
Business Current Account
Foreign National Current Account

Fixed Deposit Account type:
Corporate Fixed Deposit
Regular Income Fixed Deposit
Flexi Fixed Deposit
Cumulative Fixed Deposit
Non-Cumulative Fixed Deposit


Only output the list of accounts, with nothing else.
"""

step_2_system_message = {'role':'system', 'content': step_2_system_message_content}    


step_4_system_message_content = f"""
   You are a customer service assistant in the banking sector. \
    Respond in a friendly and helpful tone, with concise answers. \
    Make sure to ask the user relevant follow-up questions.
    """

step_4_system_message = {'role':'system', 'content': step_4_system_message_content}    

step_6_system_message_content = f"""
    You are an assistant that evaluates whether \
customer service agent responses sufficiently \
answer customer questions, and also validates that \
all the facts the assistant cites from the account \
details are correct.
The account details and user and customer \
service agent messages will be delimited by \
3 backticks, i.e. ```.
Respond with a Y or N character, with no punctuation:
Y - if the response effectively addresses the banking inquiry \
AND the information cited from the banking details is correct
N - otherwise

Output a single letter only.
"""

step_6_system_message = {'role':'system', 'content': step_6_system_message_content}    


def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0, max_tokens=500):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature, 
        max_tokens=max_tokens, 
    )
    return response.choices[0].message["content"]

def create_type():
    type_dict = { 
        'Deposit and Withdrawal': [
            'Transaction history',
            'Deposit funds',
            'Withdraw funds',
            'Check account balance'
        ],
        'Online Banking': [
            'Login issues',
            'Password reset',
            'Account activation',
            'Online transactions'
        ],
        'Loan Services': [
            'Loan application status',
            'Interest rates',
            'Loan payment',
            'Loan eligibility'
        ],
        'Security': [
            'Report suspicious activity',
            'Account authentication',
            'Fraud prevention',
            'Lost or stolen card'
        ],
        'General Inquiry': [
            'Branch locations',
            'ATM services',
            'Account types',
            'Customer feedback'
        ]
    }

    with open(types_file, 'w') as file:
        json.dump(type_dict, file)

    return type_dict



def get_types():
    with open(types_file, 'r') as file:
            types = json.load(file)
    return types


def get_Account_list():
    """
    Used in L4 to get a flat list of Accounts
    """
    Accounts = get_Accounts()
    Account_list = []
    for Account in Accounts.keys():
        Account_list.append(Acccount)
    
    return product_list

def get_Accounts_and_type():
    """
    Used in L5
    """
    Accounts = get_Accounts()
    Accounts_by_type = defaultdict(list)
    for Account_name, Account_info in Accounts.items():
        type = Account_info.get('type')
        if type:
            Accounts_by_type[type].append(Account_info.get('name'))
    
    return dict(Accounts_by_type)

def get_Accounts():
    with open(Accounts_file, 'r') as file:
        Accounts = json.load(file)
    return Accounts

def find_type_and_Account(user_input,Accounts_and_type):
    delimiter = "####"
    system_message = f"""
    You will be provided with customer service queries. \
    The customer service query will be delimited with {delimiter} characters.
    Output a python list of json objects, where each object has the following format:
        'type': <one of Savings Account (Gold Saver), \Savings Account(Youth Saver), \,Savings Account (Smart Saver), \, 
    Savings Account (Premium Plus) \, Current Account(Business Pro)\,Fixed Deposit Account (Senior Citizens FD)>,
    OR
        'Accounts': <a list of account type that must \
    be found in the allowed accounts below>

   Where the account type and account must be identified in \
   the customer service query.If a account type is mentioned, \
   it should be matched with the correct account from the \
   allowed account type below.If no account type or account are \
   identified, output an empty list.

    The allowed Accounts are provided in JSON format.
    The keys of each item represent the type.
    The values of each item is a list of Accounts that are within that type.
    Allowed Accounts: {Accounts_and_type}
    
    """
    messages =  [  
    {'role':'system', 'content': system_message},    
    {'role':'user', 'content': f"{delimiter}{user_input}{delimiter}"},  
    ] 
    return get_completion_from_messages(messages)

def find_type_and_Account_only(user_input,Accounts_and_type):
    delimiter = "####"
    system_message = f"""
    You will be provided with customer service queries. \
    The customer service query will be delimited with {delimiter} characters.
    Output a python list of objects, where each object has the following format:
   'type': <one of Savings Account (Gold Saver), \Savings Account(Youth Saver) \,
    Savings Account (Smart Saver) \, Savings Account (Premium Plus) \, 
    Current Account(Business Pro)\,Fixed Deposit Account (Senior Citizens FD)>,
    OR
   'Accounts': <a list of account type that must \
    be found in the allowed accounts below>
    
    
     Where the account type and account must be identified in \
     the customer service query.
     If a account type is mentioned, it should be matched with \
     the correct account from the allowed account type below.
     If no account type or account are identified, output an \
     empty list.

Allowed Accounts: 
 
Savings Account (Gold Saver)type:
Premium Savings Account
VIP Savings Account
Gold Priority Savings Account
Platinum Savings Account
Premium Wealth Savings Account
Exclusive Savings Account

Savings Account (Smart Saver)type:
Digital or Online Savings Account
High-Interest Savings Account
Cashback Savings Account
Health Savings Account 
Green Savings Account
Goal-Based Savings Account

Savings Account(Youth Saver)type:
Government-sponsored Youth Savings
Student Savings Account
Children's Savings Account
Charitable or Community-focused Youth 
Savings Account
Custodial Savings Account
Educational Savings Account
Incentivized Savings Account

Savings Account (Premium Plus)type:
Premium Customer Service
Exclusive Access to Financial Products
Fee Waivers
Complimentary Services
Travel Benefits
Cashback Rewards

Current Account(Business Pro)type:
Standard Current Account
Student Current Account
Premium Current Account
Business Current Account
Foreign National Current Account

Fixed Deposit Account type:
Corporate Fixed Deposit
Regular Income Fixed Deposit
Flexi Fixed Deposit
Cumulative Fixed Deposit
Non-Cumulative Fixed Deposit


Only output the list of accounts, with nothing else.
"""
  
    messages =  [  
    {'role':'system', 'content': system_message},    
    {'role':'user', 'content': f"{delimiter}{user_input}{delimiter}"},  
    ] 
    return get_completion_from_messages(messages)

def get_Accounts_from_query(user_msg):
    """
    Code from L5, used in L8
    """
    Accounts_and_type = get_Accounts_and_type()
    delimiter = "####"
    system_message = f"""
    You will be provided with customer service queries. \
    The customer service query will be delimited with {delimiter} characters.
    Output a python list of json objects, where each object has the following format:
        'type': <one of Savings Account (Gold Saver), \Savings Account(Youth Saver) \,
     Savings Account (Smart Saver) \, Savings Account (Premium Plus) \, 
     Current Account(Business Pro)\,Fixed Deposit Account (Senior Citizens FD)>,
OR
    'Accounts': <a list of account type that must \
    be found in the allowed accounts below>

    Where the account type and account must be identified in \
    the customer service query.
    If a account type is mentioned, it should be matched with \
    the correct account from the allowed account type below.
    If no account type or account are identified, output an \
    empty list.

    The allowed Accounts are provided in JSON format.
    The keys of each item represent the type.
    The values of each item is a list of Accounts that are within that type.
    Allowed Accounts: {Accounts_and_type}

    """
    
    messages =  [  
    {'role':'system', 'content': system_message},    
    {'role':'user', 'content': f"{delimiter}{user_msg}{delimiter}"},  
    ] 
    type_and_Account_response = get_completion_from_messages(messages)
    
    return type_and_Account_response


# Account look up (either by type or by Account within type)
def get_Account_by_name(name):
    Accounts = get_Accounts()
    return Accounts.get(name, None)

def get_Accounts_by_type(type):
    Accounts = get_Accounts()
    return [Account for Account in Accounts.values() if Account["type"] == type]

def get_mentioned_Account_info(data_list):
    """
    Used in L5 and L6
    """
    Account_info_l = []

    if data_list is None:
        return Account_info_l

    for data in data_list:
        try:
            if "Accounts" in data:
                Accounts_list = data["Accounts"]
                for Account_name in Accounts_list:
                    Account = get_Account_by_name(Account_name)
                    if Account:
                        Account_info_l.append(Account)
                    else:
                        print(f"Error: Account '{Account_name}' not found")
            elif "type" in data:
                type_name = data["type"]
                type_Accounts = get_Accounts_by_type(type_name)
                for Account in type_Accounts:
                    Account_info_l.append(Account)
            else:
                print("Error: Invalid object format")
        except Exception as e:
            print(f"Error: {e}")

    return Account_info_l



def read_string_to_list(input_string):
    if input_string is None:
        return None

    try:
        input_string = input_string.replace("'", "\"")  # Replace single quotes with double quotes for valid JSON
        data = json.loads(input_string)
        return data
    except json.JSONDecodeError:
        print("Error: Invalid JSON string")
        return None

def generate_output_string(data_list):
    output_string = ""

    if data_list is None:
        return output_string

    for data in data_list:
        try:
            if "Accounts" in data:
                Accounts_list = data["Accounts"]
                for Account_name in Accounts_list:
                    Account = get_Account_by_name(Account_name)
                    if Account:
                        output_string += json.dumps(Account, indent=4) + "\n"
                    else:
                        print(f"Error: Product '{Account_name}' not found")
            elif "type" in data:
                type_name = data["type"]
                type_Accounts = get_Accounts_by_type(type_name)
                for Account in type_Accounts:
                    output_string += json.dumps(Account, indent=4) + "\n"
            else:
                print("Error: Invalid object format")
        except Exception as e:
            print(f"Error: {e}")

    return output_string

# Example usage:
#Account_information_for_user_message_1 = generate_output_string(type_and_Account_list)
#print(Account_information_for_user_message_1)

def answer_user_msg(user_msg, Account_info):
    """
    Code from L5, used in L6
    """
    delimiter = "####"
    system_message = f"""
    You are a customer service assistant in the banking sector. \
    Respond in a friendly and helpful tone, with concise answers. \
    Make sure to ask the user relevant follow up questions.
    """
    # user_msg = f"""
    # tell me about the Health Savings Account  and \
    # Business Current Account, Educational Savings Account \
    # the VIP Savings Account the Premium Customer Service. \
    # Also tell me about your Fixed Deposit Account.
    # """

    messages =  [  
    {'role':'system', 'content': system_message},   
    {'role':'user', 'content': f"{delimiter}{user_msg}{delimiter}"},  
    {'role':'assistant', 'content': f"Relevant Account information:\n{Account_info}"},   
    ] 
    response = get_completion_from_messages(messages)
    return response

def create_Accounts():
    """
        Create Accounts dictionary and save it to a file named Accounts.json
    """
    # Account information
    # fun fact: all these Accounts are fake and were generated by a language model
    Accounts = {

     "Premium Savings Account": {
        "name": "Premium Savings Account",
        "category": "Savings Account (Gold Saver)",
        "brand": "TechPro",
        "model_number": "TP-UB100",
        "warranty": "1 year",
        "rating": 4.5,
        "features": ["13.3-inch display", "8GB RAM", "256GB SSD", "Intel Core i5 processor"],
        "description": "A sleek and lightweight ultrabook for everyday use.",
        "price": 799.99
    },
   "Premium Savings Account": {
        "Name": "Premium Savings Account",
       "Type": "Savings Account (Gold Saver)",
        "Transaction Type": "Deposit",
        "Fund Transfer": "Internal & External Accounts",
        "Bill Payments": "Mortgage Payments",
        "Interest Rate": "2.5%",  # Placeholder: The annual interest rate on the account.
        "Minimum Balance": "$1,000"  # Placeholder: The minimum balance required to maintain the account.
    },
    "VIP Savings Account": {
        "Name": "VIP Savings Account",
        "Type": "Savings Account (Gold Saver)",
        "Transaction Type": "Deposit/Withdrawal",
        "Fund Transfer": "Internal & External Accounts",
        "Bill Payments": "Various",
        "Interest Rate": "Assume the Interest Rate, e.g., 3.0%",
        "Minimum Balance": "$5,000",
    },
    
    "Gold Priority Savings Account": {
        "Name": "Gold Priority Savings Account",
        "Type": "Savings Account (Gold Saver)",
        "Transaction Type": "Deposit/Withdrawal",
        "Fund Transfer": "Internal & External Accounts",
        "Bill Payments": "Priority Services",
        "Interest Rate": "Assume the Interest Rate, e.g., 2.75%",
        "Minimum Balance": "$2,500"
    },
    "Platinum Savings Account": {
        "Name": "Platinum Savings Account",
        "Type": "Savings Account (Gold Saver)",
        "Transaction Type": "Deposit/Withdrawal",
        "Fund Transfer": "Internal & External Accounts",
        "Bill Payments": "Concierge Services",
        "Interest Rate": "Assume the Interest Rate, e.g., 3.5%",
        "Minimum Balance": "$10,000"
    },
    "Premium Wealth Savings Account": {
        "Name": "Premium Wealth Savings Account",
        "Type": "Savings Account (Gold Saver)",
        "Transaction Type": "Deposit/Withdrawal",
        "Fund Transfer": "Internal & External Accounts",
        "Bill Payments": "Wealth Management Services",
        "Interest Rate": "Assume the Interest Rate, e.g., 4.0%",
        "Minimum Balance": "$50,000"
    },
    "Exclusive Savings Account": {
        "Name": "Exclusive Savings Account",
        "Type": "Savings Account (Gold Saver)",
        "Transaction Type": "Deposit/Withdrawal",
        "Fund Transfer": "Internal & External Accounts",
        "Bill Payments": "Exclusive Benefits",
        "Interest Rate": "Assume the Interest Rate, e.g., 3.25%",
        "Minimum Balance": "$20,000"
    },
    "Digital or Online Savings Account": {
        "Name": "Digital or Online Savings Account",
        "Type": "Savings Account (Smart Saver)",
        "Transaction Type": "Online Transactions",
        "Fund Transfer": "Internal & External Accounts",
        "Bill Payments": "Digital Payments",
        "Interest Rate": "Assume the Interest Rate, e.g., 2.0%",
        "Minimum Balance": "$500"
    },
    "High-Interest Savings Account": {
        "Name": "High-Interest Savings Account",
        "Type": "Savings Account (Smart Saver)",
        "Transaction Type": "Deposit/Withdrawal",
        "Fund Transfer": "Internal & External Accounts",
        "Bill Payments": "Various",
        "Interest Rate": "Assume the High Interest Rate, e.g., 3.5%",
        "Minimum Balance": "$1,000"
    },
    "Cashback Savings Account": {
        "Name": "Cashback Savings Account",
        "Type": "Savings Account (Smart Saver)",
        "Transaction Type": "Cashback Rewards",
        "Fund Transfer": "Internal & External Accounts",
        "Bill Payments": "Cashback on Selected Categories",
        "Interest Rate": "Assume the Interest Rate, e.g., 2.25%",
        "Minimum Balance": "$500"
    },
    "Health Savings Account": {
        "Name": "Health Savings Account",
        "Type": "Savings Account (Smart Saver)",
        "Transaction Type": "Health-related Expenses",
        "Fund Transfer": "Internal & External Accounts",
        "Bill Payments": "Medical Bills",
        "Interest Rate": "Assume the Interest Rate, e.g., 1.75%",
        "Minimum Balance": "$1,000"
    },
    "Green Savings Account": {
        "Name": "Green Savings Account",
        "Type": "Savings Account (Smart Saver)",
        "Transaction Type": "Eco-friendly Transactions",
        "Fund Transfer": "Internal & External Accounts",
        "Bill Payments": "Green Initiatives",
        "Interest Rate": "Assume the Interest Rate, e.g., 2.0%",
        "Minimum Balance": "$500"
    },
    "Goal-Based Savings Account": {
        "Name": "Goal-Based Savings Account",
        "Type": "Savings Account (Smart Saver)",
        "Transaction Type": "Goal-oriented Deposits",
        "Fund Transfer": "Internal & External Accounts",
        "Bill Payments": "Aligned with Financial Goals",
        "Interest Rate": "Assume the Interest Rate, e.g., 2.5%",
        "Minimum Balance": "$1,000"
    },
    "Student Savings Account": {
        "Name": "Student Savings Account",
        "Type": "Savings Account (Youth Saver)",
        "Transaction Type": "Deposit/Withdrawal",
        "Fund Transfer": "Internal & External Accounts",
        "Bill Payments": "Educational Expenses",
        "Interest Rate": "Assume the Interest Rate, e.g., 1.5%",
        "Minimum Balance": "$100"
    },
    "Children's Savings Account": {
        "Name": "Children's Savings Account",
        "Type": "Savings Account (Youth Saver)",
        "Transaction Type": "Deposit/Withdrawal",
        "Fund Transfer": "Internal & External Accounts",
        "Bill Payments": "Child-related Expenses",
        "Interest Rate": "Assume the Interest Rate, e.g., 2.0%",
        "Minimum Balance": "$50"
    },
    "Charitable or Community-focused Youth Savings Account": {
        "Name": "Charitable or Community-focused Youth Savings Account",
        "Type": "Savings Account (Youth Saver)",
        "Transaction Type": "Deposit/Withdrawal",
        "Fund Transfer": "Internal & External Accounts",
        "Bill Payments": "Charitable Contributions",
        "Interest Rate": "Assume the Interest Rate, e.g., 1.75%",
        "Minimum Balance": "$75"
    },
    "Custodial Savings Account": {
        "Name": "Custodial Savings Account",
        "Type": "Savings Account (Youth Saver)",
        "Transaction Type": "Deposit/Withdrawal",
        "Fund Transfer": "Internal & External Accounts",
        "Bill Payments": "Guardianship-related Expenses",
        "Interest Rate": "Assume the Interest Rate, e.g., 1.8%",
        "Minimum Balance": "$200"
    },
    "Educational Savings Account": {
        "Name": "Educational Savings Account",
        "Type": "Current Account(Business Pro)",
        "Transaction Type": "Deposit/Withdrawal",
        "Fund Transfer": "Internal & External Accounts",
        "Bill Payments": "Educational Expenses",
        "Interest Rate": "Assume the Interest Rate, e.g., 2.5%",
        "Minimum Balance": "$150"
    },
    "Standard Current Account": {
        "Name": "Standard Current Account",
        "Type": "Current Account(Business Pro)",
        "Transaction Type": "Deposit/Withdrawal",
        "Fund Transfer": "Internal & External Accounts",
        "Bill Payments": "Various",
        "Monthly Fee": "$10",
        "Minimum Balance": "$1,000"
    },
    "Student Current Account": {
        "Name": "Student Current Account",
        "Type": "Current Account(Business Pro)",
        "Transaction Type": "Deposit/Withdrawal",
        "Fund Transfer": "Internal & External Accounts",
        "Bill Payments": "Student-related Expenses",
        "Monthly Fee": "No Monthly Fee",
        "Minimum Balance": "No Minimum Balance"
    },
    "Premium Current Account": {
        "Name": "Premium Current Account",
        "Type": "Current Account(Business Pro)",
        "Transaction Type": "Deposit/Withdrawal",
        "Fund Transfer": "Internal & External Accounts",
        "Bill Payments": "Priority Services",
        "Monthly Fee": "$20",
        "Minimum Balance": "$5,000"
    },
    "Business Current Account": {
        "Name": "Business Current Account",
        "Type": "Current Account(Business Pro)",
        "Transaction Type": "Deposit/Withdrawal",
        "Fund Transfer": "Internal & External Accounts",
        "Bill Payments": "Business-related Expenses",
        "Monthly Fee": "$30",
        "Minimum Balance": "$10,000"
    },
    "Foreign National Current Account": {
        "Name": "Foreign National Current Account",
        "Type": "Current Account(Business Pro)",
        "Transaction Type": "Deposit/Withdrawal",
        "Fund Transfer": "Internal & External Accounts",
        "Bill Payments": "International Transactions",
        "Monthly Fee": "$50",
        "Minimum Balance": "$15,000"
    },
    "Corporate Fixed Deposit": {
        "Name": "Corporate Fixed Deposit",
        "Type": "Fixed Deposit Account",
        "Deposit Term": "Fixed Duration",
        "Interest Rates": "Assume the Interest Rate, e.g., 4.0%",
        "Withdrawal Option": "Upon Maturity",
        "Minimum Deposit": "$50,000"
    },
    "Regular Income Fixed Deposit": {
        "Name": "Regular Income Fixed Deposit",
        "Type": "Fixed Deposit Account",
        "Deposit Term": "Fixed Duration",
        "Interest Rates": "Assume the Interest Rate, e.g., 3.5%",
        "Withdrawal Option": "Monthly Interest Payout",
        "Minimum Deposit": "$20,000"
    },
    "Flexi Fixed Deposit": {
        "Name": "Flexi Fixed Deposit",
        "Type": "Fixed Deposit Account",
        "Deposit Term": "Flexible Duration",
        "Interest Rates": "Assume the Interest Rate, e.g., 3.0%",
        "Withdrawal Option": "Varies",
        "Minimum Deposit": "$10,000"
    },
    "Cumulative Fixed Deposit": {
        "Name": "Cumulative Fixed Deposit",
        "Type": "Fixed Deposit Account",
        "Deposit Term": "Fixed Duration",
        "Interest Rates": "Assume the Cumulative Interest Rate, e.g., 3.75%",
        "Withdrawal Option": "Upon Maturity",
        "Minimum Deposit": "$25,000"
    },
    "Non-Cumulative Fixed Deposit": {
        "Name": "Non-Cumulative Fixed Deposit",
        "Type": "Fixed Deposit Account",
        "Deposit Term": "Fixed Duration",
        "Interest Rates": "Assume the Non-Cumulative Interest Rate, e.g., 3.25%",
        "Withdrawal Option": "Varies",
        "Minimum Deposit": "$15,000"
    }
}


    Accounts_file = 'Accounts.json'
    with open(Accounts_file, 'w') as file:
        json.dump(Accounts, file)
        
    return Accounts