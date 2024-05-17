# ----- CONFIGURE YOUR EDITOR TO USE 4 SPACES PER TAB ----- #
import settings
import sys,os
sys.path.append(os.path.join(os.path.split(os.path.abspath(__file__))[0], 'lib'))
import pymysql as db

def connection():
    ''' User this function to create your connections '''
    con = db.connect(
        settings.mysql_host, 
        settings.mysql_user, 
        settings.mysql_passwd, 
        settings.mysql_schema)
    
    return con

def findAirlinebyAge(x,y):
    
    # Create a new connection
    # Create a new connection
    con=connection()
    # Create a cursor on the connection
    cur=con.cursor()
    
   
    sql = """select l.name ,count(p.id) as 'passengers' 
    from passengers p ,flights_has_passengers fp, flights f, routes r, airlines l 
    where p.id=fp.passengers_id and fp.flights_id=f.id and f.routes_id = r.id and r.airlines_id=l.id and (2022-p.year_of_birth)<%s and (2022-p.year_of_birth)>%s
    group by l.id 
    order by passengers desc;"""%(x,y)
    
    cur.execute(sql)
    
    result = cur.fetchall()
    
    if len(result) == 0:
        return["No results"]
             
    cur.execute(sql)
    firstline = cur.fetchone()
    
    firstline = list(firstline)    
    
    
    sql2 = """select count(*)
    from airplanes a , airlines l , airlines_has_airplanes al
    where a.id = al.airplanes_id and l.id = al.airlines_id and l.name = '%s' 
    group by l.id
    """ % (firstline[0])
    
    cur.execute(sql2)
      
    result2 = cur.fetchall()
    
    if len(result2) == 0:
        return["No results"]
          
    cur.execute(sql2)
    
    result2 = cur.fetchone()
    
    result2 = list(result2)
        
    
    firstline.append(result2[0])
    
        
    firstline = tuple(firstline)
    
    List = [firstline]
    
    return[("airline_name","num_of_passengers", "num_of_aircrafts")]+List
  

def findAirportVisitors(x,a,b):
    
   # Create a new connection
    con=connection()
    
    # Create a cursor on the connection
    cur=con.cursor()
    
       
    cur.execute("""select d.name as 'Aerodromeio' , count(*) as 'Plythos episkeptwn' 
    from airlines l , routes r , airports d ,airports s, flights f , flights_has_passengers fp
    where r.airlines_id = l.id and f.routes_id = r.id and r.destination_id = d.id and r.source_id = s.id and fp.flights_id = f.id
    and l.name = '%s' and f.date >= '%s'  and f.date <= '%s'   
    group by Aerodromeio
    order by count(*) desc""" % (x,a,b)) 
   
       
    result = cur.fetchall()
    
    if len(result) == 0:
        return["No results"]
    else: 
        #return[result]
        result1 = list(result)
        return [("aiport_name", "number_of_visitors")] + result1
        
                  

def findFlights(x,a,b):


    # Create a new connection
    con=connection()
    # Create a cursor on the connection
    cur=con.cursor()
    
    cur.execute("""select f.id , l.alias , d.name , a.model 
    from flights f, routes r , airports d , airports s , airlines l , airplanes a ,airlines_has_airplanes la
    where f.routes_id = r.id and r.destination_id = d.id and r.source_id = s.id and r.airlines_id = l.id and la.airlines_id = l.id and la.airplanes_id = a.id and f.airplanes_id = a.id
    and s.city = '%s' and d.city = '%s' and f.date = '%s'""" % (a,b,x))
    
    result = cur.fetchall()
    
    if len(result) == 0:
        return["No results"]
    
    result = list(result)
    
    #return[result]
    
    return [("flight_id", "alt_name", "dest_name", "aircraft_model")] + result
    

