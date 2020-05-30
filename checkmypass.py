import requests # to send http request through python
import hashlib # to generate a random pattern(,used to conceal our password
import sys # to get user input from the terminal

# function used to request data from webpgae, and also to check the status of the given password
def request_api_data(query):
       url = 'https://api.pwnedpasswords.com/range/' + query

       res = requests.get(url)

       if res.status_code != 200:
              raise RuntimeError(f'{res.status_code} is invalid,pls try again')

       return res

# function used to split the hashed password, check if the requested data matches the remaining part of our password, then also to return the count.
def get_password_leaked_count(hashes,hash_to_check):

       hashes = (line.split(':') for line in hashes.text.splitlines())

       for h,count in hashes:
              if h == hash_to_check:
                     return count
       return 0

# function created to generate a random secure pattern for the password given
def pwned_password_check(password):
       sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()

       first_five, remaining_part = sha1password[:5],sha1password[5:]

       response = request_api_data(first_five)

       return get_password_leaked_count(response,remaining_part)

# the main function to check if our password has been pawned
def main(args):
   for password in args:
          count = pwned_password_check(password)
          if count:
                 print(f'{password} has been pwned {count} times, please use another password')
          else:
                 print('your password is secure, carry on!')
   return 'done!'
       
if __name__ == '__main__':
      sys.exit(main(sys.argv[1:]))

