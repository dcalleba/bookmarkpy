import pywhatkit as kit
# Schedule a WhatsApp message
phone_number = "+32495822340"  # Replace with the recipient's number
MESSAGE = "Daniel Hello! Don't forget our meeting at 3 PM today!"
HOUR = 15  # Scheduled hour
MINUTE = 23  # Scheduled minute
kit.sendwhatmsg(phone_number, MESSAGE, HOUR, MINUTE)
