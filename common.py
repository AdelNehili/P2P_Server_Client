def is_there_same_port(current_port, port_list):
    print(current_port,"/",port_list)
    #Si le client appelle cette fonction, il ne vérifie pas si il y a deux fois la même adresse pour se co. Grave?
    for port in port_list:
        if current_port==port:
            print("Veuillez faire attention à ne pas introduire le même port")
            return True
    return False

def check_run_code(my_list):
    if (len(my_list)<=1):
        print("Veuillez introduire le port de ce server")
        exit()
    if (not my_list[1].isdigit()):
        print("Veuillez introduire le port de ce server sous format nombre")
        exit()
    if(is_there_same_port(my_list[1],my_list[2:])):
        exit()