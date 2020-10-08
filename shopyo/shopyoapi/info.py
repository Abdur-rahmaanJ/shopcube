import datetime

info = """
   _____ _                             
  / ____| |                            
 | (___ | |__   ___  _ __  _   _  ___  
  \___ \| '_ \ / _ \| '_ \| | | |/ _ \ 
  ____) | | | | (_) | |_) | |_| | (_) |
 |_____/|_| |_|\___/| .__/ \__, |\___/ 
                    | |     __/ |      
                    |_|    |___/       
Copyright {year}
""".format(
    year=datetime.datetime.now().year
)


def printinfo():
    """
    prints Shopyo copyright in ASCII art font
    """
    print(info)