def findLargestAirlines(N):
    # Create a new connection
    con=connection()

    # Create a cursor on the connection
    cur=con.cursor()
    
    flag = True #Σωστο input (Τιμή μεταξύ του 1 και του πλήθους των εταιριών)
        
        
    sql = """select l.name , l.code , count(f.id) as 'flights'  
    from airlines l , routes r , flights f 
    where r.airlines_id = l.id and f.routes_id = r.id 
    group by l.id
    order by flights desc; """ #Βρίσκω όλες τις εταιρίες με το πλήθος πτήσεων της κάθε μιας από τις περισσότερες πτήσεις προς τις λιγότερες
    
    cur.execute(sql)
    
    result = cur.fetchall()
    
    if int(N) <= 0:  
        return["Wrong input"]
    elif int(N) > len(result): #Οταν μας λέει να εμφανίσουμε περισσότερες από τις διαθέσιμες εταιρίες εμφανίζουμε κατάλληλο μήνυμα και όσες εταιρίες διαθέτουμε 
        flag = False
        N = len(result) #Θα το χρησιμοποιήσω παρακάτω στα for για να εμφανίσω όσες εταιρίες διαθέτω
    
    if len(result) == 0:  #Θα εμφανιστεί σε περίπτωση που η βάση είναι άδεια 
        return["No results"]
        
        
    result = list(result) #Μετατροπή σε λίστα για να είναι διαχειρίσημα τα στοιχεία 
    
    x = int(N) - 1 #Αρχικοποιώ με την θέση που βρίσκεται η τελευταία εταιρεία που ζητάει ο χρήστης (αν υποθέσουμε ότι δεν έχουμε ισότητες) 
    
    for k in range (x,len(result)-1,1): #Αυτό το κάνω στην περίπτωση που υπάρχουν ισότητες μεταξύ του πλήθους των πτήσεων της τελευταίας εταιρείας (που πρέπει να εμφανιστεί) και των επόμενων 
        if result[k][2] == result[k+1][2]:
            N = int(N) + 1
        else:
            break
    
    My_List = []
    
    for k in range (0,int(N),1):
        My_List.append(result[k]) #Φτιάχνω λίστα που περιέχει μόνο όσες αεροπορικές εταιρίες μας χρειάζονται (με τα στοιχεία τους)
    
       
    for i in range (0,int(N),1):
        sql2 = """select count(*)
        from airplanes a , airlines l , airlines_has_airplanes al
        where a.id = al.airplanes_id and l.id = al.airlines_id and l.name = '%s' 
        group by l.id
        """ % (result[i][0]) #Υπολογίζω κάθε φορά το πλήθος των αεροσκαφών(aircrafts) για κάθε εταιρεία
        
        cur.execute(sql2)
        
        helper = cur.fetchone()
              
        helper = list(helper)
        
        if helper == None :
            return["No results"]
        
        My_List[i] = list(My_List[i])
        My_List[i].append(0) #Αυξάνω τη λίστα κατα ένα για να μπει και ο αριθμός των αεροσκαφών 
        
        My_List[i][3] = My_List[i][2] #Για να μπει πρώτα ο αριθμός των αεροσκαφών και μετά ο αριθμός των πτήσεων 
        My_List[i][2] = helper[0]
       

    if flag == True:
        return [("name", "id", "num_of_aircrafts", "num_of_flights")] + My_List
    else:
        return [["There_are_not_so_many_companies. Available_companies:"],("name", "id", "num_of_aircrafts", "num_of_flights")] + My_List
    
def insertNewRoute(x,y):  
    # Create a new connection
    con=connection()

    # Create a cursor on the connection
    cur=con.cursor()
    
    elegxos = "select l.id from airlines l where l.alias = '%s'"%(x) #Ελέγχω να υπάρχει το alise που έδωσε ο χρήστης
    
    cur.execute(elegxos)
    
    elegxos = cur.fetchall()
    
    if len(elegxos) == 0:
        return[["The Airline with this alise does not exist"]]
                
    elegxos2 = "select s.id from airports s where s.name = '%s'"%(y) #Ελέγχω να υπάρχει το αεροδρόμιο που έδωσε ο χρήστης (ΔΕΝ ΕΛΕΓΧΩ ΑΝ ΕΞΥΠΗΡΕΤΕΙΤΑΙ ΑΠΟ ΤΗΝ ΕΤΑΙΡΙΑ)
    
    cur.execute(elegxos2)
    
    elegxos2 = cur.fetchall()
    
    if len(elegxos2) == 0:
        return[["The Airport does not exist"]]
                
    #Βρίσκω όλα τα αεροδρόμια που είναι αεροδρόμια αναχώρησης για την εταιρεία x
    elegxos3 = """select distinct(s.name)
    from airlines l , routes r , airports s
    where r.airlines_id = l.id and r.source_id = s.id and l.alias = '%s';"""%(x)
    
    cur.execute(elegxos3)
    
    #Ελέγχω αν το αεροδρόμιο που μου έσωσε ο χρήστης είναι αεροδρόμιο αναχώρησης για την εταιρεία x
    elegxos3 = cur.fetchall()
    
    elegxos3 = list(elegxos3)
    
    new_elegxos = []
    
    for i in range(0,len(elegxos3),1):
        new_elegxos.append(elegxos3[i][0])
    
    
    if y not in new_elegxos:
        return[["The airport is not served by the company"]]
       
    
    #Βρίσκω όλα τα αεροδρόμια που έχω στη βάση
    all_cities = "select distinct(a.id) from airports a;"  
    
    cur.execute(all_cities)
    
    all_cities = cur.fetchall()
    
    List1 = []
    all_cities = list(all_cities)
    
    for i in range(0,len(all_cities),1):
        List1.append(all_cities[i][0])
       
    
    destinations_x = """select distinct(r.destination_id)
    from airlines l, routes r,airports s 
    where r.airlines_id = l.id and r.source_id = s.id 
    and l.alias = '%s' and s.name = '%s';"""%(x,y) #Βρίσκω τα ids των αεροδρομίων προορισμού της εταιρείας x από το σημείο αναχώρησης Υ 
        
    cur.execute(destinations_x)
    
    destinations_x = cur.fetchall()
    
    List2 = []
    destinations_x = list(destinations_x)
    
    for i in range(0,len(destinations_x),1):
        List2.append(destinations_x[i][0])
       
    
    if len(all_cities) == 0: #Αν η 1η ισότητα ισχύει δεν έχουμε αεροδρόμια στην βάση
        return ["No results"]
        
    cur.execute("select a.id from airports a where a.name = '%s';"%(y)) #Εύρεση του id του αεροδρομιου αναχώρησης που έδωσε ο χρήστης
                
    source_id = cur.fetchone()
    source_id = source_id[0]
        
    
    for i in List1: #Για κάθε αεροδρόμιο
        if i in List2 or i == source_id: #Αν είναι προορισμός για την εταιρεία x (με αναχώρηση από το σημείο y) ή βρεθεί το αεροδρόμιο αφαιτηρίας που μας έχει δώσει ο χρήστης (αφού δεν μπορεί να είναι και προορισμός)
            List1.remove(i) #Διέγραψε το αφού δεν μπορεί να χρησιμοποιηθεί σαν προορισμός
            
    
    if len(List1) == 0: #Αν η αεροπορική εταιρεία έχει δρομολόγια προς όλες τις πόλεις από την αφαιρητία y  
        return["airline_capacity_full"]
    
            
    else:
  
        cur.execute("select l.id from airlines l where l.alias = '%s';"%(x)) #Εύρεση του id τις εταιρείας που έδωσε ο χρήστης 
        airlines_id = cur.fetchone()
        airlines_id = airlines_id[0]
        
        destination_id = List1[0] #Παίρνω το id του 1ου αεροδρομίου που δεν είναι προορισμός για την εταιρεία x απο το y 
        
        #Βρίσκω όλα τα ids που χρησιμοποιούνται ήδη από το routes 
        evresh_id = "select r.id from routes r order by r.id DESC;"
        
        cur.execute(evresh_id)
        
        evresh_id = cur.fetchone()
        
        evresh_id = list(evresh_id)
        
        mh_xrhsimopoihmeno_id = int(evresh_id[0]) + 1 #Το νέο id θα είναι το πιο μεγάλο από τα ήδη υπάρχοντα συν 1 άρα θα είναι σίγουρα μοναδικό

        sql = "insert into routes(id,airlines_id,source_id,destination_id) values(%d,%d,%d,%d)"%(mh_xrhsimopoihmeno_id,airlines_id,source_id,destination_id)
        
        cur.execute(sql)
        
        return["OK"]
       


